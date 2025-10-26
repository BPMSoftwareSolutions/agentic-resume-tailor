# Tailor Resume from URL - Integration Guide

## Overview

The `tailor_from_url.py` script provides a **simple, unified workflow** for:
1. **Fetching** job listings from URLs
2. **Tailoring** resumes to job descriptions
3. **Generating** HTML/DOCX output

This is the **simplest way** to go from job URL → tailored resume.

## Quick Start

### Basic Usage

```bash
# Tailor Master Resume to job URL
python src/tailor_from_url.py \
  --url "https://example.com/job-posting" \
  --resume "Master Resume" \
  --out out/tailored.html

# With DOCX export
python src/tailor_from_url.py \
  --url "https://example.com/job-posting" \
  --resume "Master Resume" \
  --out out/tailored.html \
  --docx

# With RAG enhancement
python src/tailor_from_url.py \
  --url "https://example.com/job-posting" \
  --resume "Master Resume" \
  --out out/tailored.html \
  --use-rag \
  --theme modern
```

## Features

### ✅ What It Does

1. **Fetches Job Listing**
   - Downloads HTML from URL
   - Extracts job title, company, location, description
   - Saves as markdown to `data/job_listings/`
   - Auto-updates `data/job_listings/index.json`

2. **Tailors Resume**
   - Loads your resume (by name or file path)
   - Extracts keywords from job description
   - Scores and selects relevant experience bullets
   - Optionally uses RAG for context-aware selection

3. **Generates Output**
   - Creates professional HTML resume
   - Optionally exports to DOCX
   - Supports multiple themes

### 🎯 Supported Themes

- `professional` (default) - Clean, corporate look
- `modern` - Contemporary design
- `executive` - Premium appearance
- `creative` - Unique, artistic style

## Command Reference

### Required Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `--url` | Job listing URL | `https://example.com/job` |
| `--resume` | Resume name or file path | `"Master Resume"` or `data/master_resume.json` |
| `--out` | Output HTML file path | `out/tailored.html` |

### Optional Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--theme` | HTML theme | `professional` |
| `--docx` | Also export to DOCX | False |
| `--use-rag` | Use RAG for tailoring | False |
| `--use-llm-rewriting` | Use LLM for rewriting | False |
| `--vector-store` | RAG vector store path | `data/rag/vector_store.json` |

## Examples

### Example 1: Simple Tailoring

```bash
python src/tailor_from_url.py \
  --url "https://www.linkedin.com/jobs/view/123456789" \
  --resume "Master Resume" \
  --out out/linkedin_job.html
```

**Output:**
- `out/linkedin_job.html` - Tailored resume
- `data/job_listings/LinkedIn_Job_Title.md` - Saved job listing
- `data/job_listings/index.json` - Updated index

### Example 2: With DOCX Export

```bash
python src/tailor_from_url.py \
  --url "https://example.com/careers/senior-engineer" \
  --resume "Ford" \
  --out out/ford_senior_engineer.html \
  --docx \
  --theme modern
```

**Output:**
- `out/ford_senior_engineer.html` - HTML resume
- `out/ford_senior_engineer.docx` - DOCX resume
- `data/job_listings/Senior_Engineer.md` - Saved job listing

### Example 3: With RAG Enhancement

```bash
python src/tailor_from_url.py \
  --url "https://example.com/devops-role" \
  --resume "Master Resume" \
  --out out/devops_tailored.html \
  --use-rag \
  --theme executive
```

**Features:**
- Retrieves relevant experiences from RAG vector store
- Scores bullets based on job requirements
- Selects most relevant experiences
- Generates tailored resume

## Workflow Diagram

```
User provides URL
        ↓
Fetch job listing from URL
        ↓
Extract job title, company, location, description
        ↓
Save to data/job_listings/
        ↓
Update data/job_listings/index.json
        ↓
Load resume (by name or path)
        ↓
Extract keywords from job description
        ↓
[Optional] Retrieve RAG context
        ↓
Score and select relevant bullets
        ↓
Generate HTML resume
        ↓
[Optional] Export to DOCX
        ↓
Output files ready
```

## Resume Lookup

The script supports multiple ways to specify your resume:

### By File Path
```bash
--resume "data/master_resume.json"
--resume "data/resumes/abc123.json"
```

