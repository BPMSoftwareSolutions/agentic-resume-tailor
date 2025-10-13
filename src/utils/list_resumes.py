#!/usr/bin/env python3
"""
List all resumes in a formatted table.

This script reads the resume index and displays resumes in a clean table format.
Part of the CRUD operations suite for resume management.

Usage:
    python src/utils/list_resumes.py [--format table|json|simple]
    
Examples:
    python src/utils/list_resumes.py
    python src/utils/list_resumes.py --format json
    python src/utils/list_resumes.py --format simple
"""

import json
import argparse
from pathlib import Path
from datetime import datetime


def load_resume_index():
    """Load the resume index file."""
    index_path = Path("data/resumes/index.json")
    
    if not index_path.exists():
        print(f"❌ Error: Resume index not found at {index_path}")
        return None
    
    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('resumes', [])
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in resume index: {e}")
        return None
    except Exception as e:
        print(f"❌ Error reading resume index: {e}")
        return None


def format_date(date_str):
    """Format ISO date string to readable format."""
    try:
        dt = datetime.fromisoformat(date_str)
        return dt.strftime("%Y-%m-%d %H:%M")
    except:
        return date_str


def print_table(resumes):
    """Print resumes in a formatted table."""
    if not resumes:
        print("📋 No resumes found.")
        return
    
    # Calculate column widths
    max_name_len = max(len(r.get('name', '')) for r in resumes)
    max_name_len = max(max_name_len, len("Resume Name"))
    max_name_len = min(max_name_len, 50)  # Cap at 50 chars
    
    max_desc_len = max(len(r.get('description', '')) for r in resumes)
    max_desc_len = max(max_desc_len, len("Description"))
    max_desc_len = min(max_desc_len, 40)  # Cap at 40 chars
    
    # Header
    print("\n" + "=" * 120)
    print(f"📋 RESUME LIST ({len(resumes)} total)")
    print("=" * 120)
    
    # Column headers
    header = f"{'#':<3} {'Resume Name':<{max_name_len}} {'Master':<8} {'Updated':<17} {'Description':<{max_desc_len}}"
    print(header)
    print("-" * 120)
    
    # Sort: Master first, then by updated date (newest first)
    sorted_resumes = sorted(
        resumes,
        key=lambda r: (not r.get('is_master', False), r.get('updated_at', '')),
        reverse=True
    )
    
    # Rows
    for idx, resume in enumerate(sorted_resumes, 1):
        name = resume.get('name', 'N/A')
        if len(name) > max_name_len:
            name = name[:max_name_len-3] + "..."
        
        is_master = "✓" if resume.get('is_master', False) else ""
        updated = format_date(resume.get('updated_at', 'N/A'))
        
        description = resume.get('description', '')
        if len(description) > max_desc_len:
            description = description[:max_desc_len-3] + "..."
        
        print(f"{idx:<3} {name:<{max_name_len}} {is_master:<8} {updated:<17} {description:<{max_desc_len}}")
    
    print("=" * 120)
    
    # Summary
    master_count = sum(1 for r in resumes if r.get('is_master', False))
    tailored_count = len(resumes) - master_count
    
    print(f"\n📊 Summary:")
    print(f"   • Master Resumes: {master_count}")
    print(f"   • Tailored Resumes: {tailored_count}")
    print(f"   • Total: {len(resumes)}")
    print()


def print_simple(resumes):
    """Print resumes in a simple list format."""
    if not resumes:
        print("📋 No resumes found.")
        return
    
    print(f"\n📋 Resumes ({len(resumes)} total):\n")
    
    # Sort: Master first, then alphabetically
    sorted_resumes = sorted(
        resumes,
        key=lambda r: (not r.get('is_master', False), r.get('name', '').lower())
    )
    
    for idx, resume in enumerate(sorted_resumes, 1):
        name = resume.get('name', 'N/A')
        is_master = " [MASTER]" if resume.get('is_master', False) else ""
        print(f"{idx}. {name}{is_master}")
    
    print()


def print_json(resumes):
    """Print resumes in JSON format."""
    print(json.dumps({"resumes": resumes}, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description="List all resumes in a formatted table",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python src/utils/list_resumes.py                    # Table format (default)
  python src/utils/list_resumes.py --format simple    # Simple list
  python src/utils/list_resumes.py --format json      # JSON output
        """
    )
    
    parser.add_argument(
        '--format',
        choices=['table', 'json', 'simple'],
        default='table',
        help='Output format (default: table)'
    )
    
    args = parser.parse_args()
    
    # Load resumes
    resumes = load_resume_index()
    
    if resumes is None:
        return 1
    
    # Print in requested format
    if args.format == 'json':
        print_json(resumes)
    elif args.format == 'simple':
        print_simple(resumes)
    else:  # table
        print_table(resumes)
    
    return 0


if __name__ == "__main__":
    exit(main())

