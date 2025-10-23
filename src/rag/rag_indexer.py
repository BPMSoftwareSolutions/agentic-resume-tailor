"""RAG indexing - creates and manages vector store for experience documents."""

import json
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# Add packages to path for llm-labs import
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "packages" / "llm-labs" / "dist"))

from .document_chunker import DocumentChunker, RAGDocument


class RAGIndexer:
    """Manages RAG vector store creation and indexing."""

    # RAG Configuration
    RAG_CONFIG = {
        "embedding_model": "all-MiniLM-L6-v2",
        "embedding_dim": 384,
        "retrieval_top_k": 10,
        "similarity_threshold": 0.1,  # Lower threshold for real embeddings (normalized inner product)
        "vector_store_path": "data/rag/vector_store.json",
        "chunks_path": "data/rag/experience_chunks.json",
        "faiss_index_path": "data/rag/faiss_index.bin",
        "vector_store_type": "faiss",
    }

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize RAG indexer with optional config override."""
        self.config = {**self.RAG_CONFIG}
        if config:
            self.config.update(config)

        self.documents: List[RAGDocument] = []
        self.vector_store: Dict[str, Any] = {}

        # Initialize sentence transformer for real embeddings
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")

    def index_experiences(self, experiences_path: str) -> Dict[str, Any]:
        """
        Index experiences from JSON file.

        Returns indexing result with metrics.
        """
        chunker = DocumentChunker()
        self.documents = chunker.chunk_experiences(experiences_path)
        
        # Save chunks
        chunker.save_chunks(self.config["chunks_path"])
        
        # Create vector store
        self._create_vector_store()
        
        return {
            "success": True,
            "documents_indexed": len(self.documents),
            "vector_store_path": self.config["vector_store_path"],
            "chunks_path": self.config["chunks_path"],
            "config": self.config,
        }

    def index_master_resume(self, resume_path: str) -> Dict[str, Any]:
        """
        Index master resume from JSON file.

        Returns indexing result with metrics.
        """
        chunker = DocumentChunker()
        self.documents = chunker.chunk_master_resume(resume_path)
        
        # Save chunks
        chunker.save_chunks(self.config["chunks_path"])
        
        # Create vector store
        self._create_vector_store()
        
        return {
            "success": True,
            "documents_indexed": len(self.documents),
            "vector_store_path": self.config["vector_store_path"],
            "chunks_path": self.config["chunks_path"],
            "config": self.config,
        }

    def index_combined(
        self, experiences_path: str, resume_path: str
    ) -> Dict[str, Any]:
        """
        Index both experiences and master resume.

        Returns combined indexing result.
        """
        chunker = DocumentChunker()
        
        # Chunk both sources
        exp_docs = chunker.chunk_experiences(experiences_path)
        resume_docs = chunker.chunk_master_resume(resume_path)
        
        self.documents = exp_docs + resume_docs
        
        # Save combined chunks
        chunker.save_chunks(self.config["chunks_path"])
        
        # Create vector store
        self._create_vector_store()
        
        return {
            "success": True,
            "experiences_indexed": len(exp_docs),
            "resume_indexed": len(resume_docs),
            "total_documents": len(self.documents),
            "vector_store_path": self.config["vector_store_path"],
            "chunks_path": self.config["chunks_path"],
            "config": self.config,
        }

    def _generate_embeddings(self) -> None:
        """Generate real embeddings for all documents using sentence-transformers."""
        # Extract all document contents
        contents = [doc.content for doc in self.documents]

        # Generate embeddings in batch
        embeddings = self.embedder.encode(contents, normalize_embeddings=True)

        # Assign embeddings to documents
        for doc, embedding in zip(self.documents, embeddings):
            doc.embedding = embedding.tolist()

    def _build_and_save_faiss_index(self) -> None:
        """Build and save FAISS index from document embeddings."""
        if not self.documents:
            return

        # Extract embeddings from documents
        embeddings = []
        for doc in self.documents:
            if doc.embedding:
                embeddings.append(doc.embedding)
            else:
                # This shouldn't happen if _generate_embeddings was called
                embedding = self.embedder.encode(doc.content, normalize_embeddings=True)
                embeddings.append(embedding.tolist())

        # Convert to numpy array with float32 dtype (required by FAISS)
        embeddings_array = np.array(embeddings, dtype=np.float32)

        # Create FAISS index (IndexFlatIP for inner product / cosine similarity)
        embedding_dim = embeddings_array.shape[1]
        faiss_index = faiss.IndexFlatIP(embedding_dim)

        # Add embeddings to index
        faiss_index.add(embeddings_array)

        # Save FAISS index
        Path(self.config["faiss_index_path"]).parent.mkdir(
            parents=True, exist_ok=True
        )
        faiss.write_index(faiss_index, self.config["faiss_index_path"])

    def _create_vector_store(self) -> None:
        """Create and save vector store from documents."""
        # Generate real embeddings for all documents
        self._generate_embeddings()

        # Build and save FAISS index
        self._build_and_save_faiss_index()

        self.vector_store = {
            "metadata": {
                "embedding_model": self.config["embedding_model"],
                "retrieval_top_k": self.config["retrieval_top_k"],
                "similarity_threshold": self.config["similarity_threshold"],
                "vector_store_type": self.config["vector_store_type"],
                "document_count": len(self.documents),
                "faiss_index_path": self.config["faiss_index_path"],
            },
            "documents": [doc.to_dict() for doc in self.documents],
        }

        # Save vector store
        Path(self.config["vector_store_path"]).parent.mkdir(
            parents=True, exist_ok=True
        )
        with open(self.config["vector_store_path"], "w") as f:
            json.dump(self.vector_store, f, indent=2)

    def load_vector_store(self, vector_store_path: str) -> Dict[str, Any]:
        """Load existing vector store from file."""
        with open(vector_store_path, "r") as f:
            self.vector_store = json.load(f)
        
        # Reconstruct documents from vector store
        self.documents = [
            RAGDocument.from_dict(doc) for doc in self.vector_store.get("documents", [])
        ]
        
        return self.vector_store

    def get_vector_store(self) -> Dict[str, Any]:
        """Get current vector store."""
        return self.vector_store

    def get_documents(self) -> List[RAGDocument]:
        """Get indexed documents."""
        return self.documents

    def get_config(self) -> Dict[str, Any]:
        """Get current configuration."""
        return self.config

    def update_config(self, config: Dict[str, Any]) -> None:
        """Update configuration."""
        self.config.update(config)

