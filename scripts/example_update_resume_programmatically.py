#!/usr/bin/env python3
"""
Example: Update Resume Programmatically

This example shows how to use the update_resume_with_experiences functions
directly from Python code instead of the command line.

Useful for:
- Integrating into larger automation workflows
- Building custom resume update tools
- Programmatic resume management
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.update_resume_with_experiences import (
    parse_json_experiences,
    parse_markdown_experiences,
    update_resume_experiences,
)


def example_1_update_from_json():
    """Example 1: Update resume from JSON file"""
    print("=" * 60)
    print("Example 1: Update Resume from JSON File")
    print("=" * 60)

    data_dir = Path("data")
    resume_id = "141107d3-f0a9-4bc6-82dd-6fc4506e76f4"
    experiences_file = Path("data/experiences_solution_architect.json")

    # Parse experiences from JSON
    experiences = parse_json_experiences(experiences_file)
    print(f"Loaded {len(experiences)} experiences from JSON")

    # Update resume (prepend new experiences)
    update_resume_experiences(data_dir, resume_id, experiences, replace=False)
    print(f"✓ Successfully updated resume {resume_id}")
    print()


def example_2_update_from_markdown():
    """Example 2: Update resume from markdown file"""
    print("=" * 60)
    print("Example 2: Update Resume from Markdown File")
    print("=" * 60)

    data_dir = Path("data")
    resume_id = "141107d3-f0a9-4bc6-82dd-6fc4506e76f4"
    experiences_file = Path("data/experiences.md")  # Your markdown file

    # Parse experiences from markdown
    experiences = parse_markdown_experiences(experiences_file)
    print(f"Loaded {len(experiences)} experiences from markdown")

    # Update resume (replace all experiences)
    update_resume_experiences(data_dir, resume_id, experiences, replace=True)
    print(f"✓ Successfully replaced all experiences in resume {resume_id}")
    print()


def example_3_programmatic_experiences():
    """Example 3: Create experiences programmatically"""
    print("=" * 60)
    print("Example 3: Create Experiences Programmatically")
    print("=" * 60)

    # Define experiences directly in Python
    experiences = [
        {
            "employer": "Tech Company Inc",
            "role": "Senior Engineer",
            "dates": "2023 – Present",
            "location": "San Francisco, CA",
            "bullets": [
                {
                    "text": "Led development of microservices architecture",
                    "tags": ["Go", "Kubernetes", "AWS"],
                },
                {
                    "text": "Mentored team of 5 engineers",
                    "tags": ["Leadership", "Mentorship"],
                },
            ],
        },
        {
            "employer": "Another Company",
            "role": "Software Architect",
            "dates": "2020 – 2023",
            "location": "New York, NY",
            "bullets": [
                {
                    "text": "Designed cloud infrastructure",
                    "tags": ["AWS", "Terraform", "DevOps"],
                },
            ],
        },
    ]

    data_dir = Path("data")
    resume_id = "141107d3-f0a9-4bc6-82dd-6fc4506e76f4"

    # Update resume with programmatically created experiences
    update_resume_experiences(data_dir, resume_id, experiences, replace=False)
    print(f"✓ Successfully added {len(experiences)} programmatic experiences")
    print()


def example_4_merge_multiple_sources():
    """Example 4: Merge experiences from multiple sources"""
    print("=" * 60)
    print("Example 4: Merge Experiences from Multiple Sources")
    print("=" * 60)

    data_dir = Path("data")
    resume_id = "141107d3-f0a9-4bc6-82dd-6fc4506e76f4"

    # Load from JSON
    json_experiences = parse_json_experiences(
        Path("data/experiences_solution_architect.json")
    )
    print(f"Loaded {len(json_experiences)} experiences from JSON")

    # Load from markdown
    try:
        markdown_experiences = parse_markdown_experiences(Path("data/experiences.md"))
        print(f"Loaded {len(markdown_experiences)} experiences from markdown")
    except FileNotFoundError:
        markdown_experiences = []
        print("Markdown file not found, skipping")

    # Merge all experiences
    all_experiences = json_experiences + markdown_experiences
    print(f"Total experiences to add: {len(all_experiences)}")

    # Update resume with merged experiences
    update_resume_experiences(data_dir, resume_id, all_experiences, replace=False)
    print(f"✓ Successfully merged and added {len(all_experiences)} experiences")
    print()


def example_5_filter_and_update():
    """Example 5: Filter experiences before updating"""
    print("=" * 60)
    print("Example 5: Filter Experiences Before Updating")
    print("=" * 60)

    data_dir = Path("data")
    resume_id = "141107d3-f0a9-4bc6-82dd-6fc4506e76f4"

    # Load experiences
    experiences = parse_json_experiences(
        Path("data/experiences_solution_architect.json")
    )

    # Filter: only keep experiences with "Architect" in the role
    filtered = [exp for exp in experiences if "Architect" in exp.get("role", "")]
    print(f"Filtered {len(experiences)} → {len(filtered)} experiences")

    # Update resume with filtered experiences
    update_resume_experiences(data_dir, resume_id, filtered, replace=False)
    print(f"✓ Successfully added {len(filtered)} filtered experiences")
    print()


if __name__ == "__main__":
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  Resume Update Examples - Programmatic Usage".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    print()

    try:
        # Run examples
        example_1_update_from_json()
        # example_2_update_from_markdown()  # Uncomment if markdown file exists
        example_3_programmatic_experiences()
        example_4_merge_multiple_sources()
        example_5_filter_and_update()

        print("=" * 60)
        print("All examples completed successfully!")
        print("=" * 60)

    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)

