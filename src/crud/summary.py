#!/usr/bin/env python3
"""
Summary CRUD Operations

Manage summary text in resumes.

Usage:
    # Update entire summary
    python src/crud/summary.py --resume "Ford" --update "New summary text..."
    
    # Append to existing summary
    python src/crud/summary.py --resume "Ford" --append "Additional text to add."
    
    # Load summary from file
    python src/crud/summary.py --resume "Ford" --from-file "summary.txt"
    
    # Show current summary
    python src/crud/summary.py --resume "Ford" --show

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


def update_summary(resume_data: Dict[str, Any], summary: str) -> Dict[str, Any]:
    """
    Update/replace the entire summary.
    
    Args:
        resume_data: Resume data
        summary: New summary text
        
    Returns:
        Updated resume data
    """
    resume_data["summary"] = summary.strip()
    return resume_data


def append_summary(resume_data: Dict[str, Any], text: str) -> Dict[str, Any]:
    """
    Append text to existing summary.
    
    Args:
        resume_data: Resume data
        text: Text to append
        
    Returns:
        Updated resume data
    """
    current_summary = resume_data.get("summary", "")
    
    # Add space if current summary doesn't end with punctuation or whitespace
    if current_summary and not current_summary[-1] in ['.', '!', '?', ' ', '\n']:
        current_summary += " "
    
    resume_data["summary"] = (current_summary + text.strip()).strip()
    return resume_data


def load_summary_from_file(file_path: Path) -> str:
    """
    Load summary text from a file.
    
    Args:
        file_path: Path to text file
        
    Returns:
        Summary text
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Summary file not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read().strip()


def show_summary(resume_data: Dict[str, Any]) -> None:
    """
    Display current summary.
    
    Args:
        resume_data: Resume data
    """
    summary = resume_data.get("summary", "")
    
    if not summary:
        print("\nSummary: (empty)")
    else:
        print(f"\nSummary ({len(summary)} characters):")
        print(f"\n{summary}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Manage summary in resumes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Update entire summary
  python src/crud/summary.py --resume "Ford" --update "New summary text..."
  
  # Append to existing summary
  python src/crud/summary.py --resume "Ford" --append "Additional text."
  
  # Load summary from file
  python src/crud/summary.py --resume "Ford" --from-file "summary.txt"
  
  # Show current summary
  python src/crud/summary.py --resume "Ford" --show
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
        "--update",
        metavar="TEXT",
        help="Update/replace entire summary"
    )
    parser.add_argument(
        "--append",
        metavar="TEXT",
        help="Append text to existing summary"
    )
    parser.add_argument(
        "--from-file",
        metavar="FILE",
        help="Load summary from text file"
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Show current summary"
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
    operations = [args.update, args.append, args.from_file, args.show]
    if not any(operations):
        parser.error("At least one operation (--update, --append, --from-file, --show) must be specified")
    
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
            show_summary(resume_data)
        
        if args.update:
            resume_data = update_summary(resume_data, args.update)
            modified = True
            print_success(f"Updated summary ({len(args.update)} characters)")
        
        if args.append:
            resume_data = append_summary(resume_data, args.append)
            modified = True
            print_success(f"Appended to summary ({len(args.append)} characters added)")
        
        if args.from_file:
            file_path = Path(args.from_file)
            summary_text = load_summary_from_file(file_path)
            resume_data = update_summary(resume_data, summary_text)
            modified = True
            print_success(f"Loaded summary from file: {file_path} ({len(summary_text)} characters)")
        
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

