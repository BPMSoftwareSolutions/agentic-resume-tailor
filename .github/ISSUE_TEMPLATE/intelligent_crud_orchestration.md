---
name: Intelligent CRUD Orchestration for Resume Tailoring
about: Replace tailor.py with intelligent CRUD-based resume customization
title: 'Phase 2: Intelligent CRUD Orchestration & Natural Language Resume Updates'
labels: enhancement, phase-2, ai-agent, crud
assignees: ''
---

## Problem Statement

The current implementation uses `tailor.py` which:
- ❌ Creates HTML output only (not editable)
- ❌ Doesn't update the resume JSON in the database
- ❌ Uses AI rewriting instead of CRUD operations
- ❌ Doesn't leverage the CRUD scripts we built
- ❌ Doesn't use the knowledge base effectively

**The original vision was**: Agent should intelligently parse job postings and automatically run appropriate CRUD operations to update resumes.

## User Stories

### Story 1: Create Resume from Job Posting
```
User: "Using the Ford Resume, create a new for this job posting: Subscription Billing Software Engineering Manager.md"

Expected Behavior:
1. Agent duplicates Ford resume
2. Agent parses job posting to extract:
   - Required skills
   - Role title
   - Key responsibilities
   - Experience requirements
3. Agent automatically runs CRUD operations:
   - Updates title
   - Updates summary
   - Adds relevant skills
   - Emphasizes matching experience
4. Agent creates editable JSON in database
5. Optionally exports to DOCX/HTML
```

### Story 2: Update Resume from File
```
User: "Update resume_Ford with this data: C:\path\to\Tailored Experience Summary for Ford.md"

Expected Behavior:
1. Agent reads the markdown file
2. Agent parses experience sections
3. Agent runs: python src/crud/experience.py --from-markdown "file.md" --replace
4. Agent updates the resume JSON
5. Agent confirms what was updated
```

### Story 3: Natural Language Updates
```
User: "Add Python and Stripe to my technical skills"

Expected Behavior:
1. Agent identifies this is a skills update
2. Agent runs: python src/crud/technical_skills.py --resume "Master Resume" --append-to-category "languages" "Python"
3. Agent runs: python src/crud/technical_skills.py --resume "Master Resume" --append-to-category "billing" "Stripe"
4. Agent confirms the update
```

### Story 4: Intelligent Experience Emphasis
```
User: "Emphasize my billing and payment experience for this job"

Expected Behavior:
1. Agent searches resume for billing/payment-related bullets
2. Agent identifies relevant experience entries
3. Agent reorders or adds bullets to emphasize those skills
4. Agent uses CRUD operations to update experience section
```

## Technical Requirements

### 1. Job Posting Parser
**File**: `src/parsers/job_posting_parser.py`

**Functionality**:
- Parse markdown job postings
- Extract required skills (technical and soft skills)
- Extract role title and level
- Extract key responsibilities
- Extract required experience years
- Extract company/industry context

**Output**:
```python
{
    "title": "Engineering Manager - Subscription Billing",
    "required_skills": ["Python", "Stripe", "Zuora", "Leadership"],
    "preferred_skills": ["AWS", "Microservices"],
    "responsibilities": ["Lead team of 10", "Architect billing systems"],
    "experience_years": "10+",
    "keywords": ["billing", "subscription", "payment", "SaaS"]
}
```

### 2. Resume Matcher
**File**: `src/parsers/resume_matcher.py`

**Functionality**:
- Compare job requirements with resume content
- Identify matching skills
- Find relevant experience bullets
- Calculate match score
- Suggest which sections to update

**Output**:
```python
{
    "matching_skills": ["Python", "AWS", "Leadership"],
    "missing_skills": ["Stripe", "Zuora"],
    "relevant_experience": [
        {"employer": "Ford", "bullet_index": 3, "relevance": 0.95},
        {"employer": "GM", "bullet_index": 1, "relevance": 0.87}
    ],
    "suggested_updates": {
        "title": "Engineering Manager - Subscription Billing",
        "skills_to_add": ["Stripe", "Zuora"],
        "expertise_to_add": ["Subscription Billing Architecture"]
    }
}
```

### 3. CRUD Orchestrator
**File**: `src/orchestrator/crud_orchestrator.py`

**Functionality**:
- Takes job posting analysis + resume match
- Generates sequence of CRUD operations
- Executes CRUD operations in correct order
- Validates each operation
- Provides progress feedback

**Example**:
```python
orchestrator = CRUDOrchestrator(resume_id="abc-123", job_analysis=job_data)

operations = orchestrator.plan_updates()
# Returns:
# [
#   {"script": "basic_info.py", "args": ["--update-title", "Engineering Manager"]},
#   {"script": "technical_skills.py", "args": ["--add-category", "billing", "Stripe, Zuora"]},
#   {"script": "summary.py", "args": ["--update", "New summary..."]},
#   {"script": "experience.py", "args": ["--add-bullet", "--employer", "Ford", "--text", "..."]}
# ]

results = orchestrator.execute()
# Executes each operation and returns results
```

### 4. Natural Language Command Parser
**File**: `src/parsers/nl_command_parser.py`

**Functionality**:
- Parse natural language commands
- Identify intent (add, update, remove, list)
- Extract entities (skills, experience, sections)
- Map to appropriate CRUD script

