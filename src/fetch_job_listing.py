import requests
from bs4 import BeautifulSoup
import re
import os
import json
import uuid
from datetime import datetime, timezone

from urllib.parse import urlparse, parse_qs, urlunparse


def canonicalize_job_url(url: str) -> str:
    """Return a canonical job URL for known providers (e.g., Indeed).

    - Indeed: convert gnav/redirect URLs with vjk=... to /viewjob?jk=...
    - Otherwise return original URL
    """
    try:
        parsed = urlparse(url)
        host = (parsed.netloc or "").lower()
        query = parse_qs(parsed.query)
        if "indeed.com" in host:
            # If there's a vjk param, convert to canonical viewjob URL
            if "vjk" in query and query["vjk"]:
                jk = query["vjk"][0]
                return f"https://www.indeed.com/viewjob?jk={jk}"
            # If there's a jk param already, ensure canonical path
            if parsed.path != "/viewjob" and "jk" in query and query["jk"]:
                jk = query["jk"][0]
                return f"https://www.indeed.com/viewjob?jk={jk}"
        return url
    except Exception:
        return url


def is_file_url(url: str) -> bool:
    p = urlparse(url)
    return p.scheme == "file"


def read_local_file_from_url(url: str) -> str:
    p = urlparse(url)
    # Support relative paths like file://data/job_listings/foo.md
    local_path = p.path
    if local_path.startswith("/") and ":" not in local_path:
        # Windows path fix (strip leading slash)
        local_path = local_path[1:]
    if not os.path.exists(local_path):
        raise FileNotFoundError(f"Local file not found: {local_path}")
    return local_path

def update_job_listings_index(title, company, location, filepath, output_dir="job_listings"):
    """
    Update the job_listings/index.json file with the new job listing.

    Args:
        title (str): Job title
        company (str): Company name
        location (str): Job location
        filepath (str): Path to the saved markdown file
        output_dir (str): Output directory
    """
    # Determine the index file path
    if output_dir == "job_listings":
        index_path = "data/job_listings/index.json"
    else:
        index_path = os.path.join(output_dir, "index.json")

    # Create index if it doesn't exist
    if not os.path.exists(index_path):
        index_data = {"job_listings": []}
    else:
        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                index_data = json.load(f)
        except (json.JSONDecodeError, IOError):
            index_data = {"job_listings": []}

    # Create job listing entry
    job_entry = {
        "id": str(uuid.uuid4()),
        "title": title,
        "company": company,
        "location": location,
        "file": os.path.basename(filepath),
        "created_at": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        "description": f"{title} at {company}" + (f" in {location}" if location else "")
    }

    # Add to index
    index_data["job_listings"].append(job_entry)

    # Save updated index
    os.makedirs(os.path.dirname(index_path), exist_ok=True)
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=2, ensure_ascii=False)

    print(f"✓ Updated index: {index_path}")
    return job_entry


