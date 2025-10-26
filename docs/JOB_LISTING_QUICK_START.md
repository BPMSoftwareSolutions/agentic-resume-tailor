# Job Listing Fetcher - Quick Start

## 30-Second Setup

```bash
# Already installed - just run it!
python fetch_job_listing.py
```

## Common Tasks

### Fetch a Single Job Listing

```python
from fetch_job_listing import fetch_job_listing

url = "https://example.com/job-listing"
filepath = fetch_job_listing(url)
print(f"Saved to: {filepath}")
```

### Fetch Multiple Job Listings

```python
from fetch_job_listing import fetch_job_listing

urls = [
    "https://example.com/job1",
    "https://example.com/job2",
    "https://example.com/job3",
]

for url in urls:
    try:
        filepath = fetch_job_listing(url)
        print(f"✓ {filepath}")
    except Exception as e:
        print(f"✗ Failed: {e}")
```

### Save to Custom Directory

```python
from fetch_job_listing import fetch_job_listing

filepath = fetch_job_listing(url, output_dir="data/job_listings")
```

### Fetch from Indeed (Requires Selenium)

```bash
# Step 1: Install Selenium
pip install selenium

# Step 2: Download ChromeDriver
# Visit: https://chromedriver.chromium.org/
# Download version matching your Chrome browser

# Step 3: Use Selenium method
python -c "
from fetch_job_listing import fetch_job_listing_selenium
url = 'https://www.indeed.com/?from=gnav-viewjob&advn=100919326538784&vjk=fcd29f6d7f5168f9'
fetch_job_listing_selenium(url)
"
```

## Output

The script creates markdown files in the `job_listings/` directory:

```
job_listings/
├── Senior_Software_Engineer.md
├── Product_Manager.md
└── Data_Scientist.md
```

Each file contains:
```markdown
# Job Title

**Company:** Company Name

**Location:** City, State

---

Job description...
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| 403 Forbidden | Use Selenium method or try a different job site |
| Module not found | Run `pip install requests beautifulsoup4` |
| ChromeDriver not found | Download from https://chromedriver.chromium.org/ |
| No job content extracted | The website structure may be different - inspect HTML |

## File Locations

- **Main script**: `fetch_job_listing.py`
- **Examples**: `example_fetch_job_listings.py`
- **Full guide**: `JOB_LISTING_FETCHER_GUIDE.md`
- **Summary**: `JOB_FETCHER_SUMMARY.md`

## API Reference

### `fetch_job_listing(url, output_dir="job_listings")`

Fetch a job listing using requests + BeautifulSoup.

**Parameters:**
- `url` (str): Job listing URL
- `output_dir` (str): Output directory (default: "job_listings")

**Returns:**
- `str`: Path to saved markdown file

**Raises:**
- `requests.exceptions.HTTPError`: If HTTP request fails
- `requests.exceptions.RequestException`: If network error occurs

### `fetch_job_listing_selenium(url, output_dir="job_listings")`

Fetch a job listing using Selenium (requires installation).

**Parameters:**
- `url` (str): Job listing URL
- `output_dir` (str): Output directory (default: "job_listings")

**Returns:**
- `str`: Path to saved markdown file

**Raises:**
- `ImportError`: If Selenium not installed
- `Exception`: If browser automation fails

## Supported Job Sites

✓ **Works well with:**
- LinkedIn Jobs
- GitHub Jobs
- Stack Overflow Jobs
- Company career pages
- Generic job boards

⚠️ **Requires Selenium:**
- Indeed.com
- Other sites with anti-bot protection

## Tips & Tricks

1. **Batch Processing**: Use a loop to fetch multiple listings
2. **Error Handling**: Wrap calls in try-except blocks
3. **Rate Limiting**: Add delays between requests
4. **Custom Parsing**: Modify extraction logic for specific sites
5. **Integration**: Use with your resume tailor system

## Next Steps

1. Read `JOB_LISTING_FETCHER_GUIDE.md` for detailed documentation
2. Check `example_fetch_job_listings.py` for more examples
3. Customize the script for your specific needs
4. Integrate with your resume tailoring workflow

## Support

For detailed help, see:
- `JOB_LISTING_FETCHER_GUIDE.md` - Full documentation
- `example_fetch_job_listings.py` - Code examples
- `JOB_FETCHER_SUMMARY.md` - Implementation details

