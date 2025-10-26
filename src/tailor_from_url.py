#!/usr/bin/env python3
"""
Tailor Resume from Job Listing URL - Simple Integration

This script combines job listing fetching with resume tailoring:
1. Fetch job listing from URL
2. Build resume from experience log (source of truth)
3. Tailor resume to job
4. Export to HTML/DOCX

The experience log (data/experiences.json) is the primary source of truth for all resume data.

Usage:
    python src/tailor_from_url.py --url "https://example.com/job" --out out/tailored.html
    python src/tailor_from_url.py --url "https://example.com/job" --out out/tailored.html --docx
    python src/tailor_from_url.py --url "https://example.com/job" --out out/tailored.html --theme modern --use-rag
"""

import argparse
import json
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from fetch_job_listing import fetch_job_listing
from tailor import (
    ingest_jd,
    extract_keywords,
    retrieve_rag_context,
    select_and_rewrite,
    generate_html_resume,
    generate_docx_from_html,
)
from build_resume_from_experience_log import build_resume_from_experience_log
from models.resume import Resume
from models.job_listing import JobListing


def tailor_from_url(
    url: str,
    output_path: str,
    theme: str = "professional",
    export_docx: bool = False,
    use_rag: bool = False,
    use_llm_rewriting: bool = False,
    vector_store_path: str = "data/rag/vector_store.json",
    experience_log_path: str = "data/experiences.json",
    save_to_index: bool = True,
    data_dir: str = "data",
) -> bool:
    """
    Tailor resume to job listing from URL.

    Uses the experience log (data/experiences.json) as the source of truth for all resume data.

    Args:
        url: Job listing URL
        output_path: Output HTML file path
        theme: HTML theme (professional, modern, executive, creative)
        export_docx: Whether to also export to DOCX
        use_rag: Whether to use RAG for tailoring
        use_llm_rewriting: Whether to use LLM for rewriting
        vector_store_path: Path to RAG vector store
        experience_log_path: Path to experience log (source of truth)
        save_to_index: Whether to save tailored resume to resume index
        data_dir: Data directory path

    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"\n{'='*80}")
        print("TAILOR RESUME FROM URL (Using Experience Log)")
        print(f"{'='*80}\n")

        # Step 1: Fetch job listing from URL and create JobListing entry
        print(f"📥 Fetching job listing from URL...")
        print(f"   URL: {url}")
        jd_filepath = fetch_job_listing(url, output_dir="job_listings")
        print(f"✅ Job listing saved to: {jd_filepath}\n")

        # Step 2: Load and parse job description
        print("📋 Processing job description...")
        jd_path, jd_text = ingest_jd(jd_filepath)
        print(f"✅ Job description loaded ({len(jd_text)} characters)\n")

        # Step 3: Extract keywords from job description
        print("🔍 Extracting keywords from job description...")
        keywords = extract_keywords(jd_text)
        print(f"✅ Found {len(keywords)} keywords: {', '.join(keywords[:5])}...\n")

        # Step 3b: Create JobListing entry with extracted metadata
        print("📇 Creating job listing entry...")
        job_listing_model = JobListing(Path(data_dir))
        # Extract basic metadata from filename or use defaults
        job_title = Path(jd_filepath).stem or "Job Listing"
        job_listing_data = job_listing_model.create(
            title=job_title,
            company="",  # Will be extracted from job description if available
            description=jd_text,
            url=url,
            location=None,
            keywords=keywords,
        )
        job_listing_id = job_listing_data["id"]
        print(f"✅ Job listing created with ID: {job_listing_id}\n")

        # Step 4: Retrieve RAG context if requested
        rag_context = None
        if use_rag:
            print("🧠 Retrieving RAG context...")
            rag_context = retrieve_rag_context(jd_text, vector_store_path)
            if rag_context and rag_context.get("success"):
                print(f"✅ Retrieved {len(rag_context.get('context', {}).get('documents', []))} relevant experiences\n")
            else:
                print("⚠️  RAG retrieval failed, continuing without RAG context\n")

        # Step 5: Build resume from experience log (source of truth)
        print(f"📂 Building resume from experience log...")
        print(f"   Source: {experience_log_path}")
        resume_data = build_resume_from_experience_log(experience_log_path)
        print(f"✅ Resume built from experience log\n")

        # Step 6: Tailor resume to job
        print("✏️  Tailoring resume to job description...")
        tailored = select_and_rewrite(
            resume_data["experience"],
            keywords,
            rag_context=rag_context,
            use_llm_rewriting=use_llm_rewriting,
        )
        # Replace bullets with selected/re-written bullets for HTML generation
        for job in tailored:
            sel = job.get("selected_bullets")
            if sel:
                job["bullets"] = [{"text": s} if isinstance(s, str) else s for s in sel]
        resume_data["experience"] = tailored
        print(f"✅ Resume tailored\n")

        # Step 7: Generate HTML resume
        print(f"🎨 Generating HTML resume with '{theme}' theme...")
        generate_html_resume(resume_data, output_path, theme)
        print(f"✅ HTML resume written to: {output_path}\n")

        # Step 8: Generate DOCX if requested
        if export_docx:
            print("📄 Generating DOCX from HTML...")
            docx_path = generate_docx_from_html(output_path)
            print(f"✅ DOCX resume written to: {docx_path}\n")

        # Step 9: Save tailored resume to index (optional)
        if save_to_index:
            print("📇 Saving tailored resume to index...")
            try:
                resume_model = Resume(Path(data_dir))

                # Extract job title from output path or use generic name
                output_name = Path(output_path).stem
                resume_name = f"Tailored_{output_name}"

                # Create metadata for the tailored resume with job_listing_id
                metadata = resume_model.create(
                    data=resume_data,
                    name=resume_name,
                    job_listing_id=job_listing_id,  # Link to job listing
                    is_master=False,
                    description=f"Tailored resume for job listing from {url}",
                )
                print(f"✅ Tailored resume saved to index")
                print(f"   ID: {metadata.id}")
                print(f"   Name: {metadata.name}")
                print(f"   Job Listing ID: {job_listing_id}")
                print(f"   Location: data/resumes/{metadata.id}.json\n")

                # Link resume back to job listing (bidirectional)
                print("🔗 Linking resume to job listing...")
                job_listing_model.add_tailored_resume(job_listing_id, metadata.id)
                print(f"✅ Resume linked to job listing\n")
            except Exception as e:
                print(f"⚠️  Warning: Failed to save to index: {e}\n")

        print(f"{'='*80}")
        print("✅ TAILORING COMPLETE")
        print(f"{'='*80}\n")
        return True

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Tailor resume to job listing from URL"
    )
    parser.add_argument(
        "--url",
        required=True,
        help="Job listing URL",
    )
    parser.add_argument(
        "--out",
        required=True,
        help="Output HTML file path",
    )
    parser.add_argument(
        "--theme",
        choices=["professional", "modern", "executive", "creative"],
        default="professional",
        help="HTML theme (default: professional)",
    )
    parser.add_argument(
        "--docx",
        action="store_true",
        help="Also generate DOCX file",
    )
    parser.add_argument(
        "--use-rag",
        action="store_true",
        help="Use RAG to retrieve relevant experiences",
    )
    parser.add_argument(
        "--use-llm-rewriting",
        action="store_true",
        help="Use LLM for evidence-constrained bullet rewriting",
    )
    parser.add_argument(
        "--vector-store",
        default="data/rag/vector_store.json",
        help="Path to RAG vector store",
    )
    parser.add_argument(
        "--experience-log",
        default="data/experiences.json",
        help="Path to experience log (source of truth)",
    )
    parser.add_argument(
        "--save-to-index",
        action="store_true",
        default=True,
        help="Save tailored resume to resume index (default: True)",
    )
    parser.add_argument(
        "--no-save-to-index",
        action="store_false",
        dest="save_to_index",
        help="Do not save tailored resume to resume index",
    )
    parser.add_argument(
        "--data-dir",
        default="data",
        help="Data directory path (default: data)",
    )

    args = parser.parse_args()

    success = tailor_from_url(
        url=args.url,
        output_path=args.out,
        theme=args.theme,
        export_docx=args.docx,
        use_rag=args.use_rag,
        use_llm_rewriting=args.use_llm_rewriting,
        vector_store_path=args.vector_store,
        experience_log_path=args.experience_log,
        save_to_index=args.save_to_index,
        data_dir=args.data_dir,
    )

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())

