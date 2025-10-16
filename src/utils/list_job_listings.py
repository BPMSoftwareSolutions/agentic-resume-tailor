#!/usr/bin/env python3
"""
List all job listings in a formatted table.

This script reads the job listings index and displays them in a clean table format.
Part of the CRUD operations suite for job listing management.

Usage:
    python src/utils/list_job_listings.py [--format table|json|simple]

Examples:
    python src/utils/list_job_listings.py
    python src/utils/list_job_listings.py --format json
    python src/utils/list_job_listings.py --format simple
"""

import argparse
import json
from datetime import datetime
from pathlib import Path


def load_job_listings_index():
    """Load the job listings index file."""
    index_path = Path("data/job_listings/index.json")

    if not index_path.exists():
        print(f"❌ Error: Job listings index not found at {index_path}")
        return None

    try:
        with open(index_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("job_listings", [])
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in job listings index: {e}")
        return None
    except Exception as e:
        print(f"❌ Error reading job listings index: {e}")
        return None


def format_date(date_str):
    """Format ISO date string to readable format."""
    try:
        dt = datetime.fromisoformat(date_str)
        return dt.strftime("%Y-%m-%d %H:%M")
    except:
        return date_str


def print_table(job_listings):
    """Print job listings in a formatted table."""
    if not job_listings:
        print("📋 No job listings found.")
        return

    # Calculate column widths
    max_title_len = max(len(j.get("title", "")) for j in job_listings)
    max_title_len = max(max_title_len, len("Job Title"))
    max_title_len = min(max_title_len, 45)  # Cap at 45 chars

    max_company_len = max(len(j.get("company", "")) for j in job_listings)
    max_company_len = max(max_company_len, len("Company"))
    max_company_len = min(max_company_len, 25)  # Cap at 25 chars

    # Header
    print("\n" + "=" * 120)
    print(f"💼 JOB LISTINGS ({len(job_listings)} total)")
    print("=" * 120)

    # Column headers
    header = f"{'#':<3} {'Job Title':<{max_title_len}} {'Company':<{max_company_len}} {'Location':<20} {'Added':<17}"
    print(header)
    print("-" * 120)

    # Sort by added date (newest first)
    sorted_listings = sorted(
        job_listings, key=lambda j: j.get("added_at", ""), reverse=True
    )

    # Rows
    for idx, job in enumerate(sorted_listings, 1):
        title = job.get("title", "N/A")
        if len(title) > max_title_len:
            title = title[: max_title_len - 3] + "..."

        company = job.get("company", "N/A")
        if len(company) > max_company_len:
            company = company[: max_company_len - 3] + "..."

        location = job.get("location", "N/A")
        if len(location) > 20:
            location = location[:17] + "..."

        added = format_date(job.get("added_at", "N/A"))

        print(
            f"{idx:<3} {title:<{max_title_len}} {company:<{max_company_len}} {location:<20} {added:<17}"
        )

    print("=" * 120)
    print(f"\n📊 Total Job Listings: {len(job_listings)}\n")


def print_simple(job_listings):
    """Print job listings in a simple list format."""
    if not job_listings:
        print("📋 No job listings found.")
        return

    print(f"\n💼 Job Listings ({len(job_listings)} total):\n")

    # Sort by title
    sorted_listings = sorted(job_listings, key=lambda j: j.get("title", "").lower())

    for idx, job in enumerate(sorted_listings, 1):
        title = job.get("title", "N/A")
        company = job.get("company", "N/A")
        print(f"{idx}. {title} at {company}")

    print()


def print_json(job_listings):
    """Print job listings in JSON format."""
    print(json.dumps({"job_listings": job_listings}, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description="List all job listings in a formatted table",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python src/utils/list_job_listings.py                    # Table format (default)
  python src/utils/list_job_listings.py --format simple    # Simple list
  python src/utils/list_job_listings.py --format json      # JSON output
        """,
    )

    parser.add_argument(
        "--format",
        choices=["table", "json", "simple"],
        default="table",
        help="Output format (default: table)",
    )

    args = parser.parse_args()

    # Load job listings
    job_listings = load_job_listings_index()

    if job_listings is None:
        return 1

    # Print in requested format
    if args.format == "json":
        print_json(job_listings)
    elif args.format == "simple":
        print_simple(job_listings)
    else:  # table
        print_table(job_listings)

    return 0


if __name__ == "__main__":
    exit(main())
