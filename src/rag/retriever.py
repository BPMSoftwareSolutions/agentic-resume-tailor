"""RAG retriever - queries vector store for relevant experiences."""

import json
import math
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path

from .document_chunker import RAGDocument


class Retriever:
    """Retrieves relevant documents from vector store based on queries."""

    def __init__(self, vector_store_path: str):
        """Initialize retriever with vector store path."""
        self.vector_store_path = vector_store_path
        self.vector_store: Dict[str, Any] = {}
        self.documents: List[RAGDocument] = []
        self.config: Dict[str, Any] = {}
        
        self._load_vector_store()

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

    def _generate_embedding(self, text: str) -> List[float]:
        """
        Generate simple embedding for text.

        Uses hash-based approach for consistency.
        """
        # Simple hash-based embedding (384 dimensions like all-MiniLM-L6-v2)
        hash_val = sum(ord(c) for c in text)
        embedding = []
        for i in range(384):
            embedding.append(math.sin((hash_val + i) * 0.1) * 0.5 + 0.5)
        return embedding

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

    def retrieve(
        self,
        query: str,
        top_k: Optional[int] = None,
        similarity_threshold: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Retrieve top-K relevant documents for a query.

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
        
        # Generate query embedding
        query_embedding = self._generate_embedding(query)
        
        # Score all documents
        scored_docs = []
        for doc in self.documents:
            # Use stored embedding or generate one
            doc_embedding = doc.embedding or self._generate_embedding(doc.content)
            score = self._cosine_similarity(query_embedding, doc_embedding)
            scored_docs.append((doc, score))
        
        # Filter by threshold and sort by score
        filtered = [
            (doc, score) for doc, score in scored_docs if score >= similarity_threshold
        ]
        filtered.sort(key=lambda x: x[1], reverse=True)
        
        # Get top-K
        top_results = filtered[:top_k]
        
        return {
            "query": query,
            "documents": [doc.to_dict() for doc, _ in top_results],
            "scores": [score for _, score in top_results],
            "total_matched": len(filtered),
            "top_k": top_k,
            "similarity_threshold": similarity_threshold,
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
        
        # Score filtered documents
        query_embedding = self._generate_embedding(employer)
        scored = []
        for doc in employer_docs:
            doc_embedding = doc.embedding or self._generate_embedding(doc.content)
            score = self._cosine_similarity(query_embedding, doc_embedding)
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

