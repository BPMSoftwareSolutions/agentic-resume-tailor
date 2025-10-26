# Job Listing Fetcher

A Python system for fetching job listings from the internet and saving them as markdown files with automatic system integration.

## 📁 File Structure

```
agentic-resume-tailor/
├── src/
│   └── fetch_job_listing.py              # Core implementation
├── scripts/job_listing_fetcher/
│   ├── test_fetch_with_index.py          # Integration test
│   ├── verify_index.py                   # Index verification
│   ├── demo_fetch_local.py               # Local HTML demo
│   ├── demo_usage.py                     # Usage patterns
│   ├── example_fetch_job_listings.py     # 6 usage examples
│   └── demo_job_listing.html             # Sample HTML
├── docs/
│   ├── JOB_LISTING_FETCHER_README.md     # This file
│   ├── JOB_LISTING_FETCHER_GUIDE.md      # Complete user guide
│   ├── JOB_LISTING_QUICK_START.md        # Quick reference
│   ├── JOB_FETCHER_SUMMARY.md            # Implementation details
│   ├── JOB_LISTING_INDEX_INTEGRATION.md  # Index integration guide
│   └── JOB_LISTING_SYSTEM_INTEGRATION.md # System integration details
└── data/job_listings/
    ├── index.json                        # Auto-updated index
    └── *.md                              # Job listing markdown files
```

## 🚀 Quick Start

### Basic Usage

```python
from src.fetch_job_listing import fetch_job_listing

# Fetch and auto-index
filepath = fetch_job_listing("https://example.com/job")
print(f"Saved to: {filepath}")
```

### Run Tests

```bash
cd scripts/job_listing_fetcher
python test_fetch_with_index.py
python verify_index.py
```

### Run Examples

```bash
cd scripts/job_listing_fetcher
python example_fetch_job_listings.py
python demo_fetch_local.py
```

## ✨ Features

✅ **Dual Fetching Methods**
- Fast: requests + BeautifulSoup
- Robust: Selenium + Chrome (handles JavaScript)

✅ **Automatic System Integration**
- Auto-updates `data/job_listings/index.json`
- UUID generation for each listing
- ISO 8601 timestamps
- Metadata tracking

✅ **Production Ready**
- Comprehensive error handling
- Tested and verified
- Well documented

## 📚 Documentation

- **[JOB_LISTING_FETCHER_GUIDE.md](JOB_LISTING_FETCHER_GUIDE.md)** - Complete user guide with troubleshooting
- **[JOB_LISTING_QUICK_START.md](JOB_LISTING_QUICK_START.md)** - Quick reference card
- **[JOB_FETCHER_SUMMARY.md](JOB_FETCHER_SUMMARY.md)** - Implementation details
- **[JOB_LISTING_INDEX_INTEGRATION.md](JOB_LISTING_INDEX_INTEGRATION.md)** - Index integration guide
- **[JOB_LISTING_SYSTEM_INTEGRATION.md](JOB_LISTING_SYSTEM_INTEGRATION.md)** - System integration details

## 🔗 System Integration

When you fetch a job listing:

```
URL/HTML → Parse → Extract → Markdown → Save → Update Index
                                              ↓
                                    data/job_listings/
                                    ├── index.json (UPDATED)
                                    └── job_title.md
```

### Index Entry Example

```json
{
  "id": "644870ea-db70-49b3-9b1f-a1f4887c3b70",
  "title": "Senior Software Engineer",
  "company": "TechCorp Inc.",
  "location": "San Francisco, CA",
  "file": "Senior_Software_Engineer.md",
  "created_at": "2025-10-26T15:24:10.294414Z",
  "description": "Senior Software Engineer at TechCorp Inc. in San Francisco, CA"
}
```

## 🎯 Core Functions

### `fetch_job_listing(url, output_dir="job_listings")`

Fetch a job listing using requests + BeautifulSoup.

**Parameters:**
- `url` (str): Job listing URL
- `output_dir` (str): Output directory (default: "job_listings")

**Returns:**
- `str`: Path to saved markdown file

**Example:**
```python
from src.fetch_job_listing import fetch_job_listing

filepath = fetch_job_listing("https://example.com/job")
```

### `fetch_job_listing_selenium(url, output_dir="job_listings")`

Fetch a job listing using Selenium + Chrome (handles JavaScript).

**Parameters:**
- `url` (str): Job listing URL
- `output_dir` (str): Output directory (default: "job_listings")

**Returns:**
- `str`: Path to saved markdown file

**Example:**
```python
from src.fetch_job_listing import fetch_job_listing_selenium

filepath = fetch_job_listing_selenium("https://example.com/job")
```

### `update_job_listings_index(title, company, location, filepath, output_dir)`

Update the job listings index with a new entry.

**Parameters:**
- `title` (str): Job title
- `company` (str): Company name
- `location` (str): Job location
- `filepath` (str): Path to saved markdown file
- `output_dir` (str): Output directory

**Returns:**
- `dict`: The created job entry

## ✅ Test Results

**Integration Test: PASSED ✅**

- Index entries before: 19
- Index entries after: 20
- New entry added successfully
- All fields populated correctly

## 🔄 Workflow

1. **Fetch** - Get job listing from URL
2. **Parse** - Extract title, company, location, description
3. **Format** - Create markdown content
4. **Save** - Write to `data/job_listings/`
5. **Index** - Add entry to `index.json` ✨
6. **Track** - Use UUID for reference

## 🎓 Integration with AI Agent

The AI agent can now:

1. Query the index to find job listings
2. Access job files using filenames from index
3. Track listings with unique IDs
4. Automate workflows based on metadata
5. Match jobs to resumes using index data

## 📊 Statistics

- **Core Scripts**: 1 (src/fetch_job_listing.py)
- **Test/Demo Scripts**: 6 (scripts/job_listing_fetcher/)
- **Documentation**: 6 files (docs/)
- **Index Entries**: Auto-tracked

## ✅ Status

**COMPLETE AND TESTED**

All components are working and integrated with the system!

---

**Created**: 2025-10-26
**Status**: ✅ Complete
**Integration**: ✅ System-wide
**Testing**: ✅ Passed

