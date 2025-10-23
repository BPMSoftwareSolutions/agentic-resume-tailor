"""Unit tests for RAG integration - document chunking, indexing, and retrieval."""

import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

# Add src to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rag.document_chunker import DocumentChunker, RAGDocument
from rag.rag_indexer import RAGIndexer
from rag.retriever import Retriever


class TestRAGDocument:
    """Test RAGDocument class."""

    def test_rag_document_creation(self):
        """Test creating a RAG document."""
        doc = RAGDocument(
            id="test-1",
            content="Test content",
            metadata={"employer": "Test Corp", "role": "Engineer"},
        )

        assert doc.id == "test-1"
        assert doc.content == "Test content"
        assert doc.metadata["employer"] == "Test Corp"

    def test_rag_document_to_dict(self):
        """Test converting RAG document to dictionary."""
        doc = RAGDocument(
            id="test-1",
            content="Test content",
            metadata={"employer": "Test Corp"},
        )

        doc_dict = doc.to_dict()

        assert doc_dict["id"] == "test-1"
        assert doc_dict["content"] == "Test content"
        assert doc_dict["metadata"]["employer"] == "Test Corp"

    def test_rag_document_from_dict(self):
        """Test creating RAG document from dictionary."""
        data = {
            "id": "test-1",
            "content": "Test content",
            "metadata": {"employer": "Test Corp"},
        }

        doc = RAGDocument.from_dict(data)

        assert doc.id == "test-1"
        assert doc.content == "Test content"
        assert doc.metadata["employer"] == "Test Corp"


class TestDocumentChunker:
    """Test DocumentChunker class."""

    @pytest.fixture
    def sample_experiences(self):
        """Create sample experiences data."""
        return [
            {
                "id": "exp-1",
                "employer": "Tech Corp",
                "role": "Senior Engineer",
                "dates": "2020-2023",
                "location": "San Francisco",
                "bullets": [
                    "Built microservices using Python and AWS",
                    "Led team of 5 engineers",
                ],
                "skills": ["Python", "AWS", "Leadership"],
                "technologies": ["Python", "AWS", "Docker"],
            }
        ]

    def test_chunk_experiences(self, sample_experiences, tmp_path):
        """Test chunking experiences into RAG documents."""
        # Create temp experiences file
        exp_file = tmp_path / "experiences.json"
        exp_file.write_text(json.dumps(sample_experiences))

        chunker = DocumentChunker()
        documents = chunker.chunk_experiences(str(exp_file))

        assert len(documents) == 2  # 2 bullets
        assert documents[0].metadata["employer"] == "Tech Corp"
        assert documents[0].metadata["role"] == "Senior Engineer"
        assert "Python" in documents[0].metadata["skills"]

    def test_save_and_load_chunks(self, sample_experiences, tmp_path):
        """Test saving and loading chunks."""
        exp_file = tmp_path / "experiences.json"
        exp_file.write_text(json.dumps(sample_experiences))

        chunks_file = tmp_path / "chunks.json"

        # Save chunks
        chunker = DocumentChunker()
        chunker.chunk_experiences(str(exp_file))
        chunker.save_chunks(str(chunks_file))

        assert chunks_file.exists()

        # Load chunks
        chunker2 = DocumentChunker()
        loaded_docs = chunker2.load_chunks(str(chunks_file))

        assert len(loaded_docs) == 2
        assert loaded_docs[0].metadata["employer"] == "Tech Corp"

    def test_get_document_count(self, sample_experiences, tmp_path):
        """Test getting document count."""
        exp_file = tmp_path / "experiences.json"
        exp_file.write_text(json.dumps(sample_experiences))

        chunker = DocumentChunker()
        chunker.chunk_experiences(str(exp_file))

        assert chunker.get_document_count() == 2


