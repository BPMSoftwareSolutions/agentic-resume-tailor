# Resume CRUD Operations

This directory contains specialized scripts for managing individual sections of resume data. Each script provides Create, Read, Update, and Delete (CRUD) operations for a specific data model.

## Overview

The CRUD scripts enable granular control over resume content through:
- **Natural language friendly**: Use resume names like "Ford" or "Master Resume" instead of UUIDs
- **Consistent interface**: All scripts follow the same command-line pattern
- **Automatic updates**: Timestamps are automatically updated in the resume index
- **Validation**: Input validation and helpful error messages
- **AI Agent integration**: Designed to work seamlessly with the AI agent

## Available Scripts

### 1. Basic Info (`basic_info.py`)
Manage name, title, location, and contact information.

```bash
# Update title
python src/crud/basic_info.py --resume "Master Resume" --update-title "Principal Software Architect"

# Update email
python src/crud/basic_info.py --resume "Ford" --update-email "new@email.com"

# Show current info
python src/crud/basic_info.py --resume "Ford" --show
```

**Operations**: `--update-name`, `--update-title`, `--update-location`, `--update-email`, `--update-phone`, `--show`

### 2. Summary (`summary.py`)
Manage resume summary text.

```bash
# Update entire summary
python src/crud/summary.py --resume "Ford" --update "New summary text..."

# Append to summary
python src/crud/summary.py --resume "Ford" --append "Additional experience with AI/ML."

# Load from file
python src/crud/summary.py --resume "Ford" --from-file "summary.txt"

# Show current summary
python src/crud/summary.py --resume "Ford" --show
```

**Operations**: `--update`, `--append`, `--from-file`, `--show`

### 3. Technical Skills (`technical_skills.py`)
Manage technical proficiencies organized by category.

```bash
# Add new category
python src/crud/technical_skills.py --resume "Ford" --add-category "security" "OAuth, JWT, SAML"

# Update category
python src/crud/technical_skills.py --resume "Ford" --update-category "cloud" "Azure, AWS, GCP"

# Append to category
python src/crud/technical_skills.py --resume "Ford" --append-to-category "languages" "Rust, Go"

# Delete category
python src/crud/technical_skills.py --resume "Ford" --delete-category "security"

# List all categories
python src/crud/technical_skills.py --resume "Ford" --list
```

**Operations**: `--add-category`, `--update-category`, `--append-to-category`, `--delete-category`, `--list`, `--show`

**Categories**: `ai`, `cloud`, `databases`, `devops`, `languages`, `opensource`, `os`, `security`

### 4. Areas of Expertise (`expertise.py`)
Manage areas of expertise (array of strings).

```bash
# Add expertise area
python src/crud/expertise.py --resume "Ford" --add "AI/ML Engineering"

# Update expertise area
python src/crud/expertise.py --resume "Ford" --update "Old Text" "New Text"

# Delete expertise area
python src/crud/expertise.py --resume "Ford" --delete "Legacy System Maintenance"

# List all expertise areas
python src/crud/expertise.py --resume "Ford" --list
```

**Operations**: `--add`, `--list`, `--update`, `--delete`, `--clear`

### 5. Achievements (`achievements.py`)
Manage achievements (array of strings).

```bash
# Add achievement
python src/crud/achievements.py --resume "Ford" --add "AWS Certified Solutions Architect"

# Delete achievement
python src/crud/achievements.py --resume "Ford" --delete "GitHub Community Contributor"

# List all achievements
python src/crud/achievements.py --resume "Ford" --list
```

**Operations**: `--add`, `--list`, `--update`, `--delete`, `--clear`

### 6. Education (`education.py`)
Manage education entries.

```bash
# Add education entry
python src/crud/education.py --resume "Ford" --add --degree "Master of Science" --institution "MIT" --location "Cambridge, MA" --year "2020"

# Update by institution
python src/crud/education.py --resume "Ford" --update --institution "MIT" --year "2021"

# Delete by institution
python src/crud/education.py --resume "Ford" --delete --institution "University of Phoenix"

# List all education
python src/crud/education.py --resume "Ford" --list
```

**Operations**: `--add`, `--list`, `--update`, `--delete`

**Fields**: `--degree`, `--institution`, `--location`, `--year`, `--index`

### 7. Certifications (`certifications.py`)
Manage certification entries.

```bash
# Add certification
python src/crud/certifications.py --resume "Ford" --add --name "AWS Solutions Architect" --issuer "Amazon" --date "Oct 2025" --credential "ABC123"

# Update by name
python src/crud/certifications.py --resume "Ford" --update --name "PSM I" --date "June 2023"

# Delete by name
python src/crud/certifications.py --resume "Ford" --delete --name "PSM I"

# List all certifications
python src/crud/certifications.py --resume "Ford" --list
```

