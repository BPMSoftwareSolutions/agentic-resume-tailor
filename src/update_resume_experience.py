#!/usr/bin/env python3
"""
Update Resume Experience Helper Script

This script helps the AI agent update resume experience from markdown files.
It can find resumes by name/company and apply experience from markdown files.

Usage:
    python src/update_resume_experience.py --resume "Ford" --experience "data/job_listings/Tailored Experience Summary for Ford.md"
    python src/update_resume_experience.py --resume-id "d474d761-18f2-48ab-99b5-9f30c54f75b2" --experience "path/to/experience.md"
"""

import json
import argparse
import sys
import re
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List


def load_resume_index(data_dir: Path) -> Dict[str, Any]:
    """Load the resume index file."""
    index_file = data_dir / "resumes" / "index.json"
    if not index_file.exists():
        raise FileNotFoundError(f"Resume index not found: {index_file}")
    
    with open(index_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_resume_index(data_dir: Path, index_data: Dict[str, Any]) -> None:
    """Save the resume index file."""
    index_file = data_dir / "resumes" / "index.json"
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=2, ensure_ascii=False)


def find_resume_by_identifier(index_data: Dict[str, Any], identifier: str) -> Optional[Dict[str, Any]]:
    """
    Find a resume by name or company identifier.
    
    Args:
        index_data: Resume index data
        identifier: Company name or resume name to search for
        
    Returns:
        Resume metadata dict or None if not found
    """
    identifier_lower = identifier.lower()
    
    for resume in index_data.get("resumes", []):
        name = resume.get("name", "").lower()
        
        # Check for exact match or partial match
        if identifier_lower in name or name in identifier_lower:
            return resume
    
    return None


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
        # Pattern: "Company — Role (Dates)" or "Company — Role / Title (Dates)"
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


def update_resume_experience(
    data_dir: Path,
    resume_id: str,
    experiences: List[Dict[str, Any]],
    replace: bool = False
) -> None:
    """
    Update a resume's experience section.
    
    Args:
        data_dir: Data directory path
        resume_id: Resume UUID
        experiences: List of experience dictionaries
        replace: If True, replace all experience; if False, prepend new experience
    """
    resume_file = data_dir / "resumes" / f"{resume_id}.json"
    
    if not resume_file.exists():
        raise FileNotFoundError(f"Resume file not found: {resume_file}")
    
    # Load resume
    with open(resume_file, 'r', encoding='utf-8') as f:
        resume_data = json.load(f)
    
    # Update experience
    if replace:
        resume_data["experience"] = experiences
    else:
        # Prepend new experiences
        existing_experience = resume_data.get("experience", [])
        resume_data["experience"] = experiences + existing_experience
    
    # Save resume
    with open(resume_file, 'w', encoding='utf-8') as f:
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
        description="Update resume experience from markdown file"
    )
    parser.add_argument(
        "--resume",
        help="Resume name or company identifier (e.g., 'Ford', 'GM')"
    )
    parser.add_argument(
        "--resume-id",
        help="Resume UUID (alternative to --resume)"
    )
    parser.add_argument(
        "--experience",
        required=True,
        help="Path to markdown file containing experience"
    )
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Replace all experience (default: prepend)"
    )
    parser.add_argument(
        "--data-dir",
        default="data",
        help="Data directory path (default: data)"
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.resume and not args.resume_id:
        parser.error("Either --resume or --resume-id must be provided")
    
    try:
        data_dir = Path(args.data_dir)
        experience_file = Path(args.experience)
        
        # Find resume
        if args.resume_id:
            resume_id = args.resume_id
            print(f"Using resume ID: {resume_id}")
        else:
            print(f"Searching for resume matching: {args.resume}")
            index_data = load_resume_index(data_dir)
            resume_meta = find_resume_by_identifier(index_data, args.resume)
            
            if not resume_meta:
                print(f"Error: No resume found matching '{args.resume}'", file=sys.stderr)
                print("\nAvailable resumes:", file=sys.stderr)
                for r in index_data.get("resumes", []):
                    print(f"  - {r['name']} (ID: {r['id']})", file=sys.stderr)
                sys.exit(1)
            
            resume_id = resume_meta["id"]
            print(f"Found resume: {resume_meta['name']} (ID: {resume_id})")
        
        # Parse experience from markdown
        print(f"\nParsing experience from: {experience_file}")
        experiences = parse_experience_from_markdown(experience_file)
        print(f"Found {len(experiences)} experience entries")
        
        for i, exp in enumerate(experiences, 1):
            print(f"  {i}. {exp['employer']} — {exp['role']} ({exp['dates']})")
            print(f"     Bullets: {len(exp['bullets'])}")
        
        # Update resume
        print(f"\nUpdating resume...")
        update_resume_experience(data_dir, resume_id, experiences, args.replace)
        
        print(f"✅ Successfully updated resume {resume_id}")
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

