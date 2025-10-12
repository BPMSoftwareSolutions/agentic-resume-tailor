#!/usr/bin/env python3
"""
Education CRUD Operations

Manage education entries in resumes.

Usage:
    # Add education entry
    python src/crud/education.py --resume "Ford" --add --degree "Master of Science" --institution "MIT" --location "Cambridge, MA" --year "2020"
    
    # List all education entries
    python src/crud/education.py --resume "Ford" --list
    
    # Update education entry by index
    python src/crud/education.py --resume "Ford" --update --index 0 --degree "Master of Computer Science"
    
    # Update education entry by institution
    python src/crud/education.py --resume "Ford" --update --institution "MIT" --year "2021"
    
    # Delete education entry by index
    python src/crud/education.py --resume "Ford" --delete --index 0
    
    # Delete education entry by institution
    python src/crud/education.py --resume "Ford" --delete --institution "University of Phoenix"

Related to GitHub Issue #17
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import shared utilities
from crud import (
    get_resume_by_identifier,
    save_resume,
    print_success,
    print_error,
    print_info
)


def add_education(
    resume_data: Dict[str, Any],
    degree: str,
    institution: str,
    location: str = "",
    year: str = ""
) -> Dict[str, Any]:
    """
    Add a new education entry.
    
    Args:
        resume_data: Resume data
        degree: Degree name
        institution: Institution name
        location: Location (optional)
        year: Year (optional)
        
    Returns:
        Updated resume data
    """
    if "education" not in resume_data:
        resume_data["education"] = []
    
    education_entry = {
        "degree": degree,
        "institution": institution,
        "location": location,
        "year": year
    }
    
    resume_data["education"].append(education_entry)
    return resume_data


def list_education(resume_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    List all education entries.
    
    Args:
        resume_data: Resume data
        
    Returns:
        List of education entries
    """
    return resume_data.get("education", [])


def find_education_by_institution(
    resume_data: Dict[str, Any],
    institution: str
) -> Optional[int]:
    """
    Find education entry index by institution name.
    
    Args:
        resume_data: Resume data
        institution: Institution name to search for
        
    Returns:
        Index of education entry or None if not found
    """
    education_list = resume_data.get("education", [])
    institution_lower = institution.lower()
    
    for i, edu in enumerate(education_list):
        if edu.get("institution", "").lower() == institution_lower:
            return i
    
    return None