**Operations**: `--add`, `--list`, `--update`, `--delete`

**Fields**: `--name`, `--issuer`, `--date`, `--credential`, `--index`

### 8. Experience (`experience.py`)
Manage work experience entries and bullets.

```bash
# Add experience entry
python src/crud/experience.py --resume "Ford" --add --employer "Microsoft" --role "Senior Engineer" --dates "2020-2023" --location "Remote"

# Add bullet to experience
python src/crud/experience.py --resume "Ford" --add-bullet --employer "Microsoft" --text "Led team of 10 engineers" --tags "Leadership,Management"

# Update bullet
python src/crud/experience.py --resume "Ford" --update-bullet --employer "Microsoft" --index 0 --text "New bullet text"

# Delete bullet
python src/crud/experience.py --resume "Ford" --delete-bullet --employer "Microsoft" --index 0

# Delete experience entry
python src/crud/experience.py --resume "Ford" --delete --employer "Microsoft"

# List all experience
python src/crud/experience.py --resume "Ford" --list

# Import from markdown
python src/crud/experience.py --resume "Ford" --from-markdown "experience.md" --replace
```

**Operations**: `--add`, `--add-bullet`, `--update-bullet`, `--delete-bullet`, `--delete`, `--list`, `--from-markdown`

**Fields**: `--employer`, `--role`, `--dates`, `--location`, `--text`, `--tags`, `--index`, `--replace`

## Common Options

All scripts support these common options:

- `--resume "Name"`: Find resume by name (e.g., "Ford", "Master Resume")
- `--resume-id "UUID"`: Use resume UUID directly
- `--data-dir "path"`: Specify data directory (default: "data")

## Resume Identification

Scripts can find resumes by:
1. **Name matching**: Partial, case-insensitive matching against resume names in `data/resumes/index.json`
2. **UUID**: Direct UUID lookup

Examples:
- `--resume "Ford"` finds "Sidney_Jones_Senior_Software_Engineer_Ford"
- `--resume "Master Resume"` finds "Master Resume"
- `--resume-id "b3013a2a-349a-4080-802c-3bbe6714b576"` uses UUID directly

## Error Handling

All scripts use consistent exit codes:
- `0`: Success
- `1`: General error
- `2`: Resume not found
- `3`: Invalid data or operation failed

Error messages are printed to stderr with `[ERROR]` prefix.

## Natural Language Integration

These scripts are designed to work with the AI agent. The agent can translate natural language commands into script calls:

**User**: "Add Python to my technical skills"
**Agent**: `run: python src/crud/technical_skills.py --resume "Master Resume" --append-to-category "languages" "Python"`

**User**: "Update my title to Principal Architect"
**Agent**: `run: python src/crud/basic_info.py --resume "Master Resume" --update-title "Principal Architect"`

**User**: "List my certifications"
**Agent**: `run: python src/crud/certifications.py --resume "Master Resume" --list"`

## Shared Utilities

The `__init__.py` module provides shared functions used by all CRUD scripts:

- `load_resume_index()`: Load resume index
- `save_resume_index()`: Save resume index
- `find_resume_by_identifier()`: Find resume by name
- `load_resume()`: Load resume data
- `save_resume()`: Save resume data and update timestamp
- `validate_resume_structure()`: Validate resume structure
- `get_resume_by_identifier()`: Convenience function to find and load resume

## Development

### Adding New CRUD Scripts

To add a new CRUD script:

1. Create new file in `src/crud/`
2. Import shared utilities from `crud` module
3. Implement CRUD functions for the data model
4. Add command-line interface with argparse
5. Follow existing patterns for consistency
6. Update `agent_knowledge_base.json` with new operations
7. Update `agent.py` system prompt with command patterns
8. Add to whitelist in `src/api/app.py`

### Testing

Test scripts manually:
```bash
python src/crud/expertise.py --resume "Master Resume" --list
python src/crud/basic_info.py --resume "Master Resume" --show
```

## Related Documentation

- [Agent Knowledge Base](../../agent_knowledge_base.json) - Complete CRUD operations reference
- [Agent System Prompt](../../agent.py) - Natural language command patterns
- [API Whitelist](../api/app.py) - Security configuration

## Related Issues

- [#17](https://github.com/BPMSoftwareSolutions/agentic-resume-tailor/issues/17) - Create CRUD Scripts for All Resume Data Models

