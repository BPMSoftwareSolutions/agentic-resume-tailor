#!/usr/bin/env python3
"""
Clean up persisted test data from data/resumes and data/job_listings directories.

This script removes test data that was created by tests before the test isolation
fix (Issue #39). It identifies test data by looking for:
- Generic test names like "Test Resume", "Test User", "John Doe"
- Test company names like "Test Company"
- Test job titles like "Software Engineer" (generic)

Related to GitHub Issue #39: Fix Tests persisted data/resumes (anti-pattern)
"""

import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from models.resume import Resume
from models.job_listing import JobListing


# Patterns that indicate test data
TEST_PATTERNS = {
    "resume_names": [
        "Test Resume",
        "Test User",
        "John Doe",
        "Original Resume",
        "Duplicated Resume",
        "Master Resume",
        "Resume 1",
        "Resume 2",
        "Resume 3",
    ],
    "resume_titles": [
        "Software Engineer",
        "Senior Software Engineer",
    ],
    "job_companies": [
        "Test Company",
    ],
    "job_titles": [
        "Software Engineer",
        "Senior Software Engineer",
        "DevOps Engineer",
    ],
}


def is_test_resume(resume_data):
    """Check if resume data appears to be test data."""
    if not resume_data:
        return False
    
    # Check resume name
    if resume_data.get("name") in TEST_PATTERNS["resume_names"]:
        return True
    
    # Check resume title
    if resume_data.get("title") in TEST_PATTERNS["resume_titles"]:
        # Additional check: test resumes often have "Test" in contact email
        contact = resume_data.get("contact", {})
        if contact.get("email", "").startswith("test@"):
            return True
    
    return False


def is_test_job_listing(job_data):
    """Check if job listing data appears to be test data."""
    if not job_data:
        return False
    
    # Check company name
    if job_data.get("company") in TEST_PATTERNS["job_companies"]:
        return True
    
    # Check if both title and company are generic test patterns
    if (job_data.get("title") in TEST_PATTERNS["job_titles"] and
        job_data.get("company") in TEST_PATTERNS["job_companies"]):
        return True
    
    return False


def cleanup_resumes(data_dir, dry_run=True):
    """Clean up test resumes."""
    resume_model = Resume(data_dir)
    resumes = resume_model.list_all()
    
    deleted_count = 0
    for resume in resumes:
        resume_data = resume_model.get(resume.id)
        if is_test_resume(resume_data):
            if dry_run:
                print(f"[DRY RUN] Would delete resume: {resume.name} ({resume.id})")
            else:
                resume_model.delete(resume.id)
                print(f"Deleted resume: {resume.name} ({resume.id})")
            deleted_count += 1
    
    return deleted_count


def cleanup_job_listings(data_dir, dry_run=True):
    """Clean up test job listings."""
    job_model = JobListing(data_dir)
    jobs = job_model.list_all()
    
    deleted_count = 0
    for job in jobs:
        job_data = job_model.get(job["id"])
        if is_test_job_listing(job_data):
            if dry_run:
                print(f"[DRY RUN] Would delete job: {job['title']} at {job['company']} ({job['id']})")
            else:
                job_model.delete(job["id"])
                print(f"Deleted job: {job['title']} at {job['company']} ({job['id']})")
            deleted_count += 1
    
    return deleted_count


def main():
    """Main cleanup function."""
    data_dir = Path(__file__).parent.parent / "data"
    
    # Check if running in dry-run mode
    dry_run = "--force" not in sys.argv
    
    if dry_run:
        print("=" * 70)
        print("TEST DATA CLEANUP - DRY RUN MODE")
        print("=" * 70)
        print("\nThis is a dry run. Use --force to actually delete files.\n")
    else:
        print("=" * 70)
        print("TEST DATA CLEANUP - FORCE MODE")
        print("=" * 70)
        print("\nWARNING: This will permanently delete test data!\n")
        response = input("Continue? (yes/no): ")
        if response.lower() != "yes":
            print("Cleanup cancelled.")
            return
        print()
    
    # Clean up resumes
    print("Cleaning up test resumes...")
    resume_count = cleanup_resumes(data_dir, dry_run=dry_run)
    print(f"Found {resume_count} test resumes\n")
    
    # Clean up job listings
    print("Cleaning up test job listings...")
    job_count = cleanup_job_listings(data_dir, dry_run=dry_run)
    print(f"Found {job_count} test job listings\n")
    
    # Summary
    total = resume_count + job_count
    print("=" * 70)
    if dry_run:
        print(f"DRY RUN: Would delete {total} test data items")
        print("Run with --force to actually delete")
    else:
        print(f"Deleted {total} test data items")
    print("=" * 70)


if __name__ == "__main__":
    main()

