#!/usr/bin/env python3
"""
Demonstration of the Job Listing Fetcher usage patterns.
"""

import os


def main():
    print('=' * 70)
    print('JOB LISTING FETCHER - USAGE PATTERNS')
    print('=' * 70)
    print()

    # Example 1: Basic usage
    print('Example 1: Basic Usage')
    print('-' * 70)
    print('Code:')
    print('  from fetch_job_listing import fetch_job_listing')
    print('  filepath = fetch_job_listing(url)')
    print()
    print('Result: Saves job listing to job_listings/ directory')
    print()

    # Example 2: Custom output directory
    print('Example 2: Custom Output Directory')
    print('-' * 70)
    print('Code:')
    print('  filepath = fetch_job_listing(url, output_dir="data/jobs")')
    print()
    print('Result: Saves job listing to data/jobs/ directory')
    print()

    # Example 3: Error handling
    print('Example 3: Error Handling')
    print('-' * 70)
    print('Code:')
    print('  try:')
    print('      filepath = fetch_job_listing(url)')
    print('      print(f"Saved to: {filepath}")')
    print('  except Exception as e:')
    print('      print(f"Error: {e}")')
    print()
    print('Result: Gracefully handles errors')
    print()

    # Example 4: Batch processing
    print('Example 4: Batch Processing')
    print('-' * 70)
    print('Code:')
    print('  urls = ["url1", "url2", "url3"]')
    print('  for url in urls:')
    print('      try:')
    print('          filepath = fetch_job_listing(url)')
    print('          print(f"✓ {filepath}")')
    print('      except Exception as e:')
    print('          print(f"✗ {url}: {e}")')
    print()
    print('Result: Processes multiple job listings')
    print()

    # Example 5: Using Selenium
    print('Example 5: Using Selenium (for JavaScript-heavy sites)')
    print('-' * 70)
    print('Code:')
    print('  from fetch_job_listing import fetch_job_listing_selenium')
    print('  filepath = fetch_job_listing_selenium(url)')
    print()
    print('Result: Uses real browser to fetch job listing')
    print('Note: Requires Selenium and ChromeDriver installation')
    print()

    # Show available files
    print('=' * 70)
    print('FILES CREATED')
    print('=' * 70)
    print()
    files = [
        'fetch_job_listing.py',
        'example_fetch_job_listings.py',
        'demo_fetch_local.py',
        'demo_usage.py',
        'demo_job_listing.html',
        'JOB_LISTING_FETCHER_GUIDE.md',
        'QUICK_START.md',
        'JOB_FETCHER_SUMMARY.md',
    ]
    for f in files:
        exists = '✓' if os.path.exists(f) else '✗'
        print(f'{exists} {f}')
    print()

    # Show output
    print('=' * 70)
    print('OUTPUT FILES GENERATED')
    print('=' * 70)
    print()
    if os.path.exists('job_listings'):
        files_in_dir = os.listdir('job_listings')
        if files_in_dir:
            for f in files_in_dir:
                filepath = os.path.join('job_listings', f)
                size = os.path.getsize(filepath)
                print(f'✓ job_listings/{f} ({size} bytes)')
        else:
            print('(No files yet)')
    else:
        print('(Directory not created yet)')
    print()

    # Summary
    print('=' * 70)
    print('SUMMARY')
    print('=' * 70)
    print()
    print('✓ Main script: fetch_job_listing.py')
    print('  - fetch_job_listing(url) - Uses requests + BeautifulSoup')
    print('  - fetch_job_listing_selenium(url) - Uses Selenium + Chrome')
    print()
    print('✓ Documentation:')
    print('  - JOB_LISTING_FETCHER_GUIDE.md - Full guide')
    print('  - QUICK_START.md - Quick reference')
    print('  - JOB_FETCHER_SUMMARY.md - Implementation details')
    print()
    print('✓ Examples:')
    print('  - example_fetch_job_listings.py - Usage examples')
    print('  - demo_fetch_local.py - Local HTML demo')
    print('  - demo_usage.py - This file')
    print()
    print('✓ Demo files:')
    print('  - demo_job_listing.html - Sample job listing HTML')
    print()
    print('=' * 70)
    print('NEXT STEPS')
    print('=' * 70)
    print()
    print('1. Read QUICK_START.md for quick reference')
    print('2. Check example_fetch_job_listings.py for code examples')
    print('3. Run demo_fetch_local.py to see it in action')
    print('4. Use fetch_job_listing() with your own URLs')
    print('5. Install Selenium if you need to fetch from Indeed')
    print()


if __name__ == "__main__":
    main()

