#!/usr/bin/env python3
"""
Fix job listing index to ensure consistent fields and timestamp formats.

This script:
1. Ensures all job listing index entries have: id, title, company, location, url, description, created_at, updated_at
2. Standardizes all timestamps to ISO 8601 with Z suffix
3. Loads full job listing data to fill in missing fields
"""

import json
from pathlib import Path
from datetime import datetime


def get_iso_timestamp(ts: str) -> str:
    """Convert timestamp to ISO 8601 with Z suffix."""
    if not ts:
        return datetime.now().isoformat() + "Z"
    
    # If already has Z, return as-is
    if ts.endswith("Z"):
        return ts
    
    # If has +00:00, replace with Z
    if ts.endswith("+00:00"):
        return ts.replace("+00:00", "Z")
    
    # Otherwise add Z
    if not ts.endswith("Z"):
        return ts + "Z"
    
    return ts


def fix_job_listing_index():
    """Fix job listing index."""
    index_path = Path("data/job_listings/index.json")
    
    if not index_path.exists():
        print("No job listing index found")
        return
    
    print("=" * 80)
    print("FIX JOB LISTING INDEX")
    print("=" * 80 + "\n")
    
    # Load index
    with open(index_path, 'r', encoding='utf-8') as f:
        index = json.load(f)
    
    job_listings_dir = Path("data/job_listings")
    
    print(f"Processing {len(index.get('job_listings', []))} job listings...\n")
    
    # Fix each entry
    for i, job in enumerate(index.get('job_listings', [])):
        job_id = job.get('id')
        print(f"[{i+1}] {job_id}")
        
        # Load full job data if available
        job_file = job_listings_dir / f"{job_id}.json"
        full_data = {}
        if job_file.exists():
            with open(job_file, 'r', encoding='utf-8') as f:
                full_data = json.load(f)
        
        # Ensure all required fields
        job['id'] = job_id
        job['title'] = job.get('title') or full_data.get('title') or 'Unknown'
        job['company'] = job.get('company') or full_data.get('company') or ''
        job['location'] = job.get('location') or full_data.get('location') or ''
        job['url'] = job.get('url') or full_data.get('url') or ''
        job['description'] = job.get('description') or full_data.get('description') or ''
        
        # Standardize timestamps
        job['created_at'] = get_iso_timestamp(job.get('created_at', ''))
        job['updated_at'] = get_iso_timestamp(job.get('updated_at', ''))
        
        print(f"   Title: {job['title']}")
        print(f"   Company: {job['company']}")
        print(f"   Created: {job['created_at']}")
        print(f"   Updated: {job['updated_at']}")
        print()
    
    # Save updated index
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Updated {len(index.get('job_listings', []))} job listings")
    print(f"✅ Saved to {index_path}")


if __name__ == "__main__":
    fix_job_listing_index()