class TestRAGIndexer:
    """Test RAGIndexer class."""

    @pytest.fixture
    def sample_experiences(self):
        """Create sample experiences data."""
        return [
            {
                "id": "exp-1",
                "employer": "Tech Corp",
                "role": "Senior Engineer",
                "dates": "2020-2023",
                "bullets": ["Built microservices", "Led team"],
                "skills": ["Python", "AWS"],
                "technologies": ["Python", "AWS"],
            }
        ]

    def test_index_experiences(self, sample_experiences, tmp_path):
        """Test indexing experiences."""
        exp_file = tmp_path / "experiences.json"
        exp_file.write_text(json.dumps(sample_experiences))

        indexer = RAGIndexer(
            {
                "vector_store_path": str(tmp_path / "vector_store.json"),
                "chunks_path": str(tmp_path / "chunks.json"),
            }
        )

        result = indexer.index_experiences(str(exp_file))

        assert result["success"]
        assert result["documents_indexed"] == 2
        assert Path(result["vector_store_path"]).exists()
        assert Path(result["chunks_path"]).exists()

    def test_vector_store_creation(self, sample_experiences, tmp_path):
        """Test vector store creation."""
        exp_file = tmp_path / "experiences.json"
        exp_file.write_text(json.dumps(sample_experiences))

        vector_store_path = tmp_path / "vector_store.json"

        indexer = RAGIndexer(
            {
                "vector_store_path": str(vector_store_path),
                "chunks_path": str(tmp_path / "chunks.json"),
            }
        )
        indexer.index_experiences(str(exp_file))

        # Load and verify vector store
        with open(vector_store_path) as f:
            vs = json.load(f)

        assert "metadata" in vs
        assert "documents" in vs
        assert len(vs["documents"]) == 2
        assert vs["metadata"]["embedding_model"] == "all-MiniLM-L6-v2"

    def test_load_vector_store(self, sample_experiences, tmp_path):
        """Test loading existing vector store."""
        exp_file = tmp_path / "experiences.json"
        exp_file.write_text(json.dumps(sample_experiences))

        vector_store_path = tmp_path / "vector_store.json"

        # Create vector store
        indexer = RAGIndexer(
            {
                "vector_store_path": str(vector_store_path),
                "chunks_path": str(tmp_path / "chunks.json"),
            }
        )
        indexer.index_experiences(str(exp_file))

        # Load vector store
        indexer2 = RAGIndexer()
        vs = indexer2.load_vector_store(str(vector_store_path))

        assert len(indexer2.get_documents()) == 2
        assert vs["metadata"]["document_count"] == 2


class TestRetriever:
    """Test Retriever class."""

    @pytest.fixture
    def vector_store(self, tmp_path):
        """Create a sample vector store."""
        vector_store_data = {
            "metadata": {
                "embedding_model": "all-MiniLM-L6-v2",
                "retrieval_top_k": 10,
                "similarity_threshold": 0.35,
                "vector_store_type": "local",
                "document_count": 3,
            },
            "documents": [
                {
                    "id": "doc-1",
                    "content": "Built Python microservices on AWS",
                    "metadata": {
                        "employer": "Tech Corp",
                        "role": "Senior Engineer",
                        "skills": ["Python", "AWS"],
                    },
                },
                {
                    "id": "doc-2",
                    "content": "Led team of engineers using Agile",
                    "metadata": {
                        "employer": "Tech Corp",
                        "role": "Engineering Manager",
                        "skills": ["Leadership", "Agile"],
                    },
                },
                {
                    "id": "doc-3",
                    "content": "Implemented CI/CD pipelines with Docker",
                    "metadata": {
                        "employer": "Cloud Inc",
                        "role": "DevOps Engineer",
                        "skills": ["Docker", "CI/CD"],
                    },
                },
            ],
        }

        vs_file = tmp_path / "vector_store.json"
        vs_file.write_text(json.dumps(vector_store_data))
        return str(vs_file)

    def test_retriever_initialization(self, vector_store):
        """Test retriever initialization."""
        retriever = Retriever(vector_store)

        assert retriever.get_document_count() == 3
        assert retriever.get_config()["embedding_model"] == "all-MiniLM-L6-v2"

    def test_retrieve_documents(self, vector_store):
        """Test retrieving documents."""
        retriever = Retriever(vector_store)
        result = retriever.retrieve("Python", top_k=2)

        assert result["query"] == "Python"
        assert len(result["documents"]) <= 2
        assert len(result["scores"]) == len(result["documents"])
        assert result["total_matched"] > 0

    def test_retrieve_by_skill(self, vector_store):
        """Test retrieving by skill."""
        retriever = Retriever(vector_store)
        result = retriever.retrieve_by_skill("Python", top_k=2)

        assert result["skill"] == "Python"
        assert len(result["documents"]) <= 2

    def test_retrieve_by_employer(self, vector_store):
        """Test retrieving by employer."""
        retriever = Retriever(vector_store)
        result = retriever.retrieve_by_employer("Tech Corp", top_k=5)

        assert result["employer"] == "Tech Corp"
        assert result["total_matched"] == 2  # 2 docs from Tech Corp

    def test_retrieve_batch(self, vector_store):
        """Test batch retrieval."""
        retriever = Retriever(vector_store)
        requirements = ["Python", "Leadership", "Docker"]
        result = retriever.retrieve_batch(requirements, top_k=2)

        assert result["total_requirements"] == 3
        assert len(result["results"]) == 3
        assert "Python" in result["results"]

    def test_cosine_similarity(self, vector_store):
        """Test cosine similarity calculation."""
        retriever = Retriever(vector_store)

        # Test identical vectors
        a = [1.0, 0.0, 0.0]
        b = [1.0, 0.0, 0.0]
        similarity = retriever._cosine_similarity(a, b)
        assert abs(similarity - 1.0) < 0.001

        # Test orthogonal vectors
        a = [1.0, 0.0, 0.0]
        b = [0.0, 1.0, 0.0]
        similarity = retriever._cosine_similarity(a, b)
        assert abs(similarity) < 0.001

    def test_embedding_generation(self, vector_store):
        """Test embedding generation."""
        retriever = Retriever(vector_store)

        embedding1 = retriever._generate_embedding("test")
        embedding2 = retriever._generate_embedding("test")

        assert len(embedding1) == 384
        assert embedding1 == embedding2  # Same input should produce same embedding

    def test_retriever_file_not_found(self):
        """Test retriever with non-existent file."""
        with pytest.raises(FileNotFoundError):
            Retriever("non_existent_file.json")


