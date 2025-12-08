# Hybrid Resume Generation Pipeline

**Generate Professional HTML/DOCX Resume**

Complete workflow for generating professional resumes in HTML and DOCX formats with optional RAG-enhanced tailoring

---

## 📋 Sequence Metadata

| Field | Value |
|-------|-------|
| **Sequence ID** | `hybrid-resume-generation` |
| **Domain** | `agentic-resume-tailor` |
| **Package** | `agentic-resume-tailor` |
| **Kind** | `orchestration` |
| **Status** | `active` |
| **Category** | `document-generation` |
| **Total Beats** | 12 |
| **Version** | 1.0.0 |
| **Author** | Agentic Resume Tailor Team |
| **Created** | 2025-12-07 |

**Tags:** `resume`, `generation`, `html`, `docx`, `rag`, `tailoring`

## 🎵 Musical Properties

| Property | Value |
|----------|-------|
| **Key** | C major |
| **Tempo** | 120 BPM |
| **Time Signature** | 4/4 |

## 🎯 Purpose & Context

### Purpose
Transform resume JSON data into polished, themed HTML/DOCX documents ready for job applications

### Trigger
**Event:** User executes generate_hybrid_resume.py with resume JSON input

### Business Value
Enables rapid creation of professional resumes with consistent branding and formatting across multiple output formats

## 👤 User Story

**As a** Job Seeker  
**I want to** generate a professional, visually appealing resume in HTML and DOCX formats  
**So that** I can apply to jobs with a polished, tailored resume that stands out

## 🛡️ Governance

### Policies

- `input-validation`
- `data-integrity`
- `output-quality`

### Metrics

- `generation-success-rate`
- `processing-time`
- `theme-consistency`

## 📡 Events

This sequence emits the following events in order:

1. `resume.data.loaded`
2. `experiences.enriched`
3. `jd.ingested`
4. `jd.keywords.extracted`
5. `rag.context.retrieved`
6. `rag.tailoring.applied`
7. `html.structure.generated`
8. `css.theme.applied`
9. `html.document.assembled`
10. `file.saved`
11. `docx.exported`
12. `generation.complete`

## 🎼 Movements

This sequence consists of 4 movements:

| # | Movement | Beats | Error Handling | Status |
|---|----------|-------|----------------|--------|
| 1 | Data Loading and Enrichment | 2 | `abort-sequence` | `active` |
| 2 | RAG-Enhanced Tailoring (Optional) | 4 | `continue` | `active` |
| 3 | HTML Generation | 3 | `abort-sequence` | `active` |
| 4 | File Export | 3 | `abort-sequence` | `active` |

---

### Movement 1: Data Loading and Enrichment

Load resume JSON and enrich with experiences, education, and certifications

**Movement Properties:**

- **ID:** `mov-1-data-loading`
- **Tempo:** 120 BPM
- **Error Handling:** `abort-sequence`
- **Status:** `active`

**User Story:**

**As a** Job Seeker, **I want to** have my complete resume data loaded and enriched from all sources, **so that** all my experience, education, and certifications are included in the final resume

**Beats (2):**

#### Beat 1: Load Resume JSON

**Load Resume Data**

Read and parse the resume JSON file from the specified input path

| Property | Value |
|----------|-------|
| **Event** | `resume.data.loaded` |
| **Dynamics** | `f` |
| **Timing** | `sync` |
| **Error Handling** | `abort-sequence` |

**Handler:**

- **Name:** `generate_hybrid_resume#load_resume_data`
- **Source:** `src/generate_hybrid_resume.py`
- **Capabilities:** `build`, `validate`

**User Story:**

**As a** Job Seeker, **I want to** load my resume data from JSON, **so that** the system has access to all my professional information

**Acceptance Criteria:**

**Given:**
- Resume JSON file exists at specified path

**When:**
- The system reads the JSON file

**Then:**
- Resume data is successfully parsed
- All required fields are present (name, title, experience)
- Data structure is valid

**Tests:**

- **Test File:** `tests/test_integration.py`
- **Test Case:** `test_complete_pipeline - resume loading`


#### Beat 2: Enrich with Experiences

**Load Experience Log Data**

Load experiences.json to enrich resume with education, certifications, and tags

| Property | Value |
|----------|-------|
| **Event** | `experiences.enriched` |
| **Dynamics** | `mf` |
| **Timing** | `sync` |
| **Error Handling** | `continue` |
| **Dependencies** | `resume.data.loaded` |

**Handler:**

- **Name:** `generate_hybrid_resume#enrich_from_experiences`
- **Source:** `src/generate_hybrid_resume.py`
- **Capabilities:** `build`

**User Story:**

**As a** Job Seeker, **I want to** have my resume enriched with education, certifications, and skill tags, **so that** my resume includes all relevant credentials and categorized skills

