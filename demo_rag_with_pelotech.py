#!/usr/bin/env python3
"""
Demo: Complete RAG workflow with Pelotech job posting

Shows all three capabilities:
1. Parse job post → extract role, stack, must-haves, nice-to-haves
2. Embed & index experience snippets
3. Retrieve top-K experiences per requirement
"""

import json
from pathlib import Path
from src.parsers.job_posting_parser import JobPostingParser
from src.rag.rag_indexer import RAGIndexer
from src.rag.retriever import Retriever


def demo_parse_job_posting():
    """Capability 1: Parse job post → extract role, stack, must-haves, nice-to-haves"""
    print("\n" + "="*80)
    print("CAPABILITY 1: Parse Job Posting")
    print("="*80)
    
    parser = JobPostingParser()
    job_data = parser.parse_file("data/job_listings/pelotech-senior-software-engineer.md")
    
    print(f"\n📋 Job Title: {job_data['title']}")
    print(f"🏢 Company: {job_data['company']}")
    print(f"📍 Location: {job_data['location']}")
    print(f"🌐 Work Arrangement: {job_data['work_arrangement']}")
    print(f"💰 Experience Required: {job_data['experience_years']} years")
    
    print(f"\n🔴 MUST-HAVES (Required Skills):")
    for skill in job_data['required_skills'][:10]:
        print(f"   • {skill}")
    
    print(f"\n🟢 NICE-TO-HAVES (Preferred Skills):")
    for skill in job_data['preferred_skills'][:5]:
        print(f"   • {skill}")
    
    print(f"\n📝 Key Responsibilities:")
    for i, resp in enumerate(job_data['responsibilities'][:3], 1):
        print(f"   {i}. {resp[:70]}...")
    
    return job_data


def demo_index_experiences():
    """Capability 2: Embed & index experience snippets"""
    print("\n" + "="*80)
    print("CAPABILITY 2: Index Experience Snippets")
    print("="*80)
    
    # Check if vector store exists
    vector_store_path = Path("data/rag/vector_store.json")
    
    if not vector_store_path.exists():
        print("\n📦 Creating vector store...")
        indexer = RAGIndexer()
        indexer.index_experiences("data/experiences.json")
        print(f"✅ Vector store created: {vector_store_path}")
    else:
        print(f"✅ Vector store already exists: {vector_store_path}")
    
    # Load and show stats
    with open(vector_store_path, "r") as f:
        vector_store = json.load(f)
    
    doc_count = len(vector_store.get("documents", []))
    config = vector_store.get("metadata", {})
    
    print(f"\n📊 Vector Store Statistics:")
    print(f"   • Total indexed documents: {doc_count}")
    print(f"   • Embedding model: {config.get('embedding_model', 'N/A')}")
    print(f"   • Top-K retrieval: {config.get('retrieval_top_k', 'N/A')}")
    print(f"   • Similarity threshold: {config.get('similarity_threshold', 'N/A')}")
    
    # Show sample documents
    print(f"\n📄 Sample Indexed Documents:")
    for i, doc in enumerate(vector_store.get("documents", [])[:3], 1):
        print(f"\n   Document {i}:")
        print(f"   • Content: {doc['content'][:60]}...")
        print(f"   • Employer: {doc['metadata'].get('employer', 'N/A')}")
        print(f"   • Role: {doc['metadata'].get('role', 'N/A')}")
        print(f"   • Skills: {', '.join(doc['metadata'].get('skills', [])[:3])}")


def demo_retrieve_experiences(job_data):
    """Capability 3: Retrieve top-K experiences per requirement"""
    print("\n" + "="*80)
    print("CAPABILITY 3: Retrieve Top-K Experiences Per Requirement")
    print("="*80)
    
    retriever = Retriever("data/rag/vector_store.json")
    
    # Get top 5 required skills
    top_skills = job_data['required_skills'][:5]
    
    print(f"\n🔍 Retrieving experiences for top {len(top_skills)} required skills...")
    
    for skill in top_skills:
        print(f"\n{'─'*70}")
        print(f"📌 Skill: {skill}")
        print(f"{'─'*70}")
        
        result = retriever.retrieve_by_skill(skill, top_k=3)
        
        if result['documents']:
            for i, (doc, score) in enumerate(zip(result['documents'], result['scores']), 1):
                print(f"\n   {i}. [{score:.2f}] {doc['content'][:65]}...")
                print(f"      Employer: {doc['metadata'].get('employer', 'N/A')}")
                print(f"      Role: {doc['metadata'].get('role', 'N/A')}")
        else:
            print(f"   ⚠️  No matching experiences found")
    
    # Batch retrieval
    print(f"\n{'='*80}")
    print("📦 BATCH RETRIEVAL: All top 5 skills at once")
    print(f"{'='*80}")
    
    batch_result = retriever.retrieve_batch(top_skills, top_k=2)
    
    total_matches = sum(
        len(req_result['documents']) 
        for req_result in batch_result['results'].values()
    )
    
    print(f"\n✅ Retrieved {total_matches} total experiences across {len(top_skills)} requirements")
    print(f"   Average matches per requirement: {total_matches / len(top_skills):.1f}")


def main():
    """Run complete demo"""
    print("\n" + "🚀 "*40)
    print("RAG CAPABILITIES DEMO - Pelotech Senior Software Engineer")
    print("🚀 "*40)
    
    # Capability 1: Parse job posting
    job_data = demo_parse_job_posting()
    
    # Capability 2: Index experiences
    demo_index_experiences()
    
    # Capability 3: Retrieve experiences
    demo_retrieve_experiences(job_data)
    
    print("\n" + "="*80)
    print("✅ DEMO COMPLETE")
    print("="*80)
    print("\n📚 All three capabilities demonstrated:")
    print("   1. ✅ Parsed job posting (role, stack, must-haves, nice-to-haves)")
    print("   2. ✅ Indexed experience snippets with embeddings")
    print("   3. ✅ Retrieved top-K experiences per requirement")
    print("\n💡 Next steps:")
    print("   • Use retrieved experiences to tailor resume")
    print("   • Run: python src/tailor.py --jd <jd_file> --use-rag --out <output>")
    print("   • Check RAG_CAPABILITIES_ANALYSIS.md for detailed documentation")
    print()


if __name__ == "__main__":
    main()

