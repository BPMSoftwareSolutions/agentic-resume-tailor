# Agent Workflow Guide

## Understanding Resume Operations

This guide clarifies when to use each resume operation script and how the AI agent should interpret user requests.

## Key Distinction: Editable vs. Export

### Editable Resume (JSON in Database)
- **Location**: `data/resumes/{uuid}.json`
- **Purpose**: Can be edited, updated, and modified
- **Use Case**: When user wants to create a new resume they can work with
- **Script**: `duplicate_resume.py`

### Export/Output (HTML/DOCX)
- **Location**: `out/` directory
- **Purpose**: Final output for job applications
- **Use Case**: When user wants to generate a document to submit
- **Script**: `tailor.py`

## User Intent Recognition

### "Create a New Resume" → Use `duplicate_resume.py`

**User Phrases**:
- "Using the Ford resume, create a new one for X"
- "Create a new resume for the Subscription Billing position"
- "Duplicate the Ford resume"
- "Copy my Master Resume"
- "Make a new resume based on Ford"

**Agent Action**:
```bash
run: python src/duplicate_resume.py --resume "Ford" --new-name "Sidney_Jones_Engineering_Manager_Subscription_Billing"
```

**Result**:
- ✅ Creates new JSON file in `data/resumes/`
- ✅ Adds entry to `data/resumes/index.json`
- ✅ Can be edited with CRUD scripts
- ✅ Can be exported later with `tailor.py`

### "Export as HTML/DOCX" → Use `tailor.py`

**User Phrases**:
- "Export my resume as HTML"
- "Generate an HTML version for this job"
- "Create a tailored HTML for X position"
- "Make a DOCX for the job posting"

**Agent Action**:
```bash
run: python src/tailor.py --resume "Ford" --jd "data/job_listings/job.md" --out "out/output.html" --format html --theme modern
```

**Result**:
- ✅ Creates HTML/DOCX in `out/` directory
- ❌ Does NOT create editable resume in database
- ❌ Cannot be edited with CRUD scripts

## Recommended Workflow

### Scenario 1: Create New Resume for a Job

**User**: "Using the Ford resume, create a new one for the Subscription Billing position"

**Step 1**: Duplicate the resume
```bash
run: python src/duplicate_resume.py --resume "Ford" --new-name "Sidney_Jones_Engineering_Manager_Subscription_Billing"
```

**Step 2** (Optional): Update sections
```bash
run: python src/crud/summary.py --resume "Sidney_Jones_Engineering_Manager_Subscription_Billing" --update "New summary..."
run: python src/crud/technical_skills.py --resume "Sidney_Jones_Engineering_Manager_Subscription_Billing" --add-category "billing" "Stripe, Zuora"
```

**Step 3** (Optional): Export to HTML
```bash
run: python src/tailor.py --resume "Sidney_Jones_Engineering_Manager_Subscription_Billing" --jd "data/job_listings/job.md" --out "out/subscription_billing.html" --format html --theme modern
```

### Scenario 2: Quick HTML Export (No Editing Needed)

**User**: "Export my Ford resume as HTML for the Credibly job"

**Action**: Use tailor.py directly
```bash
run: python src/tailor.py --resume "Ford" --jd "data/job_listings/Sr. Software Engineer - at Credibly.md" --out "out/credibly.html" --format html --theme modern
```

## Script Comparison

| Feature | duplicate_resume.py | tailor.py |
|---------|-------------------|-----------|
| Creates editable JSON | ✅ Yes | ❌ No |
| Adds to database | ✅ Yes | ❌ No |
| Can use CRUD scripts | ✅ Yes | ❌ No |
| Generates HTML/DOCX | ❌ No | ✅ Yes |
| Tailors to job posting | ❌ No | ✅ Yes |
| Resume lookup by name | ✅ Yes | ✅ Yes |

## Common Mistakes

### ❌ Mistake 1: Using tailor.py for "Create New Resume"

**Wrong**:
```bash
# User: "Create a new resume for X"
run: python src/tailor.py --resume "Ford" --jd "job.md" --out "out/new.html"
```

**Why Wrong**: This only creates HTML output, not an editable resume

**Correct**:
```bash
run: python src/duplicate_resume.py --resume "Ford" --new-name "New_Resume_Name"
```

### ❌ Mistake 2: Using Full JSON Path Instead of Name

**Wrong**:
```bash
run: python src/tailor.py --resume data/resumes/abc-123-def-456.json --jd "job.md"
```

**Correct**:
```bash
run: python src/tailor.py --resume "Ford" --jd "job.md" --out "out/ford.html"
```

Both scripts support resume lookup by name!

### ❌ Mistake 3: Not Checking if Files Exist

**Wrong**: Blindly executing commands without verifying files exist

**Correct**: When file not found error occurs:
1. List available files: `dir data\job_listings\*.md`
2. Show user the available options
3. Suggest using an existing file or creating the missing one

## Self-Correction Examples

### Example 1: Missing Job Listing

**Error**: `File not found: data/job_listings/Subscription Billing.md`

**Agent Should**:
1. Detect the error ✅
2. Automatically list available files:
   ```bash
   run: dir data\job_listings\*.md
   ```
3. Show results to user
4. Suggest using an existing file

**Current Behavior**: Provides suggestions but doesn't auto-execute ⚠️

**Phase 2 Enhancement**: Auto-execute diagnostic commands

### Example 2: Resume Not Found

**Error**: `Resume not found: 'Frod'` (typo)

**Agent Should**:
1. Detect the error ✅
2. List available resumes:
   ```bash
   run: type data\resumes\index.json
   ```
3. Suggest correct spelling: "Did you mean 'Ford'?"

## Phase 1 vs Phase 2 Capabilities

### Phase 1 (Current) ✅
- ✅ Auto-verification of command results
- ✅ Extraction of key information (IDs, names, errors)
- ✅ Intelligent next-step suggestions
- ✅ Context-aware error messages
- ❌ Manual execution of diagnostic commands

### Phase 2 (Future) 🚀
- ✅ Autonomous self-correction
- ✅ Automatic execution of diagnostic commands
- ✅ Memory search for similar past errors
- ✅ Learning from past corrections
- ✅ Retry with automatic fixes

## Testing the Agent

### Test Case 1: Create New Resume
```
User: "Using the Ford resume, create a new one for the Subscription Billing position"

Expected:
✅ Agent uses duplicate_resume.py
✅ Creates new JSON in data/resumes/
✅ Suggests next steps (update sections, export HTML)

Not Expected:
❌ Agent uses tailor.py
❌ Only creates HTML output
```

### Test Case 2: Export HTML
```
User: "Export my Ford resume as HTML for the Credibly job"

Expected:
✅ Agent uses tailor.py
✅ Creates HTML in out/ directory
✅ Uses resume name lookup (not full path)

Not Expected:
❌ Agent uses duplicate_resume.py
❌ Uses full JSON path
```

### Test Case 3: File Not Found
```
User: "Create a new resume for job posting: NonExistent.md"

Expected:
✅ Agent detects file not found error
✅ Suggests listing available files
✅ Provides specific, actionable suggestions

Phase 2 Expected:
✅ Automatically lists available files
✅ Shows results to user
✅ Suggests using existing file
```

## Summary

**Key Principle**: 
- **"Create new resume"** = `duplicate_resume.py` (editable JSON)
- **"Export/generate HTML"** = `tailor.py` (final output)

**Workflow**:
1. Duplicate → 2. Edit (optional) → 3. Export (optional)

**Self-Correction**:
- Phase 1: Suggests fixes ✅
- Phase 2: Executes fixes automatically 🚀

