# Agent Knowledge Base System

## Overview

The AI Agent has been enhanced with a **knowledge base system** that allows it to understand the codebase structure and intelligently handle natural language commands. This enables users to give high-level commands like "Update the Ford resume with this experience" without needing to specify exact file paths or IDs.

## Architecture

### Knowledge Base File

**Location**: `agent_knowledge_base.json`

This JSON file contains:
- **Data structure mappings** - How resumes, job listings, and other data are organized
- **Common operations** - Step-by-step guides for frequent tasks
- **API endpoints** - Available REST API endpoints
- **Command patterns** - Natural language patterns the agent can recognize
- **File locations** - Key directories and files in the codebase

### Enhanced Agent System Prompt

The agent's system prompt (`agent.py`) has been updated to:
- Reference the knowledge base structure
- Understand resume naming conventions
- Parse natural language commands
- Map company names to resume files
- Execute appropriate helper scripts

## Key Features

### 1. Natural Language Command Understanding

The agent can parse commands like:

```
"Update the Ford resume with this experience: data/job_listings/Tailored Experience Summary for Ford.md"
```

And automatically:
1. Extract the company identifier ("Ford")
2. Search `data/resumes/index.json` for matching resume
3. Find the resume ID
4. Execute the update operation

### 2. Resume Discovery

The agent knows how to find resumes by:
- **Company name**: "Ford", "GM", "Credibly"
- **Partial name match**: Case-insensitive search
- **Resume ID**: Direct UUID lookup

Resume naming pattern: `{FirstName}_{LastName}_{Role}_{Company}`

Example: `Sidney_Jones_Senior_Software_Engineer_Ford`

### 3. Helper Scripts

#### `src/update_resume_experience.py`

A Python script that automates resume updates:

```bash
python src/update_resume_experience.py --resume "Ford" --experience "data/job_listings/Tailored Experience Summary for Ford.md"
```

**Features**:
- Finds resume by company name or ID
- Parses experience from markdown files
- Updates resume JSON automatically
- Updates timestamps in index.json
- Supports prepend (default) or replace mode

**Options**:
- `--resume`: Company name or resume name to search for
- `--resume-id`: Direct UUID (alternative to --resume)
- `--experience`: Path to markdown file with experience
- `--replace`: Replace all experience (default: prepend)
- `--data-dir`: Data directory path (default: data)

#### CRUD Scripts (`src/crud/`)

Specialized scripts for managing individual resume sections:

**Available Scripts**:
- `basic_info.py` - Name, title, location, contact information
- `summary.py` - Resume summary text
- `technical_skills.py` - Technical proficiencies by category
- `expertise.py` - Areas of expertise
- `achievements.py` - Achievements
- `education.py` - Education entries
- `certifications.py` - Certification entries
- `experience.py` - Work experience and bullets

**Example Usage**:
```bash
# Update title
python src/crud/basic_info.py --resume "Master Resume" --update-title "Principal Architect"

# Add technical skill
python src/crud/technical_skills.py --resume "Ford" --append-to-category "languages" "Python"

# Add certification
python src/crud/certifications.py --resume "Ford" --add --name "AWS Solutions Architect" --issuer "Amazon" --date "Nov 2025"

# List expertise areas
python src/crud/expertise.py --resume "Master Resume" --list
```

**Common Features**:
- Natural language friendly (find by resume name)
- Automatic timestamp updates
- Built-in validation
- Consistent error handling
- Comprehensive help (`--help`)

See [CRUD Operations Documentation](CRUD_OPERATIONS.md) for complete guide.

## Data Structure

### Resumes

**Location**: `data/resumes/`

**Index File**: `data/resumes/index.json`

```json
{
  "resumes": [
    {
      "id": "d474d761-18f2-48ab-99b5-9f30c54f75b2",
      "name": "Sidney_Jones_Senior_Software_Engineer_Ford",
      "created_at": "2025-10-12T08:49:00.020000",
      "updated_at": "2025-10-12T08:51:39.985858",
      "job_listing_id": null,
      "is_master": false,
      "description": "Duplicated from Sidney_Jones_Senior_Software_Engineer_GM"
    }
  ]
}
```

