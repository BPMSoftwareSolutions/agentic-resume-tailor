"""
Shared utilities for CRUD operations on resume data models.

This module provides common functions used by all CRUD scripts for managing
resume data, including index management, resume finding, and data validation.

Related to GitHub Issue #17
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


def load_resume_index(data_dir: Path) -> Dict[str, Any]:
    """
    Load the resume index file.

    Args:
        data_dir: Data directory path

    Returns:
        Resume index data

    Raises:
        FileNotFoundError: If index file doesn't exist
    """
    index_file = data_dir / "resumes" / "index.json"
    if not index_file.exists():
        raise FileNotFoundError(f"Resume index not found: {index_file}")

    with open(index_file, "r", encoding="utf-8") as f:
        return json.load(f)


def save_resume_index(data_dir: Path, index_data: Dict[str, Any]) -> None:
    """
    Save the resume index file.

    Args:
        data_dir: Data directory path
        index_data: Resume index data to save
    """
    index_file = data_dir / "resumes" / "index.json"
    with open(index_file, "w", encoding="utf-8") as f:
        json.dump(index_data, f, indent=2, ensure_ascii=False)


def find_resume_by_identifier(
    index_data: Dict[str, Any], identifier: str
) -> Optional[Dict[str, Any]]:
    """
    Find a resume by name or company identifier.

    This function searches for resumes by matching the identifier against
    resume names. It performs case-insensitive partial matching.

    Args:
        index_data: Resume index data
        identifier: Company name or resume name to search for

    Returns:
        Resume metadata dict or None if not found

    Examples:
        >>> index = load_resume_index(Path("data"))
        >>> resume = find_resume_by_identifier(index, "Ford")
        >>> if resume:
        ...     print(f"Found: {resume['name']}")
    """
    identifier_lower = identifier.lower()

    for resume in index_data.get("resumes", []):
        name = resume.get("name", "").lower()

        # Check for exact match or partial match
        if identifier_lower in name or name in identifier_lower:
            return resume

    return None


def load_resume(data_dir: Path, resume_id: str) -> Dict[str, Any]:
    """
    Load resume data from file.

    Args:
        data_dir: Data directory path
        resume_id: Resume UUID

    Returns:
        Resume data

    Raises:
        FileNotFoundError: If resume file doesn't exist
    """
    resume_file = data_dir / "resumes" / f"{resume_id}.json"

    if not resume_file.exists():
        raise FileNotFoundError(f"Resume file not found: {resume_file}")

    with open(resume_file, "r", encoding="utf-8") as f:
        return json.load(f)


def save_resume(data_dir: Path, resume_id: str, data: Dict[str, Any]) -> None:
    """
    Save resume data and update timestamp in index.

    This function saves the resume data to file and automatically updates
    the 'updated_at' timestamp in the resume index.

    Args:
        data_dir: Data directory path
        resume_id: Resume UUID
        data: Resume data to save
    """
    resume_file = data_dir / "resumes" / f"{resume_id}.json"

    # Save resume data
    with open(resume_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Update timestamp in index
    try:
        index_data = load_resume_index(data_dir)
        for resume in index_data.get("resumes", []):
            if resume["id"] == resume_id:
                resume["updated_at"] = datetime.now().isoformat()
                break
        save_resume_index(data_dir, index_data)
    except Exception as e:
        print(f"Warning: Could not update index timestamp: {e}", file=sys.stderr)


def validate_resume_structure(data: Dict[str, Any]) -> bool:
    """
    Validate basic resume data structure.

    Checks that the resume has the expected top-level fields.

    Args:
        data: Resume data to validate

    Returns:
        True if valid, False otherwise
    """
    required_fields = [
        "name",
        "title",
        "location",
        "contact",
        "summary",
        "technical_proficiencies",
        "areas_of_expertise",
        "experience",
        "education",
        "certifications",
    ]

    for field in required_fields:
        if field not in data:
            print(f"[ERROR] Missing required field: {field}", file=sys.stderr)
            return False

    return True


def print_success(message: str) -> None:
    """
    Print a success message.

    Args:
        message: Success message to print
    """
    print(f"[SUCCESS] {message}")


def print_error(message: str) -> None:
    """
    Print an error message to stderr.

    Args:
        message: Error message to print
    """
    print(f"[ERROR] {message}", file=sys.stderr)


def print_info(message: str) -> None:
    """
    Print an informational message.

    Args:
        message: Info message to print
    """
    print(f"[INFO] {message}")


def list_available_resumes(index_data: Dict[str, Any]) -> None:
    """
    Print a list of available resumes.

    Args:
        index_data: Resume index data
    """
    print("\nAvailable resumes:", file=sys.stderr)
    for r in index_data.get("resumes", []):
        print(f"  - {r['name']} (ID: {r['id']})", file=sys.stderr)


def get_resume_by_identifier(
    data_dir: Path, identifier: Optional[str] = None, resume_id: Optional[str] = None
) -> tuple[str, Dict[str, Any]]:
    """
    Get resume ID and data by identifier or resume ID.

    This is a convenience function that combines finding and loading a resume.

    Args:
        data_dir: Data directory path
        identifier: Resume name or company identifier (optional)
        resume_id: Resume UUID (optional)

    Returns:
        Tuple of (resume_id, resume_data)

    Raises:
        ValueError: If neither identifier nor resume_id provided
        FileNotFoundError: If resume not found

    Examples:
        >>> resume_id, data = get_resume_by_identifier(Path("data"), identifier="Ford")
        >>> print(f"Found resume: {data['name']}")
    """
    if not identifier and not resume_id:
        raise ValueError("Either identifier or resume_id must be provided")

    # If resume_id provided, use it directly
    if resume_id:
        print_info(f"Using resume ID: {resume_id}")
        data = load_resume(data_dir, resume_id)
        return resume_id, data

    # Otherwise, find by identifier
    print_info(f"Searching for resume matching: {identifier}")
    index_data = load_resume_index(data_dir)
    resume_meta = find_resume_by_identifier(index_data, identifier)

    if not resume_meta:
        print_error(f"No resume found matching '{identifier}'")
        list_available_resumes(index_data)
        raise FileNotFoundError(f"Resume not found: {identifier}")

    found_id = resume_meta["id"]
    print_info(f"Found resume: {resume_meta['name']} (ID: {found_id})")

    data = load_resume(data_dir, found_id)
    return found_id, data
