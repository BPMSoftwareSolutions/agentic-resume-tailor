#!/usr/bin/env python3
"""
Areas of Expertise CRUD Operations

Manage areas of expertise data in resumes.

Usage:
    # Add new expertise area
    python src/crud/expertise.py --resume "Ford" --add "AI/ML Engineering"

    # List all expertise areas
    python src/crud/expertise.py --resume "Ford" --list

    # Update/replace an expertise area
    python src/crud/expertise.py --resume "Ford" --update "Old Text" "New Text"

    # Delete an expertise area
    python src/crud/expertise.py --resume "Ford" --delete "Text to remove"

    # Clear all expertise areas
    python src/crud/expertise.py --resume "Ford" --clear

Related to GitHub Issue #17
"""

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import shared utilities
from crud import (get_resume_by_identifier, print_error, print_info,
                  print_success, save_resume)


def add_expertise(resume_data: Dict[str, Any], expertise: str) -> Dict[str, Any]:
    """
    Add a new expertise area to the resume.

    Args:
        resume_data: Resume data
        expertise: Expertise area to add

    Returns:
        Updated resume data
    """
    if "areas_of_expertise" not in resume_data:
        resume_data["areas_of_expertise"] = []

    # Check for duplicates (case-insensitive)
    expertise_lower = expertise.lower()
    for existing in resume_data["areas_of_expertise"]:
        if existing.lower() == expertise_lower:
            print_error(f"Expertise area already exists: {existing}")
            sys.exit(3)

    resume_data["areas_of_expertise"].append(expertise)
    return resume_data


def list_expertise(resume_data: Dict[str, Any]) -> List[str]:
    """
    List all expertise areas in the resume.

    Args:
        resume_data: Resume data

    Returns:
        List of expertise areas
    """
    return resume_data.get("areas_of_expertise", [])


def update_expertise(
    resume_data: Dict[str, Any], old_text: str, new_text: str
) -> Dict[str, Any]:
    """
    Update/replace an expertise area.

    Args:
        resume_data: Resume data
        old_text: Text to find and replace
        new_text: New text

    Returns:
        Updated resume data
    """
    if "areas_of_expertise" not in resume_data:
        resume_data["areas_of_expertise"] = []

    # Find and replace (case-insensitive search)
    old_lower = old_text.lower()
    found = False

    for i, expertise in enumerate(resume_data["areas_of_expertise"]):
        if expertise.lower() == old_lower:
            resume_data["areas_of_expertise"][i] = new_text
            found = True
            break

    if not found:
        print_error(f"Expertise area not found: {old_text}")
        sys.exit(3)

    return resume_data


def delete_expertise(resume_data: Dict[str, Any], text: str) -> Dict[str, Any]:
    """
    Delete an expertise area.

    Args:
        resume_data: Resume data
        text: Text to delete

    Returns:
        Updated resume data
    """
    if "areas_of_expertise" not in resume_data:
        resume_data["areas_of_expertise"] = []

    # Find and remove (case-insensitive search)
    text_lower = text.lower()
    original_count = len(resume_data["areas_of_expertise"])

    resume_data["areas_of_expertise"] = [
        e for e in resume_data["areas_of_expertise"] if e.lower() != text_lower
    ]

    if len(resume_data["areas_of_expertise"]) == original_count:
        print_error(f"Expertise area not found: {text}")
        sys.exit(3)

    return resume_data


def clear_expertise(resume_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Clear all expertise areas.

    Args:
        resume_data: Resume data

    Returns:
        Updated resume data
    """
    resume_data["areas_of_expertise"] = []
    return resume_data


def main():
    parser = argparse.ArgumentParser(
        description="Manage areas of expertise in resumes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add new expertise area
  python src/crud/expertise.py --resume "Ford" --add "AI/ML Engineering"
  
  # List all expertise areas
  python src/crud/expertise.py --resume "Ford" --list
  
  # Update an expertise area
  python src/crud/expertise.py --resume "Ford" --update "Old Text" "New Text"
  
  # Delete an expertise area
  python src/crud/expertise.py --resume "Ford" --delete "Legacy System Maintenance"
  
  # Clear all expertise areas
  python src/crud/expertise.py --resume "Ford" --clear
        """,
    )

    # Resume identification
    parser.add_argument(
        "--resume",
        help="Resume name or company identifier (e.g., 'Ford', 'Master Resume')",
    )
    parser.add_argument("--resume-id", help="Resume UUID (alternative to --resume)")

    # Operations
    parser.add_argument("--add", metavar="TEXT", help="Add new expertise area")
    parser.add_argument("--list", action="store_true", help="List all expertise areas")
    parser.add_argument(
        "--update",
        nargs=2,
        metavar=("OLD", "NEW"),
        help="Update/replace expertise area",
    )
    parser.add_argument("--delete", metavar="TEXT", help="Delete expertise area")
    parser.add_argument(
        "--clear", action="store_true", help="Clear all expertise areas"
    )

    # Options
    parser.add_argument(
        "--data-dir", default="data", help="Data directory path (default: data)"
    )

    args = parser.parse_args()

    # Validate arguments
    if not args.resume and not args.resume_id:
        parser.error("Either --resume or --resume-id must be provided")

    # Check that at least one operation is specified
    operations = [args.add, args.list, args.update, args.delete, args.clear]
    if not any(operations):
        parser.error(
            "At least one operation (--add, --list, --update, --delete, --clear) must be specified"
        )

    try:
        data_dir = Path(args.data_dir)

        # Get resume
        resume_id, resume_data = get_resume_by_identifier(
            data_dir, identifier=args.resume, resume_id=args.resume_id
        )

        # Perform operation
        modified = False

        if args.list:
            expertise_list = list_expertise(resume_data)
            print(f"\nAreas of Expertise ({len(expertise_list)}):")
            for i, expertise in enumerate(expertise_list, 1):
                print(f"  {i}. {expertise}")

        if args.add:
            resume_data = add_expertise(resume_data, args.add)
            modified = True
            print_success(f"Added expertise area: {args.add}")

        if args.update:
            old_text, new_text = args.update
            resume_data = update_expertise(resume_data, old_text, new_text)
            modified = True
            print_success(f"Updated expertise area: '{old_text}' -> '{new_text}'")

        if args.delete:
            resume_data = delete_expertise(resume_data, args.delete)
            modified = True
            print_success(f"Deleted expertise area: {args.delete}")

        if args.clear:
            resume_data = clear_expertise(resume_data)
            modified = True
            print_success("Cleared all expertise areas")

        # Save if modified
        if modified:
            save_resume(data_dir, resume_id, resume_data)
            print_info(f"Resume updated: {resume_id}")

        sys.exit(0)

    except FileNotFoundError as e:
        print_error(str(e))
        sys.exit(2)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
