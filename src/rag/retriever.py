"""RAG retriever - queries vector store for relevant experiences."""

import json
import math
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer, CrossEncoder
from .document_chunker import RAGDocument


class Retriever:
    """Retrieves relevant documents from vector store based on queries."""

    def __init__(self, vector_store_path: str, use_reranking: bool = True):
        """
        Initialize retriever with vector store path.

        Args:
            vector_store_path: Path to vector store JSON file
            use_reranking: Whether to use cross-encoder reranking (default: True)
        """
        self.vector_store_path = vector_store_path
        self.vector_store: Dict[str, Any] = {}
        self.documents: List[RAGDocument] = []
        self.config: Dict[str, Any] = {}
        self.use_reranking = use_reranking

        # Initialize sentence transformer for real embeddings
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")

        # Initialize cross-encoder for reranking
        self.reranker: Optional[CrossEncoder] = None
        if use_reranking:
            try:
                self.reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
            except Exception as e:
                print(f"⚠️  Failed to load reranker: {e}. Reranking disabled.")
                self.use_reranking = False

        # FAISS index for efficient similarity search
        self.faiss_index: Optional[faiss.IndexFlatIP] = None

        self._load_vector_store()
        self._build_faiss_index()

    def _load_vector_store(self) -> None:
        """Load vector store from file."""
        if not Path(self.vector_store_path).exists():
            raise FileNotFoundError(f"Vector store not found: {self.vector_store_path}")

        with open(self.vector_store_path, "r") as f:
            self.vector_store = json.load(f)

        self.config = self.vector_store.get("metadata", {})
        self.documents = [
            RAGDocument.from_dict(doc) for doc in self.vector_store.get("documents", [])
        ]

    def _build_faiss_index(self) -> None:
        """Build FAISS index from document embeddings."""
        if not self.documents:
            return

        # Extract embeddings from documents
        embeddings = []
        for doc in self.documents:
            if doc.embedding:
                embeddings.append(doc.embedding)
            else:
                # Generate embedding if not present
                embedding = self.embedder.encode(doc.content, normalize_embeddings=True)
                embeddings.append(embedding.tolist())

        # Convert to numpy array with float32 dtype (required by FAISS)
        embeddings_array = np.array(embeddings, dtype=np.float32)

        # Create FAISS index (IndexFlatIP for inner product / cosine similarity)
        embedding_dim = embeddings_array.shape[1]
        self.faiss_index = faiss.IndexFlatIP(embedding_dim)

        # Add embeddings to index
        self.faiss_index.add(embeddings_array)

    def _generate_embedding(self, text: str) -> List[float]:
        """
        Generate real semantic embedding for text using sentence-transformers.

        Uses all-MiniLM-L6-v2 model for efficient semantic embeddings.
        """
        # Generate embedding using sentence transformer
        embedding = self.embedder.encode(text, normalize_embeddings=True)
        return embedding.tolist()

    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        if len(a) != len(b):
            raise ValueError("Vectors must have same length")

        dot_product = sum(x * y for x, y in zip(a, b))
        magnitude_a = math.sqrt(sum(x * x for x in a))
        magnitude_b = math.sqrt(sum(x * x for x in b))

        if magnitude_a == 0 or magnitude_b == 0:
            return 0.0

        return dot_product / (magnitude_a * magnitude_b)

    def _rerank_results(
        self,
        query: str,
        candidates: List[Tuple[RAGDocument, float]],
        top_k: int,
    ) -> List[Tuple[RAGDocument, float]]:
        """
        Rerank candidates using cross-encoder for better quality.

        Args:
            query: Search query
            candidates: List of (document, score) tuples
            top_k: Number of results to return

        Returns:
            Reranked list of (document, score) tuples
        """
        if not self.reranker or not candidates:
            return candidates[:top_k]

        try:
            # Prepare pairs for reranking
            pairs = [[query, doc.content] for doc, _ in candidates]

            # Get reranking scores
            rerank_scores = self.reranker.predict(pairs)

            # Combine with documents and sort
            reranked = [
                (doc, float(score))
                for (doc, _), score in zip(candidates, rerank_scores)
            ]
            reranked.sort(key=lambda x: x[1], reverse=True)

            return reranked[:top_k]
        except Exception as e:
            print(f"⚠️  Reranking failed: {e}. Returning original results.")
            return candidates[:top_k]

    def retrieve(
        self,
        query: str,
        top_k: Optional[int] = None,
        similarity_threshold: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Retrieve top-K relevant documents for a query using FAISS.

        Args:
            query: Search query string
            top_k: Number of results to return (uses config default if None)
            similarity_threshold: Minimum similarity score (uses config default if None)

        Returns:
            Dictionary with query, documents, and scores
        """
        if top_k is None:
            top_k = self.config.get("retrieval_top_k", 10)

        if similarity_threshold is None:
            similarity_threshold = self.config.get("similarity_threshold", 0.35)

        # If no FAISS index, fall back to linear search
        if self.faiss_index is None or len(self.documents) == 0:
            return {
                "query": query,
                "documents": [],
                "scores": [],
                "total_matched": 0,
                "top_k": top_k,
                "similarity_threshold": similarity_threshold,
            }

        # Generate query embedding
        query_embedding = self._generate_embedding(query)
        query_array = np.array([query_embedding], dtype=np.float32)

        # Search FAISS index for top-K candidates (get more to filter by threshold)
        search_k = min(len(self.documents), max(top_k * 2, 20))
        scores, indices = self.faiss_index.search(query_array, search_k)

        # Build results with threshold filtering
        results = []
        for idx, score in zip(indices[0], scores[0]):
            if score >= similarity_threshold:
                results.append((self.documents[idx], float(score)))

        # Sort by score
        results.sort(key=lambda x: x[1], reverse=True)

        # Apply reranking if enabled
        if self.use_reranking and self.reranker:
            top_results = self._rerank_results(query, results, top_k)
        else:
            top_results = results[:top_k]

        return {
            "query": query,
            "documents": [doc.to_dict() for doc, _ in top_results],
            "scores": [score for _, score in top_results],
            "total_matched": len(results),
            "top_k": top_k,
            "similarity_threshold": similarity_threshold,
            "reranked": self.use_reranking and self.reranker is not None,
        }

    def retrieve_by_requirement(
        self,
        requirement: str,
        top_k: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Retrieve documents matching a job requirement.

        Args:
            requirement: Job requirement string (e.g., "Python experience")
            top_k: Number of results to return

        Returns:
            Dictionary with requirement, documents, and scores
        """
        result = self.retrieve(requirement, top_k=top_k)
        result["requirement"] = requirement
        return result

    def retrieve_batch(
        self,
        requirements: List[str],
        top_k: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Retrieve documents for multiple requirements.

        Args:
            requirements: List of requirement strings
            top_k: Number of results per requirement

        Returns:
            Dictionary with results for each requirement
        """
        results = {}
        for req in requirements:
            results[req] = self.retrieve_by_requirement(req, top_k=top_k)
        
        return {
            "requirements": requirements,
            "results": results,
            "total_requirements": len(requirements),
        }

    def retrieve_by_skill(
        self,
        skill: str,
        top_k: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Retrieve documents related to a specific skill.

        Args:
            skill: Skill name (e.g., "Python", "AWS")
            top_k: Number of results to return

        Returns:
            Dictionary with skill, documents, and scores
        """
        result = self.retrieve(skill, top_k=top_k)
        result["skill"] = skill
        return result

    def retrieve_by_employer(
        self,
        employer: str,
        top_k: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Retrieve documents from a specific employer.

        Args:
            employer: Employer name
            top_k: Number of results to return

        Returns:
            Dictionary with employer, documents, and scores
        """
        # Filter documents by employer metadata
        employer_docs = [
            doc for doc in self.documents
            if doc.metadata.get("employer", "").lower() == employer.lower()
        ]

        if not employer_docs:
            return {
                "employer": employer,
                "documents": [],
                "scores": [],
                "total_matched": 0,
            }

        # Get indices of employer documents
        employer_indices = [
            i for i, doc in enumerate(self.documents)
            if doc.metadata.get("employer", "").lower() == employer.lower()
        ]

        # Score filtered documents using their embeddings
        scored = []
        for idx in employer_indices:
            doc = self.documents[idx]
            if doc.embedding:
                # Use stored embedding
                embedding = np.array([doc.embedding], dtype=np.float32)
            else:
                # Generate embedding if not present
                embedding = self.embedder.encode(doc.content, normalize_embeddings=True)
                embedding = np.array([embedding], dtype=np.float32)

            # Calculate similarity (inner product for normalized embeddings)
            score = float(embedding[0].dot(embedding[0]))
            scored.append((doc, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        top_results = scored[:top_k] if top_k else scored

        return {
            "employer": employer,
            "documents": [doc.to_dict() for doc, _ in top_results],
            "scores": [score for _, score in top_results],
            "total_matched": len(employer_docs),
        }

    def get_config(self) -> Dict[str, Any]:
        """Get retriever configuration."""
        return self.config

    def get_document_count(self) -> int:
        """Get total number of indexed documents."""
        return len(self.documents)

