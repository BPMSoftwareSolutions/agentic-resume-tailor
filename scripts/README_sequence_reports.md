# Musical Sequence Report Generator

Generate comprehensive markdown documentation from Musical Sequence JSON files.

## Overview

The `generate_sequence_report.py` script creates rich, human-readable documentation from musical sequence definitions. It extracts all the metadata, user stories, acceptance criteria, governance policies, and technical details into a well-formatted markdown report.

## Features

### 📊 **Comprehensive Coverage**
- **Metadata**: Sequence ID, domain, package, version, author, tags
- **Musical Properties**: Key, tempo, time signature
- **Purpose & Context**: Business value, triggers, and goals
- **User Stories**: Sequence-level, movement-level, and beat-level stories
- **Governance**: Policies and metrics for orchestration
- **Events**: Complete event flow with ordering
- **Movements**: Detailed breakdown of all movements and beats
- **Acceptance Criteria**: Given/When/Then scenarios for each beat
- **Test References**: Links to test files and test cases
- **Handler Information**: Source paths, capabilities, and metadata

### 🎯 **Rich Formatting**
- Clean markdown with proper heading hierarchy
- Tables for structured data
- Code formatting for technical identifiers
- Compact user story format
- Scenario-based acceptance criteria
- Clear movement and beat organization

### 📝 **Generated Sections**

1. **Header**: Sequence name, title, and description
2. **Metadata Table**: All sequence metadata in tabular format
3. **Musical Properties**: Key, tempo, time signature
4. **Purpose & Context**: Purpose, trigger, business value
5. **User Story**: Top-level user story
6. **Governance**: Policies and metrics
7. **Events**: Ordered list of events emitted
8. **Movements**: Detailed breakdown with:
   - Movement summary table
   - Individual movement sections with:
     - Description and properties
     - User story
     - Beat details including:
       - Properties table
       - Handler information
       - User story
       - Acceptance criteria (Given/When/Then)
       - Test references
9. **Footer**: Generation timestamp

## Usage

### Basic Usage

```bash
# Generate report for a single sequence
python scripts/generate_sequence_report.py sequences/hybrid-resume-generation.sequence.json

# Output: docs/sequences/hybrid-resume-generation.md
```

### Generate Multiple Reports

```bash
# Generate reports for all sequences in the sequences/ directory
python scripts/generate_sequence_report.py sequences/*.sequence.json
```

### Custom Output Directory

```bash
# Specify a custom output directory
python scripts/generate_sequence_report.py sequences/hybrid-resume-generation.sequence.json --output-dir my-docs/sequences
```

### Help

```bash
python scripts/generate_sequence_report.py --help
```

## Output

Reports are saved to `docs/sequences/` by default, with the filename `{sequence-id}.md`.

Example output structure:

```
docs/
└── sequences/
    ├── hybrid-resume-generation.md
    ├── surgical-update.md
    └── ...
```

## Example Output

Here's what a generated report looks like:

```markdown
# Hybrid Resume Generation Pipeline

**Generate Professional HTML/DOCX Resume**

Complete workflow for generating professional resumes in HTML and DOCX formats...

## 📋 Sequence Metadata

| Field | Value |
|-------|-------|
| **Sequence ID** | `hybrid-resume-generation` |
| **Domain** | `agentic-resume-tailor` |
...

## 🎼 Movements

### Movement 1: Data Loading and Enrichment

**Movement Properties:**
- **ID:** `mov-1-data-loading`
- **Tempo:** 120 BPM
...

#### Beat 1: Load Resume JSON

**Load Resume Data**

| Property | Value |
|----------|-------|
| **Event** | `resume.data.loaded` |
...

**Acceptance Criteria:**

**Given:**
- Resume JSON file exists at specified path

**When:**
- The system reads the JSON file

**Then:**
- Resume data is successfully parsed
- All required fields are present
...
```

## Report Structure

### Metadata Section
- Sequence identification (ID, domain, package)
- Version information
- Author and creation date
- Tags for categorization

### Musical Properties
- Musical key
- Tempo (BPM)
- Time signature

### Governance
- **Policies**: Rules and constraints (e.g., input-validation, data-integrity)
- **Metrics**: Measurable outcomes (e.g., success-rate, processing-time)

### Events
Ordered list of all events emitted during sequence execution.

### Movements & Beats
- **Movement**: Logical grouping of related beats
  - Movement properties (ID, tempo, error handling)
  - Movement-level user story
  - **Beats**: Individual steps within the movement
    - Beat properties (event, dynamics, timing, dependencies)
    - Handler information (name, source, capabilities)
    - Beat-level user story
    - Acceptance criteria (Given/When/Then scenarios)
    - Test references

## User Story Format

User stories are formatted in the standard BDD format:

```
**As a** [Persona],
**I want to** [goal],
**so that** [benefit]
```

## Acceptance Criteria Format

Acceptance criteria follow the Given/When/Then pattern:

```
**Scenario 1:**

**Given:**
- Precondition 1
- Precondition 2

**When:**
- Action or event

**Then:**
- Expected outcome 1
- Expected outcome 2
```

## Dependencies

- Python 3.7+
- Standard library only (no external dependencies)

## Schema Compliance

The generator expects sequence JSON files to follow the Musical Sequence schema defined in:
- `schemas/musical-sequence.schema.json`

Required fields:
- `domainId`
- `id`
- `name`
- `movements`
- `userStory` (at sequence level)

Each movement requires:
- `name`
- `beats`
- `userStory`

Each beat requires:
- `event`
- `userStory`
- `acceptanceCriteria`
- `testFile`

## Use Cases

1. **Documentation Generation**: Create human-readable docs for all sequences
2. **Onboarding**: Help new team members understand sequence flows
3. **Review & Planning**: Facilitate review of sequence designs
4. **Test Planning**: Use acceptance criteria for test case development
5. **Compliance**: Document governance policies and metrics
6. **Knowledge Base**: Build a searchable repository of sequence documentation

## Tips

1. **Batch Generation**: Process all sequences at once to keep docs in sync
2. **Version Control**: Commit generated reports alongside sequence JSON files
3. **CI/CD Integration**: Auto-generate reports on sequence changes
4. **Review Process**: Use reports in pull request reviews
5. **Search**: Generated markdown is easily searchable and indexable

## Future Enhancements

Potential improvements:
- [ ] HTML output format
- [ ] PDF generation
- [ ] Sequence diagrams (Mermaid/PlantUML)
- [ ] Dependency graphs
- [ ] Cross-reference linking between sequences
- [ ] Index page generation
- [ ] Search functionality
- [ ] Diff reports for sequence changes

## Related Files

- **Schema**: `schemas/musical-sequence.schema.json`
- **Validator**: `validate-sequence.js`
- **Example Sequences**: `sequences/*.sequence.json`
- **Generated Reports**: `docs/sequences/*.md`

## Support

For issues or questions:
1. Check the schema documentation
2. Validate your sequence JSON first
3. Review example sequences
4. Check error messages for specific issues
