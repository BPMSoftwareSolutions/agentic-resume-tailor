"""Document chunking for RAG - converts experiences into RAG documents."""

import json
import uuid
from typing import List, Dict, Any, Optional
from pathlib import Path


class RAGDocument:
    """Represents a single RAG document with content and metadata."""

    def __init__(
        self,
        id: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
        embedding: Optional[List[float]] = None,
    ):
        self.id = id
        self.content = content
        self.metadata = metadata or {}
        self.embedding = embedding

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = {
            "id": self.id,
            "content": self.content,
            "metadata": self.metadata,
        }
        if self.embedding:
            result["embedding"] = self.embedding
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RAGDocument":
        """Create from dictionary."""
        return cls(
            id=data["id"],
            content=data["content"],
            metadata=data.get("metadata"),
            embedding=data.get("embedding"),
        )


class DocumentChunker:
    """Chunks experience data into RAG documents."""

    def __init__(self):
        self.documents: List[RAGDocument] = []

    def chunk_experiences(self, experiences_path: str) -> List[RAGDocument]:
        """
        Load experiences from JSON and chunk into RAG documents.

        Each bullet becomes a document with context about employer, role, skills, etc.
        """
        self.documents = []

        with open(experiences_path, "r") as f:
            experiences = json.load(f)

        for exp in experiences:
            employer = exp.get("employer", "Unknown")
            role = exp.get("role", "Unknown")
            dates = exp.get("dates", "")
            location = exp.get("location", "")
            skills = exp.get("skills", [])
            technologies = exp.get("technologies", [])
            bullets = exp.get("bullets", [])

            # Create a document for each bullet
            for bullet in bullets:
                doc_id = str(uuid.uuid4())
                
                # Build content with context
                content = f"{bullet}"
                
                # Build metadata with rich context
                metadata = {
                    "employer": employer,
                    "role": role,
                    "dates": dates,
                    "location": location,
                    "skills": skills,
                    "technologies": technologies,
                    "bullet_text": bullet,
                    "source": "experiences.json",
                }

                doc = RAGDocument(
                    id=doc_id,
                    content=content,
                    metadata=metadata,
                )
                self.documents.append(doc)

        return self.documents

    def chunk_master_resume(self, resume_path: str) -> List[RAGDocument]:
        """
        Load master resume and chunk into RAG documents.

        Extracts experience bullets from the master resume JSON.
        """
        with open(resume_path, "r") as f:
            resume = json.load(f)

        # Extract experience section
        experience_section = resume.get("experience", [])

        for exp in experience_section:
            employer = exp.get("employer", "Unknown")
            position = exp.get("position", "Unknown")
            dates = exp.get("dates", "")
            bullets = exp.get("bullets", [])

            for bullet in bullets:
                doc_id = str(uuid.uuid4())
                
                content = f"{bullet}"
                
                metadata = {
                    "employer": employer,
                    "position": position,
                    "dates": dates,
                    "bullet_text": bullet,
                    "source": "master_resume.json",
                }

                doc = RAGDocument(
                    id=doc_id,
                    content=content,
                    metadata=metadata,
                )
                self.documents.append(doc)

        return self.documents

    def save_chunks(self, output_path: str) -> None:
        """Save chunked documents to JSON file."""
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        chunks_data = [doc.to_dict() for doc in self.documents]
        
        with open(output_path, "w") as f:
            json.dump(chunks_data, f, indent=2)

    def load_chunks(self, input_path: str) -> List[RAGDocument]:
        """Load previously chunked documents from JSON file."""
        with open(input_path, "r") as f:
            chunks_data = json.load(f)
        
        self.documents = [RAGDocument.from_dict(chunk) for chunk in chunks_data]
        return self.documents

    def get_documents(self) -> List[RAGDocument]:
        """Get all chunked documents."""
        return self.documents

    def get_document_count(self) -> int:
        """Get count of documents."""
        return len(self.documents)