**Acceptance Criteria:**

**Scenario 1:**

**Given:**
- experiences.json exists in data directory

**When:**
- The system loads the experience log

**Then:**
- Education entries (id starts with 'edu-') are extracted
- Certification entries (id starts with 'cert-') are extracted
- Experience tags (skills, technologies, techniques, principles) are added
- Duplicate tags are removed while preserving order

**Scenario 2:**

**Given:**
- experiences.json does not exist

**When:**
- The system attempts to load it

**Then:**
- Processing continues without enrichment
- Original resume data is preserved

**Tests:**

- **Test File:** `tests/test_experience_log.py`
- **Test Case:** `Experience log enrichment`


---

### Movement 2: RAG-Enhanced Tailoring (Optional)

Apply RAG-based tailoring to customize resume for specific job description

**Movement Properties:**

- **ID:** `mov-2-rag-tailoring`
- **Tempo:** 100 BPM
- **Error Handling:** `continue`
- **Status:** `active`

**User Story:**

**As a** Job Seeker, **I want to** have my resume automatically tailored to match a specific job description, **so that** my resume highlights the most relevant experience and skills for the job

**Beats (4):**

#### Beat 3: Ingest Job Description

**Fetch or Load Job Description**

Load JD from local file or fetch from URL, then save to job_listings directory

| Property | Value |
|----------|-------|
| **Event** | `jd.ingested` |
| **Dynamics** | `mf` |
| **Timing** | `sync` |
| **Error Handling** | `abort-sequence` |
| **Dependencies** | `experiences.enriched` |

**Handler:**

- **Name:** `jd_fetcher#ingest_jd`
- **Source:** `src/jd_fetcher.py`
- **Capabilities:** `build`, `validate`

**User Story:**

**As a** Job Seeker, **I want to** have the job description loaded from URL or local file, **so that** the system can access the JD content for keyword extraction and tailoring

**Acceptance Criteria:**

**Scenario 1:**

**Given:**
- JD source is a URL

**When:**
- The system fetches the JD

**Then:**
- HTML is downloaded with proper user-agent headers
- HTML is parsed to extract text content
- Extracted text is validated (minimum 100 characters)
- JD is saved to data/job_listings/ directory with slug filename
- File path and content are returned

**Scenario 2:**

**Given:**
- JD source is a local file path

**When:**
- The system loads the file

**Then:**
- File existence is verified
- File content is read with UTF-8 encoding
- If not in job_listings/ directory, file is copied there
- File path and content are returned

**Tests:**

- **Test File:** `tests/test_jd_fetcher.py`
- **Test Case:** `test_ingest_jd`


#### Beat 4: Extract JD Keywords

**Extract Job Description Keywords**

Parse job description and extract relevant keywords and skills

| Property | Value |
|----------|-------|
| **Event** | `jd.keywords.extracted` |
| **Dynamics** | `mf` |
| **Timing** | `sync` |
| **Error Handling** | `continue` |
| **Dependencies** | `jd.ingested` |

**Handler:**

- **Name:** `jd_parser#extract_keywords`
- **Source:** `src/jd_parser.py`
- **Capabilities:** `validate`

**User Story:**

**As a** Job Seeker, **I want to** have keywords extracted from the job description, **so that** the system knows what skills and experience to emphasize

**Acceptance Criteria:**

**Given:**
- Job description file is provided via --jd flag
- RAG is enabled via --use-rag flag

**When:**
- The system parses the job description

**Then:**
- Keywords are extracted and normalized (lowercase)
- Technical terms are identified
- Skills and requirements are cataloged

**Tests:**

- **Test File:** `tests/test_jd_parser.py`
- **Test Case:** `test_extract_keywords`


#### Beat 5: Retrieve RAG Context

**Retrieve Relevant RAG Context**

Query vector store to retrieve relevant experience context for each keyword

| Property | Value |
|----------|-------|
| **Event** | `rag.context.retrieved` |
| **Dynamics** | `mf` |
| **Timing** | `sync` |
| **Error Handling** | `continue` |
| **Dependencies** | `jd.keywords.extracted` |

**Handler:**

- **Name:** `tailor#retrieve_rag_context`
- **Source:** `src/tailor.py`
- **Capabilities:** `validate`

**User Story:**

**As a** Job Seeker, **I want to** retrieve relevant experience context from the vector store, **so that** the system can intelligently select and rewrite my experience bullets

**Acceptance Criteria:**

**Scenario 1:**

**Given:**
- Vector store exists at specified path
- Keywords have been extracted

**When:**
- The system queries the vector store

**Then:**
- Relevant documents are retrieved for each keyword
- Context includes document content and metadata
- Success status is returned

**Scenario 2:**

