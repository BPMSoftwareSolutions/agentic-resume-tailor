# Musical Sequences for Agentic Resume Tailor

## Overview

This document describes the Musical Sequence orchestration framework for the Agentic Resume Tailor project. Musical Sequences provide a structured, testable, and self-documenting way to define workflow orchestrations.

## What are Musical Sequences?

Musical Sequences use musical metaphors to make complex workflows more intuitive and manageable:

| Musical Term | Workflow Meaning | Example |
|--------------|-----------------|---------|
| **Sequence** | Complete workflow/orchestration | "Hybrid Resume Generation" |
| **Movement** | Major phase of the workflow | "Data Loading", "HTML Generation" |
| **Beat** | Individual step/action | "Load Resume JSON", "Generate CSS" |
| **Tempo** | Processing speed (BPM) | 120 BPM = normal pace |
| **Dynamics** | Priority/importance level | f = forte (high priority) |
| **Key** | Organizational context | "C major" |

## Schema

All sequences conform to the canonical schema: [schemas/musical-sequence.schema.json](../schemas/musical-sequence.schema.json)

The schema enforces:
- Required fields at all levels (sequence, movement, beat)
- User stories with persona, goal, and benefit
- Acceptance criteria in Given/When/Then format
- Handler references with source paths
- Test file linkage for traceability

## Benefits

1. **Self-Documenting**: Every beat includes user stories and acceptance criteria
2. **Testable**: Each beat links to test files and test cases
3. **Traceable**: Clear dependencies between beats
4. **Maintainable**: Structured format makes changes easy
5. **Governable**: Built-in policies and metrics
6. **Executable**: Can be executed by orchestration engines

## Current Sequences

### 1. Hybrid Resume Generation

**File**: [sequences/hybrid-resume-generation.sequence.json](../sequences/hybrid-resume-generation.sequence.json)

**Purpose**: Transform resume JSON data into polished, themed HTML/DOCX documents

**Implementation**: [src/generate_hybrid_resume.py](../src/generate_hybrid_resume.py)

**Structure**:
- **4 Movements**
- **11 Beats**
- **Status**: Active ✅

#### Movement 1: Data Loading and Enrichment (2 beats)

1. **Load Resume JSON** - Parse resume data from JSON file
   - Validates required fields (name, title, experience)
   - Tests: `tests/test_integration.py`

2. **Enrich with Experiences** - Add education, certifications, and tags
   - Loads from `data/experiences.json`
   - Extracts education (id starts with 'edu-')
   - Extracts certifications (id starts with 'cert-')
   - Adds skill tags to experience entries

#### Movement 2: RAG-Enhanced Tailoring (Optional) (3 beats)

3. **Extract JD Keywords** - Parse job description for relevant terms
   - Normalizes keywords to lowercase
   - Tests: `tests/test_jd_parser.py`

4. **Retrieve RAG Context** - Query vector store for relevant experiences
   - Uses `data/rag/vector_store.json`
   - Tests: `tests/test_rag_integration.py`

5. **Tailor Experience Bullets** - Select and rewrite bullets for job
   - Scores bullets by keyword relevance
   - Optional LLM rewriting
   - Tests: `tests/test_tailor_bullets.py`

#### Movement 3: HTML Generation (3 beats)

6. **Generate HTML Structure** - Convert JSON to semantic HTML
   - Creates sections: header, summary, experience, education
   - Tests: `tests/test_integration.py`

7. **Generate Theme CSS** - Apply theme styles
   - Themes: professional, modern, executive, creative
   - Responsive and print-friendly
   - Tests: `tests/test_visual_appearance_validation.py`

8. **Assemble Complete HTML** - Combine structure and styles
   - Valid HTML5 document
   - Includes metadata and title
   - Tests: `tests/test_integration.py`

#### Movement 4: File Export (3 beats)

9. **Save HTML File** - Write document to disk
   - UTF-8 encoding
   - Browser-ready output
   - Tests: `tests/test_integration.py`

10. **Export to DOCX** - Convert to Word format (optional)
    - Preserves content and formatting
    - Tests: `tests/test_docx_export.py`

11. **Report Generation Complete** - Display summary
    - Shows file paths, theme, options used
    - Tests: `tests/test_integration.py`