class TestRAGIntegration:
    """Integration tests for RAG pipeline."""

    @pytest.fixture
    def sample_experiences(self):
        """Create sample experiences data."""
        return [
            {
                "id": "exp-1",
                "employer": "Tech Corp",
                "role": "Senior Engineer",
                "dates": "2020-2023",
                "bullets": [
                    "Built Python microservices on AWS",
                    "Implemented CI/CD pipelines",
                ],
                "skills": ["Python", "AWS", "CI/CD"],
                "technologies": ["Python", "AWS", "Docker"],
            },
            {
                "id": "exp-2",
                "employer": "Cloud Inc",
                "role": "DevOps Engineer",
                "dates": "2018-2020",
                "bullets": ["Managed Kubernetes clusters", "Automated deployments"],
                "skills": ["Kubernetes", "Automation"],
                "technologies": ["Kubernetes", "Docker"],
            },
        ]

    def test_end_to_end_rag_pipeline(self, sample_experiences, tmp_path):
        """Test complete RAG pipeline: chunk -> index -> retrieve."""
        # Setup
        exp_file = tmp_path / "experiences.json"
        exp_file.write_text(json.dumps(sample_experiences))

        vector_store_path = tmp_path / "vector_store.json"
        chunks_path = tmp_path / "chunks.json"

        # Step 1: Index
        indexer = RAGIndexer(
            {
                "vector_store_path": str(vector_store_path),
                "chunks_path": str(chunks_path),
            }
        )
        index_result = indexer.index_experiences(str(exp_file))

        assert index_result["success"]
        assert index_result["documents_indexed"] == 4  # 4 bullets total

        # Step 2: Retrieve
        retriever = Retriever(str(vector_store_path))
        retrieve_result = retriever.retrieve("Python", top_k=3)

        assert retrieve_result["query"] == "Python"
        assert len(retrieve_result["documents"]) > 0
        assert retrieve_result["total_matched"] > 0

    def test_rag_accuracy_on_keywords(self, sample_experiences, tmp_path):
        """Test RAG retrieval accuracy on sample keywords."""
        exp_file = tmp_path / "experiences.json"
        exp_file.write_text(json.dumps(sample_experiences))

        vector_store_path = tmp_path / "vector_store.json"

        # Index
        indexer = RAGIndexer(
            {
                "vector_store_path": str(vector_store_path),
                "chunks_path": str(tmp_path / "chunks.json"),
            }
        )
        indexer.index_experiences(str(exp_file))

        # Retrieve
        retriever = Retriever(str(vector_store_path))

        # Test keyword retrieval
        keywords = ["Python", "Kubernetes", "AWS"]
        for keyword in keywords:
            result = retriever.retrieve(keyword, top_k=5)
            assert result["total_matched"] > 0, f"No results for {keyword}"
            assert len(result["documents"]) > 0, f"No documents for {keyword}"

    def test_rag_batch_retrieval_for_job_requirements(
        self, sample_experiences, tmp_path
    ):
        """Test batch retrieval for multiple job requirements."""
        exp_file = tmp_path / "experiences.json"
        exp_file.write_text(json.dumps(sample_experiences))

        vector_store_path = tmp_path / "vector_store.json"

        # Index
        indexer = RAGIndexer(
            {
                "vector_store_path": str(vector_store_path),
                "chunks_path": str(tmp_path / "chunks.json"),
            }
        )
        indexer.index_experiences(str(exp_file))

        # Batch retrieve
        retriever = Retriever(str(vector_store_path))
        job_requirements = [
            "Python development",
            "Cloud infrastructure",
            "DevOps",
        ]
        batch_result = retriever.retrieve_batch(job_requirements, top_k=3)

        assert batch_result["total_requirements"] == 3
        assert len(batch_result["results"]) == 3

        # Verify each requirement has results
        for req in job_requirements:
            assert req in batch_result["results"]
            assert batch_result["results"][req]["total_matched"] > 0

