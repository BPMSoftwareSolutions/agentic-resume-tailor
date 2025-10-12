#!/usr/bin/env python3
"""
Certifications CRUD Operations

Manage certification entries in resumes.

Usage:
    # Add certification
    python src/crud/certifications.py --resume "Ford" --add --name "AWS Solutions Architect" --issuer "Amazon" --date "Oct 2025" --credential "ABC123"
    
    # List all certifications
    python src/crud/certifications.py --resume "Ford" --list
    
    # Update certification by index
    python src/crud/certifications.py --resume "Ford" --update --index 0 --date "Nov 2025"
    
    # Update certification by name
    python src/crud/certifications.py --resume "Ford" --update --name "PSM I" --date "June 2023"
    
    # Delete certification by index
    python src/crud/certifications.py --resume "Ford" --delete --index 0
    
    # Delete certification by name
    python src/crud/certifications.py --resume "Ford" --delete --name "PSM I"

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


def add_certification(
    resume_data: Dict[str, Any],
    name: str,
    issuer: str,
    date: str = "",
    credential: str = ""
) -> Dict[str, Any]:
    """
    Add a new certification entry.
    
    Args:
        resume_data: Resume data
        name: Certification name
        issuer: Issuing organization
        date: Date obtained (optional)
        credential: Credential ID (optional)
        
    Returns:
        Updated resume data
    """
    if "certifications" not in resume_data:
        resume_data["certifications"] = []
    
    cert_entry = {
        "name": name,
        "issuer": issuer,
        "date": date
    }
    
    # Only add credential if provided
    if credential:
        cert_entry["credential"] = credential
    
    resume_data["certifications"].append(cert_entry)
    return resume_data


def list_certifications(resume_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    List all certification entries.
    
    Args:
        resume_data: Resume data
        
    Returns:
        List of certification entries
    """
    return resume_data.get("certifications", [])


def find_certification_by_name(
    resume_data: Dict[str, Any],
    name: str
) -> Optional[int]:
    """
    Find certification entry index by name.
    
    Args:
        resume_data: Resume data
        name: Certification name to search for
        
    Returns:
        Index of certification entry or None if not found
    """
    certifications_list = resume_data.get("certifications", [])
    name_lower = name.lower()
    
    for i, cert in enumerate(certifications_list):
        if cert.get("name", "").lower() == name_lower:
            return i
    
    return None


def update_certification(
    resume_data: Dict[str, Any],
    index: Optional[int] = None,
    name: Optional[str] = None,
    new_name: Optional[str] = None,
    issuer: Optional[str] = None,
    date: Optional[str] = None,
    credential: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update a certification entry.
    
    Args:
        resume_data: Resume data
        index: Index of entry to update (optional)
        name: Certification name to find entry (optional)
        new_name: New certification name (optional)
        issuer: New issuer (optional)
        date: New date (optional)
        credential: New credential (optional)
        
    Returns:
        Updated resume data
    """
    if "certifications" not in resume_data:
        resume_data["certifications"] = []
    
    # Find entry by index or name
    if index is not None:
        if index < 0 or index >= len(resume_data["certifications"]):
            print_error(f"Invalid index: {index}")
            sys.exit(3)
        entry_index = index
    elif name:
        entry_index = find_certification_by_name(resume_data, name)
        if entry_index is None:
            print_error(f"Certification not found: {name}")
            sys.exit(3)
    else:
        print_error("Either --index or --name must be provided for update")
        sys.exit(3)
    
    # Update fields
    if new_name is not None:
        resume_data["certifications"][entry_index]["name"] = new_name
    if issuer is not None:
        resume_data["certifications"][entry_index]["issuer"] = issuer
    if date is not None:
        resume_data["certifications"][entry_index]["date"] = date
    if credential is not None:
        resume_data["certifications"][entry_index]["credential"] = credential
    
    return resume_data


def delete_certification(
    resume_data: Dict[str, Any],
    index: Optional[int] = None,
    name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Delete a certification entry.
    
    Args:
        resume_data: Resume data
        index: Index of entry to delete (optional)
        name: Certification name to find entry (optional)
        
    Returns:
        Updated resume data
    """
    if "certifications" not in resume_data:
        resume_data["certifications"] = []
    
    # Find entry by index or name
    if index is not None:
        if index < 0 or index >= len(resume_data["certifications"]):
            print_error(f"Invalid index: {index}")
            sys.exit(3)
        entry_index = index
    elif name:
        entry_index = find_certification_by_name(resume_data, name)
        if entry_index is None:
            print_error(f"Certification not found: {name}")
            sys.exit(3)
    else:
        print_error("Either --index or --name must be provided for delete")
        sys.exit(3)
    
    # Delete entry
    deleted = resume_data["certifications"].pop(entry_index)
    return resume_data


def main():
    parser = argparse.ArgumentParser(
        description="Manage certifications in resumes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add certification
  python src/crud/certifications.py --resume "Ford" --add --name "AWS Solutions Architect" --issuer "Amazon" --date "Oct 2025" --credential "ABC123"
  
  # List all certifications
  python src/crud/certifications.py --resume "Ford" --list
  
  # Update by index
  python src/crud/certifications.py --resume "Ford" --update --index 0 --date "Nov 2025"
  
  # Update by name
  python src/crud/certifications.py --resume "Ford" --update --name "PSM I" --date "June 2023"
  
  # Delete by index
  python src/crud/certifications.py --resume "Ford" --delete --index 0
  
  # Delete by name
  python src/crud/certifications.py --resume "Ford" --delete --name "PSM I"
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
        help="Add new certification"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all certifications"
    )
    parser.add_argument(
        "--update",
        action="store_true",
        help="Update certification"
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="Delete certification"
    )
    
    # Fields for add/update
    parser.add_argument("--name", help="Certification name")
    parser.add_argument("--new-name", help="New certification name (for update)")
    parser.add_argument("--issuer", help="Issuing organization")
    parser.add_argument("--date", help="Date obtained")
    parser.add_argument("--credential", help="Credential ID")
    
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
            certs_list = list_certifications(resume_data)
            print(f"\nCertifications ({len(certs_list)} entries):")
            for i, cert in enumerate(certs_list):
                print(f"  [{i}] {cert.get('name', 'N/A')}")
                print(f"      Issuer: {cert.get('issuer', 'N/A')}")
                if cert.get('date'):
                    print(f"      Date: {cert['date']}")
                if cert.get('credential'):
                    print(f"      Credential: {cert['credential']}")
        
        if args.add:
            if not args.name or not args.issuer:
                parser.error("--add requires --name and --issuer")
            
            resume_data = add_certification(
                resume_data,
                args.name,
                args.issuer,
                args.date or "",
                args.credential or ""
            )
            modified = True
            print_success(f"Added certification: {args.name}")
        
        if args.update:
            resume_data = update_certification(
                resume_data,
                index=args.index,
                name=args.name,
                new_name=args.new_name,
                issuer=args.issuer,
                date=args.date,
                credential=args.credential
            )
            modified = True
            print_success("Updated certification")
        
        if args.delete:
            resume_data = delete_certification(
                resume_data,
                index=args.index,
                name=args.name
            )
            modified = True
            print_success("Deleted certification")
        
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

