# Resume Update Script - Complete Solution

## Overview

Created a **fully reusable, parameterized Python script** to update any resume with professional experiences. No hard-coding. Supports multiple input formats and flexible resume matching.

## Files Created

### 1. **Main Script** (`scripts/update_resume_with_experiences.py`)
The core reusable script with the following features:

- **No Hard-Coding**: Fully parameterized for any resume and experience data
- **Multiple Input Formats**: JSON and markdown support
- **Flexible Resume Matching**: Find by name, company identifier, or UUID
- **Prepend or Replace**: Add new experiences or replace all existing ones
- **Automatic Indexing**: Updates resume index with timestamps
- **Bullet Point Tags**: Support for technology tags on each bullet
- **Error Handling**: Clear error messages and validation

**Key Functions:**
- `parse_json_experiences()` - Parse JSON experience files
- `parse_markdown_experiences()` - Parse markdown experience files
- `update_resume_experiences()` - Update resume with experiences
- `main()` - CLI entry point

### 2. **Experience Data** (`data/experiences_solution_architect.json`)
Pre-populated JSON file with your 3 experiences:

- **Daugherty – Cox Communications** (Aug 2021 – Nov 2024)
  - 5 bullet points with technology tags
  
- **CGI – Daugherty / Edward Jones** (Nov 2021 – Aug 2024)
  - 5 bullet points with technology tags
  
- **BPM Software Solutions** (Jul 2017 – Nov 2021)
  - 5 bullet points with technology tags

### 3. **Documentation** (`scripts/UPDATE_RESUME_WITH_EXPERIENCES_README.md`)
Comprehensive guide including:

- Feature overview
- Installation instructions
- Usage examples
- Command-line argument reference
- Input format specifications (JSON and markdown)
- Error handling guide
- Integration notes

### 4. **Programmatic Examples** (`scripts/example_update_resume_programmatically.py`)
5 practical examples showing how to use the script from Python code:

1. Update from JSON file
2. Update from markdown file
3. Create experiences programmatically
4. Merge experiences from multiple sources
5. Filter and update experiences

## Usage

### Command Line

```bash
# Update resume with your experiences
python scripts/update_resume_with_experiences.py \
    --resume-id "141107d3-f0a9-4bc6-82dd-6fc4506e76f4" \
    --experiences-file "data/experiences_solution_architect.json"

# Update by resume name
python scripts/update_resume_with_experiences.py \
    --resume "Master Resume" \
    --experiences-file "data/experiences_solution_architect.json"

# Replace all experiences instead of prepending
python scripts/update_resume_with_experiences.py \
    --resume-id "141107d3-f0a9-4bc6-82dd-6fc4506e76f4" \
    --experiences-file "data/experiences_solution_architect.json" \
    --replace

# Use markdown format
python scripts/update_resume_with_experiences.py \
    --resume "Ford" \
    --experiences-file "experiences.md" \
    --format markdown
```

### From Python Code

```python
from scripts.update_resume_with_experiences import (
    parse_json_experiences,
    update_resume_experiences,
)
from pathlib import Path

# Load experiences
experiences = parse_json_experiences(Path("data/experiences_solution_architect.json"))

# Update resume
update_resume_experiences(
    data_dir=Path("data"),
    resume_id="141107d3-f0a9-4bc6-82dd-6fc4506e76f4",
    experiences=experiences,
    replace=False  # prepend new experiences
)
```

## Verification

The script was successfully tested with your resume:

```
Using resume ID: 141107d3-f0a9-4bc6-82dd-6fc4506e76f4

Parsing experiences from: data/experiences_solution_architect.json (format: json)
Found 3 experience entries
  1. Daugherty – Cox Communications — Platform Architect – Cloud Infrastructure & Automation (Aug 2021 – Nov 2024)
     Bullets: 5
  2. CGI – Daugherty / Edward Jones — Principal Consultant / Platform Team Delivery Lead (Nov 2021 – Aug 2024)
     Bullets: 5
  3. BPM Software Solutions — Senior Software Architect / Engineering Lead (Jul 2017 – Nov 2021)
     Bullets: 5

Updating resume...

[SUCCESS] Successfully updated resume 141107d3-f0a9-4bc6-82dd-6fc4506e76f4
   Experience entries: prepended
```

## Key Features

### 1. **Reusability**
- No hard-coded resume IDs, file paths, or experience data
- Works with any resume in the system
- Works with any experience data format

### 2. **Flexibility**
- **Input Formats**: JSON or markdown
- **Resume Matching**: UUID, name, or company identifier
- **Update Mode**: Prepend (default) or replace
- **Custom Data Directory**: Support for different data locations

### 3. **Robustness**
- Comprehensive error handling
- Clear error messages with suggestions
- Automatic index updates
- Validation of resume structure

### 4. **Integration**
- Works with existing resume system
- Compatible with CRUD operations
- Updates resume index automatically
- Maintains data consistency

## Input Format Examples

### JSON Format
```json
{
  "experiences": [
    {
      "employer": "Company Name",
      "role": "Job Title",
      "dates": "Start – End",
      "location": "City, State",
      "bullets": [
        {
          "text": "Accomplishment",
          "tags": ["Technology1", "Technology2"]
        }
      ]
    }
  ]
}
```

### Markdown Format
```markdown
### Company Name — Job Title (Start – End)

* Accomplishment bullet point 1
* Accomplishment bullet point 2

**Tags:** Technology1, Technology2
```

## Next Steps

1. **Use the script** to update any resume with experiences
2. **Create experience files** in JSON or markdown format
3. **Integrate into workflows** using the programmatic API
4. **Extend functionality** by modifying the script as needed

## Files Summary

| File | Purpose |
|------|---------|
| `scripts/update_resume_with_experiences.py` | Main reusable script |
| `data/experiences_solution_architect.json` | Your 3 experiences in JSON format |
| `scripts/UPDATE_RESUME_WITH_EXPERIENCES_README.md` | Complete documentation |
| `scripts/example_update_resume_programmatically.py` | 5 practical examples |

## Support

For detailed usage information, see:
- `scripts/UPDATE_RESUME_WITH_EXPERIENCES_README.md` - Full documentation
- `scripts/example_update_resume_programmatically.py` - Code examples
- `scripts/update_resume_with_experiences.py` - Source code with docstrings

