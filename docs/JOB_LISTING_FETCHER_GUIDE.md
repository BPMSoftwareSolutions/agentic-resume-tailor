# Job Listing Fetcher Guide

This guide explains how to use the `fetch_job_listing.py` script to pull job listings from the internet and save them as markdown files.

## Overview

The script provides two methods for fetching job listings:

1. **Method 1: Using `requests` library** (Simple, but may be blocked by some sites)
2. **Method 2: Using Selenium** (More robust, works with JavaScript-heavy sites)

## Quick Start

### Basic Usage

```bash
python fetch_job_listing.py
```

This will attempt to fetch the job listing from the URL defined in the script and save it as a markdown file in the `job_listings/` directory.

### Using the Script in Your Code

```python
from fetch_job_listing import fetch_job_listing

# Fetch a job listing
url = "https://www.indeed.com/?from=gnav-viewjob&advn=100919326538784&vjk=fcd29f6d7f5168f9"
filepath = fetch_job_listing(url, output_dir="job_listings")
print(f"Job listing saved to: {filepath}")
```

## Method 1: Using Requests Library

### How It Works

- Uses the `requests` library to fetch the HTML content
- Parses the HTML with BeautifulSoup
- Extracts job title, company, location, and description
- Saves the content as a markdown file

### Advantages

- Simple and lightweight
- No additional dependencies beyond `requests` and `beautifulsoup4`
- Fast

### Disadvantages

- May be blocked by sites with anti-bot protection (like Indeed)
- Doesn't execute JavaScript, so dynamic content won't be captured

### Installation

The required packages are already in `requirements.txt`:
- `requests`
- `beautifulsoup4`

If not installed, run:
```bash
pip install requests beautifulsoup4
```

### Example

```python
from fetch_job_listing import fetch_job_listing

url = "https://example.com/job-listing"
filepath = fetch_job_listing(url)
```

## Method 2: Using Selenium

### How It Works

- Uses Selenium to open a real browser (Chrome)
- Waits for JavaScript to execute and content to load
- Parses the rendered HTML with BeautifulSoup
- Saves the content as a markdown file

### Advantages

- Works with JavaScript-heavy sites
- Bypasses many anti-bot protections
- Captures fully rendered content

### Disadvantages

- Requires additional setup (ChromeDriver)
- Slower than the requests method
- Requires more system resources

### Installation

1. Install Selenium:
```bash
pip install selenium
```

2. Download ChromeDriver:
   - Visit: https://chromedriver.chromium.org/
   - Download the version matching your Chrome browser version
   - Extract the executable to a location in your PATH, or specify the path when creating the driver

3. Verify installation:
```bash
chromedriver --version
```

### Example

```python
from fetch_job_listing import fetch_job_listing_selenium

url = "https://www.indeed.com/?from=gnav-viewjob&advn=100919326538784&vjk=fcd29f6d7f5168f9"
filepath = fetch_job_listing_selenium(url)
```

## Output Format

The script saves job listings as markdown files with the following structure:

```markdown
# Job Title

**Company:** Company Name

**Location:** City, State

---

Job description content here...
```

The filename is derived from the job title, with special characters replaced by underscores.

## Troubleshooting

### 403 Forbidden Error

**Problem:** The script returns a 403 Forbidden error.

**Solutions:**
1. Use Selenium instead of requests
2. Add delays between requests if fetching multiple listings
3. Use a VPN or proxy
4. Check if the site has a robots.txt that blocks automated access

### ChromeDriver Not Found

**Problem:** "ChromeDriver not found" error when using Selenium.

**Solutions:**
1. Download ChromeDriver from https://chromedriver.chromium.org/
2. Ensure it matches your Chrome browser version
3. Add the ChromeDriver location to your system PATH
4. Or specify the path directly in the code:
   ```python
   driver = webdriver.Chrome('/path/to/chromedriver', options=options)
   ```

### Job Content Not Extracted

**Problem:** The script runs but doesn't extract job details properly.

**Possible causes:**
- The website structure is different from expected
- The job content is loaded dynamically (use Selenium)
- The HTML selectors need to be updated

**Solution:** Inspect the website's HTML and update the selectors in the script.

## Customization

### Changing Output Directory

```python
fetch_job_listing(url, output_dir="my_job_listings")
```

### Extracting Additional Information

You can modify the script to extract additional fields like:
- Salary
- Job type (Full-time, Part-time, etc.)
- Application deadline
- Required qualifications

Edit the extraction logic in the `fetch_job_listing()` or `fetch_job_listing_selenium()` functions.

## Legal and Ethical Considerations

- Always check the website's `robots.txt` and Terms of Service
- Respect rate limits and don't make excessive requests
- Some sites may prohibit automated scraping
- Consider using official APIs if available
- Add appropriate delays between requests when fetching multiple listings

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the script comments for implementation details
3. Inspect the website's HTML to understand its structure
4. Consider using the website's official API if available

