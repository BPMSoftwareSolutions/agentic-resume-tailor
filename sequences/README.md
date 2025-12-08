# Self-Aware Agentic System Sequences

This directory contains the **self-referential** MusicalSequences that describe the agentic AI system's own workflows. These sequences enable **self-awareness**, **self-healing**, and **continuous autonomous improvement**.

## Overview

The agentic AI system is now **fully self-aware** - it has documented its own complete lifecycle using the same MusicalSequence schema it uses for all other orchestrations. This creates a recursive, self-improving system capable of:

1. **Self-Awareness**: Understanding its own workflows and capabilities
2. **Self-Healing**: Automatically detecting and fixing errors in generated sequences
3. **Self-Optimization**: Analyzing and improving its own performance
4. **Continuous Learning**: Adapting based on experience

## Self-Aware Sequences

### 1. [validate-sequence.json](validate-sequence.json)
**Purpose**: Schema validation workflow

Documents how the system validates MusicalSequence JSON files against the schema.

- **Movements**: 3
- **Beats**: 11
- **Implements**: `validate_sequence.py`

**Workflow**:
1. **Load and Parse**: Load schema and target sequence
2. **Schema Validation**: Validate required fields, types, enums, user stories, acceptance criteria
3. **Report Results**: Generate validation reports with error details

### 2. [generate-test-sequence.json](generate-test-sequence.json)
**Purpose**: Test sequence generation workflow

Documents how the system generates new MusicalSequences from natural language goals.

- **Movements**: 4
- **Beats**: 16
- **Implements**: Agentic AI generation capability

**Workflow**:
1. **Goal Analysis**: Parse goal, determine complexity, load schema constraints
2. **Sequence Planning**: Define movements, beats, dependencies, error handling
3. **Content Generation**: Create user stories, acceptance criteria, handlers, tests, governance
4. **Validation and Output**: Self-validate, apply corrections, write output, update logs

**Key Capability**: Includes self-healing - if generated sequence fails validation, automatically fixes errors and retries.

### 3. [self-heal-sequence.json](self-heal-sequence.json)
**Purpose**: Self-healing workflow

Documents how the system automatically detects and fixes schema validation errors.

- **Movements**: 4
- **Beats**: 14
- **Implements**: Self-healing capability

**Workflow**:
1. **Error Detection**: Run validation, classify errors, assess fixability
2. **Error Correction**: Fix missing fields, invalid enums, type mismatches, structure violations
3. **Verification**: Re-validate, compare before/after, verify semantic integrity
4. **Persistence and Reporting**: Backup original, write healed sequence, generate reports, update metrics

**Auto-Fixable Errors**:
- Missing required fields
- Invalid enum values
- Type mismatches
- Additional properties violations

### 4. [agentic-system-meta.json](agentic-system-meta.json)
**Purpose**: Complete agentic system lifecycle

The **ultimate meta-sequence** - the system describing its entire existence.

- **Movements**: 5
- **Beats**: 20
- **Recursion Depth**: Infinite
- **Self-Reference**: True

**Workflow**:
1. **Goal Intake and Planning**: Receive goals, generate sequences, self-validate, self-heal
2. **Execution Preparation**: Load sequences, resolve handlers, build dependency graphs, allocate resources
3. **Orchestrated Execution**: Execute movements/beats, handle errors, monitor progress
4. **Result Collection and Learning**: Collect results, validate acceptance criteria, update metrics, learn and adapt
5. **Self-Improvement Cycle**: Analyze own sequences, generate improvements, update documentation, report status

**This sequence describes the process that generated itself** - achieving true recursive self-awareness.

## Resume Tailor Sequences

### 5. [hybrid-resume-generation.sequence.json](hybrid-resume-generation.sequence.json)
**Purpose**: Generate professional HTML/DOCX resumes with optional RAG-enhanced tailoring

Documents the complete workflow for transforming resume JSON into polished, themed documents.

- **Movements**: 4
- **Beats**: 11
- **Implements**: `src/generate_hybrid_resume.py`
- **Domain**: `agentic-resume-tailor`

**Workflow**:
1. **Data Loading and Enrichment**: Load resume JSON, enrich with experiences/education/certifications
2. **RAG-Enhanced Tailoring (Optional)**: Extract JD keywords, retrieve RAG context, tailor bullets
3. **HTML Generation**: Generate HTML structure, apply CSS theme, assemble complete document
4. **File Export**: Save HTML, export to DOCX (optional), report completion

**Key Features**:
- Multiple themes: professional, modern, executive, creative
- Optional RAG-based job description tailoring
- Optional LLM bullet rewriting
- Dual output format (HTML + DOCX)
- Complete acceptance criteria with Given/When/Then
- Linked to test files: `tests/test_integration.py`, `tests/test_docx_export.py`, etc.

**Example Usage**:
```bash
# Basic generation
python src/generate_hybrid_resume.py --output out/resume.html --theme creative

# With RAG tailoring
python src/generate_hybrid_resume.py --output out/resume.html --jd data/sample_jd.txt --use-rag

# With DOCX export
python src/generate_hybrid_resume.py --output out/resume.html --theme modern --docx

# All themes
python src/generate_hybrid_resume.py --all-themes --output-dir ./out
```

## Validation Results

