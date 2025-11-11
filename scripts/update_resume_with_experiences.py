#!/usr/bin/env python3
"""
Reusable Script to Update Resumes with Experiences

This script provides a flexible way to update any resume with new experiences.
Supports multiple input formats: JSON, markdown, or direct Python data structures.

Usage Examples:
    # Update from JSON file
    python scripts/update_resume_with_experiences.py \\
        --resume-id "141107d3-f0a9-4bc6-82dd-6fc4506e76f4" \\
        --experiences-file "experiences.json"

    # Update from markdown file
    python scripts/update_resume_with_experiences.py \\
        --resume "Master Resume" \\
        --experiences-file "experiences.md" \\
        --format markdown

    # Replace all experiences (default: prepend)
    python scripts/update_resume_with_experiences.py \\
        --resume-id "141107d3-f0a9-4bc6-82dd-6fc4506e76f4" \\
        --experiences-file "experiences.json" \\
        --replace

    # Use custom data directory
    python scripts/update_resume_with_experiences.py \\
        --resume "Ford" \\
        --experiences-file "experiences.json" \\
        --data-dir "data"
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.crud import get_resume_by_identifier, save_resume


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


def parse_json_experiences(json_file: Path) -> List[Dict[str, Any]]:
    """
    Parse experiences from JSON file.

    Expected format:
    {
        "experiences": [
            {
                "employer": "Company Name",
                "role": "Job Title",
                "dates": "Start – End",
                "location": "City, State",
                "bullets": [
                    {"text": "Bullet point 1", "tags": ["tag1", "tag2"]},
                    {"text": "Bullet point 2", "tags": []}
                ]
            }
        ]
    }
    """
    if not json_file.exists():
        raise FileNotFoundError(f"Experiences file not found: {json_file}")

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Support both direct array and wrapped object
    if isinstance(data, list):
        return data
    elif isinstance(data, dict) and "experiences" in data:
        return data["experiences"]
    else:
        raise ValueError("JSON must contain 'experiences' array or be an array directly")


def parse_markdown_experiences(md_file: Path) -> List[Dict[str, Any]]:
    """
    Parse experiences from markdown file.

    Expected format:
    ### Company Name — Role (Dates)
    * Bullet point 1
    * Bullet point 2

    **Tags:** tag1, tag2
    """
    if not md_file.exists():
        raise FileNotFoundError(f"Experiences file not found: {md_file}")

    with open(md_file, "r", encoding="utf-8") as f:
        content = f.read()

    experiences = []
    sections = re.split(r"\n### ", content)

    for section in sections[1:]:  # Skip first section
        lines = section.strip().split("\n")
        if not lines:
            continue

        header = lines[0].strip()
        match = re.match(r"(.+?)\s*[—–-]\s*(.+?)\s*\((.+?)\)", header)

        if not match:
            print(f"Warning: Could not parse header: {header}", file=sys.stderr)
            continue

        employer = match.group(1).strip()
        role = match.group(2).strip()
        dates = match.group(3).strip()

        bullets = []
        tags = []

        for line in lines[1:]:
            line = line.strip()

            if line.startswith("**Tags:**"):
                tags_str = line.replace("**Tags:**", "").strip()
                tags = [tag.strip() for tag in tags_str.split(",")]
                continue

            if line.startswith("*"):
                bullet_text = line[1:].strip()
                if bullet_text:
                    bullets.append({"text": bullet_text, "tags": tags if tags else []})

        experience = {
            "employer": employer,
            "role": role,
            "dates": dates,
            "location": "",
            "bullets": bullets,
        }

        experiences.append(experience)

    return experiences


def parse_experiences(experiences_file: Path, format_type: str) -> List[Dict[str, Any]]:
    """
    Parse experiences from file based on format.

    Args:
        experiences_file: Path to experiences file
        format_type: Format type ('json' or 'markdown')

    Returns:
        List of experience dictionaries
    """
    if format_type == "json":
        return parse_json_experiences(experiences_file)
    elif format_type == "markdown":
        return parse_markdown_experiences(experiences_file)
    else:
        raise ValueError(f"Unsupported format: {format_type}")


def update_resume_experiences(
    data_dir: Path,
    resume_id: str,
    experiences: List[Dict[str, Any]],
    replace: bool = False,
) -> None:
    """
    Update a resume's experience section.

    Args:
        data_dir: Data directory path
        resume_id: Resume UUID
        experiences: List of experience dictionaries
        replace: If True, replace all experience; if False, prepend
    """
    resume_file = data_dir / "resumes" / f"{resume_id}.json"

    if not resume_file.exists():
        raise FileNotFoundError(f"Resume file not found: {resume_file}")

    # Load resume
    with open(resume_file, "r", encoding="utf-8") as f:
        resume_data = json.load(f)

    # Update experience
    if replace:
        resume_data["experience"] = experiences
    else:
        existing_experience = resume_data.get("experience", [])
        resume_data["experience"] = experiences + existing_experience

    # Save resume
    with open(resume_file, "w", encoding="utf-8") as f:
        json.dump(resume_data, f, indent=2, ensure_ascii=False)

    # Update timestamp in index
    index_data = load_resume_index(data_dir)
    for resume in index_data.get("resumes", []):
        if resume["id"] == resume_id:
            resume["updated_at"] = datetime.now().isoformat()
            break

    save_resume_index(data_dir, index_data)


def main():
    parser = argparse.ArgumentParser(
        description="Update resume with new experiences from file"
    )
    parser.add_argument(
        "--resume", help="Resume name or company identifier (e.g., 'Ford', 'Master Resume')"
    )
    parser.add_argument("--resume-id", help="Resume UUID (alternative to --resume)")
    parser.add_argument(
        "--experiences-file",
        required=True,
        help="Path to experiences file (JSON or markdown)",
    )
    parser.add_argument(
        "--format",
        choices=["json", "markdown"],
        default="json",
        help="File format (default: json)",
    )
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Replace all experience (default: prepend)",
    )
    parser.add_argument(
        "--data-dir", default="data", help="Data directory path (default: data)"
    )

    args = parser.parse_args()

    if not args.resume and not args.resume_id:
        parser.error("Either --resume or --resume-id must be provided")

    try:
        data_dir = Path(args.data_dir)
        experiences_file = Path(args.experiences_file)

        # Find resume
        if args.resume_id:
            resume_id = args.resume_id
            print(f"Using resume ID: {resume_id}")
        else:
            print(f"Searching for resume matching: {args.resume}")
            index_data = load_resume_index(data_dir)
            resume_meta = None
            for r in index_data.get("resumes", []):
                if args.resume.lower() in r["name"].lower() or r["name"].lower() in args.resume.lower():
                    resume_meta = r
                    break

            if not resume_meta:
                print(f"Error: No resume found matching '{args.resume}'", file=sys.stderr)
                print("\nAvailable resumes:", file=sys.stderr)
                for r in index_data.get("resumes", []):
                    print(f"  - {r['name']} (ID: {r['id']})", file=sys.stderr)
                sys.exit(1)

            resume_id = resume_meta["id"]
            print(f"Found resume: {resume_meta['name']} (ID: {resume_id})")

        # Parse experiences
        print(f"\nParsing experiences from: {experiences_file} (format: {args.format})")
        experiences = parse_experiences(experiences_file, args.format)
        print(f"Found {len(experiences)} experience entries")

        for i, exp in enumerate(experiences, 1):
            print(f"  {i}. {exp['employer']} — {exp['role']} ({exp['dates']})")
            print(f"     Bullets: {len(exp.get('bullets', []))}")

        # Update resume
        print(f"\nUpdating resume...")
        update_resume_experiences(data_dir, resume_id, experiences, args.replace)

        print(f"\n[SUCCESS] Successfully updated resume {resume_id}")
        print(f"   Experience entries: {'replaced' if args.replace else 'prepended'}")

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

