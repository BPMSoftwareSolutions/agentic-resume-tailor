# Experience Log as Source of Truth

## Overview

The **experience log** (`data/experiences.json`) is now the **primary source of truth** for all resume data. The old `master_resume.json` is deprecated.

## Architecture

### Old Architecture (Deprecated)
```
master_resume.json (outdated)
        ↓
generate_hybrid_resume.py
        ↓
HTML output
```

### New Architecture (Current)
```
experiences.json (source of truth)
        ↓
build_resume_from_experience_log.py
        ↓
Resume data structure
        ↓
generate_html_resume() or tailor_from_url()
        ↓
HTML output
```

## Experience Log Structure

The experience log (`data/experiences.json`) is an array of experience entries:

```json
[
  {
    "id": "uuid",
    "employer": "Company Name",
    "role": "Job Title",
    "dates": "2017 – 2021",
    "location": "City, State",
    "bullets": ["Achievement 1", "Achievement 2", ...],
    "skills": ["Skill1", "Skill2", ...],
    "technologies": ["Tech1", "Tech2", ...],
    "techniques": ["Technique1", ...],
    "principles": ["Principle1", ...],
    "notes": "Optional notes"
  }
]
```

### Special Entry Types

| ID Prefix | Type | Purpose |
|-----------|------|---------|
| `edu-*` | Education | Degree, institution, location, year |
| `cert-*` | Certification | Cert name, issuer, date |
| (other) | Experience | Work experience with bullets |

## New Functions

### `build_resume_from_experience_log()`

**Location**: `src/build_resume_from_experience_log.py`

Builds a complete resume from the experience log:

```python
from src.build_resume_from_experience_log import build_resume_from_experience_log

# Build resume from experience log
resume = build_resume_from_experience_log(
    experience_log_path="data/experiences.json",
    personal_info={
        "name": "Sidney Jones",
        "email": "sjones@example.com",
        ...
    }
)

# Resume structure:
{
    "name": "Sidney Jones",
    "title": "Senior DevOps Software Engineer",
    "location": "West Bloomfield, MI",
    "email": "sjones@bpmsoftwaresolutions.com",
    "phone": "(248) 802-1847",
    "summary": "...",
    "experience": [...],
    "education": [...],
    "certifications": [...],
    "technical_proficiencies": {...},
    "areas_of_expertise": [...]
}
```

**What it does:**
1. Loads experience log
2. Separates entries by type (experience, education, certification)
3. Extracts education entries (id: `edu-*`)
4. Extracts certification entries (id: `cert-*`)
5. Combines skills, technologies, techniques, principles into tags
6. Builds complete resume structure

## Updated `tailor_from_url.py`

The `tailor_from_url.py` script now uses the experience log:

### Old Usage (Deprecated)
```bash
python src/tailor_from_url.py \
  --url "https://example.com/job" \
  --resume "Master Resume" \
  --out out/tailored.html
```

### New Usage (Current)
```bash
python src/tailor_from_url.py \
  --url "https://example.com/job" \
  --out out/tailored.html
```

### With Options
```bash
# With DOCX export
python src/tailor_from_url.py \
  --url "https://example.com/job" \
  --out out/tailored.html \
  --docx

# With RAG enhancement
python src/tailor_from_url.py \
  --url "https://example.com/job" \
  --out out/tailored.html \
  --use-rag \
  --theme modern

# With custom experience log
python src/tailor_from_url.py \
  --url "https://example.com/job" \
  --out out/tailored.html \
  --experience-log data/experiences.json
```

## Workflow

### Step-by-Step

1. **Fetch job listing** from URL
2. **Parse job description** and extract keywords
3. **Build resume** from experience log
4. **Tailor resume** to job (score and select bullets)
5. **Generate HTML** with tailored bullets
6. **Export DOCX** (optional)

### Code Flow

```python
# 1. Fetch job listing
jd_filepath = fetch_job_listing(url)

# 2. Parse and extract keywords
jd_path, jd_text = ingest_jd(jd_filepath)
keywords = extract_keywords(jd_text)

# 3. Build resume from experience log
resume_data = build_resume_from_experience_log(experience_log_path)

# 4. Tailor resume
resume_data["experience"] = select_and_rewrite(
    resume_data["experience"],
    keywords,
    rag_context=rag_context
)

# 5. Generate HTML
generate_html_resume(resume_data, output_path, theme)

# 6. Export DOCX (optional)
if export_docx:
    generate_docx_from_html(output_path)
```

## Benefits

✅ **Single Source of Truth** - Experience log is the only source
✅ **No Duplication** - No need to maintain master_resume.json
✅ **Rich Metadata** - Skills, technologies, techniques, principles
✅ **Reusable Data** - Experience entries can be used across multiple resumes
✅ **Easy Maintenance** - Update experience log, all resumes update automatically
✅ **Better Tailoring** - More data available for keyword matching

## Migration

### From Old System

If you were using `master_resume.json`:

1. **Import experience data** into `data/experiences.json`
   ```bash
   python scripts/import_resumes_to_experience_log.py
   ```

2. **Build resume** from experience log
   ```bash
   python src/build_resume_from_experience_log.py
   ```

3. **Use new tailor_from_url.py**
   ```bash
   python src/tailor_from_url.py --url "..." --out "..."
   ```

## Files

### Core Files
- **`data/experiences.json`** - Experience log (source of truth)
- **`src/build_resume_from_experience_log.py`** - Build resume from experience log
- **`src/tailor_from_url.py`** - Tailor resume from URL (updated)

### Deprecated Files
- **`data/master_resume.json`** - Old, outdated (no longer used)

## Testing

Run the integration test:
```bash
python scripts/test_tailor_from_url.py
```

Build resume from experience log:
```bash
python src/build_resume_from_experience_log.py
```

## Summary

The **experience log** is now the **source of truth** for all resume data:

- ✅ Single source of truth
- ✅ Rich metadata (skills, technologies, techniques, principles)
- ✅ Support for education and certifications
- ✅ Reusable across multiple resumes
- ✅ Better tailoring capabilities

**No more confusion** - use the experience log for everything!

---

**Source of Truth**: `data/experiences.json`  
**Build Function**: `src/build_resume_from_experience_log.py`  
**Tailoring Script**: `src/tailor_from_url.py`  
**Last Updated**: 2025-10-26

