#!/usr/bin/env python3
"""
Demo script for RAG retrieval - demonstrates end-to-end RAG functionality.

This script:
1. Creates RAG documents from experiences.json
2. Indexes them into a vector store
3. Retrieves relevant experiences for sample job requirements
4. Shows before/after tailored resume with RAG context
"""

import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rag.document_chunker import DocumentChunker
from rag.rag_indexer import RAGIndexer
from rag.retriever import Retriever


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def demo_document_chunking():
    """Demonstrate document chunking."""
    print_section("STEP 1: Document Chunking")

    chunker = DocumentChunker()
    experiences_path = "data/experiences.json"

    if not Path(experiences_path).exists():
        print(f"❌ Experiences file not found: {experiences_path}")
        return None

    print(f"📂 Loading experiences from {experiences_path}...")
    documents = chunker.chunk_experiences(experiences_path)

    print(f"✅ Chunked {len(documents)} experience bullets into RAG documents")
    print(f"\n📋 Sample documents:")
    for i, doc in enumerate(documents[:3]):
        print(f"\n  Document {i + 1}:")
        print(f"    ID: {doc.id}")
        print(f"    Employer: {doc.metadata.get('employer')}")
        print(f"    Role: {doc.metadata.get('role')}")
        print(f"    Content: {doc.content[:100]}...")

    return chunker


def demo_rag_indexing():
    """Demonstrate RAG indexing."""
    print_section("STEP 2: RAG Indexing")

    indexer = RAGIndexer()
    experiences_path = "data/experiences.json"

    if not Path(experiences_path).exists():
        print(f"❌ Experiences file not found: {experiences_path}")
        return None

    print(f"📂 Indexing experiences from {experiences_path}...")
    result = indexer.index_experiences(experiences_path)

    print(f"✅ Indexing complete!")
    print(f"   Documents indexed: {result['documents_indexed']}")
    print(f"   Vector store path: {result['vector_store_path']}")
    print(f"   Chunks path: {result['chunks_path']}")
    print(f"\n⚙️  Configuration:")
    for key, value in result["config"].items():
        print(f"   {key}: {value}")

    return indexer


def demo_retrieval():
    """Demonstrate RAG retrieval."""
    print_section("STEP 3: RAG Retrieval")

    vector_store_path = "data/rag/vector_store.json"

    if not Path(vector_store_path).exists():
        print(f"❌ Vector store not found: {vector_store_path}")
        print("   Run demo_rag_indexing() first to create the vector store")
        return

    print(f"📂 Loading vector store from {vector_store_path}...")
    retriever = Retriever(vector_store_path)

    print(f"✅ Vector store loaded with {retriever.get_document_count()} documents")

    # Sample job requirements
    requirements = [
        "Python development experience",
        "AWS cloud architecture",
        "Microservices design",
        "CI/CD pipeline implementation",
        "Team leadership and mentoring",
    ]

    print(f"\n🔍 Retrieving experiences for {len(requirements)} job requirements:")

    for req in requirements:
        print(f"\n  📌 Requirement: {req}")
        result = retriever.retrieve(req, top_k=3)

        print(f"     Found {result['total_matched']} matching documents")
        print(f"     Top 3 results:")

        for i, (doc, score) in enumerate(
            zip(result["documents"], result["scores"]), 1
        ):
            print(f"\n       {i}. Score: {score:.3f}")
            print(f"          Employer: {doc['metadata'].get('employer')}")
            print(f"          Role: {doc['metadata'].get('role')}")
            print(f"          Content: {doc['content'][:80]}...")


def demo_batch_retrieval():
    """Demonstrate batch retrieval for multiple requirements."""
    print_section("STEP 4: Batch Retrieval")

    vector_store_path = "data/rag/vector_store.json"

    if not Path(vector_store_path).exists():
        print(f"❌ Vector store not found: {vector_store_path}")
        return

    print(f"📂 Loading vector store...")
    retriever = Retriever(vector_store_path)

    # Sample job requirements (like from a job description)
    job_requirements = [
        "Python",
        "AWS",
        "Docker",
        "Kubernetes",
        "Microservices",
        "CI/CD",
    ]

    print(f"🔍 Batch retrieving for {len(job_requirements)} job requirements...")
    batch_result = retriever.retrieve_batch(job_requirements, top_k=5)

    print(f"\n✅ Batch retrieval complete!")
    print(f"   Requirements processed: {batch_result['total_requirements']}")

    # Show summary
    print(f"\n📊 Summary by requirement:")
    for req, result in batch_result["results"].items():
        matched = result["total_matched"]
        print(f"   {req}: {matched} matching documents")


def demo_skill_retrieval():
    """Demonstrate skill-based retrieval."""
    print_section("STEP 5: Skill-Based Retrieval")

    vector_store_path = "data/rag/vector_store.json"

    if not Path(vector_store_path).exists():
        print(f"❌ Vector store not found: {vector_store_path}")
        return

    print(f"📂 Loading vector store...")
    retriever = Retriever(vector_store_path)

    skills = ["Python", "AWS", "Leadership"]

    print(f"🔍 Retrieving experiences by skill:")

    for skill in skills:
        print(f"\n  📌 Skill: {skill}")
        result = retriever.retrieve_by_skill(skill, top_k=3)

        print(f"     Found {result['total_matched']} documents")
        for i, (doc, score) in enumerate(
            zip(result["documents"], result["scores"]), 1
        ):
            print(f"     {i}. Score: {score:.3f} - {doc['content'][:60]}...")


def main():
    """Run all demos."""
    print("\n" + "=" * 70)
    print("  RAG RETRIEVAL DEMONSTRATION")
    print("=" * 70)

    # Step 1: Document Chunking
    chunker = demo_document_chunking()

    # Step 2: RAG Indexing
    indexer = demo_rag_indexing()

    # Step 3: Retrieval
    demo_retrieval()

    # Step 4: Batch Retrieval
    demo_batch_retrieval()

    # Step 5: Skill-Based Retrieval
    demo_skill_retrieval()

    print_section("DEMO COMPLETE")
    print("✅ RAG retrieval demonstration finished successfully!")
    print("\nNext steps:")
    print("  1. Use RAG in tailor.py: python src/tailor.py --jd <jd_file> --use-rag --out <output>")
    print("  2. Check data/rag/vector_store.json for indexed documents")
    print("  3. Check data/rag/experience_chunks.json for chunked documents")


if __name__ == "__main__":
    main()

