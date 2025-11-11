#!/usr/bin/env python3
"""
Surgical Resume Update - Replace specific experiences/sections only

This script surgically replaces ONLY the experiences/sections you specify,
leaving all other content untouched.

Usage Examples:
    # Replace specific experiences by employer name
    python scripts/surgical_resume_update.py \
        --resume-id "141107d3-f0a9-4bc6-82dd-6fc4506e76f4" \
        --experiences-file "data/experiences_solution_architect.json" \
        --replace-employers "Daugherty – Cox Communications" "CGI – Daugherty / Edward Jones" "BPM Software Solutions"

    # Replace experiences and update summary
    python scripts/surgical_resume_update.py \
        --resume-id "141107d3-f0a9-4bc6-82dd-6fc4506e76f4" \
        --experiences-file "data/experiences_solution_architect.json" \
        --replace-employers "Daugherty – Cox Communications" "CGI – Daugherty / Edward Jones" "BPM Software Solutions" \
        --updates-file "data/resume_updates_solution_architect.json"

    # Replace by resume name
    python scripts/surgical_resume_update.py \
        --resume "Master Resume" \
        --experiences-file "data/experiences_solution_architect.json" \
        --replace-employers "Daugherty – Cox Communications" "CGI – Daugherty / Edward Jones" "BPM Software Solutions"
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent.parent))


def load_resume_index(data_dir: Path) -> Dict[str, Any]:
    """Load the resume index file."""
    index_file = data_dir / "resumes" / "index.json"
    if not index_file.exists():
        raise FileNotFoundError(f"Resume index not found: {index_file}")
    with open(index_file, "r", encoding="utf-8") as f:
        return json.load(f)


def save_resume_index(data_dir: Path, index_data: Dict[str, Any]) -> None:
    """Save the resume index file."""
    index_file = data_dir / "resumes" / "index.json"
    with open(index_file, "w", encoding="utf-8") as f:
        json.dump(index_data, f, indent=2, ensure_ascii=False)


def find_resume_by_identifier(
    index_data: Dict[str, Any], identifier: str
) -> Optional[Dict[str, Any]]:
    """Find a resume by name or company identifier."""
    identifier_lower = identifier.lower()
    for resume in index_data.get("resumes", []):
        name = resume.get("name", "").lower()
        if identifier_lower in name or name in identifier_lower:
            return resume
    return None


def load_resume(data_dir: Path, resume_id: str) -> Dict[str, Any]:
    """Load a resume by ID."""
    resume_file = data_dir / "resumes" / f"{resume_id}.json"
    if not resume_file.exists():
        raise FileNotFoundError(f"Resume file not found: {resume_file}")
    with open(resume_file, "r", encoding="utf-8") as f:
        return json.load(f)


def save_resume(data_dir: Path, resume_id: str, resume_data: Dict[str, Any]) -> None:
    """Save a resume by ID."""
    resume_file = data_dir / "resumes" / f"{resume_id}.json"
    with open(resume_file, "w", encoding="utf-8") as f:
        json.dump(resume_data, f, indent=2, ensure_ascii=False)


def parse_json_experiences(json_file: Path) -> List[Dict[str, Any]]:
    """Parse experiences from JSON file."""
    if not json_file.exists():
        raise FileNotFoundError(f"Experiences file not found: {json_file}")

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list):
        return data
    elif isinstance(data, dict) and "experiences" in data:
        return data["experiences"]
    else:
        raise ValueError("JSON must contain 'experiences' array or be an array directly")


def load_updates(updates_file: Path) -> Dict[str, Any]:
    """Load section updates from JSON file."""
    if not updates_file.exists():
        raise FileNotFoundError(f"Updates file not found: {updates_file}")

    with open(updates_file, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize_employer_name(name: str) -> str:
    """Normalize employer name for comparison (handle special characters)."""
    # Convert to lowercase and normalize unicode characters
    normalized = name.lower()
    # Replace common dash variants with standard hyphen
    normalized = normalized.replace("–", "-").replace("—", "-").replace("−", "-")
    return normalized


def ensure_experience_level_tags(exp: Dict[str, Any]) -> Dict[str, Any]:
    """Ensure tags exist at the experience level by promoting any bullet-level tags.

    - Collects unique tags from bullets (if present)
    - Merges with existing exp['tags'] if already present
    - Does NOT remove bullet-level tags (non-destructive)
    """
    # Collect from bullets
    promoted: List[str] = []
    for b in exp.get("bullets", []) or []:
        tags = b.get("tags")
        if isinstance(tags, list):
            promoted.extend([str(t) for t in tags])

    # Merge with existing experience-level tags
    existing = exp.get("tags", []) or []
    merged = []
    seen = set()
    for t in list(existing) + promoted:
        if t not in seen:
            merged.append(t)
            seen.add(t)

    if merged:
        exp["tags"] = merged
    return exp


def select_matching_new_experiences(
    employers_to_replace: List[str], new_experiences: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Select only the new experiences whose employer matches the replacement list."""
    by_employer = {
        normalize_employer_name(e.get("employer", "")): e for e in new_experiences
    }
    selected: List[Dict[str, Any]] = []
    missing: List[str] = []
    for emp in employers_to_replace:
        key = normalize_employer_name(emp)
        if key in by_employer:
            selected.append(ensure_experience_level_tags(by_employer[key]))
        else:
            missing.append(emp)

    if missing:
        print(
            "Warning: No matching new experiences found for: "
            + ", ".join(missing),
            file=sys.stderr,
        )
    return selected


