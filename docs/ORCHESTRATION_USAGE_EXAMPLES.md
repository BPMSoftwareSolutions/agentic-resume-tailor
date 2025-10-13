# Intelligent Resume Orchestration - Usage Examples

This document provides practical examples of using the Phase 2 intelligent orchestration system.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Parsing Job Postings](#parsing-job-postings)
3. [Matching Resumes](#matching-resumes)
4. [Generating CRUD Operations](#generating-crud-operations)
5. [Complete Workflow](#complete-workflow)
6. [Natural Language Commands](#natural-language-commands)
7. [Agent Integration](#agent-integration)

## Quick Start

### Scenario: Tailor Resume for a Job Posting

```bash
# Step 1: Parse the job posting
python src/parsers/job_posting_parser.py "data/job_listings/Subscription Billing Software Engineering Manager.md"

# Step 2: Match your resume with the job
python src/orchestrator/resume_matcher.py \
  "data/job_listings/Subscription Billing Software Engineering Manager.md" \
  "data/resumes/1e2c70dc-0103-4fa1-b591-93a4fae05de5.json"

# Step 3: Generate tailoring operations (dry-run)
python src/orchestrator/crud_orchestrator.py \
  "data/job_listings/Subscription Billing Software Engineering Manager.md" \
  "data/resumes/1e2c70dc-0103-4fa1-b591-93a4fae05de5.json" \
  "Ford"
```

## Parsing Job Postings

### Example 1: Parse a Job Posting File

```bash
python src/parsers/job_posting_parser.py "data/job_listings/GM Job.md"
```

**Output:**
```
=== Job Posting Analysis ===

Title: Subscription Billing Software Engineering Manager
Company: General Motors
Location: Austin, TX
Work Arrangement: hybrid

Required Skills (16):
  - zuora
  - revpro
  - java
  - spring boot
  - microservices
  - rest api
  - aws
  - azure
  - gcp
  - ci/cd
  - git
  - datadog
  - subscription billing
  - sox
  - audit
  - compliance

Responsibilities (6):
  - Lead the end-to-end implementation and ongoing operation of Zuora...
  - Collaborate with cross-functional teams...
  - Ensure compliance with SOX and audit requirements...
  - Drive technical excellence through code reviews...
  - Mentor and develop engineering talent...
  - Establish and maintain observability practices...

Experience Required: 5+ years management
```

### Example 2: Programmatic Usage

```python
from parsers import JobPostingParser

parser = JobPostingParser()
job_data = parser.parse_file("data/job_listings/GM Job.md")

print(f"Job Title: {job_data['title']}")
print(f"Company: {job_data['company']}")
print(f"Required Skills: {', '.join(job_data['required_skills'][:5])}")
```

## Matching Resumes

### Example 1: Calculate Match Score

```bash
python src/orchestrator/resume_matcher.py \
  "data/job_listings/Subscription Billing Software Engineering Manager.md" \
  "data/resumes/1e2c70dc-0103-4fa1-b591-93a4fae05de5.json"
```

**Output:**
```
=== Resume Match Analysis ===

Overall Match Score: 65.5%

Skill Match: 50.0%
  - Matching: 8 skills
  - Missing: 8 skills

Matching Skills:
  ✓ python
  ✓ java
  ✓ microservices
  ✓ rest api
  ✓ aws
  ✓ docker
  ✓ kubernetes
  ✓ ci/cd

Missing Skills:
  ✗ zuora
  ✗ revpro
  ✗ azure
  ✗ gcp
  ✗ datadog
  ✗ subscription billing
  ✗ sox
  ✗ compliance

Relevant Experience (2 entries):
  - Tech Corp (Senior Software Engineer)
    Relevance: 8.5, Matching bullets: 3
  - Previous Company (Software Engineer)
    Relevance: 5.0, Matching bullets: 1

Suggestions:
  1. Add these missing skills: zuora, revpro, azure, gcp, datadog
  2. Consider updating title to match job: 'Subscription Billing Software Engineering Manager'
  3. Emphasize experience at Tech Corp - it has 3 relevant bullets
  4. Align experience bullets with key responsibilities
  5. Highlight experience with: SOX, audit, compliance
```

### Example 2: Programmatic Usage

```python
from orchestrator import ResumeMatcher
from parsers import JobPostingParser
import json

# Parse job
parser = JobPostingParser()
job_data = parser.parse_file("data/job_listings/GM Job.md")

# Load resume
with open("data/resumes/resume_id.json", 'r') as f:
    resume_data = json.load(f)

# Match
matcher = ResumeMatcher()
result = matcher.match(job_data, resume_data)

print(f"Match Score: {result['score']}%")
print(f"Missing Skills: {', '.join(result['missing_skills'][:5])}")
```

## Generating CRUD Operations

### Example 1: Generate Operations (Dry-Run)

```bash
python src/orchestrator/crud_orchestrator.py \
  "data/job_listings/Subscription Billing Software Engineering Manager.md" \
  "data/resumes/1e2c70dc-0103-4fa1-b591-93a4fae05de5.json" \
  "Ford"
```

**Output:**
```
=== CRUD Orchestration Plan ===

Resume: Ford
Job: Subscription Billing Software Engineering Manager at General Motors
Match Score: 65.5%

Generated 10 operations:

1. Update title to: Subscription Billing Software Engineering Manager
   Command: python src/crud/basic_info.py --resume "Ford" --update-title "Subscription Billing Software Engineering Manager"

2. Add languages skills: java, microservices, rest
   Command: python src/crud/technical_skills.py --resume "Ford" --append-to-category "languages" "java, microservices, rest"

3. Add cloud skills: aws, azure, gcp
   Command: python src/crud/technical_skills.py --resume "Ford" --append-to-category "cloud" "aws, azure, gcp"

4. Add devops skills: ci/cd, datadog, git
   Command: python src/crud/technical_skills.py --resume "Ford" --append-to-category "devops" "ci/cd, datadog, git"

5. Add billing skills: revpro, subscription billing, zuora
   Command: python src/crud/technical_skills.py --resume "Ford" --append-to-category "billing" "revpro, subscription billing, zuora"

6. Update summary to highlight: Tech Corp experience [MANUAL]
   Command: # Manual: Update summary to emphasize: Tech Corp experience

7. Add expertise: Billing
   Command: python src/crud/expertise.py --resume "Ford" --add "Billing"

8. Add expertise: Subscription
   Command: python src/crud/expertise.py --resume "Ford" --add "Subscription"

9. Add expertise: Revenue
   Command: python src/crud/expertise.py --resume "Ford" --add "Revenue"

10. Highlight compliance experience: compliance, audit, SOX [MANUAL]
    Command: # Manual: Emphasize compliance, audit, SOX experience


=== Executing Operations (DRY RUN) ===

[1/10] Update title to: Subscription Billing Software Engineering Manager
  → DRY RUN: python src/crud/basic_info.py --resume "Ford" --update-title "Subscription Billing Software Engineering Manager"
[2/10] Add languages skills: java, microservices, rest
  → DRY RUN: python src/crud/technical_skills.py --resume "Ford" --append-to-category "languages" "java, microservices, rest"
...

Results:
  Total: 10
  Successful: 8
  Failed: 0
  Skipped: 2
```

### Example 2: Programmatic Usage with Custom Callback

```python
from orchestrator import CRUDOrchestrator
from parsers import JobPostingParser
import json

# Parse job
parser = JobPostingParser()
job_data = parser.parse_file("data/job_listings/GM Job.md")

# Load resume
with open("data/resumes/resume_id.json", 'r') as f:
    resume_data = json.load(f)

# Match
from orchestrator import ResumeMatcher
matcher = ResumeMatcher()
match_result = matcher.match(job_data, resume_data)

# Generate operations
orchestrator = CRUDOrchestrator(dry_run=True)

# Set progress callback
def progress_callback(message):
    print(f"[PROGRESS] {message}")

orchestrator.set_progress_callback(progress_callback)

# Generate and execute
operations = orchestrator.generate_operations(job_data, match_result, "Ford")
results = orchestrator.execute_operations(operations)

print(f"\nCompleted: {results['successful']}/{results['total']} operations")
```

## Complete Workflow

### Scenario: Tailor Resume for GM Subscription Billing Role

```bash
#!/bin/bash
# complete_workflow.sh

JOB_FILE="data/job_listings/Subscription Billing Software Engineering Manager.md"
RESUME_ID="1e2c70dc-0103-4fa1-b591-93a4fae05de5"
RESUME_FILE="data/resumes/${RESUME_ID}.json"
RESUME_NAME="Ford"
OUTPUT_DIR="out"

echo "=== Step 1: Parse Job Posting ==="
python src/parsers/job_posting_parser.py "$JOB_FILE"

echo -e "\n=== Step 2: Match Resume ==="
python src/orchestrator/resume_matcher.py "$JOB_FILE" "$RESUME_FILE"

echo -e "\n=== Step 3: Generate Operations (Dry-Run) ==="
python src/orchestrator/crud_orchestrator.py "$JOB_FILE" "$RESUME_FILE" "$RESUME_NAME"

echo -e "\n=== Step 4: Review and Execute Operations ==="
read -p "Execute operations? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    # Execute each operation manually or modify orchestrator to execute
    echo "Executing operations..."
    # Add execution logic here
fi

echo -e "\n=== Step 5: Export Resume ==="
python src/tailor.py \
  --resume "$RESUME_NAME" \
  --jd "$JOB_FILE" \
  --out "${OUTPUT_DIR}/gm_subscription_billing.html" \
  --format html \
  --theme modern \
  --docx

echo -e "\n✅ Workflow complete!"
echo "Output files:"
echo "  - ${OUTPUT_DIR}/gm_subscription_billing.html"
echo "  - ${OUTPUT_DIR}/gm_subscription_billing.docx"
```

## Natural Language Commands

### Example 1: Parse Natural Language Commands

```python
from parsers import NLCommandParser

parser = NLCommandParser()

commands = [
    "Add Python and Java to my technical skills",
    "Update my title to Principal Architect",
    "List my certifications",
    "Duplicate the Ford resume as GM_Resume"
]

for cmd in commands:
    result = parser.parse(cmd, default_resume="Master Resume")
    print(f"Command: {cmd}")
    print(f"Intent: {result['intent']}")
    print(f"Entity: {result['entity']}")
    print(f"CRUD Command: {result['command']}")
    print()
```

**Output:**
```
Command: Add Python and Java to my technical skills
Intent: add
Entity: technical_skills
CRUD Command: python src/crud/technical_skills.py --resume "Master Resume" --append-to-category "languages" "Python, Java"

Command: Update my title to Principal Architect
Intent: update
Entity: basic_info
CRUD Command: python src/crud/basic_info.py --resume "Master Resume" --update-title "Principal Architect"

Command: List my certifications
Intent: list
Entity: certification
CRUD Command: python src/crud/certifications.py --resume "Master Resume" --list

Command: Duplicate the Ford resume as GM_Resume
Intent: duplicate
Entity: resume
CRUD Command: python src/duplicate_resume.py --resume "Ford" --new-name "GM_Resume"
```

## Agent Integration

### Example 1: Using the Agent

```bash
# Start the agent
python agent.py
```

**Conversation:**
```
You: Tailor my Ford resume for the GM Subscription Billing position

Agent: I'll analyze the job posting and intelligently tailor your Ford resume.

run: python src/orchestrator/crud_orchestrator.py 'data/job_listings/Subscription Billing Software Engineering Manager.md' 'data/resumes/1e2c70dc-0103-4fa1-b591-93a4fae05de5.json' 'Ford'

[Execution output shows match score and operations]

✅ Generated 10 tailoring operations:
   - Update title to match job
   - Add missing skills (aws, azure, zuora, etc.)
   - Add relevant expertise areas
   - Suggestions for manual updates

Would you like me to execute these operations to update your resume?

You: Yes, execute them

Agent: [Executes operations one by one with progress feedback]

✅ Successfully updated your Ford resume!
   - Title updated
   - Added 12 new skills
   - Added 3 expertise areas
   - 2 manual suggestions provided

Would you like me to export the resume to HTML/DOCX?
```

### Example 2: Agent API Usage

```python
import requests

# Chat with agent
response = requests.post('http://localhost:5000/api/agent/chat', json={
    'message': 'Tailor my Ford resume for the GM position'
})

print(response.json()['response'])

# Get agent memory
memory = requests.get('http://localhost:5000/api/agent/memory')
print(f"Memory: {len(memory.json()['memory'])} messages")
```

## Best Practices

1. **Always start with dry-run mode** to review operations before executing
2. **Review match scores** to understand resume gaps
3. **Manually review suggestions** for summary and experience updates
4. **Test with sample data** before modifying production resumes
5. **Keep backups** of resume JSON files before bulk operations
6. **Use version control** to track resume changes over time

## Troubleshooting

### Issue: Low Match Score

**Solution:** Review missing skills and add them using CRUD operations:
```bash
python src/crud/technical_skills.py --resume "Ford" --append-to-category "cloud" "aws, azure, gcp"
```

### Issue: Parser Not Finding Skills

**Solution:** Check job posting format and ensure it follows expected structure:
- Title on first line
- Company on second line
- Skills in "Required Skills" or "Your Skills & Abilities" section

### Issue: Operations Not Executing

**Solution:** Ensure resume name is correct and exists in index:
```bash
cat data/resumes/index.json | grep -i "ford"
```

## Next Steps

- Review [PHASE_2_IMPLEMENTATION_SUMMARY.md](PHASE_2_IMPLEMENTATION_SUMMARY.md) for technical details
- Check [agent_knowledge_base.json](../agent_knowledge_base.json) for complete API reference
- Run tests: `python -m pytest tests/test_orchestration.py -v`

