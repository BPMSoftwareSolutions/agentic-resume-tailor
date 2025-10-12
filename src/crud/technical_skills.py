#!/usr/bin/env python3
"""
Technical Skills CRUD Operations

Manage technical proficiencies (skills organized by category) in resumes.

Usage:
    # Add new category
    python src/crud/technical_skills.py --resume "Ford" --add-category "security" "OAuth, JWT, SAML"
    
    # Update category (replace)
    python src/crud/technical_skills.py --resume "Ford" --update-category "cloud" "Azure, AWS, GCP"
    
    # Append to category
    python src/crud/technical_skills.py --resume "Ford" --append-to-category "languages" "Rust, Go"
    
    # Delete category
    python src/crud/technical_skills.py --resume "Ford" --delete-category "security"
    
    # List all categories
    python src/crud/technical_skills.py --resume "Ford" --list
    
    # Show specific category
    python src/crud/technical_skills.py --resume "Ford" --show "cloud"

Related to GitHub Issue #17
"""

import argparse
import sys
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


def add_category(resume_data: Dict[str, Any], category: str, skills: str) -> Dict[str, Any]:
    """
    Add a new skills category.
    
    Args:
        resume_data: Resume data
        category: Category name
        skills: Skills for this category
        
    Returns:
        Updated resume data
    """
    if "technical_proficiencies" not in resume_data:
        resume_data["technical_proficiencies"] = {}
    
    category_lower = category.lower()
    
    # Check if category already exists
    if category_lower in resume_data["technical_proficiencies"]:
        print_error(f"Category already exists: {category_lower}")
        print_info("Use --update-category to replace or --append-to-category to add skills")
        sys.exit(3)
    
    resume_data["technical_proficiencies"][category_lower] = skills.strip()
    return resume_data


def update_category(resume_data: Dict[str, Any], category: str, skills: str) -> Dict[str, Any]:
    """
    Update/replace a skills category.
    
    Args:
        resume_data: Resume data
        category: Category name
        skills: New skills for this category
        
    Returns:
        Updated resume data
    """
    if "technical_proficiencies" not in resume_data:
        resume_data["technical_proficiencies"] = {}
    
    category_lower = category.lower()
    
    if category_lower not in resume_data["technical_proficiencies"]:
        print_error(f"Category not found: {category_lower}")
        print_info("Use --add-category to create a new category")
        sys.exit(3)
    
    resume_data["technical_proficiencies"][category_lower] = skills.strip()
    return resume_data


def append_to_category(resume_data: Dict[str, Any], category: str, skills: str) -> Dict[str, Any]:
    """
    Append skills to an existing category.
    
    Args:
        resume_data: Resume data
        category: Category name
        skills: Skills to append
        
    Returns:
        Updated resume data
    """
    if "technical_proficiencies" not in resume_data:
        resume_data["technical_proficiencies"] = {}
    
    category_lower = category.lower()
    
    if category_lower not in resume_data["technical_proficiencies"]:
        print_error(f"Category not found: {category_lower}")
        print_info("Use --add-category to create a new category")
        sys.exit(3)
    
    current_skills = resume_data["technical_proficiencies"][category_lower]
    
    # Add comma separator if needed
    if current_skills and not current_skills.endswith(','):
        current_skills += ", "
    elif current_skills and current_skills.endswith(','):
        current_skills += " "
    
    resume_data["technical_proficiencies"][category_lower] = (current_skills + skills.strip()).strip()
    return resume_data


def delete_category(resume_data: Dict[str, Any], category: str) -> Dict[str, Any]:
    """
    Delete a skills category.
    
    Args:
        resume_data: Resume data
        category: Category name to delete
        
    Returns:
        Updated resume data
    """
    if "technical_proficiencies" not in resume_data:
        resume_data["technical_proficiencies"] = {}
    
    category_lower = category.lower()
    
    if category_lower not in resume_data["technical_proficiencies"]:
        print_error(f"Category not found: {category_lower}")
        sys.exit(3)
    
    del resume_data["technical_proficiencies"][category_lower]
    return resume_data


def list_categories(resume_data: Dict[str, Any]) -> None:
    """
    List all skills categories.
    
    Args:
        resume_data: Resume data
    """
    proficiencies = resume_data.get("technical_proficiencies", {})
    
    if not proficiencies:
        print("\nTechnical Proficiencies: (empty)")
        return
    
    print(f"\nTechnical Proficiencies ({len(proficiencies)} categories):")
    for category, skills in sorted(proficiencies.items()):
        print(f"  {category}:")
        print(f"    {skills}")


def show_category(resume_data: Dict[str, Any], category: str) -> None:
    """
    Show a specific skills category.
    
    Args:
        resume_data: Resume data
        category: Category name
    """
    proficiencies = resume_data.get("technical_proficiencies", {})
    category_lower = category.lower()
    
    if category_lower not in proficiencies:
        print_error(f"Category not found: {category_lower}")
        sys.exit(3)
    
    print(f"\n{category_lower}:")
    print(f"  {proficiencies[category_lower]}")


def main():
    parser = argparse.ArgumentParser(
        description="Manage technical skills in resumes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add new category
  python src/crud/technical_skills.py --resume "Ford" --add-category "security" "OAuth, JWT, SAML"
  
  # Update category (replace)
  python src/crud/technical_skills.py --resume "Ford" --update-category "cloud" "Azure, AWS, GCP"
  
  # Append to category
  python src/crud/technical_skills.py --resume "Ford" --append-to-category "languages" "Rust, Go"
  
  # Delete category
  python src/crud/technical_skills.py --resume "Ford" --delete-category "security"
  
  # List all categories
  python src/crud/technical_skills.py --resume "Ford" --list
  
  # Show specific category
  python src/crud/technical_skills.py --resume "Ford" --show "cloud"
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
        "--add-category",
        nargs=2,
        metavar=("CATEGORY", "SKILLS"),
        help="Add new skills category"
    )
    parser.add_argument(
        "--update-category",
        nargs=2,
        metavar=("CATEGORY", "SKILLS"),
        help="Update/replace skills category"
    )
    parser.add_argument(
        "--append-to-category",
        nargs=2,
        metavar=("CATEGORY", "SKILLS"),
        help="Append skills to existing category"
    )
    parser.add_argument(
        "--delete-category",
        metavar="CATEGORY",
        help="Delete skills category"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all skills categories"
    )
    parser.add_argument(
        "--show",
        metavar="CATEGORY",
        help="Show specific skills category"
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
        args.add_category,
        args.update_category,
        args.append_to_category,
        args.delete_category,
        args.list,
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
        
        if args.list:
            list_categories(resume_data)
        
        if args.show:
            show_category(resume_data, args.show)
        
        if args.add_category:
            category, skills = args.add_category
            resume_data = add_category(resume_data, category, skills)
            modified = True
            print_success(f"Added category '{category}' with skills: {skills}")
        
        if args.update_category:
            category, skills = args.update_category
            resume_data = update_category(resume_data, category, skills)
            modified = True
            print_success(f"Updated category '{category}' with skills: {skills}")
        
        if args.append_to_category:
            category, skills = args.append_to_category
            resume_data = append_to_category(resume_data, category, skills)
            modified = True
            print_success(f"Appended to category '{category}': {skills}")
        
        if args.delete_category:
            resume_data = delete_category(resume_data, args.delete_category)
            modified = True
            print_success(f"Deleted category: {args.delete_category}")
        
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

