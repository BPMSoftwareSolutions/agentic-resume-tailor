#!/usr/bin/env python3
"""
Demo: Tailor Resume from Experience Log

This script demonstrates the complete workflow:
1. Load job description from local file
2. Build resume from experience log
3. Tailor resume to job
4. Generate HTML output

This shows the new architecture where experience log is the source of truth.
"""

import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from tailor import (
    ingest_jd,
    extract_keywords,
    retrieve_rag_context,
    select_and_rewrite,
    generate_html_resume,
    generate_docx_from_html,
)
from build_resume_from_experience_log import build_resume_from_experience_log


def demo_tailor_from_experience_log():
    """Demo: Tailor resume from experience log."""
    
    print("\n" + "="*80)
    print("DEMO: TAILOR RESUME FROM EXPERIENCE LOG")
    print("="*80 + "\n")

    # Step 1: Load job description
    print("📋 Step 1: Loading job description...")
    job_file = "data/job_listings/senior_devops_engineer.md"
    if not Path(job_file).exists():
        print(f"❌ Job file not found: {job_file}")
        return False

    jd_path, jd_text = ingest_jd(job_file)
    print(f"✅ Job description loaded ({len(jd_text)} characters)")
    print(f"   File: {job_file}\n")

    # Step 2: Extract keywords
    print("🔍 Step 2: Extracting keywords from job description...")
    keywords = extract_keywords(jd_text)
    print(f"✅ Found {len(keywords)} keywords")
    print(f"   Top keywords: {', '.join(keywords[:10])}\n")

    # Step 3: Build resume from experience log
    print("📂 Step 3: Building resume from experience log...")
    resume_data = build_resume_from_experience_log("data/experiences.json")
    print(f"✅ Resume built from experience log")
    print(f"   - {len(resume_data['experience'])} experience entries")
    print(f"   - {len(resume_data['education'])} education entries")
    print(f"   - {len(resume_data['certifications'])} certifications\n")

    # Step 4: Retrieve RAG context
    print("🧠 Step 4: Retrieving RAG context...")
    rag_context = retrieve_rag_context(jd_text, "data/rag/vector_store.json")
    if rag_context and rag_context.get("success"):
        num_docs = len(rag_context.get("context", {}).get("documents", []))
        print(f"✅ Retrieved {num_docs} relevant experiences from RAG\n")
    else:
        print("⚠️  RAG retrieval skipped (vector store not available)\n")
        rag_context = None

    # Step 5: Tailor resume
    print("✏️  Step 5: Tailoring resume to job...")
    tailored_experience = select_and_rewrite(
        resume_data["experience"],
        keywords,
        rag_context=rag_context
    )
    resume_data["experience"] = tailored_experience
    print(f"✅ Resume tailored to job\n")

    # Step 6: Generate HTML
    print("🎨 Step 6: Generating HTML resume...")
    output_html = "out/demo_tailored_resume.html"
    generate_html_resume(
        resume_data,
        output_html,
        theme="modern"
    )
    print(f"✅ HTML resume generated")
    print(f"   Output: {output_html}\n")

    # Step 7: Generate DOCX
    print("📄 Step 7: Generating DOCX resume...")
    output_docx = "out/demo_tailored_resume.docx"
    try:
        generate_docx_from_html(output_html, output_docx)
        print(f"✅ DOCX resume generated")
        print(f"   Output: {output_docx}\n")
    except Exception as e:
        print(f"⚠️  DOCX generation skipped: {e}\n")

    # Summary
    print("="*80)
    print("✅ DEMO COMPLETE")
    print("="*80)
    print("\n📊 Summary:")
    print(f"  ✓ Job description: {job_file}")
    print(f"  ✓ Keywords extracted: {len(keywords)}")
    print(f"  ✓ Resume built from: data/experiences.json")
    print(f"  ✓ Experience entries tailored: {len(tailored_experience)}")
    print(f"  ✓ HTML output: {output_html}")
    print(f"  ✓ DOCX output: {output_docx}")
    print("\n🎯 Architecture:")
    print("  experiences.json (source of truth)")
    print("        ↓")
    print("  build_resume_from_experience_log()")
    print("        ↓")
    print("  select_and_rewrite() [tailoring]")
    print("        ↓")
    print("  generate_html_resume()")
    print("        ↓")
    print("  HTML/DOCX output")
    print("\n✨ Key Points:")
    print("  • Experience log is the single source of truth")
    print("  • No dependency on outdated master_resume.json")
    print("  • Rich metadata (skills, technologies, techniques, principles)")
    print("  • RAG-enhanced tailoring for better keyword matching")
    print("  • Supports multiple output formats (HTML, DOCX)")
    print("\n")

    return True


if __name__ == "__main__":
    try:
        success = demo_tailor_from_experience_log()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