**Resume Files**: `data/resumes/{UUID}.json`

### Job Listings

**Location**: `data/job_listings/`

**File Types**:
- **JSON files**: `{UUID}.json` - Structured job listing data
- **Markdown files**: 
  - Job descriptions: `Sr. Software Engineer - at Credibly.md`
  - Tailored experiences: `Tailored Experience Summary for Ford.md`

## Common Operations

### Update Resume with Experience

**User Command**:
```
Update the Ford resume with this experience: "data/job_listings/Tailored Experience Summary for Ford.md"
```

**Agent Execution**:
```bash
run: python src/update_resume_experience.py --resume "Ford" --experience "data/job_listings/Tailored Experience Summary for Ford.md"
```

**What Happens**:
1. Script searches `data/resumes/index.json` for resume containing "Ford"
2. Finds: `Sidney_Jones_Senior_Software_Engineer_Ford` (ID: `d474d761-18f2-48ab-99b5-9f30c54f75b2`)
3. Parses experience sections from markdown file
4. Updates `data/resumes/d474d761-18f2-48ab-99b5-9f30c54f75b2.json`
5. Updates timestamp in index.json

### List Available Resumes

**User Command**:
```
List all resumes
```

**Agent Execution**:
```bash
run: cat data/resumes/index.json
```

Or via API:
```bash
GET http://localhost:5000/api/resumes
```

### CRUD Operations (Granular Updates)

#### Update Basic Information

**User Command**:
```
Update my title to Principal Software Architect
```

**Agent Execution**:
```bash
run: python src/crud/basic_info.py --resume "Master Resume" --update-title "Principal Software Architect"
```

#### Add Technical Skills

**User Command**:
```
Add Python and Rust to my programming languages
```

**Agent Execution**:
```bash
run: python src/crud/technical_skills.py --resume "Master Resume" --append-to-category "languages" "Python, Rust"
```

#### Add Certification

**User Command**:
```
Add my AWS certification
```

**Agent Execution**:
```bash
run: python src/crud/certifications.py --resume "Master Resume" --add --name "AWS Solutions Architect" --issuer "Amazon" --date "November 2025"
```

#### List Expertise Areas

**User Command**:
```
List my areas of expertise
```

**Agent Execution**:
```bash
run: python src/crud/expertise.py --resume "Master Resume" --list
```

#### Add Experience Bullet

**User Command**:
```
Add a bullet to my Microsoft experience about leading a team
```

**Agent Execution**:
```bash
run: python src/crud/experience.py --resume "Master Resume" --add-bullet --employer "Microsoft" --text "Led team of 10 engineers in developing cloud-native solutions" --tags "Leadership,Cloud"
```

### Tailor Resume to Job

**User Command**:
```
Tailor my resume for the Credibly position
```

**Agent Execution**:
```bash
run: python src/tailor.py --resume data/master_resume.json --jd "data/job_listings/Sr. Software Engineer - at Credibly.md" --out out/credibly_tailored.html --format html --theme professional
```

## Command Whitelisting

For security, the agent can only execute whitelisted commands:

- `python src/tailor.py` - Resume tailoring
- `python src/update_resume_experience.py` - Resume updates
- `python -m pytest` - Running tests
- `python -m json.tool` - JSON formatting
- `git status`, `git log`, `git diff` - Git operations
- `ls`, `dir`, `pwd`, `echo` - File system navigation
- `cat`, `type` - File reading

Dangerous commands are blocked (e.g., `rm -rf`, `format`, `sudo`).

## API Integration

The agent can also use REST API endpoints:

### Agent Endpoints
- `POST /api/agent/chat` - Send messages to agent
- `GET /api/agent/memory` - Get conversation history
- `POST /api/agent/memory/clear` - Clear memory
- `POST /api/agent/validate-command` - Validate command security