**Usage Examples**:

```bash
# Basic generation with creative theme
python src/generate_hybrid_resume.py --output out/resume.html --theme creative

# With RAG-enhanced tailoring
python src/generate_hybrid_resume.py \
  --output out/resume.html \
  --jd data/sample_jd.txt \
  --use-rag \
  --theme modern

# With DOCX export
python src/generate_hybrid_resume.py \
  --output out/resume.html \
  --theme professional \
  --docx

# Generate all themes
python src/generate_hybrid_resume.py \
  --all-themes \
  --output-dir ./out
```

## Sequence Structure

### Top Level Properties

```json
{
  "domainId": "agentic-resume-tailor",
  "id": "hybrid-resume-generation",
  "name": "Hybrid Resume Generation Pipeline",
  "title": "Generate Professional HTML/DOCX Resume",
  "description": "Complete workflow for generating professional resumes...",
  "purpose": "Transform resume JSON data into polished documents...",
  "trigger": "User executes generate_hybrid_resume.py...",
  "packageName": "agentic-resume-tailor",
  "kind": "orchestration",
  "status": "active",
  "key": "C major",
  "tempo": 120,
  "timeSignature": "4/4",
  "category": "document-generation",
  "beats": 11
}
```

### Governance

Each sequence includes governance metadata:

```json
{
  "governance": {
    "policies": [
      "input-validation",
      "data-integrity",
      "output-quality"
    ],
    "metrics": [
      "generation-success-rate",
      "processing-time",
      "theme-consistency"
    ]
  }
}
```

### User Stories

Every level (sequence, movement, beat) includes a user story:

```json
{
  "userStory": {
    "persona": "Job Seeker",
    "goal": "generate a professional resume in HTML and DOCX formats",
    "benefit": "I can apply to jobs with a polished, tailored resume"
  }
}
```

### Acceptance Criteria

Each beat includes structured acceptance criteria:

```json
{
  "acceptanceCriteria": [
    {
      "given": ["Resume JSON file exists at specified path"],
      "when": ["The system reads the JSON file"],
      "then": [
        "Resume data is successfully parsed",
        "All required fields are present",
        "Data structure is valid"
      ]
    }
  ]
}
```

### Handler References

Beats reference handler functions with metadata:

```json
{
  "handler": {
    "name": "generate_hybrid_resume#load_resume_data",
    "scope": "orchestration",
    "kind": "automation",
    "sourcePath": "src/generate_hybrid_resume.py",
    "handlerCapabilities": ["build", "validate"]
  }
}
```

**Handler Scopes**:
- `plugin` - Plugin-level handlers
- `orchestration` - Orchestration handlers
- `system` - System-level handlers
- `policy` - Policy enforcement handlers

**Handler Kinds**:
- `validation` - Data/schema validation
- `orchestration` - Workflow coordination
- `reporting` - Status/metrics reporting
- `policy-enforcement` - Policy checks
- `metrics` - Metrics collection
- `automation` - Automated tasks

**Handler Capabilities**:
- `audit` - Audit trail generation
- `build` - Build/transform data
- `deploy` - Deploy/save artifacts
- `report` - Generate reports
- `validate` - Validate data
- `measure` - Collect measurements
- `learn` - Machine learning
- `rollback` - Rollback changes

## Validation

### Automated Validation

We provide two validation methods:

#### Node.js Validation Script

```bash
node validate-sequence.js
```

This script validates:
- JSON is well-formed
- All required fields are present
- User stories have persona/goal/benefit
- Acceptance criteria exist

#### Python Test Suite

```bash
python -m pytest tests/test_sequence_validation.py -v
```

This comprehensive test suite validates:
- JSON Schema compliance
- Required fields at all levels
- User story structure
- Acceptance criteria format
- Handler reference validity
- Enum values
- Data types

### Validation Results

```
✓✓✓ All validations passed! ✓✓✓

=== Sequence Information ===
ID: hybrid-resume-generation
Domain: agentic-resume-tailor
Name: Hybrid Resume Generation Pipeline
Status: active
Movements: 4
  Movement 1: Data Loading and Enrichment (2 beats)
  Movement 2: RAG-Enhanced Tailoring (Optional) (3 beats)
  Movement 3: HTML Generation (3 beats)
  Movement 4: File Export (3 beats)
Total beats: 11

✓ All required top-level fields present
✓ All movements have required fields
✓ All beats have required fields
✓ All user stories have required fields (persona, goal, benefit)
```

