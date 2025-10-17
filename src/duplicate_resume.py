#!/usr/bin/env python3
"""
Duplicate Resume Script

This script duplicates an existing resume with a new name.
It follows the same patterns as CRUD scripts for consistency.

Usage:
    # Duplicate by resume name
    python src/duplicate_resume.py --resume "Ford" --new-name "Sidney_Jones_Engineering_Manager_Subscription_Billing"

    # Duplicate by resume ID
    python src/duplicate_resume.py --resume-id "d474d761-18f2-48ab-99b5-9f30c54f75b2" --new-name "New Resume Name"

    # Duplicate with description
    python src/duplicate_resume.py --resume "Ford" --new-name "New Resume" --description "Tailored for X position"

Related to GitHub Issue #19
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import shared utilities from CRUD
from src.crud import print_error, print_info, print_success
# Import Resume model
from src.models.resume import Resume


def duplicate_resume(
    data_dir: Path,
    source_identifier: Optional[str] = None,
    source_id: Optional[str] = None,
    new_name: str = "",
    description: str = "",
) -> bool:
    """
    Duplicate a resume.

    Args:
        data_dir: Data directory path
        source_identifier: Source resume name or company identifier (optional)
        source_id: Source resume UUID (optional)
        new_name: Name for the duplicated resume
        description: Optional description for the new resume

    Returns:
        True if successful, False otherwise

    Raises:
        ValueError: If neither identifier nor source_id provided
        FileNotFoundError: If source resume not found
    """
    if not source_identifier and not source_id:
        raise ValueError("Either source identifier or source_id must be provided")

    if not new_name:
        raise ValueError("New name must be provided")

    # Initialize Resume model
    resume_model = Resume(data_dir)

    # Find source resume
    if source_id:
        print_info(f"Using resume ID: {source_id}")
        # Verify resume exists
        source_data = resume_model.get(source_id)
        if not source_data:
            raise FileNotFoundError(f"Resume with ID '{source_id}' not found")
    else:
        print_info(f"Searching for resume: {source_identifier}")
        # Search by name
        all_resumes = resume_model.list_all()
        source_id = None
        identifier_lower = source_identifier.lower()

        for resume in all_resumes:
            name = resume.name.lower()
            if identifier_lower in name or name in identifier_lower:
                source_id = resume.id
                print_info(f"Found resume: {resume.name} (ID: {source_id})")
                break

        if not source_id:
            raise FileNotFoundError(f"No resume found matching '{source_identifier}'")

    # Duplicate the resume
    print_info(f"Duplicating resume...")
    try:
        new_metadata = resume_model.duplicate(source_id, new_name)
    except ValueError as e:
        # Handle duplicate name error
        raise ValueError(str(e))

    if not new_metadata:
        raise RuntimeError("Failed to duplicate resume")

    # Update description if provided
    if description:
        resume_model.update_metadata(new_metadata.id, description=description)
        print_info(f"Set description: {description}")
        # Reload metadata to get updated description
        all_resumes = resume_model.list_all()
        for resume in all_resumes:
            if resume.id == new_metadata.id:
                new_metadata = resume
                break

    return new_metadata


def main():
    parser = argparse.ArgumentParser(
        description="Duplicate an existing resume with a new name",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Duplicate by resume name
  python src/duplicate_resume.py --resume "Ford" --new-name "Sidney_Jones_Engineering_Manager_Subscription_Billing"
  
  # Duplicate by resume ID
  python src/duplicate_resume.py --resume-id "d474d761-18f2-48ab-99b5-9f30c54f75b2" --new-name "New Resume Name"
  
  # Duplicate with description
  python src/duplicate_resume.py --resume "Ford" --new-name "New Resume" --description "Tailored for X position"
  
  # Duplicate master resume
  python src/duplicate_resume.py --resume "Master Resume" --new-name "Sidney_Jones_Senior_Engineer_NewCo"

Resume Identification:
  - Use --resume with name (e.g., "Ford", "Master Resume")
  - Use --resume-id with UUID for direct lookup
  - Name matching is case-insensitive and supports partial matches
        """,
    )

    # Resume identification
    resume_group = parser.add_mutually_exclusive_group(required=True)
    resume_group.add_argument(
        "--resume",
        help="Resume name or company identifier (e.g., 'Ford', 'Master Resume')",
    )
    resume_group.add_argument("--resume-id", help="Resume UUID for direct lookup")

    # Required arguments
    parser.add_argument(
        "--new-name", required=True, help="Name for the duplicated resume"
    )

    # Optional arguments
    parser.add_argument(
        "--description", default="", help="Optional description for the new resume"
    )

    parser.add_argument(
        "--data-dir", default="data", help="Data directory path (default: data)"
    )

    args = parser.parse_args()

    try:
        data_dir = Path(args.data_dir)

        # Duplicate the resume
        new_metadata = duplicate_resume(
            data_dir=data_dir,
            source_identifier=args.resume,
            source_id=args.resume_id,
            new_name=args.new_name,
            description=args.description,
        )

        # Print success message
        print()
        print_success("Successfully duplicated resume!")
        print_info(f"   New Resume ID: {new_metadata.id}")
        print_info(f"   New Resume Name: {new_metadata.name}")
        if new_metadata.description:
            print_info(f"   Description: {new_metadata.description}")
        print()

        sys.exit(0)

    except FileNotFoundError as e:
        print_error(str(e))
        sys.exit(2)
    except ValueError as e:
        print_error(str(e))
        print_info("\n💡 Tip: Use a unique name for the new resume. You can include:")
        print_info("   - Company name (e.g., 'Ford', 'GM')")
        print_info("   - Position title (e.g., 'Senior Engineer', 'Manager')")
        print_info("   - Date or version (e.g., 'v2', '2025-01')")
        sys.exit(3)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
