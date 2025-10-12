#!/usr/bin/env python3
"""
Experience CRUD Operations

Manage work experience entries in resumes.

Usage:
    # Add experience entry
    python src/crud/experience.py --resume "Ford" --add --employer "Microsoft" --role "Senior Engineer" --dates "2020-2023" --location "Remote"
    
    # Add bullet to experience
    python src/crud/experience.py --resume "Ford" --add-bullet --employer "Microsoft" --text "Led team of 10 engineers" --tags "Leadership,Management"
    
    # Update bullet
    python src/crud/experience.py --resume "Ford" --update-bullet --employer "Microsoft" --index 0 --text "New bullet text"
    
    # Delete bullet
    python src/crud/experience.py --resume "Ford" --delete-bullet --employer "Microsoft" --index 0
    
    # Delete experience entry
    python src/crud/experience.py --resume "Ford" --delete --employer "Microsoft"
    
    # List all experience
    python src/crud/experience.py --resume "Ford" --list
    
    # Import from markdown
    python src/crud/experience.py --resume "Ford" --from-markdown "experience.md" --replace

Related to GitHub Issue #17
"""

import argparse
import sys
import re
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


def find_experience_by_employer(
    resume_data: Dict[str, Any],
    employer: str
) -> Optional[int]:
    """
    Find experience entry index by employer name.
    
    Args:
        resume_data: Resume data
        employer: Employer name to search for
        
    Returns:
        Index of experience entry or None if not found
    """
    experience_list = resume_data.get("experience", [])
    employer_lower = employer.lower()
    
    for i, exp in enumerate(experience_list):
        if exp.get("employer", "").lower() == employer_lower:
            return i
    
    return None


def add_experience(
    resume_data: Dict[str, Any],
    employer: str,
    role: str,
    dates: str,
    location: str = ""
) -> Dict[str, Any]:
    """
    Add a new experience entry.
    
    Args:
        resume_data: Resume data
        employer: Employer name
        role: Job role/title
        dates: Employment dates
        location: Location (optional)
        
    Returns:
        Updated resume data
    """
    if "experience" not in resume_data:
        resume_data["experience"] = []
    
    exp_entry = {
        "employer": employer,
        "role": role,
        "dates": dates,
        "location": location,
        "bullets": []
    }
    
    resume_data["experience"].append(exp_entry)
    return resume_data


