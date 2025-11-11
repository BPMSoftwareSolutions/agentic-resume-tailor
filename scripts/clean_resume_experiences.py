#!/usr/bin/env python3
"""Remove duplicate/old experiences from a resume, keeping only the first 3 (the clean ones with proper tags)."""

import json
import sys
from pathlib import Path

def clean_resume(resume_file: Path) -> None:
    """Keep only the first 3 experiences (the clean ones with proper tags)."""
    if not resume_file.exists():
        print(f"Error: Resume file not found: {resume_file}", file=sys.stderr)
        sys.exit(1)

    # Load the resume
    with open(resume_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Get the first 3 experiences (the clean ones)
    original_count = len(data.get('experience', []))
    data['experience'] = data.get('experience', [])[:3]

    # Save it back
    with open(resume_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✓ Cleaned resume. Removed {original_count - 3} duplicate/old experiences.")
    print(f"  Kept {len(data['experience'])} clean experiences:")
    for i, exp in enumerate(data['experience'], 1):
        print(f"    {i}. {exp['employer']} - {exp['role']}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python clean_resume_experiences.py <resume_file>")
        sys.exit(1)

    resume_file = Path(sys.argv[1])
    clean_resume(resume_file)

