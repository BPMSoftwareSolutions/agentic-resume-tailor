# Quick Start Guide - Update Resume with Experiences

## 30-Second Setup

```bash
# Update your resume with the provided experiences
python scripts/update_resume_with_experiences.py \
    --resume-id "141107d3-f0a9-4bc6-82dd-6fc4506e76f4" \
    --experiences-file "data/experiences_solution_architect.json"
```

Done! Your resume now has 3 new experiences prepended.

## Common Commands

### Update by Resume UUID
```bash
python scripts/update_resume_with_experiences.py \
    --resume-id "141107d3-f0a9-4bc6-82dd-6fc4506e76f4" \
    --experiences-file "data/experiences_solution_architect.json"
```

### Update by Resume Name
```bash
python scripts/update_resume_with_experiences.py \
    --resume "Master Resume" \
    --experiences-file "data/experiences_solution_architect.json"
```

### Replace All Experiences
```bash
python scripts/update_resume_with_experiences.py \
    --resume-id "141107d3-f0a9-4bc6-82dd-6fc4506e76f4" \
    --experiences-file "data/experiences_solution_architect.json" \
    --replace
```

### Use Markdown Format
```bash
python scripts/update_resume_with_experiences.py \
    --resume "Ford" \
    --experiences-file "experiences.md" \
    --format markdown
```

## Create Your Own Experience File

### JSON Format
```json
{
  "experiences": [
    {
      "employer": "Company Name",
      "role": "Job Title",
      "dates": "Aug 2021 – Nov 2024",
      "location": "City, State",
      "bullets": [
        {
          "text": "Accomplishment bullet point",
          "tags": ["Technology1", "Technology2"]
        }
      ]
    }
  ]
}
```

### Markdown Format
```markdown
### Company Name — Job Title (Aug 2021 – Nov 2024)

* Accomplishment bullet point 1
* Accomplishment bullet point 2

**Tags:** Technology1, Technology2
```

## What Gets Updated

✅ Experience entries added to resume  
✅ Bullet points with technology tags  
✅ Resume index updated with new timestamp  
✅ Automatic backup created (if using API)  

## Prepend vs Replace

**Default (Prepend):**
```
New experiences added to TOP of resume
[New Experience 1]
[New Experience 2]
[Existing Experience 1]
[Existing Experience 2]
```

**With --replace:**
```
All existing experiences replaced
[New Experience 1]
[New Experience 2]
```

## Find Your Resume ID

```bash
# List all resumes
python -c "import json; data = json.load(open('data/resumes/index.json')); [print(f\"{r['name']}: {r['id']}\") for r in data['resumes']]"
```

## Troubleshooting

### "Resume not found"
Use `--resume-id` with the UUID instead of `--resume`

### "File not found"
Check the path to your experiences file is correct

### "Invalid JSON"
Validate your JSON file using an online JSON validator

### "Markdown parsing failed"
Ensure headers follow format: `### Company — Role (Dates)`

## Next Steps

1. **Create your experience file** (JSON or markdown)
2. **Run the script** with your resume ID
3. **Verify** the resume was updated in the web UI
4. **Repeat** for other resumes as needed

## Full Documentation

See `scripts/UPDATE_RESUME_WITH_EXPERIENCES_README.md` for complete documentation.

## Examples

See `scripts/example_update_resume_programmatically.py` for 5 practical examples.

