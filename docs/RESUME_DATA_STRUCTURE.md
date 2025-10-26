# Resume Data Structure - JSON to HTML

## Overview

The resume system uses a **two-layer architecture**:

1. **JSON Source** - Master resume data stored as JSON
2. **HTML Rendering** - Rendered HTML with semantic data attributes

## JSON Source Data

**Location**: `data/master_resume.json`

This is the **source of truth** for all resume data. It contains:

```json
{
  "name": "Sidney Jones",
  "title": "Senior DevOps Software Engineer",
  "location": "West Bloomfield, MI",
  "email": "sjones@bpmsoftwaresolutions.com",
  "phone": "(248) 802-1847",
  "summary": "...",
  "technical_proficiencies": {
    "ai": "...",
    "cloud": "...",
    "databases": "...",
    "devops": "...",
    "languages": "...",
    "opensource": "...",
    "os": "...",
    "security": "..."
  },
  "areas_of_expertise": [
    "Enterprise Architecture & Cloud Transformation",
    "Revenue Growth & Cost Optimization",
    ...
  ],
  "experience": [
    {
      "employer": "Edward Jones",
      "role": "Senior Application Architect",
      "location": "Remote",
      "dates": "2021 - 2024",
      "bullets": [
        "Spearheaded transformation of Online Access platform...",
        "Bolstered team capabilities...",
        ...
      ]
    },
    ...
  ],
  "education": [
    {
      "degree": "Bachelor of Technology",
      "institution": "University of Phoenix",
      "location": "Troy, MI"
    },
    ...
  ],
  "certifications": [
    {
      "name": "SAFe 5 Certified DevOps Practitioner",
      "issuer": "SAFe by Scaled Agile, Inc.",
      "date": "Jan 2023"
    },
    ...
  ]
}
```

## HTML Rendering

**Location**: `out/test_tailored_resume.html` (and other generated files)

The HTML file is a **rendered version** of the JSON data with:

### Semantic Data Attributes

Each HTML element includes `data-*` attributes for structure:

```html
<!-- Personal Info -->
<div class="personal-info" data-section="personal_info">
  <h1 data-field="name">Sidney Jones</h1>
  <div class="title" data-field="title">Senior DevOps Software Engineer</div>
</div>

<!-- Skills Section -->
<section class="section" data-section="skills">
  <div class="skill-category" data-category="ai">
    <div class="skill-label">AI:</div>
    <div class="skill-value">Large Language Models (LLMs)...</div>
  </div>
</section>

<!-- Experience Section -->
<div class="experience-item" data-position="0" data-company="edward_jones">
  <div class="employer" data-field="employer">Edward Jones</div>
  <div class="role" data-field="role">Senior Application Architect</div>
  <div class="bullet-item" data-bullet="0">
    <div class="bullet-text">Spearheaded transformation...</div>
  </div>
</div>

<!-- Education Section -->
<div class="education-item" data-position="0">
  <div class="degree" data-field="degree">Bachelor of Technology</div>
  <div class="institution" data-field="institution">University of Phoenix</div>
</div>

<!-- Certifications Section -->
<div class="certification-item" data-position="0">
  SAFe 5 Certified DevOps Practitioner (SAFe by Scaled Agile, Inc., Jan 2023)
</div>
```

### Data Attributes Reference

| Attribute | Purpose | Example |
|-----------|---------|---------|
| `data-section` | Identifies major sections | `data-section="experience"` |
| `data-field` | Identifies specific fields | `data-field="name"` |
| `data-category` | Skill category | `data-category="ai"` |
| `data-position` | Item position in list | `data-position="0"` |
| `data-company` | Company identifier | `data-company="edward_jones"` |
| `data-bullet` | Bullet point index | `data-bullet="0"` |
| `data-item` | Generic item index | `data-item="0"` |

## Data Flow

```
data/master_resume.json
        ↓
    load_resume()
        ↓
    Resume data (Python dict)
        ↓
    select_and_rewrite()
    (Tailor bullets to job)
        ↓
    Modified resume data
        ↓
    generate_html_resume()
        ↓
    HTML with data attributes
        ↓
    out/tailored_resume.html
```

## Extracting Data from HTML

### Using Data Attributes (JavaScript)

```javascript
// Get all experience items
const experiences = document.querySelectorAll('[data-section="experience"] .experience-item');

// Get specific field
const name = document.querySelector('[data-field="name"]').textContent;

// Get all skills in a category
const aiSkills = document.querySelector('[data-category="ai"] .skill-value').textContent;

// Get all bullets for a position
const bullets = document.querySelectorAll('[data-position="0"] .bullet-text');
```

### Using Python

```python
from bs4 import BeautifulSoup

with open('out/test_tailored_resume.html') as f:
    soup = BeautifulSoup(f, 'html.parser')

# Get name
name = soup.find(attrs={'data-field': 'name'}).text

# Get all experience items
experiences = soup.find_all(attrs={'data-section': 'experience'})

# Get all bullets
bullets = soup.find_all(attrs={'data-bullet': True})
```

## JSON to HTML Conversion

The `generate_html_resume()` function in `src/generate_hybrid_resume.py`:

1. **Reads JSON data** from resume file
2. **Iterates through sections** (personal info, skills, experience, education, certifications)
3. **Renders HTML** with semantic data attributes
4. **Embeds CSS** for styling
5. **Outputs HTML file** with all data preserved

## Tailored Resume Data

When you use `tailor_from_url.py`:

1. **Loads JSON** from `data/master_resume.json`
2. **Extracts keywords** from job description
3. **Scores bullets** using keyword matching
4. **Reorders bullets** by relevance score
5. **Modifies experience** section in JSON
6. **Generates HTML** with tailored bullets
7. **Saves HTML** to output file

The **JSON data is modified** before HTML generation, so the tailored resume reflects the job-specific changes.

## Accessing Resume Data

### Option 1: Use JSON Directly
```python
import json

with open('data/master_resume.json') as f:
    resume = json.load(f)

print(resume['name'])
print(resume['experience'][0]['bullets'])
```

### Option 2: Parse HTML with Data Attributes
```python
from bs4 import BeautifulSoup

with open('out/test_tailored_resume.html') as f:
    soup = BeautifulSoup(f, 'html.parser')

name = soup.find(attrs={'data-field': 'name'}).text
```

### Option 3: Use Tailor API
```python
from src.tailor import load_resume

resume = load_resume('data/master_resume.json')
print(resume['name'])
print(resume['experience'])
```

## Summary

- **JSON** = Source data (structured, machine-readable)
- **HTML** = Rendered output (human-readable, styled)
- **Data attributes** = Bridge between JSON and HTML
- **Tailoring** = Modifies JSON before HTML generation
- **Output** = HTML file with semantic structure

The HTML file contains **all the resume data** in semantic HTML elements with data attributes, making it easy to extract, parse, or re-render the data.

---

**Source**: `data/master_resume.json`  
**Rendered**: `out/test_tailored_resume.html`  
**Last Updated**: 2025-10-26

