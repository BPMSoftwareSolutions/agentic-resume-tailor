#!/usr/bin/env python3
"""
Demo script showing the job listing fetcher in action with a local HTML file.

This demonstrates how the fetcher parses HTML and extracts job information.
"""

from bs4 import BeautifulSoup
import re
import os


def demo_fetch_from_local_html(html_file, output_dir="job_listings"):
    """
    Demo: Parse a local HTML file and extract job information.
    This shows how the fetcher works without needing to hit a live website.
    """
    print("=" * 70)
    print("JOB LISTING FETCHER - DEMO")
    print("=" * 70)
    print()
    
    # Read the HTML file
    print(f"📂 Reading HTML file: {html_file}")
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    print(f"✓ File loaded ({len(html_content)} bytes)")
    print()
    
    # Parse with BeautifulSoup
    print("🔍 Parsing HTML with BeautifulSoup...")
    soup = BeautifulSoup(html_content, "html.parser")
    print("✓ HTML parsed successfully")
    print()
    
    # Extract job title
    print("📋 Extracting job information...")
    title_tag = soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else "Job Title Not Found"
    print(f"  ✓ Title: {title}")
    
    # Extract company
    company = ""
    company_tag = soup.find("div", string=re.compile("Company|Employer", re.I))
    if company_tag:
        company = company_tag.get_text(strip=True)
    print(f"  ✓ Company: {company}")
    
    # Extract location
    location = ""
    location_tag = soup.find("div", string=re.compile("Location", re.I))
    if location_tag:
        location = location_tag.get_text(strip=True)
    print(f"  ✓ Location: {location}")
    
    # Extract description
    desc_tag = soup.find("div", id=re.compile("jobDescriptionText|jobDescription", re.I))
    if not desc_tag:
        desc_tag = soup.find("div", class_=re.compile("jobsearch-JobComponent-description|description", re.I))
    description = desc_tag.get_text("\n", strip=True) if desc_tag else "Job description not found."
    desc_preview = description[:200] + "..." if len(description) > 200 else description
    print(f"  ✓ Description: {desc_preview}")
    print()
    
    # Create markdown
    print("📝 Creating markdown content...")
    md = f"# {title}\n\n"
    if company:
        md += f"**Company:** {company}\n\n"
    if location:
        md += f"**Location:** {location}\n\n"
    md += "---\n\n"
    md += description
    
    print(f"✓ Markdown created ({len(md)} bytes)")
    print()
    
    # Save to file
    print("💾 Saving to file...")
    os.makedirs(output_dir, exist_ok=True)
    safe_title = re.sub(r"[^a-zA-Z0-9_-]", "_", title)[:50]
    filename = f"{safe_title or 'job_listing'}.md"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(md)
    
    print(f"✓ Saved to: {filepath}")
    print()
    
    # Display the result
    print("=" * 70)
    print("GENERATED MARKDOWN FILE")
    print("=" * 70)
    print()
    print(md)
    print()
    print("=" * 70)
    print("✅ DEMO COMPLETE!")
    print("=" * 70)
    print()
    print("This is what the fetcher does:")
    print("  1. Fetches HTML from a URL (or reads from a file)")
    print("  2. Parses the HTML structure")
    print("  3. Extracts job title, company, location, and description")
    print("  4. Formats as markdown")
    print("  5. Saves to a file")
    print()
    print("To use with real URLs:")
    print("  from fetch_job_listing import fetch_job_listing")
    print("  filepath = fetch_job_listing('https://example.com/job')")
    print()


if __name__ == "__main__":
    demo_fetch_from_local_html("demo_job_listing.html")

