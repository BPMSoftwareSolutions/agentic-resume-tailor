#!/usr/bin/env python3
"""
Fix resume timestamps to ISO 8601 format with Z suffix.

This script:
1. Loads all resume metadata from index
2. Fixes malformed timestamps (e.g., "2025-10-11\n1T19:07:06.199315" -> "2025-10-11T19:07:06.199315Z")
3. Ensures all timestamps end with Z
"""

import json
import re
from pathlib import Path


def fix_timestamp(ts: str) -> str:
    """Fix malformed timestamp to ISO 8601 with Z suffix."""
    if not ts:
        return ts
    
    # If already has Z, return as-is
    if ts.endswith("Z"):
        return ts
    
    # Fix newline issues (e.g., "2025-10-11\n1T19:07:06.199315")
    ts = ts.replace("\n", "")
    
    # If has +00:00, replace with Z
    if ts.endswith("+00:00"):
        return ts.replace("+00:00", "Z")
    
    # Add Z if not present
    if not ts.endswith("Z"):
        return ts + "Z"
    
    return ts


def fix_resume_timestamps():
    """Fix resume timestamps."""
    print("=" * 80)
    print("FIX RESUME TIMESTAMPS")
    print("=" * 80 + "\n")
    
    index_path = Path("data/resumes/index.json")
    
    if not index_path.exists():
        print("No resume index found")
        return
    
    # Load index
    with open(index_path, 'r', encoding='utf-8') as f:
        index = json.load(f)
    
    print(f"Processing {len(index.get('resumes', []))} resumes...\n")
    
    # Fix each resume
    fixed_count = 0
    for resume in index.get('resumes', []):
        resume_id = resume.get('id')
        created_at = resume.get('created_at', '')
        updated_at = resume.get('updated_at', '')
        
        fixed_created = fix_timestamp(created_at)
        fixed_updated = fix_timestamp(updated_at)
        
        if fixed_created != created_at or fixed_updated != updated_at:
            print(f"[{fixed_count + 1}] {resume_id}")
            if fixed_created != created_at:
                print(f"   created_at: {created_at} -> {fixed_created}")
                resume['created_at'] = fixed_created
            if fixed_updated != updated_at:
                print(f"   updated_at: {updated_at} -> {fixed_updated}")
                resume['updated_at'] = fixed_updated
            fixed_count += 1
            print()
    
    # Save updated index
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Fixed {fixed_count} resumes")
    print(f"✅ Saved to {index_path}")


if __name__ == "__main__":
    fix_resume_timestamps()