**Given:**
- Vector store does not exist

**When:**
- The system attempts to retrieve context

**Then:**
- Warning is displayed
- Processing continues without RAG context
- Original experience bullets are preserved

**Tests:**

- **Test File:** `tests/test_rag_integration.py`
- **Test Case:** `RAG context retrieval`


#### Beat 6: Tailor Experience Bullets

**Apply RAG-Based Tailoring**

Select and optionally rewrite experience bullets using RAG context

| Property | Value |
|----------|-------|
| **Event** | `rag.tailoring.applied` |
| **Dynamics** | `f` |
| **Timing** | `sync` |
| **Error Handling** | `continue` |
| **Dependencies** | `rag.context.retrieved` |

**Handler:**

- **Name:** `tailor#select_and_rewrite`
- **Source:** `src/tailor.py`
- **Capabilities:** `build`

**User Story:**

**As a** Job Seeker, **I want to** have my experience bullets tailored to the job description, **so that** my resume emphasizes the most relevant accomplishments

**Acceptance Criteria:**

**Scenario 1:**

**Given:**
- RAG context has been retrieved
- Experience entries exist in resume

**When:**
- The system applies tailoring

**Then:**
- Experience bullets are scored based on keyword relevance
- Top-scoring bullets are selected
- Bullets are optionally rewritten using LLM (if --use-llm-rewriting)
- Tailored experience is returned

**Scenario 2:**

**Given:**
- RAG tailoring fails

**When:**
- An error occurs during tailoring

**Then:**
- Warning is displayed
- Original resume data is preserved
- Processing continues

**Tests:**

- **Test File:** `tests/test_tailor_bullets.py`
- **Test Case:** `test_select_and_rewrite`


---

### Movement 3: HTML Generation

Generate HTML structure, apply CSS theme, and assemble complete document

**Movement Properties:**

- **ID:** `mov-3-html-generation`
- **Tempo:** 140 BPM
- **Error Handling:** `abort-sequence`
- **Status:** `active`

**User Story:**

**As a** Job Seeker, **I want to** have my resume rendered as a professional HTML document, **so that** I can view and share my resume in a web browser or convert it to PDF

**Beats (3):**

#### Beat 7: Generate HTML Structure

**Process Resume Data to HTML**

Convert resume JSON to structured HTML using HybridResumeProcessor

| Property | Value |
|----------|-------|
| **Event** | `html.structure.generated` |
| **Dynamics** | `f` |
| **Timing** | `sync` |
| **Error Handling** | `abort-sequence` |
| **Dependencies** | `rag.tailoring.applied` |

**Handler:**

- **Name:** `HybridResumeProcessor#generate_html`
- **Source:** `src/hybrid_resume_processor.py`
- **Capabilities:** `build`

**User Story:**

**As a** Job Seeker, **I want to** have my resume data converted to HTML structure, **so that** my resume is properly formatted with semantic HTML

**Acceptance Criteria:**

**Given:**
- Resume data is available
- Theme is specified

**When:**
- HybridResumeProcessor generates HTML

**Then:**
- HTML structure is created with proper sections (header, summary, experience, education, etc.)
- All resume data is included in HTML
- HTML is semantically structured

**Tests:**

- **Test File:** `tests/test_integration.py`
- **Test Case:** `HTML structure validation`


#### Beat 8: Generate Theme CSS

**Generate CSS Theme**

Generate CSS styles based on selected theme (professional, modern, executive, creative)

| Property | Value |
|----------|-------|
| **Event** | `css.theme.applied` |
| **Dynamics** | `mf` |
| **Timing** | `sync` |
| **Error Handling** | `abort-sequence` |
| **Dependencies** | `html.structure.generated` |

**Handler:**

- **Name:** `HybridCSSGenerator#generate_css`
- **Source:** `src/hybrid_css_generator.py`
- **Capabilities:** `build`

**User Story:**

**As a** Job Seeker, **I want to** have my resume styled with a professional theme, **so that** my resume has a polished, visually appealing appearance

**Acceptance Criteria:**

**Given:**
- Theme name is valid (professional, modern, executive, creative)

**When:**
- CSS generator processes the theme

**Then:**
- CSS is generated with theme-specific colors
- Typography is applied consistently
- Layout is responsive and print-friendly
- Theme-specific visual elements are included

**Tests:**

- **Test File:** `tests/test_visual_appearance_validation.py`
- **Test Case:** `Theme CSS validation`


#### Beat 9: Assemble Complete HTML

**Assemble Final HTML Document**

Combine HTML structure and CSS into complete HTML document with metadata

| Property | Value |
|----------|-------|
| **Event** | `html.document.assembled` |
| **Dynamics** | `f` |
| **Timing** | `sync` |
| **Error Handling** | `abort-sequence` |
| **Dependencies** | `css.theme.applied` |

