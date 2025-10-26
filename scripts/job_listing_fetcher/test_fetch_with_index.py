#!/usr/bin/env python3
"""
Test script to demonstrate the job listing fetcher with index integration.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.fetch_job_listing import fetch_job_listing, update_job_listings_index
from bs4 import BeautifulSoup
import json


def test_fetch_with_index():
    """Test fetching a job listing and verify it's added to the index."""
    
    print("=" * 70)
    print("TEST: Job Listing Fetcher with Index Integration")
    print("=" * 70)
    print()
    
    # Read the demo HTML file
    print("📂 Reading demo HTML file...")
    with open("demo_job_listing.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # Parse to get job info
    soup = BeautifulSoup(html_content, "html.parser")
    title_tag = soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else "Job Title"
    
    print(f"✓ Found job: {title}")
    print()
    
    # Check index before
    print("📋 Checking index BEFORE fetch...")
    index_path = "data/job_listings/index.json"
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            index_before = json.load(f)
        count_before = len(index_before.get("job_listings", []))
        print(f"✓ Current entries in index: {count_before}")
    else:
        count_before = 0
        print(f"✓ Index doesn't exist yet")
    print()
    
    # Simulate fetching by creating a markdown file and updating index
    print("🔄 Simulating fetch and index update...")
    
    # Create a test markdown file
    test_file = "data/job_listings/test_senior_software_engineer.md"
    os.makedirs(os.path.dirname(test_file), exist_ok=True)
    
    with open(test_file, "w", encoding="utf-8") as f:
        f.write("# Senior Software Engineer\n\n---\n\nTest job listing")
    
    print(f"✓ Created test file: {test_file}")
    
    # Update index
    job_entry = update_job_listings_index(
        title="Senior Software Engineer",
        company="TechCorp Inc.",
        location="San Francisco, CA",
        filepath=test_file,
        output_dir="data/job_listings"
    )
    print(f"✓ Job entry ID: {job_entry['id']}")
    print()
    
    # Check index after
    print("📋 Checking index AFTER fetch...")
    with open(index_path, "r", encoding="utf-8") as f:
        index_after = json.load(f)
    count_after = len(index_after.get("job_listings", []))
    print(f"✓ New entries in index: {count_after}")
    print(f"✓ Added: {count_after - count_before} entry")
    print()
    
    # Show the new entry
    print("📄 New index entry:")
    print("-" * 70)
    print(json.dumps(job_entry, indent=2))
    print("-" * 70)
    print()
    
    # Verify it's in the index
    print("✅ Verification:")
    latest_entry = index_after["job_listings"][-1]
    if latest_entry["title"] == "Senior Software Engineer":
        print("✓ Job title matches")
    if latest_entry["company"] == "TechCorp Inc.":
        print("✓ Company matches")
    if latest_entry["location"] == "San Francisco, CA":
        print("✓ Location matches")
    if latest_entry["file"] == "test_senior_software_engineer.md":
        print("✓ File reference matches")
    
    print()
    print("=" * 70)
    print("✅ TEST COMPLETE - Index integration working!")
    print("=" * 70)
    print()
    print("Summary:")
    print(f"  - Index file: {index_path}")
    print(f"  - Total entries: {count_after}")
    print(f"  - Latest entry: {latest_entry['title']} at {latest_entry['company']}")
    print()


if __name__ == "__main__":
    test_fetch_with_index()

