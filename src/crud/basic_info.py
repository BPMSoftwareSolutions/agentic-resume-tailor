#!/usr/bin/env python3
"""
Basic Info CRUD Operations

Manage basic information (name, title, location, contact) in resumes.

Usage:
    # Update name
    python src/crud/basic_info.py --resume "Ford" --update-name "John Doe"
    
    # Update title
    python src/crud/basic_info.py --resume "Ford" --update-title "Principal Software Architect"
    
    # Update location
    python src/crud/basic_info.py --resume "Ford" --update-location "Remote"
    
    # Update email
    python src/crud/basic_info.py --resume "Ford" --update-email "john@example.com"
    
    # Update phone
    python src/crud/basic_info.py --resume "Ford" --update-phone "(555) 123-4567"
    
    # Show current basic info
    python src/crud/basic_info.py --resume "Ford" --show

Related to GitHub Issue #17
"""

import argparse
import sys
import re
from pathlib import Path
from typing import Dict, Any

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


def validate_email(email: str) -> bool:
    """
    Validate email format.
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone: str) -> bool:
    """
    Validate phone format (basic validation).
    
    Args:
        phone: Phone number to validate
        
    Returns:
        True if valid, False otherwise
    """
    # Allow various formats: (123) 456-7890, 123-456-7890, 123.456.7890, etc.
    pattern = r'^[\d\s\(\)\-\.+]+$'
    return re.match(pattern, phone) is not None and len(re.sub(r'\D', '', phone)) >= 10


def update_name(resume_data: Dict[str, Any], name: str) -> Dict[str, Any]:
    """
    Update resume name.
    
    Args:
        resume_data: Resume data
        name: New name
        
    Returns:
        Updated resume data
    """
    resume_data["name"] = name
    return resume_data


def update_title(resume_data: Dict[str, Any], title: str) -> Dict[str, Any]:
    """
    Update resume title.
    
    Args:
        resume_data: Resume data
        title: New title
        
    Returns:
        Updated resume data
    """
    resume_data["title"] = title
    return resume_data


def update_location(resume_data: Dict[str, Any], location: str) -> Dict[str, Any]:
    """
    Update resume location.
    
    Args:
        resume_data: Resume data
        location: New location
        
    Returns:
        Updated resume data
    """
    resume_data["location"] = location
    return resume_data


def update_email(resume_data: Dict[str, Any], email: str) -> Dict[str, Any]:
    """
    Update contact email.
    
    Args:
        resume_data: Resume data
        email: New email
        
    Returns:
        Updated resume data
    """
    if not validate_email(email):
        print_error(f"Invalid email format: {email}")
        sys.exit(3)
    
    if "contact" not in resume_data:
        resume_data["contact"] = {}
    
    resume_data["contact"]["email"] = email
    return resume_data


def update_phone(resume_data: Dict[str, Any], phone: str) -> Dict[str, Any]:
    """
    Update contact phone.
    
    Args:
        resume_data: Resume data
        phone: New phone number
        
    Returns:
        Updated resume data
    """
    if not validate_phone(phone):
        print_error(f"Invalid phone format: {phone}")
        sys.exit(3)
    
    if "contact" not in resume_data:
        resume_data["contact"] = {}
    
    resume_data["contact"]["phone"] = phone
    return resume_data


def show_basic_info(resume_data: Dict[str, Any]) -> None:
    """
    Display current basic information.
    
    Args:
        resume_data: Resume data
    """
    print("\nBasic Information:")
    print(f"  Name:     {resume_data.get('name', 'N/A')}")
    print(f"  Title:    {resume_data.get('title', 'N/A')}")
    print(f"  Location: {resume_data.get('location', 'N/A')}")
    
    contact = resume_data.get('contact', {})
    print(f"  Email:    {contact.get('email', 'N/A')}")
    print(f"  Phone:    {contact.get('phone', 'N/A')}")


def main():
    parser = argparse.ArgumentParser(
        description="Manage basic information in resumes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Update name
  python src/crud/basic_info.py --resume "Ford" --update-name "John Doe"
  
  # Update title
  python src/crud/basic_info.py --resume "Ford" --update-title "Principal Software Architect"
  
  # Update location
  python src/crud/basic_info.py --resume "Ford" --update-location "Remote"
  
  # Update email
  python src/crud/basic_info.py --resume "Ford" --update-email "john@example.com"
  
  # Update phone
  python src/crud/basic_info.py --resume "Ford" --update-phone "(555) 123-4567"
  
  # Show current basic info
  python src/crud/basic_info.py --resume "Ford" --show
        """
    )
    
    # Resume identification
    parser.add_argument(
        "--resume",
        help="Resume name or company identifier (e.g., 'Ford', 'Master Resume')"
    )
    parser.add_argument(
        "--resume-id",
        help="Resume UUID (alternative to --resume)"
    )
    
    # Operations
    parser.add_argument(
        "--update-name",
        metavar="NAME",
        help="Update name"
    )
    parser.add_argument(
        "--update-title",
        metavar="TITLE",
        help="Update title"
    )
    parser.add_argument(
        "--update-location",
        metavar="LOCATION",
        help="Update location"
    )
    parser.add_argument(
        "--update-email",
        metavar="EMAIL",
        help="Update email"
    )
    parser.add_argument(
        "--update-phone",
        metavar="PHONE",
        help="Update phone"
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Show current basic information"
    )
    
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
    
    # Check that at least one operation is specified
    operations = [
        args.update_name,
        args.update_title,
        args.update_location,
        args.update_email,
        args.update_phone,
        args.show
    ]
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
        
        if args.show:
            show_basic_info(resume_data)
        
        if args.update_name:
            resume_data = update_name(resume_data, args.update_name)
            modified = True
            print_success(f"Updated name: {args.update_name}")
        
        if args.update_title:
            resume_data = update_title(resume_data, args.update_title)
            modified = True
            print_success(f"Updated title: {args.update_title}")
        
        if args.update_location:
            resume_data = update_location(resume_data, args.update_location)
            modified = True
            print_success(f"Updated location: {args.update_location}")
        
        if args.update_email:
            resume_data = update_email(resume_data, args.update_email)
            modified = True
            print_success(f"Updated email: {args.update_email}")
        
        if args.update_phone:
            resume_data = update_phone(resume_data, args.update_phone)
            modified = True
            print_success(f"Updated phone: {args.update_phone}")
        
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