**Handler:**

- **Name:** `HybridHTMLAssembler#assemble_html`
- **Source:** `src/hybrid_html_assembler.py`
- **Capabilities:** `build`

**User Story:**

**As a** Job Seeker, **I want to** have a complete, valid HTML document ready to save, **so that** my resume is ready to be viewed in any web browser

**Acceptance Criteria:**

**Given:**
- HTML structure is generated
- CSS theme is generated

**When:**
- Assembler combines them into final document

**Then:**
- Complete HTML document is created with DOCTYPE
- HTML includes head with metadata and styles
- HTML includes body with resume content
- Document is valid HTML5
- Document title includes resume name

**Tests:**

- **Test File:** `tests/test_integration.py`
- **Test Case:** `Complete HTML document validation`


---

### Movement 4: File Export

Save HTML file and optionally export to DOCX format

**Movement Properties:**

- **ID:** `mov-4-export`
- **Tempo:** 110 BPM
- **Error Handling:** `abort-sequence`
- **Status:** `active`

**User Story:**

**As a** Job Seeker, **I want to** have my resume saved in HTML and optionally DOCX formats, **so that** I can submit my resume in the format required by employers

**Beats (3):**

#### Beat 10: Save HTML File

**Write HTML to File**

Save the complete HTML document to the specified output path

| Property | Value |
|----------|-------|
| **Event** | `file.saved` |
| **Dynamics** | `f` |
| **Timing** | `sync` |
| **Error Handling** | `abort-sequence` |
| **Dependencies** | `html.document.assembled` |

**Handler:**

- **Name:** `HybridHTMLAssembler#save_html`
- **Source:** `src/hybrid_html_assembler.py`
- **Capabilities:** `deploy`

**User Story:**

**As a** Job Seeker, **I want to** have my HTML resume saved to disk, **so that** I can open and view my resume in a web browser

**Acceptance Criteria:**

**Given:**
- Complete HTML document is ready
- Output path is specified

**When:**
- System saves HTML to file

**Then:**
- HTML file is created at specified path
- File is encoded as UTF-8
- File can be opened in any web browser
- Success status is returned

**Tests:**

- **Test File:** `tests/test_integration.py`
- **Test Case:** `HTML file save validation`


#### Beat 11: Export to DOCX

**Convert HTML to DOCX**

Convert the HTML resume to DOCX format using DOCXResumeExporter (if --docx flag is set)

| Property | Value |
|----------|-------|
| **Event** | `docx.exported` |
| **Dynamics** | `mf` |
| **Timing** | `sync` |
| **Error Handling** | `continue` |
| **Dependencies** | `file.saved` |

**Handler:**

- **Name:** `DOCXResumeExporter#export_to_docx`
- **Source:** `src/docx_resume_exporter.py`
- **Capabilities:** `deploy`

**User Story:**

**As a** Job Seeker, **I want to** have my resume exported to DOCX format, **so that** I can submit my resume to employers who require Word documents

**Acceptance Criteria:**

**Scenario 1:**

**Given:**
- --docx flag is set
- HTML file has been saved

**When:**
- System exports to DOCX

**Then:**
- DOCX file is created with same base name as HTML
- DOCX preserves resume content and formatting
- DOCX can be opened in Microsoft Word
- Success status is returned

**Scenario 2:**

**Given:**
- --docx flag is not set

**When:**
- Export phase executes

**Then:**
- DOCX export is skipped
- Only HTML file is generated

**Tests:**

- **Test File:** `tests/test_docx_export.py`
- **Test Case:** `test_export_to_docx`


#### Beat 12: Report Generation Complete

**Display Completion Summary**

Display summary of generated files, theme, and options used

| Property | Value |
|----------|-------|
| **Event** | `generation.complete` |
| **Dynamics** | `ff` |
| **Timing** | `sync` |
| **Error Handling** | `continue` |
| **Dependencies** | `docx.exported` |

**Handler:**

- **Name:** `generate_hybrid_resume#report_completion`
- **Source:** `src/generate_hybrid_resume.py`
- **Capabilities:** `report`

**User Story:**

**As a** Job Seeker, **I want to** see a summary of what was generated, **so that** I know exactly where my resume files are located and what options were used

**Acceptance Criteria:**

**Given:**
- Generation process has completed

**When:**
- System reports completion

**Then:**
- HTML file path is displayed
- DOCX file path is displayed (if applicable)
- Theme name is displayed
- Resume name is displayed
- RAG status is displayed (if applicable)
- Success banner is shown

**Tests:**

- **Test File:** `tests/test_integration.py`
- **Test Case:** `Generation completion reporting`


---

---

*Report generated on 2025-12-07 21:06:30*