def replace_experiences_surgically(
    resume_data: Dict[str, Any],
    new_experiences: List[Dict[str, Any]],
    employers_to_replace: List[str],
) -> Dict[str, Any]:
    """
    Surgically replace only the specified experiences by employer name.

    - Keeps all other experiences intact
    - Inserts only the provided matching new experiences (does not add unrelated ones)

    Args:
        resume_data: Resume data
        new_experiences: List of new experience entries
        employers_to_replace: List of employer names to replace

    Returns:
        Updated resume data
    """
    if "experience" not in resume_data:
        resume_data["experience"] = []

    # Create a set of normalized employers to replace
    employers_normalized = {normalize_employer_name(emp) for emp in employers_to_replace}

    # Keep only experiences NOT in the replacement list
    kept_experiences = [
        exp
        for exp in resume_data.get("experience", [])
        if normalize_employer_name(exp.get("employer", "")) not in employers_normalized
    ]

    # Select only matching new experiences and ensure experience-level tags
    matching_new = select_matching_new_experiences(employers_to_replace, new_experiences)

    # Add new experiences at the beginning (preserves all others)
    resume_data["experience"] = matching_new + kept_experiences

    return resume_data


def update_sections(resume_data: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    """Update specified sections of the resume."""
    for section, value in updates.items():
        resume_data[section] = value
    return resume_data


def main():
    parser = argparse.ArgumentParser(
        description="Surgically update resume - replace only specified experiences/sections"
    )
    parser.add_argument(
        "--resume", help="Resume name or company identifier (e.g., 'Ford', 'Master Resume')"
    )
    parser.add_argument("--resume-id", help="Resume UUID (alternative to --resume)")
    parser.add_argument(
        "--experiences-file",
        help="Path to JSON file with new experiences",
    )
    parser.add_argument(
        "--replace-employers",
        nargs="+",
        help="Employer names to replace (e.g., 'Daugherty – Cox Communications' 'BPM Software Solutions')",
    )
    parser.add_argument(
        "--updates-file",
        help="Path to JSON file with section updates (summary, core_competencies, etc.)",
    )
    parser.add_argument(
        "--data-dir", default="data", help="Data directory path (default: data)"
    )

    args = parser.parse_args()

    # Validate arguments
    if not args.resume and not args.resume_id:
        parser.error("Either --resume or --resume-id must be provided")

    if not args.experiences_file and not args.updates_file:
        parser.error("Either --experiences-file or --updates-file must be provided")

    if args.experiences_file and not args.replace_employers:
        parser.error("--experiences-file requires --replace-employers to specify which employers to replace")

    try:
        data_dir = Path(args.data_dir)

        # Find resume
        if args.resume_id:
            resume_id = args.resume_id
            print(f"Using resume ID: {resume_id}")
        else:
            print(f"Searching for resume matching: {args.resume}")
            index_data = load_resume_index(data_dir)
            resume_meta = find_resume_by_identifier(index_data, args.resume)

            if not resume_meta:
                print(f"Error: No resume found matching '{args.resume}'", file=sys.stderr)
                print("\nAvailable resumes:", file=sys.stderr)
                for r in index_data.get("resumes", []):
                    print(f"  - {r['name']} (ID: {r['id']})", file=sys.stderr)
                sys.exit(1)

            resume_id = resume_meta["id"]
            print(f"Found resume: {resume_meta['name']} (ID: {resume_id})")

        # Load resume
        print(f"\nLoading resume...")
        resume_data = load_resume(data_dir, resume_id)

        # Replace experiences surgically
        if args.experiences_file and args.replace_employers:
            print(f"\nParsing new experiences from: {args.experiences_file}")
            new_experiences = parse_json_experiences(Path(args.experiences_file))
            print(f"Found {len(new_experiences)} new experience entries")

            print(f"\nReplacing experiences for:")
            for employer in args.replace_employers:
                print(f"  • {employer}")

            resume_data = replace_experiences_surgically(
                resume_data, new_experiences, args.replace_employers
            )
            print(f"✓ Experiences replaced surgically")

        # Update other sections
        if args.updates_file:
            print(f"\nLoading section updates from: {args.updates_file}")
            updates = load_updates(Path(args.updates_file))
            print(f"Updating {len(updates)} sections:")
            for section in updates.keys():
                print(f"  • {section}")

            resume_data = update_sections(resume_data, updates)
            print(f"✓ Sections updated")

        # Save resume
        print(f"\nSaving resume...")
        save_resume(data_dir, resume_id, resume_data)

        # Update timestamp in index
        index_data = load_resume_index(data_dir)
        for resume in index_data.get("resumes", []):
            if resume["id"] == resume_id:
                resume["updated_at"] = datetime.now().isoformat()
                break

        save_resume_index(data_dir, index_data)

        print(f"\n[SUCCESS] Successfully updated resume {resume_id}")

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