### Resume Endpoints
- `GET /api/resumes` - List all resumes
- `GET /api/resumes/{id}` - Get specific resume
- `POST /api/resumes` - Create new resume
- `PUT /api/resumes/{id}` - Update resume
- `POST /api/resumes/{id}/duplicate` - Duplicate resume
- `POST /api/resumes/{id}/tailor` - Tailor resume

### Job Listing Endpoints
- `GET /api/job-listings` - List all job listings
- `GET /api/job-listings/{id}` - Get specific job listing
- `POST /api/job-listings` - Create new job listing

## Example Interactions

### Example 1: Update Resume

**User**: 
```
Update the Ford resume with this experience: "C:\source\repos\bpm\internal\agentic-resume-tailor\data\job_listings\Tailored Experience Summary for Ford.md"
```

**Agent Response**:
```
I'll update the Ford resume with the experience from that file.

run: python src/update_resume_experience.py --resume "Ford" --experience "data/job_listings/Tailored Experience Summary for Ford.md"

✅ Successfully updated resume d474d761-18f2-48ab-99b5-9f30c54f75b2
   Found resume: Sidney_Jones_Senior_Software_Engineer_Ford
   Added 5 experience entries
```

### Example 2: List Resumes

**User**: 
```
What resumes do I have?
```

**Agent Response**:
```
Let me check your available resumes.

run: cat data/resumes/index.json

You have the following resumes:
1. Master Resume (ID: b3013a2a-349a-4080-802c-3bbe6714b576)
2. Sidney_Jones_Senior_Software_Engineer_Credibly (ID: a041bd2e-d54b-488f-adda-e4c707d5332d)
3. Sidney_Jones_Senior_Software_Engineer_GM (ID: f3bc0d6d-aea7-4e08-96b8-5fc6b581138b)
4. Sidney_Jones_Senior_Software_Engineer_Ford (ID: d474d761-18f2-48ab-99b5-9f30c54f75b2)
```

### Example 3: Tailor Resume

**User**: 
```
Tailor my resume for the GM position
```

**Agent Response**:
```
I'll tailor your resume for the GM position. Let me use the master resume and the GM job description.

run: python src/tailor.py --resume data/master_resume.json --jd "data/job_listings/Tailored Experience Summary for GM.md" --out out/gm_tailored.html --format html --theme professional

✅ Resume tailored successfully!
   Output: out/gm_tailored.html
```

## Testing

Tests for the knowledge base system are in:
- `tests/test_update_resume_experience.py` - Tests for the helper script

Run tests:
```bash
python -m pytest tests/test_update_resume_experience.py -v
```

## Future Enhancements

Potential improvements to the knowledge base system:

1. **Semantic Search** - Use embeddings to find similar resumes/experiences
2. **Auto-tagging** - Automatically tag experiences with relevant skills
3. **Resume Comparison** - Compare different resume versions
4. **Job Matching** - Suggest which resume to use for a job posting
5. **Experience Library** - Maintain a library of reusable experience bullets
6. **Version Control** - Track changes to resumes over time
7. **Analytics** - Track which resumes get the most responses

## Troubleshooting

### Agent Can't Find Resume

**Problem**: Agent says "No resume found matching 'Ford'"

**Solution**: 
1. Check `data/resumes/index.json` to see available resumes
2. Verify the company name is in the resume name
3. Try using the full resume name or ID

### Experience Not Parsing Correctly

**Problem**: Experience from markdown file isn't being added

**Solution**:
1. Verify markdown format uses `### Company — Role (Dates)` headers
2. Check that bullets start with `*`
3. Ensure tags line uses `**Tags:**` format

### Command Not Whitelisted

**Problem**: Agent says command is not allowed

**Solution**:
1. Check `src/api/app.py` for `ALLOWED_COMMAND_PREFIXES`
2. Use one of the helper scripts instead of direct commands
3. Request the command be added to the whitelist

## Contributing

To extend the knowledge base:

1. Update `agent_knowledge_base.json` with new operations
2. Update agent system prompt in `agent.py`
3. Add new helper scripts to `src/`
4. Update command whitelist in `src/api/app.py`
5. Add tests for new functionality
6. Update this documentation