def update_education(
    resume_data: Dict[str, Any],
    index: Optional[int] = None,
    institution: Optional[str] = None,
    degree: Optional[str] = None,
    new_institution: Optional[str] = None,
    location: Optional[str] = None,
    year: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update an education entry.
    
    Args:
        resume_data: Resume data
        index: Index of entry to update (optional)
        institution: Institution name to find entry (optional)
        degree: New degree (optional)
        new_institution: New institution name (optional)
        location: New location (optional)
        year: New year (optional)
        
    Returns:
        Updated resume data
    """
    if "education" not in resume_data:
        resume_data["education"] = []
    
    # Find entry by index or institution
    if index is not None:
        if index < 0 or index >= len(resume_data["education"]):
            print_error(f"Invalid index: {index}")
            sys.exit(3)
        entry_index = index
    elif institution:
        entry_index = find_education_by_institution(resume_data, institution)
        if entry_index is None:
            print_error(f"Education entry not found for institution: {institution}")
            sys.exit(3)
    else:
        print_error("Either --index or --institution must be provided for update")
        sys.exit(3)
    
    # Update fields
    if degree is not None:
        resume_data["education"][entry_index]["degree"] = degree
    if new_institution is not None:
        resume_data["education"][entry_index]["institution"] = new_institution
    if location is not None:
        resume_data["education"][entry_index]["location"] = location
    if year is not None:
        resume_data["education"][entry_index]["year"] = year
    
    return resume_data


def delete_education(
    resume_data: Dict[str, Any],
    index: Optional[int] = None,
    institution: Optional[str] = None
) -> Dict[str, Any]:
    """
    Delete an education entry.
    
    Args:
        resume_data: Resume data
        index: Index of entry to delete (optional)
        institution: Institution name to find entry (optional)
        
    Returns:
        Updated resume data
    """
    if "education" not in resume_data:
        resume_data["education"] = []
    
    # Find entry by index or institution
    if index is not None:
        if index < 0 or index >= len(resume_data["education"]):
            print_error(f"Invalid index: {index}")
            sys.exit(3)
        entry_index = index
    elif institution:
        entry_index = find_education_by_institution(resume_data, institution)
        if entry_index is None:
            print_error(f"Education entry not found for institution: {institution}")
            sys.exit(3)
    else:
        print_error("Either --index or --institution must be provided for delete")
        sys.exit(3)
    
    # Delete entry
    deleted = resume_data["education"].pop(entry_index)
    return resume_data


def main():
    parser = argparse.ArgumentParser(
        description="Manage education entries in resumes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add education entry
  python src/crud/education.py --resume "Ford" --add --degree "Master of Science" --institution "MIT" --location "Cambridge, MA" --year "2020"
  
  # List all education entries
  python src/crud/education.py --resume "Ford" --list
  
  # Update by index
  python src/crud/education.py --resume "Ford" --update --index 0 --degree "Master of Computer Science"
  
  # Update by institution
  python src/crud/education.py --resume "Ford" --update --institution "MIT" --year "2021"
  
  # Delete by index
  python src/crud/education.py --resume "Ford" --delete --index 0
  
  # Delete by institution
  python src/crud/education.py --resume "Ford" --delete --institution "University of Phoenix"
        """
    )
    
    # Resume identification
    parser.add_argument(
        "--resume",
        help="Resume name or company identifier"
    )
    parser.add_argument(
        "--resume-id",
        help="Resume UUID (alternative to --resume)"
    )
    
    # Operations
    parser.add_argument(
        "--add",
        action="store_true",
        help="Add new education entry"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all education entries"
    )
    parser.add_argument(
        "--update",
        action="store_true",
        help="Update education entry"
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="Delete education entry"
    )
    
    # Fields for add/update
    parser.add_argument("--degree", help="Degree name")
    parser.add_argument("--institution", help="Institution name")
    parser.add_argument("--new-institution", help="New institution name (for update)")
    parser.add_argument("--location", help="Location")
    parser.add_argument("--year", help="Year")
    
    # Selectors for update/delete
    parser.add_argument("--index", type=int, help="Index of entry (0-based)")
    
    # Options
    parser.add_argument(
        "--data-dir",
        default="data",
        help="Data directory path (default: data)"
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.resume and not args.resume_id:
        parser.error("Either --resume or --resume-id must be provided")
    
    operations = [args.add, args.list, args.update, args.delete]
    if not any(operations):
        parser.error("At least one operation must be specified")
    
    try:
        data_dir = Path(args.data_dir)
        
        # Get resume
        resume_id, resume_data = get_resume_by_identifier(
            data_dir,
            identifier=args.resume,
            resume_id=args.resume_id
        )
        
        # Perform operations
        modified = False
        
        if args.list:
            education_list = list_education(resume_data)
            print(f"\nEducation ({len(education_list)} entries):")
            for i, edu in enumerate(education_list):
                print(f"  [{i}] {edu.get('degree', 'N/A')}")
                print(f"      {edu.get('institution', 'N/A')}")
                if edu.get('location'):
                    print(f"      {edu['location']}")
                if edu.get('year'):
                    print(f"      {edu['year']}")
        
        if args.add:
            if not args.degree or not args.institution:
                parser.error("--add requires --degree and --institution")
            
            resume_data = add_education(
                resume_data,
                args.degree,
                args.institution,
                args.location or "",
                args.year or ""
            )
            modified = True
            print_success(f"Added education: {args.degree} from {args.institution}")
        
        if args.update:
            resume_data = update_education(
                resume_data,
                index=args.index,
                institution=args.institution,
                degree=args.degree,
                new_institution=args.new_institution,
                location=args.location,
                year=args.year
            )
            modified = True
            print_success("Updated education entry")
        
        if args.delete:
            resume_data = delete_education(
                resume_data,
                index=args.index,
                institution=args.institution
            )
            modified = True
            print_success("Deleted education entry")
        
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

