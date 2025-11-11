#!/usr/bin/env python3
"""
Update Resume Sections - Comprehensive Resume Update Script

This script updates any section of a resume: summary, competencies, experience, etc.
Fully reusable with no hard-coding.

Usage Examples:
    # Update summary
    python scripts/update_resume_sections.py \
        --resume-id "141107d3-f0a9-4bc6-82dd-6fc4506e76f4" \
        --section summary \
        --value "Your new summary text here"

    # Update core competencies
    python scripts/update_resume_sections.py \
        --resume-id "141107d3-f0a9-4bc6-82dd-6fc4506e76f4" \
        --section core_competencies \
        --file "competencies.json"

    # Update from file
    python scripts/update_resume_sections.py \
        --resume "Master Resume" \
        --section summary \
        --file "summary.txt"

    # Update multiple sections from JSON
    python scripts/update_resume_sections.py \
        --resume-id "141107d3-f0a9-4bc6-82dd-6fc4506e76f4" \
        --file "resume_updates.json"
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

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


def update_resume_section(
    resume_data: Dict[str, Any], section: str, value: Any
) -> Dict[str, Any]:
    """
    Update a single section of the resume.

    Args:
        resume_data: Resume data
        section: Section name (e.g., 'summary', 'core_competencies')
        value: New value for the section

    Returns:
        Updated resume data
    """
    resume_data[section] = value
    return resume_data


def update_resume_multiple_sections(
    resume_data: Dict[str, Any], updates: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update multiple sections of the resume.

    Args:
        resume_data: Resume data
        updates: Dictionary of section -> value pairs

    Returns:
        Updated resume data
    """
    for section, value in updates.items():
        resume_data[section] = value
    return resume_data


def load_value_from_file(file_path: Path) -> Any:
    """
    Load value from file (JSON or text).

    Args:
        file_path: Path to file

    Returns:
        Parsed value
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Try to parse as JSON first
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # Return as plain text
        return content.strip()


def main():
    parser = argparse.ArgumentParser(
        description="Update resume sections (summary, competencies, etc.)"
    )
    parser.add_argument(
        "--resume", help="Resume name or company identifier (e.g., 'Ford', 'Master Resume')"
    )
    parser.add_argument("--resume-id", help="Resume UUID (alternative to --resume)")
    parser.add_argument(
        "--section",
        help="Section to update (e.g., 'summary', 'core_competencies', 'professional_summary')",
    )
    parser.add_argument("--value", help="Value to set (for single section updates)")
    parser.add_argument(
        "--file",
        help="File containing value(s) to update. For single section: text or JSON. For multiple: JSON with section->value pairs",
    )
    parser.add_argument(
        "--data-dir", default="data", help="Data directory path (default: data)"
    )

    args = parser.parse_args()

    # Validate arguments
    if not args.resume and not args.resume_id:
        parser.error("Either --resume or --resume-id must be provided")

    if not args.section and not args.file:
        parser.error("Either --section or --file must be provided")

    if args.section and not args.value and not args.file:
        parser.error("For single section update, provide --value or --file")

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

        # Determine updates
        if args.file:
            file_path = Path(args.file)
            value = load_value_from_file(file_path)

            if args.section:
                # Single section update from file
                print(f"Updating section '{args.section}' from file: {file_path}")
                resume_data = update_resume_section(resume_data, args.section, value)
                print(f"  ✓ Section updated")
            else:
                # Multiple sections from JSON file
                if not isinstance(value, dict):
                    print(
                        "Error: For multiple section updates, file must contain JSON object",
                        file=sys.stderr,
                    )
                    sys.exit(1)

                print(f"Updating {len(value)} sections from file: {file_path}")
                resume_data = update_resume_multiple_sections(resume_data, value)
                for section in value.keys():
                    print(f"  ✓ Section '{section}' updated")
        else:
            # Single section update from command line
            print(f"Updating section '{args.section}'")
            resume_data = update_resume_section(resume_data, args.section, args.value)
            print(f"  ✓ Section updated")

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