def fetch_job_listing(url, output_dir="job_listings"):
    """
    Fetch a job listing from a URL and save it as a markdown file.

    Supports:
    - Indeed.com job listings (with URL canonicalization)
    - Generic job listing pages
    - file:// URLs for local markdown/html (useful for offline testing)

    Args:
        url (str): The URL of the job listing
        output_dir (str): Directory to save the markdown file

    Returns:
        str: Path to the saved markdown file
    """
    # Handle local file URLs (useful for tests/demos)
    if is_file_url(url):
        local_path = read_local_file_from_url(url)
        # Copy file into output_dir with normalized name
        os.makedirs(output_dir, exist_ok=True)
        safe_title = os.path.splitext(os.path.basename(local_path))[0]
        dest_path = os.path.join(output_dir, f"{safe_title}.md")
        with open(local_path, "r", encoding="utf-8") as src, open(dest_path, "w", encoding="utf-8") as dst:
            dst.write(src.read())
        print(f"✓ Loaded local job listing from {local_path}")
        update_job_listings_index(safe_title, "", "", dest_path, output_dir)
        return dest_path

    # Canonicalize URL for known providers
    url = canonicalize_job_url(url)

    # Enhanced headers to avoid 403 errors
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Referer": "https://www.indeed.com/",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
    }

    # First attempt: requests
    try:
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=15, allow_redirects=True)
        if response.status_code in (403, 404):
            raise requests.exceptions.HTTPError(
                f"{response.status_code} Error for url: {url}", response=response
            )
        response.raise_for_status()
        html_text = response.text
        source = "requests"
    except requests.exceptions.HTTPError as e:
        status = getattr(e.response, "status_code", "?")
        print(f"HTTP Error: {e}")
        print(f"Status Code: {status}")
        # Fallback 1: text proxy (r.jina.ai)
        try:
            parsed = urlparse(url)
            proxy_url = f"https://r.jina.ai/http://{parsed.netloc}{parsed.path}"
            if parsed.query:
                proxy_url += f"?{parsed.query}"
            print(f"↪️  Falling back to read-only proxy: {proxy_url}")
            proxy_resp = requests.get(proxy_url, timeout=15)
            proxy_resp.raise_for_status()
            html_text = proxy_resp.text
            source = "proxy"
        except Exception as proxy_err:
            print(f"Proxy fallback failed: {proxy_err}")
            # Fallback 2: Selenium (if available)
            try:
                print("↪️  Attempting Selenium fallback (if installed)...")
                return fetch_job_listing_selenium(url, output_dir)
            except Exception as sel_err:
                print("Selenium fallback unavailable or failed.")
                print("Install with: pip install selenium webdriver-manager")
                raise e
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        raise

    # Parse content
    soup = BeautifulSoup(html_text, "html.parser")

    # Try to extract job title
    title_tag = soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else "Job Title Not Found"

    # Try to extract company and location
    company = ""
    location = ""
    company_tag = soup.find("div", string=re.compile("Company|Employer", re.I))
    if company_tag:
        company = company_tag.get_text(strip=True)
    else:
        # Try meta tags
        meta_company = soup.find("meta", {"property": "og:site_name"})
        if meta_company:
            company = meta_company.get("content", "")

    # Try to extract location
    location_tag = soup.find("div", string=re.compile("Location", re.I))
    if location_tag:
        location = location_tag.get_text(strip=True)

    # Try to extract job description
    desc_tag = soup.find("div", id=re.compile("jobDescriptionText|jobDescription", re.I))
    if not desc_tag:
        desc_tag = soup.find("div", class_=re.compile("jobsearch-JobComponent-description|description", re.I))
    description = desc_tag.get_text("\n", strip=True) if desc_tag else "Job description not found."

    # Prepare markdown content
    md = f"# {title}\n\n"
    if company:
        md += f"**Company:** {company}\n\n"
    if location:
        md += f"**Location:** {location}\n\n"
    md += "---\n\n"
    md += description

    # Prepare output directory and filename
    os.makedirs(output_dir, exist_ok=True)
    safe_title = re.sub(r"[^a-zA-Z0-9_-]", "_", title)[:50]
    filename = f"{safe_title or 'job_listing'}.md"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"✓ Saved job listing to {filepath}")

    # Update the job listings index
    update_job_listings_index(title, company, location, filepath, output_dir)

    return filepath

def fetch_job_listing_selenium(url, output_dir="job_listings"):
    """
    Fetch a job listing using Selenium (requires selenium and webdriver).
    This method works better with JavaScript-heavy sites like Indeed.

    Args:
        url (str): The URL of the job listing
        output_dir (str): Directory to save the markdown file

    Returns:
        str: Path to the saved markdown file
    """
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
    except ImportError:
        print("Selenium is not installed. Install it with: pip install selenium")
        print("You'll also need to download ChromeDriver from: https://chromedriver.chromium.org/")
        raise

    # Initialize Chrome driver
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)

        # Wait for job content to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )

        # Get page source and parse with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Extract job information
        title_tag = soup.find("h1")
        title = title_tag.get_text(strip=True) if title_tag else "Job Title Not Found"

        company = ""
        location = ""
        company_tag = soup.find("div", string=re.compile("Company|Employer", re.I))
        if company_tag:
            company = company_tag.get_text(strip=True)

        location_tag = soup.find("div", string=re.compile("Location", re.I))
        if location_tag:
            location = location_tag.get_text(strip=True)

        desc_tag = soup.find("div", id=re.compile("jobDescriptionText|jobDescription", re.I))
        if not desc_tag:
            desc_tag = soup.find("div", class_=re.compile("jobsearch-JobComponent-description|description", re.I))
        description = desc_tag.get_text("\n", strip=True) if desc_tag else "Job description not found."

        # Prepare markdown content
        md = f"# {title}\n\n"
        if company:
            md += f"**Company:** {company}\n\n"
        if location:
            md += f"**Location:** {location}\n\n"
        md += "---\n\n"
        md += description

        # Save to file
        os.makedirs(output_dir, exist_ok=True)
        safe_title = re.sub(r"[^a-zA-Z0-9_-]", "_", title)[:50]
        filename = f"{safe_title or 'job_listing'}.md"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"✓ Saved job listing to {filepath}")

        # Update the job listings index
        update_job_listings_index(title, company, location, filepath, output_dir)

        return filepath

    finally:
        driver.quit()


if __name__ == "__main__":
    url = "https://www.indeed.com/?from=gnav-viewjob&advn=100919326538784&vjk=fcd29f6d7f5168f9"

    print("Attempting to fetch job listing...")
    print(f"URL: {url}\n")

    try:
        # Try with requests first
        print("Method 1: Using requests library...")
        fetch_job_listing(url)
    except Exception as e:
        print(f"\nMethod 1 failed: {e}")
        print("\nMethod 2: Using Selenium (requires installation)...")
        print("To use Selenium, install it with:")
        print("  pip install selenium")
        print("\nThen download ChromeDriver from:")
        print("  https://chromedriver.chromium.org/")
        print("\nOr use the fetch_job_listing_selenium() function directly.")
