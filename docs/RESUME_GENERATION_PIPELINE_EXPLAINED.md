# Resume Generation Pipeline - Explained

## The Real Architecture

You're absolutely right! The resume generation pipeline uses **BOTH** sources:

1. **`data/master_resume.json`** - Base resume structure (name, contact, summary, areas of expertise)
2. **`data/experiences.json`** - Experience log with detailed bullets, skills, technologies, techniques, principles

## Data Sources

### Source 1: Master Resume (`data/master_resume.json`)

Contains the **static resume structure**:
```json
{
  "name": "Sidney Jones",
  "title": "Senior DevOps Software Engineer",
  "location": "West Bloomfield, MI",
  "email": "sjones@bpmsoftwaresolutions.com",
  "phone": "(248) 802-1847",
  "summary": "...",
  "technical_proficiencies": {...},
  "areas_of_expertise": [...],
  "experience": [
    {
      "employer": "Edward Jones",
      "role": "Senior Application Architect",
      "location": "Remote",
      "dates": "2021 - 2024",
      "bullets": [...]  // Basic bullets
    }
  ],
  "education": [...],
  "certifications": [...]
}
```

### Source 2: Experience Log (`data/experiences.json`)

Contains the **detailed experience database** with rich metadata:
```json
[
  {
    "id": "0defdac1-d9bd-457f-904a-4c0609b84c32",
    "employer": "BPM Software Solutions",
    "role": "Principle Consultant",
    "dates": "2017 – 2021",
    "location": "West Bloomfield, MI",
    "bullets": [
      "Developed secure SFTP services...",
      "Engineered Voice of Customer (VOC) AI...",
      ...
    ],
    "skills": ["SFTP", "ETL", "Paylocity", "AI", ...],
    "technologies": ["Azure", "AWS", "Docker", ...],
    "techniques": ["CI/CD", "TDD", ...],
    "principles": ["DRY", "YAGNI", ...]
  }
]
```

## Generation Pipeline

### Step 1: Load Master Resume
```python
with open('data/master_resume.json') as f:
    resume_data = json.load(f)
```

### Step 2: Load Experience Log
```python
experiences_path = Path('data/experiences.json')
if experiences_path.exists():
    with open(experiences_path) as f:
        experiences = json.load(f)
```

### Step 3: Merge Experience Log into Resume
The `generate_hybrid_resume.py` function:

1. **Extracts education entries** (id starts with 'edu-')
   ```python
   education_entries = [e for e in experiences if e.get('id', '').startswith('edu-')]
   resume_data['education'] = [...]
   ```

2. **Extracts certification entries** (id starts with 'cert-')
   ```python
   cert_entries = [e for e in experiences if e.get('id', '').startswith('cert-')]
   resume_data['certifications'] = [...]
   ```

3. **Adds tags to experience entries**
   - Matches experiences by employer + role
   - Combines skills, technologies, techniques, principles
   - Adds as tags to resume experience entries

### Step 4: Apply RAG Tailoring (Optional)
```python
if use_rag and jd_path:
    keywords = extract_keywords(jd_text)
    rag_context = retrieve_rag_context(keywords, vector_store_path)
    resume_data['experience'] = select_and_rewrite(
        resume_data['experience'],
        keywords,
        rag_context=rag_context
    )
```

### Step 5: Generate HTML
```python
generate_html_resume(resume_data, output_html_path, theme)
```

## Data Flow Diagram

```
data/master_resume.json          data/experiences.json
        ↓                                ↓
    Load resume                    Load experience log
        ↓                                ↓
        └────────────────┬───────────────┘
                         ↓
                  Merge data:
                  - Extract education (edu-*)
                  - Extract certifications (cert-*)
                  - Add tags to experiences
                         ↓
                  Merged resume data
                         ↓
              [Optional] Apply RAG tailoring
                         ↓
              select_and_rewrite() - Tailor bullets
                         ↓
              generate_html_resume() - Render HTML
                         ↓
              out/tailored_resume.html
```

## Key Functions

### `generate_hybrid_resume()` in `src/generate_hybrid_resume.py`

**Lines 62-126**: Load and merge data
- Loads master resume JSON
- Loads experience log
- Extracts education/certifications
- Adds tags to experiences

**Lines 127-160**: Apply RAG tailoring
- Extracts keywords from job description
- Retrieves RAG context
- Calls `select_and_rewrite()` to tailor bullets

**Lines 161+**: Generate HTML
- Processes resume data
- Generates HTML with CSS
- Optionally exports to DOCX

## Experience Log Structure

The experience log (`data/experiences.json`) is an array of `Experience` objects:

```python
@dataclass
class Experience:
    id: str                          # UUID
    employer: str                    # Company name
    role: str                        # Job title
    dates: str                       # Date range
    location: Optional[str]          # Location
    bullets: List[str]               # Achievement bullets
    skills: List[str]                # Skills used
    technologies: List[str]          # Tech stack
    techniques: List[str]            # Methodologies
    principles: List[str]            # Design principles
    notes: Optional[str]             # Additional notes
```

## Special Entry Types

The experience log supports special entry types via ID prefix:

| ID Prefix | Type | Purpose |
|-----------|------|---------|
| `edu-*` | Education | Degree, institution, location, year |
| `cert-*` | Certification | Cert name, issuer, date |
| (other) | Experience | Work experience with bullets |

## Tailoring Pipeline

When tailoring a resume for a job:

1. **Extract keywords** from job description
2. **Score bullets** from experience log against keywords
3. **Select top bullets** (default: 3 per job)
4. **Rewrite bullets** (optional: using LLM)
5. **Generate HTML** with tailored bullets

## Integration with `tailor_from_url.py`

The new `tailor_from_url.py` script:

1. Fetches job listing from URL
2. Extracts keywords
3. Loads resume (master_resume.json)
4. Calls `select_and_rewrite()` to tailor bullets
5. Generates HTML

**Note**: Currently uses `master_resume.json` directly. Could be enhanced to:
- Load experience log
- Use experience log bullets for tailoring
- Merge experience log data into output

## Why Two Sources?

**Master Resume** (`master_resume.json`):
- ✅ Quick resume generation
- ✅ Static structure (name, contact, summary)
- ✅ Default bullets for each job

**Experience Log** (`experiences.json`):
- ✅ Rich metadata (skills, technologies, techniques, principles)
- ✅ Reusable across multiple resumes
- ✅ Supports education/certification entries
- ✅ Enables advanced tailoring and filtering

## Current Implementation

The `generate_hybrid_resume.py` function:
- ✅ Loads both sources
- ✅ Merges education/certifications from experience log
- ✅ Adds tags from experience log to resume
- ✅ Supports RAG-based tailoring
- ✅ Generates HTML with all data

## Future Enhancement

The `tailor_from_url.py` could be enhanced to:
1. Load experience log
2. Use experience log bullets for tailoring
3. Merge experience log metadata
4. Generate more intelligent tailored resumes

## Summary

The resume generation pipeline is **dual-source**:

- **Master Resume** = Structure + base content
- **Experience Log** = Rich metadata + reusable bullets
- **Generation** = Merge both + tailor + render

This architecture enables:
- ✅ Reusable experience data
- ✅ Rich metadata for filtering/tailoring
- ✅ Multiple resume variants
- ✅ Advanced RAG-based tailoring

---

**Master Resume**: `data/master_resume.json`  
**Experience Log**: `data/experiences.json`  
**Generation Pipeline**: `src/generate_hybrid_resume.py`  
**Tailoring Pipeline**: `src/tailor.py`  
**Last Updated**: 2025-10-26