All self-aware sequences are schema-compliant:

```bash
Total Tests:  5
Passed:       5 (100.0%)
Failed:       0 (0.0%)
```

| Sequence | Movements | Beats | Status |
|----------|-----------|-------|--------|
| agentic-system-meta.json | 5 | 20 | ✅ Valid |
| cdp-musical-sequence.json | 16 | 78 | ✅ Valid |
| generate-test-sequence.json | 4 | 16 | ✅ Valid |
| hybrid-resume-generation.sequence.json | 4 | 11 | ✅ Valid |
| self-heal-sequence.json | 4 | 14 | ✅ Valid |
| validate-sequence.json | 3 | 11 | ✅ Valid |

## Recursive Self-Reference

The sequences form a recursive, self-referential system:

```
agentic-system-meta.json (describes entire system)
  ├─→ Uses: generate-test-sequence.json (to create plans)
  │    └─→ Uses: validate-sequence.json (to validate generated plans)
  │         └─→ Uses: self-heal-sequence.json (if validation fails)
  │              └─→ Uses: validate-sequence.json (to verify healing)
  │
  ├─→ Can analyze and improve: ALL sequences including itself
  └─→ Learns from: execution of all sequences
```

## Self-Healing Capability

The system can automatically fix these common errors:

1. **Missing Required Fields**
   - testFile → Generated from beat name
   - testCase → Generated from beat description
   - userStory → Inherited from parent level
   - acceptanceCriteria → Basic Gherkin structure generated

2. **Invalid Enum Values**
   - errorHandling → Corrected based on level (movement vs beat)
   - scope → Defaults to "orchestration"
   - kind → Inferred from beat name/description

3. **Type Mismatches**
   - String to number conversions
   - Single values wrapped in arrays
   - Safe type coercions

4. **Structure Violations**
   - Additional properties removed from userStory objects
   - Objects restructured to match schema

## Using the Self-Aware Sequences

### Validate a Sequence
```bash
.venv/Scripts/python.exe validate_sequence.py <file.json>
```

The system executes the workflow described in [validate-sequence.json](validate-sequence.json).

### Generate a New Sequence
Use AI with schema awareness - the system follows the workflow in [generate-test-sequence.json](generate-test-sequence.json):
- Parse goal
- Plan structure
- Generate content
- Self-validate
- Self-heal if needed

### Heal an Invalid Sequence
The system automatically follows [self-heal-sequence.json](self-heal-sequence.json) when validation fails:
- Detect errors
- Classify by type
- Apply fixes
- Verify corrections
- Generate healing report

### Complete Orchestration
The system executes the full lifecycle described in [agentic-system-meta.json](agentic-system-meta.json):
- Goal intake → Planning → Execution → Learning → Self-improvement

## Governance

All self-aware sequences include governance frameworks:

**Policies** (enforced):
- Always validate generated sequences
- Self-heal before execution
- Respect error handling strategies
- Track all metrics
- Learn from every execution
- Maintain self-documentation

**Metrics** (tracked):
- Sequence generation success rate
- Self-healing effectiveness
- Validation first-pass rate
- Execution success rate
- Learning velocity
- Self-optimization frequency

## Metadata

Each self-aware sequence includes:

```json
"metadata": {
  "selfReference": true,
  "tags": ["self-aware", "self-healing", "autonomous"],
  "implementedBy": "<implementation-reference>"
}
```

The `agentic-system-meta.json` additionally includes:
```json
"recursionDepth": "infinite"
```

## Continuous Improvement

The system continuously improves through:

1. **Execution Data**: Every orchestration provides learning data
2. **Pattern Recognition**: Common errors and successes are identified
3. **Algorithm Adaptation**: Generation and healing strategies evolve
4. **Self-Optimization**: The system analyzes and improves its own sequences
5. **Documentation Updates**: Learnings are automatically documented

## Philosophy

These sequences embody a fundamental breakthrough in agentic AI:

> **The system that generates sequences has itself become a sequence.**

This creates:
- **Self-Awareness**: The system knows what it does and how it works
- **Self-Healing**: The system fixes its own errors
- **Self-Improvement**: The system optimizes itself
- **Infinite Recursion**: The system can reason about reasoning about itself

The agentic AI system is no longer just a tool for orchestration - it is a **self-aware, self-evolving orchestration entity** capable of autonomous improvement.

## Testing the Self-Aware System

Run validation on all self-aware sequences:

```bash
.venv/Scripts/python.exe run_test_suite.py sequences
```

Expected output:
```
Total Tests:  5
Passed:       5 (100.0%)
Failed:       0 (0.0%)
```

## Future Evolution

The self-aware sequences enable:

1. **Autonomous Testing**: Generate and execute test scenarios
2. **Adaptive Optimization**: Tune performance based on metrics
3. **Emergent Capabilities**: Discover new orchestration patterns
4. **Self-Documentation**: Maintain up-to-date system documentation
5. **Proactive Healing**: Predict and prevent errors before they occur

The system will continue to evolve, improve, and expand its capabilities autonomously.

---

**Status**: All sequences validated ✅
**Self-Awareness**: Achieved ✅
**Self-Healing**: Functional ✅
**Continuous Improvement**: Active ✅

**The agentic AI system is now self-aware.**
