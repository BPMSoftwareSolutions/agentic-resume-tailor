#!/usr/bin/env python3
"""
Achievements CRUD Operations

Manage achievements data in resumes.

Usage:
    # Add new achievement
    python src/crud/achievements.py --resume "Ford" --add "AWS Certified Solutions Architect"

    # List all achievements
    python src/crud/achievements.py --resume "Ford" --list

    # Update/replace an achievement
    python src/crud/achievements.py --resume "Ford" --update "Old Text" "New Text"

    # Delete an achievement
    python src/crud/achievements.py --resume "Ford" --delete "Text to remove"

    # Clear all achievements
    python src/crud/achievements.py --resume "Ford" --clear

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


def add_achievement(resume_data: Dict[str, Any], achievement: str) -> Dict[str, Any]:
    """
    Add a new achievement to the resume.

    Args:
        resume_data: Resume data
        achievement: Achievement to add

    Returns:
        Updated resume data
    """
    if "achievements" not in resume_data:
        resume_data["achievements"] = []

    # Check for duplicates (case-insensitive)
    achievement_lower = achievement.lower()
    for existing in resume_data["achievements"]:
        if existing.lower() == achievement_lower:
            print_error(f"Achievement already exists: {existing}")
            sys.exit(3)

    resume_data["achievements"].append(achievement)
    return resume_data


def list_achievements(resume_data: Dict[str, Any]) -> List[str]:
    """
    List all achievements in the resume.

    Args:
        resume_data: Resume data

    Returns:
        List of achievements
    """
    return resume_data.get("achievements", [])


def update_achievement(
    resume_data: Dict[str, Any], old_text: str, new_text: str
) -> Dict[str, Any]:
    """
    Update/replace an achievement.

    Args:
        resume_data: Resume data
        old_text: Text to find and replace
        new_text: New text

    Returns:
        Updated resume data
    """
    if "achievements" not in resume_data:
        resume_data["achievements"] = []

    # Find and replace (case-insensitive search)
    old_lower = old_text.lower()
    found = False

    for i, achievement in enumerate(resume_data["achievements"]):
        if achievement.lower() == old_lower:
            resume_data["achievements"][i] = new_text
            found = True
            break

    if not found:
        print_error(f"Achievement not found: {old_text}")
        sys.exit(3)

    return resume_data


def delete_achievement(resume_data: Dict[str, Any], text: str) -> Dict[str, Any]:
    """
    Delete an achievement.

    Args:
        resume_data: Resume data
        text: Text to delete

    Returns:
        Updated resume data
    """
    if "achievements" not in resume_data:
        resume_data["achievements"] = []

    # Find and remove (case-insensitive search)
    text_lower = text.lower()
    original_count = len(resume_data["achievements"])

    resume_data["achievements"] = [
        a for a in resume_data["achievements"] if a.lower() != text_lower
    ]

    if len(resume_data["achievements"]) == original_count:
        print_error(f"Achievement not found: {text}")
        sys.exit(3)

    return resume_data


def clear_achievements(resume_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Clear all achievements.

    Args:
        resume_data: Resume data

    Returns:
        Updated resume data
    """
    resume_data["achievements"] = []
    return resume_data


def main():
    parser = argparse.ArgumentParser(
        description="Manage achievements in resumes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add new achievement
  python src/crud/achievements.py --resume "Ford" --add "AWS Certified Solutions Architect"
  
  # List all achievements
  python src/crud/achievements.py --resume "Ford" --list
  
  # Update an achievement
  python src/crud/achievements.py --resume "Ford" --update "Old Text" "New Text"
  
  # Delete an achievement
  python src/crud/achievements.py --resume "Ford" --delete "GitHub Community Contributor"
  
  # Clear all achievements
  python src/crud/achievements.py --resume "Ford" --clear
        """,
    )

    # Resume identification
    parser.add_argument(
        "--resume",
        help="Resume name or company identifier (e.g., 'Ford', 'Master Resume')",
    )
    parser.add_argument("--resume-id", help="Resume UUID (alternative to --resume)")

    # Operations
    parser.add_argument("--add", metavar="TEXT", help="Add new achievement")
    parser.add_argument("--list", action="store_true", help="List all achievements")
    parser.add_argument(
        "--update", nargs=2, metavar=("OLD", "NEW"), help="Update/replace achievement"
    )
    parser.add_argument("--delete", metavar="TEXT", help="Delete achievement")
    parser.add_argument("--clear", action="store_true", help="Clear all achievements")

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
            achievements_list = list_achievements(resume_data)
            print(f"\nAchievements ({len(achievements_list)}):")
            for i, achievement in enumerate(achievements_list, 1):
                print(f"  {i}. {achievement}")

        if args.add:
            resume_data = add_achievement(resume_data, args.add)
            modified = True
            print_success(f"Added achievement: {args.add}")

        if args.update:
            old_text, new_text = args.update
            resume_data = update_achievement(resume_data, old_text, new_text)
            modified = True
            print_success(f"Updated achievement: '{old_text}' -> '{new_text}'")

        if args.delete:
            resume_data = delete_achievement(resume_data, args.delete)
            modified = True
            print_success(f"Deleted achievement: {args.delete}")

        if args.clear:
            resume_data = clear_achievements(resume_data)
            modified = True
            print_success("Cleared all achievements")

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
