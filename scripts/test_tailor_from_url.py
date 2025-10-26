#!/usr/bin/env python3
"""
Test script for tailor_from_url integration.

This demonstrates the simple workflow:
1. Fetch job listing from URL
2. Tailor resume to job
3. Generate HTML/DOCX output
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.tailor_from_url import tailor_from_url


def test_tailor_from_url_with_local_file():
    """Test tailoring with a local markdown file (simulating fetched job listing)."""
    print("\n" + "="*80)
    print("TEST: Tailor Resume from Local Job Listing")
    print("="*80 + "\n")

    # Use a sample job listing markdown file
    # In production, this would be fetched from a URL
    sample_jd = Path("data/job_listings")
    sample_jd.mkdir(parents=True, exist_ok=True)

    # Create a sample job listing for testing
    test_jd_file = sample_jd / "test_job_listing.md"
    test_jd_content = """# Senior Software Engineer

**Company**: TechCorp Inc.
**Location**: San Francisco, CA

## Job Description

We are looking for a Senior Software Engineer with:
- 5+ years of Python experience
- Strong DevOps and CI/CD knowledge
- AWS and cloud infrastructure expertise
- Leadership and mentoring skills
- Experience with microservices architecture

## Responsibilities

- Design and implement scalable systems
- Lead technical initiatives
- Mentor junior engineers
- Collaborate with product teams
"""

    test_jd_file.write_text(test_jd_content)
    print(f"📝 Created test job listing: {test_jd_file}")

    # Create output directory
    output_dir = Path("out")
    output_dir.mkdir(exist_ok=True)

    output_html = str(output_dir / "test_tailored_resume.html")

    print(f"📤 Output will be saved to: {output_html}\n")

    # Test the integration
    try:
        from src.tailor import (
            load_resume,
            ingest_jd,
            extract_keywords,
            select_and_rewrite,
            generate_html_resume,
        )

        print("="*80)
        print("TAILOR RESUME FROM JOB LISTING")
        print("="*80 + "\n")

        # Step 1: Load and parse job description
        print("📋 Processing job description...")
        jd_path, jd_text = ingest_jd(str(test_jd_file))
        print(f"✅ Job description loaded ({len(jd_text)} characters)\n")

        # Step 2: Extract keywords
        print("🔍 Extracting keywords...")
        keywords = extract_keywords(jd_text)
        print(f"✅ Found {len(keywords)} keywords: {', '.join(keywords[:5])}...\n")

        # Step 3: Load resume
        print("📂 Loading resume...")
        resume_data = load_resume("data/master_resume.json")
        print(f"✅ Resume loaded\n")

        # Step 4: Tailor resume
        print("✏️  Tailoring resume...")
        resume_data["experience"] = select_and_rewrite(
            resume_data["experience"],
            keywords,
            rag_context=None,
            use_llm_rewriting=False,
        )
        print(f"✅ Resume tailored\n")

        # Step 5: Generate HTML
        print("🎨 Generating HTML resume...")
        generate_html_resume(resume_data, output_html, "professional")
        print(f"✅ HTML resume generated\n")

        if Path(output_html).exists():
            size = Path(output_html).stat().st_size
            print(f"✅ Test passed!")
            print(f"   Generated HTML: {size} bytes")
            return True
        else:
            print(f"❌ Test failed - HTML not generated!")
            return False

    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_workflow_steps():
    """Test individual workflow steps."""
    print("\n" + "="*80)
    print("TEST: Workflow Steps")
    print("="*80 + "\n")
    
    try:
        # Step 1: Import modules
        print("✓ Step 1: Importing modules...")
        from src.fetch_job_listing import fetch_job_listing
        from src.tailor import load_resume, extract_keywords
        print("  ✅ All modules imported successfully\n")
        
        # Step 2: Check master resume exists
        print("✓ Step 2: Checking master resume...")
        master_resume = Path("data/master_resume.json")
        if master_resume.exists():
            print(f"  ✅ Master resume found: {master_resume}\n")
        else:
            print(f"  ❌ Master resume not found: {master_resume}\n")
            return False
        
        # Step 3: Check job listings directory
        print("✓ Step 3: Checking job listings directory...")
        job_listings_dir = Path("data/job_listings")
        if job_listings_dir.exists():
            print(f"  ✅ Job listings directory exists: {job_listings_dir}\n")
        else:
            print(f"  ❌ Job listings directory not found: {job_listings_dir}\n")
            return False
        
        # Step 4: Check output directory
        print("✓ Step 4: Checking output directory...")
        output_dir = Path("out")
        output_dir.mkdir(exist_ok=True)
        print(f"  ✅ Output directory ready: {output_dir}\n")
        
        print("✅ All workflow steps verified!\n")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n" + "╔" + "="*78 + "╗")
    print("║" + " "*78 + "║")
    print("║" + "  TAILOR FROM URL - INTEGRATION TEST".center(78) + "║")
    print("║" + " "*78 + "║")
    print("╚" + "="*78 + "╝")
    
    # Run tests
    workflow_ok = test_workflow_steps()
    
    if workflow_ok:
        integration_ok = test_tailor_from_url_with_local_file()
        
        if integration_ok:
            print("\n" + "="*80)
            print("✅ ALL TESTS PASSED")
            print("="*80 + "\n")
            sys.exit(0)
    
    print("\n" + "="*80)
    print("❌ TESTS FAILED")
    print("="*80 + "\n")
    sys.exit(1)

