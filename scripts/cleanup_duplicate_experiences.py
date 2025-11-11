#!/usr/bin/env python3
"""Remove duplicate experiences from a resume, keeping only the first occurrence of each employer."""

import json
import sys
from pathlib import Path

def cleanup_duplicates(resume_file: Path) -> None:
    """Remove duplicate experiences by employer name."""
    if not resume_file.exists():
        print(f"Error: Resume file not found: {resume_file}", file=sys.stderr)
        sys.exit(1)

    # Load the resume
    with open(resume_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Get unique experiences by employer name (keep first occurrence)
    seen_employers = set()
    unique_experiences = []

    for exp in data.get('experience', []):
        employer = exp.get('employer', '')
        if employer not in seen_employers:
            unique_experiences.append(exp)
            seen_employers.add(employer)

    # Update the resume
    data['experience'] = unique_experiences

    # Save it back
    with open(resume_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✓ Cleaned up duplicates. Now have {len(unique_experiences)} unique experiences:")
    for i, exp in enumerate(unique_experiences, 1):
        print(f"  {i}. {exp['employer']} - {exp['role']}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python cleanup_duplicate_experiences.py <resume_file>")
        sys.exit(1)

    resume_file = Path(sys.argv[1])
    cleanup_duplicates(resume_file)

