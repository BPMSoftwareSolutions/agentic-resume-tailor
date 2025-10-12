# Resume CRUD Operations Guide

Complete guide to managing resume data using CRUD (Create, Read, Update, Delete) operations.

## Table of Contents

- [Overview](#overview)
- [Getting Started](#getting-started)
- [Natural Language Commands](#natural-language-commands)
- [Script Reference](#script-reference)
- [Common Use Cases](#common-use-cases)
- [Troubleshooting](#troubleshooting)

## Overview

The Resume CRUD system provides granular control over every section of your resume through specialized command-line scripts. Instead of manually editing JSON files, you can use simple commands to update your resume data.

### Key Benefits

- **Natural Language Friendly**: Use resume names like "Ford" instead of UUIDs
- **AI Agent Integration**: Works seamlessly with the AI agent for voice-like commands
- **Automatic Updates**: Timestamps and indexes are automatically maintained
- **Data Validation**: Built-in validation prevents errors
- **Consistent Interface**: All scripts follow the same patterns

### Architecture

```
src/crud/
├── __init__.py              # Shared utilities
├── basic_info.py            # Name, title, location, contact
├── summary.py               # Resume summary text
├── technical_skills.py      # Technical proficiencies by category
├── expertise.py             # Areas of expertise
├── achievements.py          # Achievements
├── education.py             # Education entries
├── certifications.py        # Certification entries
└── experience.py            # Work experience and bullets
```

## Getting Started

### Prerequisites

- Python 3.8+
- Resume data in `data/resumes/` directory
- Resume index at `data/resumes/index.json`

### Basic Usage Pattern

All CRUD scripts follow this pattern:

```bash
python src/crud/{script}.py --resume "{resume_name}" {operation} {parameters}
```

**Example:**
```bash
python src/crud/expertise.py --resume "Master Resume" --list
```

### Finding Your Resume

Scripts can find resumes by name (case-insensitive, partial match):

```bash
# These all work:
--resume "Master Resume"
--resume "master"
--resume "Ford"
--resume "Sidney_Jones_Senior_Software_Engineer_Ford"

# Or use UUID directly:
--resume-id "b3013a2a-349a-4080-802c-3bbe6714b576"
```

## Natural Language Commands

The AI agent can translate natural language into CRUD commands:

### Basic Info

| Natural Language | Command |
|-----------------|---------|
| "Update my title to Principal Architect" | `python src/crud/basic_info.py --resume "Master Resume" --update-title "Principal Architect"` |
| "Change my email to new@email.com" | `python src/crud/basic_info.py --resume "Master Resume" --update-email "new@email.com"` |
| "Show my contact information" | `python src/crud/basic_info.py --resume "Master Resume" --show` |

### Technical Skills

| Natural Language | Command |
|-----------------|---------|
| "Add Python to my programming languages" | `python src/crud/technical_skills.py --resume "Master Resume" --append-to-category "languages" "Python"` |
| "Update my cloud skills to include GCP" | `python src/crud/technical_skills.py --resume "Master Resume" --append-to-category "cloud" "GCP"` |
| "List my technical skills" | `python src/crud/technical_skills.py --resume "Master Resume" --list` |

### Expertise

| Natural Language | Command |
|-----------------|---------|
| "Add AI/ML Engineering to my expertise" | `python src/crud/expertise.py --resume "Master Resume" --add "AI/ML Engineering"` |
| "Remove Legacy Systems from my expertise" | `python src/crud/expertise.py --resume "Master Resume" --delete "Legacy Systems"` |
| "List my areas of expertise" | `python src/crud/expertise.py --resume "Master Resume" --list` |

### Certifications

| Natural Language | Command |
|-----------------|---------|
| "Add my AWS certification" | `python src/crud/certifications.py --resume "Master Resume" --add --name "AWS Solutions Architect" --issuer "Amazon" --date "Oct 2025"` |
| "Update my PSM I certification date" | `python src/crud/certifications.py --resume "Master Resume" --update --name "PSM I" --date "June 2023"` |
| "List my certifications" | `python src/crud/certifications.py --resume "Master Resume" --list` |

### Experience

| Natural Language | Command |
|-----------------|---------|
| "Add a bullet to my Microsoft experience" | `python src/crud/experience.py --resume "Master Resume" --add-bullet --employer "Microsoft" --text "Led team of 10 engineers" --tags "Leadership"` |
| "List my work experience" | `python src/crud/experience.py --resume "Master Resume" --list` |

## Script Reference

### 1. Basic Info

**Purpose**: Manage name, title, location, and contact information

**Operations**:
```bash
# Update individual fields
--update-name "John Doe"
--update-title "Principal Software Architect"
--update-location "Remote"
--update-email "john@example.com"
--update-phone "(555) 123-4567"

# Show current info
--show
```

**Example**:
```bash
python src/crud/basic_info.py --resume "Ford" --update-title "Senior Solutions Architect"
```

### 2. Summary

**Purpose**: Manage resume summary text

**Operations**:
```bash
# Replace entire summary
--update "New summary text..."

# Append to existing summary
--append "Additional text."

# Load from file
--from-file "summary.txt"

# Show current summary
--show
```

**Example**:
```bash
python src/crud/summary.py --resume "Ford" --append "Extensive experience with Kubernetes and cloud-native technologies."
```

### 3. Technical Skills

**Purpose**: Manage technical proficiencies organized by category

**Categories**: `ai`, `cloud`, `databases`, `devops`, `languages`, `opensource`, `os`, `security`

**Operations**:
```bash
# Add new category
--add-category "security" "OAuth, JWT, SAML"

# Update category (replace)
--update-category "cloud" "Azure, AWS, GCP"

# Append to category
--append-to-category "languages" "Rust, Go"

# Delete category
--delete-category "security"

# List all categories
--list

# Show specific category
--show "cloud"
```

**Example**:
```bash
python src/crud/technical_skills.py --resume "Ford" --append-to-category "devops" "Kubernetes, Helm"
```

### 4. Areas of Expertise

**Purpose**: Manage areas of expertise (array of strings)

**Operations**:
```bash
# Add expertise area
--add "AI/ML Engineering"

# Update expertise area
--update "Old Text" "New Text"

# Delete expertise area
--delete "Text to remove"

# Clear all
--clear

# List all
--list
```

**Example**:
```bash
python src/crud/expertise.py --resume "Ford" --add "Cloud-Native Architecture"
```

### 5. Achievements

**Purpose**: Manage achievements (array of strings)

**Operations**: Same as expertise (`--add`, `--update`, `--delete`, `--clear`, `--list`)

**Example**:
```bash
python src/crud/achievements.py --resume "Ford" --add "AWS Certified Solutions Architect - Professional"
```

### 6. Education

**Purpose**: Manage education entries

**Operations**:
```bash
# Add education entry
--add --degree "Master of Science" --institution "MIT" --location "Cambridge, MA" --year "2020"

# Update by institution or index
--update --institution "MIT" --year "2021"
--update --index 0 --degree "Master of Computer Science"

# Delete by institution or index
--delete --institution "University of Phoenix"
--delete --index 0

# List all
--list
```

**Example**:
```bash
python src/crud/education.py --resume "Ford" --add --degree "Master of Science in Computer Science" --institution "Stanford University" --year "2015"
```

### 7. Certifications

**Purpose**: Manage certification entries

**Operations**:
```bash
# Add certification
--add --name "AWS Solutions Architect" --issuer "Amazon" --date "Oct 2025" --credential "ABC123"

# Update by name or index
--update --name "PSM I" --date "June 2023"
--update --index 0 --date "July 2023"

# Delete by name or index
--delete --name "PSM I"
--delete --index 0

# List all
--list
```

**Example**:
```bash
python src/crud/certifications.py --resume "Ford" --add --name "Certified Kubernetes Administrator" --issuer "CNCF" --date "November 2025"
```

### 8. Experience

**Purpose**: Manage work experience entries and bullets

**Operations**:
```bash
# Add experience entry
--add --employer "Microsoft" --role "Senior Engineer" --dates "2020-2023" --location "Remote"

# Add bullet to experience
--add-bullet --employer "Microsoft" --text "Led team of 10 engineers" --tags "Leadership,Management"

# Update bullet
--update-bullet --employer "Microsoft" --index 0 --text "New bullet text"

# Delete bullet
--delete-bullet --employer "Microsoft" --index 0

# Delete experience entry
--delete --employer "Microsoft"
--delete --index 0

# List all experience
--list

# Import from markdown
--from-markdown "experience.md" --replace
```

**Example**:
```bash
python src/crud/experience.py --resume "Ford" --add-bullet --employer "Edward Jones" --text "Architected microservices platform serving 13 teams" --tags "Architecture,Microservices,Leadership"
```

## Common Use Cases

### Updating Resume for New Job Application

```bash
# 1. Update title to match job posting
python src/crud/basic_info.py --resume "Ford" --update-title "Senior Cloud Architect"

# 2. Add relevant skills
python src/crud/technical_skills.py --resume "Ford" --append-to-category "cloud" "Google Cloud Platform"

# 3. Add relevant expertise
python src/crud/expertise.py --resume "Ford" --add "Multi-Cloud Architecture"

# 4. Update summary to emphasize cloud experience
python src/crud/summary.py --resume "Ford" --append "Extensive experience designing and implementing multi-cloud solutions."
```

### Adding New Certification

```bash
python src/crud/certifications.py --resume "Master Resume" --add \
  --name "AWS Certified Solutions Architect - Professional" \
  --issuer "Amazon Web Services" \
  --date "November 2025" \
  --credential "AWS-PSA-12345"
```

### Managing Experience Bullets

```bash
# List current experience to find employer
python src/crud/experience.py --resume "Master Resume" --list

# Add new bullet
python src/crud/experience.py --resume "Master Resume" --add-bullet \
  --employer "Edward Jones" \
  --text "Led migration of 50+ microservices to Kubernetes, reducing infrastructure costs by 40%" \
  --tags "Kubernetes,Cost Optimization,Migration,Leadership"

# Update existing bullet (index 0)
python src/crud/experience.py --resume "Master Resume" --update-bullet \
  --employer "Edward Jones" \
  --index 0 \
  --text "Spearheaded migration of 50+ microservices to Kubernetes, achieving 40% cost reduction"
```

## Troubleshooting

### Resume Not Found

**Error**: `[ERROR] No resume found matching 'Ford'`

**Solution**:
1. Check available resumes: `python src/crud/expertise.py --resume "Master Resume" --list` (any script works)
2. Use exact or partial name from the list
3. Or use `--resume-id` with UUID

### Invalid Data

**Error**: `[ERROR] Invalid email format: notanemail`

**Solution**: Ensure data matches expected format (emails, phone numbers, etc.)

### Permission Errors

**Error**: `[ERROR] Could not save resume`

**Solution**: Check file permissions on `data/resumes/` directory

### Import Errors

**Error**: `ModuleNotFoundError: No module named 'crud'`

**Solution**: Run scripts from repository root directory

## Best Practices

1. **Always use Master Resume as source of truth**: Make changes to Master Resume, then duplicate for tailored versions
2. **Use descriptive tags**: Tag experience bullets with relevant keywords for better searchability
3. **Keep backups**: The system automatically backs up, but consider manual backups before major changes
4. **Test with --list first**: Before modifying, use `--list` to see current state
5. **Use --show for verification**: After updates, use `--show` to verify changes

## Related Documentation

- [src/crud/README.md](../src/crud/README.md) - Technical reference for developers
- [agent_knowledge_base.json](../agent_knowledge_base.json) - Complete CRUD operations reference
- [Agent Integration Guide](./AGENT_WEB_INTEGRATION.md) - Using CRUD with AI agent

## Support

For issues or questions:
- GitHub Issues: [#17](https://github.com/BPMSoftwareSolutions/agentic-resume-tailor/issues/17)
- Documentation: [docs/](../docs/)

