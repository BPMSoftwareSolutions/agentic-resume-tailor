#!/usr/bin/env python3
"""
Verify that no resumes reference deleted experience IDs.

Deleted IDs:
- 0defdac1-d9bd-457f-904a-4c0609b84c32
- 363bf2ac-eab2-43ba-8c01-28f834a53799
- 3395fe5a-c811-4c31-8847-7a08431cca2f
"""

import json
from pathlib import Path

DELETED_IDS = {
    "0defdac1-d9bd-457f-904a-4c0609b84c32",
    "363bf2ac-eab2-43ba-8c01-28f834a53799",
    "3395fe5a-c811-4c31-8847-7a08431cca2f",
}


def check_resume_references():
    """Check all resumes for references to deleted IDs."""
    resumes_dir = Path("data/resumes")
    
    if not resumes_dir.exists():
        print("No resumes directory found")
        return True
    
    # Check index
    index_file = resumes_dir / "index.json"
    if index_file.exists():
        with open(index_file, 'r', encoding='utf-8') as f:
            index = json.load(f)
        
        print(f"Checking {len(index.get('resumes', []))} resumes in index...")
        for resume_meta in index.get('resumes', []):
            resume_id = resume_meta.get('id')
            resume_name = resume_meta.get('name')
            print(f"  - {resume_name} ({resume_id})")
    
    # Check individual resume files
    resume_files = list(resumes_dir.glob("*.json"))
    resume_files = [f for f in resume_files if f.name != "index.json"]
    
    print(f"\nChecking {len(resume_files)} resume files for deleted experience references...")
    
    found_references = False
    for resume_file in resume_files:
        try:
            with open(resume_file, 'r', encoding='utf-8') as f:
                resume_data = json.load(f)
            
            # Check if any experience entry has a deleted ID
            for exp in resume_data.get('experience', []):
                exp_id = exp.get('id')
                if exp_id in DELETED_IDS:
                    print(f"  ❌ {resume_file.name}: Found deleted experience ID {exp_id}")
                    found_references = True
        except Exception as e:
            print(f"  ⚠️  Error reading {resume_file.name}: {e}")
    
    if not found_references:
        print("  ✅ No references to deleted experience IDs found")
    
    return not found_references


if __name__ == "__main__":
    print("=" * 80)
    print("VERIFY NO DELETED EXPERIENCE REFERENCES")
    print("=" * 80 + "\n")
    
    success = check_resume_references()
    
    if success:
        print("\n✅ Verification passed: No resumes reference deleted experience IDs")
    else:
        print("\n❌ Verification failed: Found references to deleted experience IDs")
        exit(1)