## Creating New Sequences

When creating a new sequence:

1. **Start with the schema**: Reference [schemas/musical-sequence.schema.json](../schemas/musical-sequence.schema.json)

2. **Define the workflow**:
   - Break into major movements (phases)
   - Identify individual beats (steps)
   - Map dependencies between beats

3. **Write user stories** at all levels:
   - Sequence-level: Overall value proposition
   - Movement-level: Phase-specific value
   - Beat-level: Step-specific value

4. **Define acceptance criteria**:
   - Use Given/When/Then format
   - Be specific and testable
   - Cover edge cases

5. **Link to tests**:
   - Reference existing test files
   - Create new tests if needed

6. **Add handler references**:
   - Include sourcePath
   - Specify scope and kind
   - List capabilities

7. **Validate**:
   ```bash
   node validate-sequence.js
   python -m pytest tests/test_sequence_validation.py -v
   ```

## Planned Sequences

### 2. Tailor Resume from URL

**Status**: Planned

Transform a job URL into a tailored resume in one command.

**Movements**:
1. Job Listing Fetch
2. Resume Building from Experience Log
3. Intelligent Tailoring
4. Multi-Format Export

### 3. Intelligent CRUD Orchestration

**Status**: Planned

Automatically update resumes based on job analysis.

**Movements**:
1. Job Posting Analysis
2. Resume Gap Analysis
3. CRUD Operation Generation
4. Automated Updates

### 4. Job Posting Analysis

**Status**: Planned

Extract structured data from job postings.

**Movements**:
1. Content Extraction
2. Skill Categorization
3. Requirement Analysis
4. Structured Output

## Integration with CI/CD

Musical Sequences integrate with the existing CI/CD pipeline:

```yaml
# .github/workflows/ci.yml (example)
- name: Validate Sequences
  run: |
    node validate-sequence.js
    python -m pytest tests/test_sequence_validation.py -v
```

## Best Practices

1. **Keep beats atomic**: Each beat should do one thing well
2. **Use clear names**: Descriptive names for sequences, movements, and beats
3. **Write complete user stories**: Always include persona, goal, and benefit
4. **Define comprehensive acceptance criteria**: Cover normal and edge cases
5. **Link to tests**: Every beat should reference a test file
6. **Use proper error handling**: Choose `continue` or `abort-sequence` wisely
7. **Document dependencies**: Explicitly list beat dependencies
8. **Version sequences**: Track changes in metadata.version

## Troubleshooting

### Validation Fails

1. Check JSON syntax with `node -e "JSON.parse(require('fs').readFileSync('file.json'))"`
2. Review error messages from validation script
3. Compare against schema: [schemas/musical-sequence.schema.json](../schemas/musical-sequence.schema.json)
4. Check required fields are present
5. Verify enum values are valid

### Test References Don't Match

1. Ensure test files exist at specified paths
2. Update test files if implementation changed
3. Create new tests for new functionality

### Handler References Invalid

1. Verify sourcePath points to actual file
2. Check scope and kind are valid enum values
3. Ensure capabilities are valid

## Resources

- **Schema**: [schemas/musical-sequence.schema.json](../schemas/musical-sequence.schema.json)
- **Sequences**: [sequences/](../sequences/)
- **Tests**: [tests/test_sequence_validation.py](../tests/test_sequence_validation.py)
- **Validation Script**: [validate-sequence.js](../validate-sequence.js)
- **Main README**: [README.md](../README.md)

## Appendix: Complete Example

See [sequences/hybrid-resume-generation.sequence.json](../sequences/hybrid-resume-generation.sequence.json) for a complete, production-ready example.

Key highlights:
- 4 movements with clear separation of concerns
- 11 beats with atomic, testable actions
- Complete user stories at all levels
- Comprehensive acceptance criteria
- Linked to 5+ test files
- Full handler references with source paths
- Governance policies and metrics
- Valid against schema ✅

---

**Questions?** See [sequences/README.md](../sequences/README.md) or review the schema documentation.