### By Resume Name
```bash
--resume "Master Resume"
--resume "Ford"
--resume "Sidney_Jones_Engineering_Manager"
```

The system automatically looks up the resume by name in `data/resumes/index.json`.

## Output Files

### Generated Files

1. **HTML Resume**
   - Location: `out/tailored.html` (or specified path)
   - Format: Professional HTML with embedded CSS
   - Themes: Professional, Modern, Executive, Creative

2. **DOCX Resume** (if `--docx` flag used)
   - Location: `out/tailored.docx`
   - Format: Microsoft Word document
   - Fully editable

3. **Job Listing** (auto-saved)
   - Location: `data/job_listings/Job_Title.md`
   - Format: Markdown
   - Contains: Title, company, location, description

4. **Index Update** (auto-updated)
   - Location: `data/job_listings/index.json`
   - Contains: Metadata for all fetched job listings
   - Fields: ID, title, company, location, file, created_at

## Integration with Agent

The agent can use this script to tailor resumes:

```
User: "Tailor my resume for this job: https://example.com/job"

Agent: "I'll tailor your resume to that job posting.

run: python src/tailor_from_url.py --url "https://example.com/job" --resume "Master Resume" --out out/tailored.html --docx

[After execution]
✅ Resume tailored successfully!
   - HTML: out/tailored.html
   - DOCX: out/tailored.docx
   - Job listing saved to: data/job_listings/Job_Title.md
```

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'fetch_job_listing'"

**Solution:** Make sure you're running from the repository root:
```bash
cd c:\source\repos\bpm\internal\agentic-resume-tailor
python src/tailor_from_url.py --url "..." --resume "..." --out "..."
```

### Issue: "Resume not found"

**Solution:** Check that the resume name exists:
```bash
# List available resumes
python -c "import json; print(json.load(open('data/resumes/index.json')))"
```

### Issue: "Job listing fetch failed"

**Solution:** Some sites have anti-bot protection. Try:
1. Using a different URL
2. Checking if the URL is publicly accessible
3. Using a local HTML file for testing

### Issue: "RAG context not found"

**Solution:** Make sure the vector store exists:
```bash
ls -la data/rag/vector_store.json
```

If missing, build it first:
```bash
python src/rag/rag_indexer.py
```

## Testing

Run the integration test:

```bash
python scripts/test_tailor_from_url.py
```

Expected output:
```
✅ ALL TESTS PASSED
```

## Performance

- **Fetch job listing**: ~2-5 seconds
- **Extract keywords**: ~0.5 seconds
- **Tailor resume**: ~1-2 seconds
- **Generate HTML**: ~1-2 seconds
- **Export DOCX**: ~2-3 seconds

**Total time**: ~7-15 seconds (depending on options)

## Advanced Usage

### Custom Vector Store

```bash
python src/tailor_from_url.py \
  --url "https://example.com/job" \
  --resume "Master Resume" \
  --out out/tailored.html \
  --use-rag \
  --vector-store "data/rag/custom_store.json"
```

### LLM-Enhanced Rewriting

```bash
python src/tailor_from_url.py \
  --url "https://example.com/job" \
  --resume "Master Resume" \
  --out out/tailored.html \
  --use-rag \
  --use-llm-rewriting
```

Requires:
- RAG enabled (`--use-rag`)
- LLM API key configured
- Vector store populated

## Architecture

```
tailor_from_url.py
├── fetch_job_listing()      # Fetch from URL
├── ingest_jd()              # Parse job description
├── extract_keywords()       # Extract keywords
├── retrieve_rag_context()   # [Optional] RAG retrieval
├── load_resume()            # Load resume
├── select_and_rewrite()     # Tailor bullets
├── generate_html_resume()   # Generate HTML
└── generate_docx_from_html() # [Optional] Export DOCX
```

## See Also

- [Job Listing Fetcher](JOB_LISTING_FETCHER_README.md)
- [Resume Tailoring](AGENT_RESUME_TAILORING_IMPLEMENTATION.md)
- [RAG System](RAG_CAPABILITIES_ANALYSIS.md)
- [Agent Workflow](AGENT_WORKFLOW_GUIDE.md)

---

**Status**: ✅ Production Ready  
**Last Updated**: 2025-10-26