**Examples**:
```python
parse("Add Python to my technical skills")
# Returns: {"script": "technical_skills.py", "operation": "append", "category": "languages", "value": "Python"}

parse("Update my title to Senior Engineer")
# Returns: {"script": "basic_info.py", "operation": "update-title", "value": "Senior Engineer"}

parse("Remove my GM experience")
# Returns: {"script": "experience.py", "operation": "delete", "employer": "GM"}
```

### 5. Experience File Parser
**File**: `src/parsers/experience_parser.py`

**Functionality**:
- Parse markdown files with experience sections
- Extract employer, role, dates, bullets
- Handle different markdown formats
- Validate extracted data

**Input Example**:
```markdown
### Ford Motor Company
**Senior Software Engineer** | 2020-2023 | Dearborn, MI

- Led development of subscription billing platform
- Architected payment processing system
- Managed team of 8 engineers
```

**Output**:
```python
{
    "employer": "Ford Motor Company",
    "role": "Senior Software Engineer",
    "dates": "2020-2023",
    "location": "Dearborn, MI",
    "bullets": [
        {"text": "Led development of subscription billing platform", "tags": ["Leadership", "Billing"]},
        {"text": "Architected payment processing system", "tags": ["Architecture", "Payments"]},
        {"text": "Managed team of 8 engineers", "tags": ["Leadership", "Management"]}
    ]
}
```

## Implementation Plan

### Phase 2A: Parsers (Week 1)
- [ ] Create `src/parsers/` directory
- [ ] Implement `job_posting_parser.py`
- [ ] Implement `experience_parser.py`
- [ ] Implement `nl_command_parser.py`
- [ ] Write unit tests for all parsers
- [ ] Update agent knowledge base with parser info

### Phase 2B: Matching & Orchestration (Week 2)
- [ ] Implement `resume_matcher.py`
- [ ] Implement `crud_orchestrator.py`
- [ ] Create orchestration workflow
- [ ] Write integration tests
- [ ] Update agent system prompt

### Phase 2C: Agent Integration (Week 3)
- [ ] Update `agent.py` to use orchestrator
- [ ] Remove dependency on `tailor.py` for resume creation
- [ ] Add natural language command handling
- [ ] Add progress feedback during CRUD operations
- [ ] Update web UI to show orchestration progress

### Phase 2D: Testing & Documentation (Week 4)
- [ ] Test all user stories
- [ ] Create comprehensive documentation
- [ ] Update README with new workflow
- [ ] Create video demo
- [ ] Deprecate `tailor.py` (keep for backward compatibility)

## Success Criteria

### Functional Requirements
- [ ] Agent can parse job postings and extract requirements
- [ ] Agent can match job requirements to resume content
- [ ] Agent automatically runs appropriate CRUD operations
- [ ] Agent handles natural language commands for updates
- [ ] Agent can parse experience markdown files
- [ ] All updates create editable JSON in database
- [ ] No reliance on `tailor.py` for resume creation

### User Experience
- [ ] User says "create new resume for job X" → Agent does it automatically
- [ ] User says "update resume with file Y" → Agent parses and updates
- [ ] User says "add skill Z" → Agent updates immediately
- [ ] Agent provides clear progress feedback
- [ ] Agent explains what it's doing at each step

### Technical Quality
- [ ] 50+ unit tests for parsers
- [ ] 20+ integration tests for orchestration
- [ ] All CRUD operations validated
- [ ] Error handling for malformed inputs
- [ ] Performance: < 5 seconds for full orchestration

## Example Workflow

```
User: "Using the Ford Resume, create a new for this job posting: Subscription Billing Software Engineering Manager.md"

Agent Response:
"I'll create a new resume tailored for the Subscription Billing Engineering Manager position.

Step 1: Duplicating Ford resume...
✅ Created: Sidney_Jones_Engineering_Manager_Subscription_Billing

Step 2: Analyzing job posting...
📋 Found requirements:
   - Skills: Python, Stripe, Zuora, AWS, Leadership
   - Experience: 10+ years
   - Focus: Billing systems, team leadership

Step 3: Matching your experience...
✅ Found 8 relevant experience bullets
✅ Matching skills: Python, AWS, Leadership
⚠️  Missing skills: Stripe, Zuora (will add)

Step 4: Updating resume sections...
✅ Updated title: Engineering Manager - Subscription Billing
✅ Updated summary with billing focus
✅ Added billing skills: Stripe, Zuora, Recurly
✅ Added expertise: Subscription Billing Architecture
✅ Emphasized 5 billing-related experience bullets

✅ Resume ready! 
   ID: abc-123-def-456
   Name: Sidney_Jones_Engineering_Manager_Subscription_Billing
   Match Score: 87%

Would you like me to:
1. Export to DOCX for submission
2. Make additional customizations
3. Review the changes"
```

## Dependencies

- Existing CRUD scripts (already implemented)
- Knowledge base (already implemented)
- Agent auto-verification (Issue #24 - completed)
- Resume duplication (already implemented)

## Related Issues

- #24 - Auto-Verification & Token Management (completed)
- #23 - Intelligent Agent Memory Management
- #19 - Resume Duplication (completed)

## Notes

This is the **correct implementation** of the original vision. The CRUD operations were built specifically to enable this intelligent, automated workflow. The `tailor.py` script should only be used for final HTML/DOCX export, not for resume creation or updates.

