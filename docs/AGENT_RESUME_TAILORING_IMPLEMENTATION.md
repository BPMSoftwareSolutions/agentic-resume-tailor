# Agent-Driven Resume Tailoring Implementation

**Issue:** [#10 - Agent-Driven Resume Tailoring from Job Posting + Local Resume](https://github.com/BPMSoftwareSolutions/agentic-resume-tailor/issues/10)

**Pull Request:** [#11](https://github.com/BPMSoftwareSolutions/agentic-resume-tailor/pull/11)

**Branch:** `feat/#10-agent-resume-tailoring`

---

## Summary

Implemented a complete agent-driven resume tailoring pipeline that accepts job postings (URLs or local files) and automatically:

1. Parses the job description
2. Extracts keywords
3. Scores and selects top bullets per role
4. Rewrites bullets in STAR/impact style
5. Generates HTML/DOCX export artifacts
6. Provides JD analysis summary

---

## Implementation Details

### 1. JD Ingestion Module (`src/jd_fetcher.py`)

**Purpose:** Fetch and process job descriptions from various sources.

**Features:**
- ✅ Load JD from local files (.md, .txt)
- ✅ Download JD from URLs (Indeed, LinkedIn, etc.)
- ✅ HTML text extraction with script/style filtering
- ✅ Automatic slug generation for filenames
- ✅ Save to `data/job_listings/` directory

**Key Functions:**
- `is_url(path)` - Detect if input is URL or local path
- `generate_slug(url)` - Create filename-safe slug from URL
- `fetch_from_url(url)` - Download and extract text from HTML
- `load_from_file(path)` - Load from local file
- `ingest_jd(source)` - Main entry point for JD ingestion

**Example Usage:**
```python
from jd_fetcher import ingest_jd

# From local file
file_path, content = ingest_jd("data/job_listings/job.md")

# From URL (future)
file_path, content = ingest_jd("https://example.com/job-posting")
```

---

### 2. Enhanced Tailor Pipeline (`src/tailor.py`)

**New Features:**

#### a) JD Ingestion Integration
- Automatically detects URLs vs local files
- Downloads and saves JDs when needed
- Seamless integration with existing pipeline

#### b) DOCX Export Flag
- Added `--docx` flag for automatic DOCX generation
- Uses existing `DOCXResumeExporter` infrastructure
- Only works with HTML format (warns if used with markdown)

#### c) JD Summary Generation
- Extracts top 12 keywords from job description
- Generates natural language summary of role emphasis
- Displays in formatted output after generation

**New CLI Arguments:**
```
--docx              Also generate DOCX file (only works with HTML format)
```

**Enhanced Output:**
```
📋 Processing job description...
🔍 Extracting keywords...
📝 Tailoring resume...
🎨 Generating HTML resume with 'professional' theme...
✅ Tailored HTML resume written to out/resume.html
📄 Generating DOCX from HTML...
✅ DOCX resume written to out/resume.docx

============================================================
📊 JOB DESCRIPTION ANALYSIS
============================================================

🎯 Top Keywords (12):
   microservices, data science, javascript, typescript, mentoring, 
   security, testing, docker, python, react, agile, java

💡 Summary:
   This role emphasizes microservices, data science, javascript, 
   typescript, mentoring, security, and testing, docker, python, 
   react, agile, java

============================================================
```

---

### 3. Agent Enhancement (`agent.py`)

**New System Prompt:**
- Recognizes resume tailoring intents
- Provides guidance on command syntax
- Lists available themes and options
- Helps users construct proper commands

**Detected Intent Phrases:**
- "tailor my resume"
- "fit my resume to this job"
- "customize resume for"
- "adapt my resume"
- "optimize resume for this position"

**Example Interaction:**
```
User: "Tailor my resume for this job"

Agent: "I can help you tailor your resume! I'll need:
1. Job description file path or URL
2. Your resume JSON file path
3. Output format (HTML or markdown)
4. Theme (if HTML): professional, modern, executive, creative
5. Whether you want DOCX export

Example command:
run: python src/tailor.py --resume data/master_resume.json --jd "data/job_listings/job.md" --out out/tailored.html --format html --theme professional --docx
```

---

## Testing

### New Test Files

#### 1. `tests/test_jd_fetcher.py` (18 tests)
- URL detection and validation
- Slug generation from URLs
- HTML text extraction
- File loading and saving
- JD ingestion from various sources

#### 2. `tests/test_tailor_enhancements.py` (8 tests)
- JD summary generation
- DOCX export functionality
- Integration tests for tailoring pipeline
- Keyword extraction and bullet scoring

### Test Results
```
============================== test session starts ==============================
...
============================== 204 passed in 2.47s ==============================
```

**All 204 tests pass** ✅

---

## Usage Examples

### 1. Markdown Output
```powershell
python src/tailor.py \
  --resume data/master_resume.json \
  --jd "data/job_listings/Sr. Software Engineer - at Credibly.md" \
  --out out/credibly_tailored.md \
  --format markdown
```

### 2. HTML with Professional Theme
```powershell
python src/tailor.py \
  --resume data/master_resume.json \
  --jd "data/job_listings/Sr. Software Engineer - at Credibly.md" \
  --out out/credibly_tailored.html \
  --format html \
  --theme professional
```

### 3. HTML + DOCX Export
```powershell
python src/tailor.py \
  --resume data/master_resume.json \
  --jd "data/job_listings/Sr. Software Engineer - at Credibly.md" \
  --out out/credibly_tailored.html \
  --format html \
  --theme professional \
  --docx
```

### 4. All Available Themes
- `professional` - Clean, traditional layout
- `modern` - Contemporary design with accent colors
- `executive` - Bold, leadership-focused
- `creative` - Unique, standout design

---

## End-to-End Testing

### Test Case: Credibly Senior Software Engineer

**Input:**
- Resume: `data/resumes/a041bd2e-d54b-488f-adda-e4c707d5332d.json`
- JD: `data/job_listings/Sr. Software Engineer - at Credibly.md`

**Command:**
```powershell
python src/tailor.py \
  --resume "data/resumes/a041bd2e-d54b-488f-adda-e4c707d5332d.json" \
  --jd "data/job_listings/Sr. Software Engineer - at Credibly.md" \
  --out "out/credibly_tailored_test.html" \
  --format html \
  --theme professional \
  --docx
```

**Results:**
- ✅ HTML resume generated: `out/credibly_tailored_test.html` (37,667 bytes)
- ✅ DOCX resume generated: `out/credibly_tailored_test.docx` (41,235 bytes)
- ✅ Keywords extracted: microservices, data science, javascript, typescript, mentoring, security, testing, docker, python, react, agile, java
- ✅ JD summary generated
- ✅ Bullets scored and rewritten for impact

---

## Acceptance Criteria

All acceptance criteria from issue #10 have been met:

- [x] Agent recognizes tailoring intent from natural language and/or a `tailor:` command
- [x] Given a JD file + resume JSON, pipeline produces:
  - [x] Tailored Markdown **or** HTML in `out/`
  - [x] (Optional) DOCX when pandoc/python-docx present
- [x] Tailored bullets are **scored** against JD keywords and **rewritten** for impact
- [x] Agent prints detected **top keywords** and a brief JD-fit summary
- [x] Works with the provided resume JSON structure (name, summary, experience, skills, etc.)

---

## Files Changed

1. **New Files:**
   - `src/jd_fetcher.py` - JD ingestion module
   - `tests/test_jd_fetcher.py` - JD fetcher tests
   - `tests/test_tailor_enhancements.py` - Tailor enhancement tests
   - `agent.py` - Local AI agent (from issue #8, enhanced for #10)
   - `data/job_listings/index.json` - Job listings index
   - `data/resumes/index.json` - Resumes index

2. **Modified Files:**
   - `src/tailor.py` - Enhanced with DOCX export, JD ingestion, summary generation

**Total Changes:**
- +1,172 lines added
- -9 lines removed
- 7 files changed

---

## Future Enhancements

1. **URL Fetching Improvements:**
   - Better handling of JavaScript-rendered pages
   - Support for more job board formats
   - Rate limiting and caching

2. **Multi-JD Comparison:**
   - Compare multiple job descriptions
   - Generate role-specific variants in one run
   - Identify common vs unique requirements

3. **Cover Letter Generator:**
   - Reuse JD keywords + resume highlights
   - Generate tailored cover letters
   - Multiple templates

4. **RAG Integration:**
   - Learn from prior applications
   - Refine keyword weighting per employer
   - Track application success rates

---

## Related Documentation

- [Issue #10](https://github.com/BPMSoftwareSolutions/agentic-resume-tailor/issues/10)
- [Pull Request #11](https://github.com/BPMSoftwareSolutions/agentic-resume-tailor/pull/11)
- [Local AI Agent Documentation](docs/LOCAL_AI_AGENT.md)
- [Hybrid HTML Resume Generation](docs/HYBRID_HTML_RESUME_GENERATION.md)

---

**Implementation Date:** October 12, 2025

**Status:** ✅ Complete - PR #11 Created and Awaiting Review