def add_bullet(
    resume_data: Dict[str, Any],
    employer: str,
    text: str,
    tags: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Add a bullet point to an experience entry.
    
    Args:
        resume_data: Resume data
        employer: Employer name
        text: Bullet text
        tags: List of tags (optional)
        
    Returns:
        Updated resume data
    """
    if "experience" not in resume_data:
        resume_data["experience"] = []
    
    exp_index = find_experience_by_employer(resume_data, employer)
    if exp_index is None:
        print_error(f"Experience entry not found for employer: {employer}")
        sys.exit(3)
    
    bullet = {
        "text": text,
        "tags": tags or []
    }
    
    resume_data["experience"][exp_index]["bullets"].append(bullet)
    return resume_data


def update_bullet(
    resume_data: Dict[str, Any],
    employer: str,
    index: int,
    text: Optional[str] = None,
    tags: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Update a bullet point in an experience entry.
    
    Args:
        resume_data: Resume data
        employer: Employer name
        index: Bullet index
        text: New bullet text (optional)
        tags: New tags (optional)
        
    Returns:
        Updated resume data
    """
    if "experience" not in resume_data:
        resume_data["experience"] = []
    
    exp_index = find_experience_by_employer(resume_data, employer)
    if exp_index is None:
        print_error(f"Experience entry not found for employer: {employer}")
        sys.exit(3)
    
    bullets = resume_data["experience"][exp_index]["bullets"]
    if index < 0 or index >= len(bullets):
        print_error(f"Invalid bullet index: {index}")
        sys.exit(3)
    
    if text is not None:
        bullets[index]["text"] = text
    if tags is not None:
        bullets[index]["tags"] = tags
    
    return resume_data


def delete_bullet(
    resume_data: Dict[str, Any],
    employer: str,
    index: int
) -> Dict[str, Any]:
    """
    Delete a bullet point from an experience entry.
    
    Args:
        resume_data: Resume data
        employer: Employer name
        index: Bullet index
        
    Returns:
        Updated resume data
    """
    if "experience" not in resume_data:
        resume_data["experience"] = []
    
    exp_index = find_experience_by_employer(resume_data, employer)
    if exp_index is None:
        print_error(f"Experience entry not found for employer: {employer}")
        sys.exit(3)
    
    bullets = resume_data["experience"][exp_index]["bullets"]
    if index < 0 or index >= len(bullets):
        print_error(f"Invalid bullet index: {index}")
        sys.exit(3)
    
    bullets.pop(index)
    return resume_data


def delete_experience(
    resume_data: Dict[str, Any],
    employer: Optional[str] = None,
    index: Optional[int] = None
) -> Dict[str, Any]:
    """
    Delete an experience entry.
    
    Args:
        resume_data: Resume data
        employer: Employer name (optional)
        index: Experience index (optional)
        
    Returns:
        Updated resume data
    """
    if "experience" not in resume_data:
        resume_data["experience"] = []
    
    if employer:
        exp_index = find_experience_by_employer(resume_data, employer)
        if exp_index is None:
            print_error(f"Experience entry not found for employer: {employer}")
            sys.exit(3)
    elif index is not None:
        if index < 0 or index >= len(resume_data["experience"]):
            print_error(f"Invalid experience index: {index}")
            sys.exit(3)
        exp_index = index
    else:
        print_error("Either --employer or --index must be provided for delete")
        sys.exit(3)
    
    resume_data["experience"].pop(exp_index)
    return resume_data


def list_experience(resume_data: Dict[str, Any]) -> None:
    """
    List all experience entries.
    
    Args:
        resume_data: Resume data
    """
    experience_list = resume_data.get("experience", [])
    print(f"\nExperience ({len(experience_list)} entries):")
    
    for i, exp in enumerate(experience_list):
        print(f"\n  [{i}] {exp.get('employer', 'N/A')} — {exp.get('role', 'N/A')}")
        print(f"      {exp.get('dates', 'N/A')}")
        if exp.get('location'):
            print(f"      {exp['location']}")
        
        bullets = exp.get('bullets', [])
        print(f"      Bullets: {len(bullets)}")
        for j, bullet in enumerate(bullets):
            text = bullet.get('text', '')
            preview = text[:80] + "..." if len(text) > 80 else text
            print(f"        [{j}] {preview}")


def parse_experience_from_markdown(md_file: Path) -> List[Dict[str, Any]]:
    """
    Parse experience entries from a markdown file.
    
    Expected format:
    ### Company Name — Role (Dates)
    * Bullet point 1
    * Bullet point 2
    
    **Tags:** tag1, tag2, tag3
    
    Args:
        md_file: Path to markdown file
        
    Returns:
        List of experience dictionaries
    """
    if not md_file.exists():
        raise FileNotFoundError(f"Experience file not found: {md_file}")
    
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    experiences = []
    
    # Split by ### headers (experience sections)
    sections = re.split(r'\n### ', content)
    
    for section in sections[1:]:  # Skip first section (usually intro text)
        lines = section.strip().split('\n')
        if not lines:
            continue
        
        # Parse header: "Company Name — Role (Dates)"
        header = lines[0].strip()
        
        # Try to extract company, role, and dates
        match = re.match(r'(.+?)\s*[—–-]\s*(.+?)\s*\((.+?)\)', header)
        
        if not match:
            print(f"Warning: Could not parse header: {header}", file=sys.stderr)
            continue
        
        employer = match.group(1).strip()
        role = match.group(2).strip()
        dates = match.group(3).strip()
        
        # Extract bullets (lines starting with *)
        bullets = []
        tags = []
        
        for line in lines[1:]:
            line = line.strip()
            
            # Check for tags line
            if line.startswith('**Tags:**'):
                tags_str = line.replace('**Tags:**', '').strip()
                tags = [tag.strip() for tag in tags_str.split(',')]
                continue
            
            # Check for bullet point
            if line.startswith('*'):
                bullet_text = line[1:].strip()
                if bullet_text:
                    bullets.append({
                        "text": bullet_text,
                        "tags": tags if tags else []
                    })
        
        # Create experience entry
        experience = {
            "employer": employer,
            "role": role,
            "dates": dates,
            "location": "",  # Not typically in markdown
            "bullets": bullets
        }
        
        experiences.append(experience)
    
    return experiences


def main():
    parser = argparse.ArgumentParser(
        description="Manage work experience in resumes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add experience entry
  python src/crud/experience.py --resume "Ford" --add --employer "Microsoft" --role "Senior Engineer" --dates "2020-2023" --location "Remote"
  
  # Add bullet
  python src/crud/experience.py --resume "Ford" --add-bullet --employer "Microsoft" --text "Led team" --tags "Leadership,Management"
  
  # Update bullet
  python src/crud/experience.py --resume "Ford" --update-bullet --employer "Microsoft" --index 0 --text "New text"
  
  # Delete bullet
  python src/crud/experience.py --resume "Ford" --delete-bullet --employer "Microsoft" --index 0
  
  # Delete experience
  python src/crud/experience.py --resume "Ford" --delete --employer "Microsoft"
  
  # List all experience
  python src/crud/experience.py --resume "Ford" --list
  
  # Import from markdown
  python src/crud/experience.py --resume "Ford" --from-markdown "experience.md"
        """
    )
    
    # Resume identification
    parser.add_argument("--resume", help="Resume name or company identifier")
    parser.add_argument("--resume-id", help="Resume UUID")
    
    # Operations
    parser.add_argument("--add", action="store_true", help="Add experience entry")
    parser.add_argument("--add-bullet", action="store_true", help="Add bullet to experience")
    parser.add_argument("--update-bullet", action="store_true", help="Update bullet")
    parser.add_argument("--delete-bullet", action="store_true", help="Delete bullet")
    parser.add_argument("--delete", action="store_true", help="Delete experience entry")
    parser.add_argument("--list", action="store_true", help="List all experience")
    parser.add_argument("--from-markdown", metavar="FILE", help="Import from markdown file")
    
    # Fields
    parser.add_argument("--employer", help="Employer name")
    parser.add_argument("--role", help="Job role/title")
    parser.add_argument("--dates", help="Employment dates")
    parser.add_argument("--location", help="Location")
    parser.add_argument("--text", help="Bullet text")
    parser.add_argument("--tags", help="Comma-separated tags")
    parser.add_argument("--index", type=int, help="Bullet or experience index")
    parser.add_argument("--replace", action="store_true", help="Replace all experience (for --from-markdown)")
    
    # Options
    parser.add_argument("--data-dir", default="data", help="Data directory path")
    
    args = parser.parse_args()
    
    if not args.resume and not args.resume_id:
        parser.error("Either --resume or --resume-id must be provided")
    
    operations = [args.add, args.add_bullet, args.update_bullet, args.delete_bullet, args.delete, args.list, args.from_markdown]
    if not any(operations):
        parser.error("At least one operation must be specified")
    
    try:
        data_dir = Path(args.data_dir)
        resume_id, resume_data = get_resume_by_identifier(data_dir, identifier=args.resume, resume_id=args.resume_id)
        
        modified = False
        
        if args.list:
            list_experience(resume_data)
        
        if args.add:
            if not args.employer or not args.role or not args.dates:
                parser.error("--add requires --employer, --role, and --dates")
            resume_data = add_experience(resume_data, args.employer, args.role, args.dates, args.location or "")
            modified = True
            print_success(f"Added experience: {args.employer}")
        
        if args.add_bullet:
            if not args.employer or not args.text:
                parser.error("--add-bullet requires --employer and --text")
            tags = [t.strip() for t in args.tags.split(',')] if args.tags else []
            resume_data = add_bullet(resume_data, args.employer, args.text, tags)
            modified = True
            print_success(f"Added bullet to {args.employer}")
        
        if args.update_bullet:
            if not args.employer or args.index is None:
                parser.error("--update-bullet requires --employer and --index")
            tags = [t.strip() for t in args.tags.split(',')] if args.tags else None
            resume_data = update_bullet(resume_data, args.employer, args.index, args.text, tags)
            modified = True
            print_success(f"Updated bullet in {args.employer}")
        
        if args.delete_bullet:
            if not args.employer or args.index is None:
                parser.error("--delete-bullet requires --employer and --index")
            resume_data = delete_bullet(resume_data, args.employer, args.index)
            modified = True
            print_success(f"Deleted bullet from {args.employer}")
        
        if args.delete:
            resume_data = delete_experience(resume_data, args.employer, args.index)
            modified = True
            print_success("Deleted experience entry")
        
        if args.from_markdown:
            md_file = Path(args.from_markdown)
            experiences = parse_experience_from_markdown(md_file)
            print_info(f"Parsed {len(experiences)} experience entries from {md_file}")
            
            if args.replace:
                resume_data["experience"] = experiences
            else:
                if "experience" not in resume_data:
                    resume_data["experience"] = []
                resume_data["experience"] = experiences + resume_data["experience"]
            
            modified = True
            print_success(f"Imported experience from {md_file} ({'replaced' if args.replace else 'prepended'})")
        
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

