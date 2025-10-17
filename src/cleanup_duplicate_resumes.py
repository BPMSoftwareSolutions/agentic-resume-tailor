#!/usr/bin/env python3
"""
Clean up duplicate resumes in the index.

This script identifies resumes with duplicate names and removes all but the most
recently updated copy, keeping the data consistent.

Usage:
    python src/cleanup_duplicate_resumes.py [--dry-run]

Options:
    --dry-run: Show what would be deleted without actually deleting

Related to GitHub Issue #XX (Duplicate Resume Names)
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.models.resume import Resume


def find_duplicates(resumes: List[Dict]) -> Dict[str, List[Dict]]:
    """
    Find resumes with duplicate names.

    Args:
        resumes: List of resume metadata dictionaries

    Returns:
        Dictionary mapping resume names to list of resume metadata
    """
    duplicates = {}
    for resume in resumes:
        name = resume["name"].lower()
        if name not in duplicates:
            duplicates[name] = []
        duplicates[name].append(resume)

    # Filter to only those with duplicates
    return {k: v for k, v in duplicates.items() if len(v) > 1}


def get_cleanup_plan(duplicates: Dict[str, List[Dict]]) -> List[Tuple[str, str]]:
    """
    Generate a cleanup plan: which resumes to delete.

    For each duplicate name, keep the most recently updated resume and mark
    others for deletion.

    Args:
        duplicates: Dictionary of duplicate resume names and their metadata

    Returns:
        List of (resume_id, resume_name) tuples to delete
    """
    to_delete = []

    for name, resumes in duplicates.items():
        # Sort by updated_at (newest first)
        sorted_resumes = sorted(
            resumes, key=lambda r: r.get("updated_at", ""), reverse=True
        )

        # Keep the first (newest), delete the rest
        for resume in sorted_resumes[1:]:
            to_delete.append((resume["id"], resume["name"]))

    return to_delete


def cleanup_duplicates(data_dir: Path, dry_run: bool = True) -> bool:
    """
    Clean up duplicate resumes.

    Args:
        data_dir: Data directory path
        dry_run: If True, only show what would be deleted

    Returns:
        True if successful, False otherwise
    """
    try:
        # Load resume index
        index_file = data_dir / "resumes" / "index.json"
        with open(index_file, "r", encoding="utf-8") as f:
            index = json.load(f)

        resumes = index.get("resumes", [])

        # Find duplicates
        duplicates = find_duplicates(resumes)

        if not duplicates:
            print("✅ No duplicate resumes found!")
            return True

        print(f"\n📋 Found {len(duplicates)} resume names with duplicates:\n")
        for name, resume_list in sorted(duplicates.items()):
            print(f"   • {name}: {len(resume_list)} copies")

        # Get cleanup plan
        to_delete = get_cleanup_plan(duplicates)

        print(f"\n🗑️  Will delete {len(to_delete)} resume(s):\n")
        for resume_id, resume_name in to_delete:
            print(f"   • {resume_name} (ID: {resume_id})")

        if dry_run:
            print("\n⚠️  DRY RUN MODE - No changes made")
            print("   Run without --dry-run to actually delete these resumes")
            return True

        # Initialize Resume model
        resume_model = Resume(data_dir)

        # Delete duplicates
        print("\n🔄 Deleting duplicate resumes...\n")
        deleted_count = 0
        for resume_id, resume_name in to_delete:
            if resume_model.delete(resume_id):
                print(f"   ✅ Deleted: {resume_name}")
                deleted_count += 1
            else:
                print(f"   ❌ Failed to delete: {resume_name}")

        print(f"\n✅ Cleanup complete! Deleted {deleted_count} resume(s)")
        return True

    except Exception as e:
        print(f"❌ Error during cleanup: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Clean up duplicate resumes in the index",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Show what would be deleted (dry run)
  python src/cleanup_duplicate_resumes.py --dry-run
  
  # Actually delete duplicate resumes
  python src/cleanup_duplicate_resumes.py
        """,
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be deleted without actually deleting",
    )

    parser.add_argument(
        "--data-dir", default="data", help="Data directory path (default: data)"
    )

    args = parser.parse_args()

    data_dir = Path(args.data_dir)

    success = cleanup_duplicates(data_dir, dry_run=args.dry_run)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

