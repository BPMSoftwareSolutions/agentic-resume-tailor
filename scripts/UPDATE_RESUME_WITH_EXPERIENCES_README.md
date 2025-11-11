# Update Resume with Experiences Script

A flexible, reusable Python script to update any resume with new professional experiences. Supports multiple input formats (JSON, markdown) and can prepend or replace existing experiences.

## Features

✅ **No Hard-Coding** - Fully parameterized for any resume and experience data  
✅ **Multiple Formats** - Support for JSON and markdown input files  
✅ **Flexible Matching** - Find resumes by name, company identifier, or UUID  
✅ **Prepend or Replace** - Add new experiences or replace all existing ones  
✅ **Automatic Indexing** - Updates resume index with new timestamps  
✅ **Bullet Point Tags** - Support for technology tags on each bullet point  
✅ **Error Handling** - Clear error messages and validation  

## Installation

No additional dependencies required. Uses only Python standard library.

## Usage

### Basic Usage

```bash
# Update resume by UUID with JSON experiences
python scripts/update_resume_with_experiences.py \
    --resume-id "141107d3-f0a9-4bc6-82dd-6fc4506e76f4" \
    --experiences-file "data/experiences_solution_architect.json"

# Update resume by name with markdown experiences
python scripts/update_resume_with_experiences.py \
    --resume "Master Resume" \
    --experiences-file "experiences.md" \
    --format markdown

# Replace all experiences instead of prepending
python scripts/update_resume_with_experiences.py \
    --resume "Ford" \
    --experiences-file "experiences.json" \
    --replace

# Use custom data directory
python scripts/update_resume_with_experiences.py \
    --resume-id "141107d3-f0a9-4bc6-82dd-6fc4506e76f4" \
    --experiences-file "experiences.json" \
    --data-dir "custom/data/path"
```

## Command-Line Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--resume` | No* | Resume name or company identifier (e.g., "Ford", "Master Resume") |
| `--resume-id` | No* | Resume UUID (alternative to `--resume`) |
| `--experiences-file` | Yes | Path to experiences file (JSON or markdown) |
| `--format` | No | File format: `json` (default) or `markdown` |
| `--replace` | No | Replace all experiences (default: prepend new ones) |
| `--data-dir` | No | Data directory path (default: `data`) |

*Either `--resume` or `--resume-id` must be provided.

## Input Formats

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
          "text": "Accomplishment bullet point",
          "tags": ["Technology1", "Technology2"]
        },
        {
          "text": "Another accomplishment",
          "tags": []
        }
      ]
    }
  ]
}
```

Or directly as an array:

```json
[
  {
    "employer": "Company Name",
    "role": "Job Title",
    ...
  }
]
```

### Markdown Format

```markdown
### Company Name — Job Title (Start – End)

* Accomplishment bullet point 1
* Accomplishment bullet point 2

**Tags:** Technology1, Technology2

### Another Company — Another Role (Start – End)

* Bullet point
```

## Examples

### Example 1: Update with Solution Architect Experiences

```bash
python scripts/update_resume_with_experiences.py \
    --resume-id "141107d3-f0a9-4bc6-82dd-6fc4506e76f4" \
    --experiences-file "data/experiences_solution_architect.json"
```

This prepends 3 new experiences (Daugherty, CGI, BPM) to the resume.

### Example 2: Replace All Experiences

```bash
python scripts/update_resume_with_experiences.py \
    --resume "Master Resume" \
    --experiences-file "experiences.json" \
    --replace
```

This replaces all existing experiences with the new ones from the file.

### Example 3: Find Resume by Name

```bash
python scripts/update_resume_with_experiences.py \
    --resume "Ford" \
    --experiences-file "ford_experiences.md" \
    --format markdown
```

The script will search for a resume with "Ford" in its name and update it.

## Output

The script provides clear feedback:

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

## Error Handling

The script provides helpful error messages:

- **Resume not found**: Lists all available resumes with their IDs
- **File not found**: Specifies which file is missing
- **Invalid format**: Explains expected JSON/markdown structure
- **Parsing errors**: Shows which line failed to parse

## Integration with Other Tools

This script works seamlessly with:

- **Resume Editor Web UI** - Updates are reflected immediately
- **CRUD Operations** - Compatible with existing CRUD scripts
- **Resume Index** - Automatically updates timestamps
- **Backup System** - Works with existing backup mechanisms

## Notes

- **Prepend vs Replace**: By default, new experiences are prepended (added to the top). Use `--replace` to replace all existing experiences.
- **Tags**: Technology tags are optional but recommended for better resume tailoring.
- **Dates Format**: Use consistent date formats (e.g., "Aug 2021 – Nov 2024" or "2021-2024").
- **Location**: Location field is optional in markdown format (defaults to empty string).

## Troubleshooting

### Resume not found
Make sure the resume name matches exactly (case-insensitive). Use `--resume-id` with the UUID if unsure.

### File not found
Verify the path to the experiences file is correct and relative to the current working directory.

### Invalid JSON
Ensure the JSON file is valid. Use a JSON validator if needed.

### Markdown parsing issues
Check that headers follow the format: `### Company — Role (Dates)`

## See Also

- `src/crud/experience.py` - Individual experience CRUD operations
- `src/update_resume_experience.py` - Legacy markdown-only update script
- `src/api/app.py` - REST API for resume updates

