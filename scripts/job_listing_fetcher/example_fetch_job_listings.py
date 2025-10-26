#!/usr/bin/env python3
"""
Example script demonstrating how to use the fetch_job_listing module.

This script shows various ways to fetch job listings and save them as markdown files.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.fetch_job_listing import fetch_job_listing, fetch_job_listing_selenium


def example_1_single_job():
    """Example 1: Fetch a single job listing using requests."""
    print("=" * 60)
    print("Example 1: Fetch a single job listing")
    print("=" * 60)
    
    url = "https://www.indeed.com/?from=gnav-viewjob&advn=100919326538784&vjk=fcd29f6d7f5168f9"
    
    try:
        filepath = fetch_job_listing(url, output_dir="job_listings")
        print(f"✓ Successfully saved to: {filepath}\n")
    except Exception as e:
        print(f"✗ Failed to fetch: {e}\n")


def example_2_multiple_jobs():
    """Example 2: Fetch multiple job listings."""
    print("=" * 60)
    print("Example 2: Fetch multiple job listings")
    print("=" * 60)
    
    urls = [
        "https://www.indeed.com/viewjob?jk=example1",
        "https://www.indeed.com/viewjob?jk=example2",
        "https://www.indeed.com/viewjob?jk=example3",
    ]
    
    for i, url in enumerate(urls, 1):
        print(f"\nFetching job {i}/{len(urls)}...")
        try:
            filepath = fetch_job_listing(url, output_dir="job_listings")
            print(f"✓ Saved to: {filepath}")
        except Exception as e:
            print(f"✗ Failed: {e}")


def example_3_custom_output_dir():
    """Example 3: Save to a custom output directory."""
    print("=" * 60)
    print("Example 3: Custom output directory")
    print("=" * 60)
    
    url = "https://www.indeed.com/?from=gnav-viewjob&advn=100919326538784&vjk=fcd29f6d7f5168f9"
    custom_dir = "data/job_listings"
    
    try:
        filepath = fetch_job_listing(url, output_dir=custom_dir)
        print(f"✓ Saved to: {filepath}\n")
    except Exception as e:
        print(f"✗ Failed: {e}\n")


def example_4_selenium_method():
    """Example 4: Fetch using Selenium (for JavaScript-heavy sites)."""
    print("=" * 60)
    print("Example 4: Using Selenium")
    print("=" * 60)
    print("Note: This requires Selenium and ChromeDriver to be installed.\n")
    
    url = "https://www.indeed.com/?from=gnav-viewjob&advn=100919326538784&vjk=fcd29f6d7f5168f9"
    
    try:
        filepath = fetch_job_listing_selenium(url, output_dir="job_listings")
        print(f"✓ Saved to: {filepath}\n")
    except ImportError:
        print("✗ Selenium not installed. Install with: pip install selenium\n")
    except Exception as e:
        print(f"✗ Failed: {e}\n")


def example_5_error_handling():
    """Example 5: Proper error handling."""
    print("=" * 60)
    print("Example 5: Error handling")
    print("=" * 60)
    
    urls = [
        "https://www.indeed.com/?from=gnav-viewjob&advn=100919326538784&vjk=fcd29f6d7f5168f9",
        "https://invalid-url-that-does-not-exist.com/job",
    ]
    
    results = {
        "successful": [],
        "failed": []
    }
    
    for url in urls:
        try:
            filepath = fetch_job_listing(url, output_dir="job_listings")
            results["successful"].append(filepath)
            print(f"✓ {url}")
        except Exception as e:
            results["failed"].append((url, str(e)))
            print(f"✗ {url}: {e}")
    
    print(f"\nSummary:")
    print(f"  Successful: {len(results['successful'])}")
    print(f"  Failed: {len(results['failed'])}\n")


def example_6_batch_processing():
    """Example 6: Batch processing with file output."""
    print("=" * 60)
    print("Example 6: Batch processing")
    print("=" * 60)
    
    # Example URLs (replace with real job URLs)
    job_urls = [
        "https://www.indeed.com/?from=gnav-viewjob&advn=100919326538784&vjk=fcd29f6d7f5168f9",
    ]
    
    output_dir = "job_listings"
    os.makedirs(output_dir, exist_ok=True)
    
    results = []
    
    for url in job_urls:
        try:
            filepath = fetch_job_listing(url, output_dir=output_dir)
            results.append({
                "url": url,
                "status": "success",
                "filepath": filepath
            })
        except Exception as e:
            results.append({
                "url": url,
                "status": "failed",
                "error": str(e)
            })
    
    # Print summary
    print(f"\nProcessed {len(results)} job listings:")
    for result in results:
        status = "✓" if result["status"] == "success" else "✗"
        print(f"{status} {result['url']}")
        if result["status"] == "success":
            print(f"   → {result['filepath']}")
        else:
            print(f"   → Error: {result['error']}")
    
    print()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Job Listing Fetcher - Examples")
    print("=" * 60 + "\n")
    
    # Run examples
    example_1_single_job()
    # example_2_multiple_jobs()
    # example_3_custom_output_dir()
    # example_4_selenium_method()
    # example_5_error_handling()
    # example_6_batch_processing()
    
    print("=" * 60)
    print("Examples completed!")
    print("=" * 60)
    print("\nTo run other examples, uncomment them in the __main__ section.")

