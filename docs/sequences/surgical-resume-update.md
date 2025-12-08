# Surgical Resume Update Pipeline

**Selective Experience Replacement via Markdown**

Surgically update specific resume sections and employers' experiences using Markdown input while preserving all other resume content

---

## 📋 Sequence Metadata

| Field | Value |
|-------|-------|
| **Sequence ID** | `surgical-resume-update` |
| **Domain** | `agentic-resume-tailor` |
| **Package** | `agentic-resume-tailor` |
| **Kind** | `orchestration` |
| **Status** | `active` |
| **Category** | `resume-editing` |
| **Total Beats** | 10 |
| **Version** | 1.0.0 |
| **Author** | Agentic Resume Tailor Team |
| **Created** | 2025-12-07 |

**Tags:** `surgical-update`, `markdown`, `selective-replacement`, `resume-editing`, `tag-promotion`

## 🎵 Musical Properties

| Property | Value |
|----------|-------|
| **Key** | D major |
| **Tempo** | 110 BPM |
| **Time Signature** | 4/4 |

## 🎯 Purpose & Context

### Purpose
Enable precise, targeted updates to resume sections without requiring full resume editing, maintaining data integrity for unchanged content

### Trigger
**Event:** User pastes Markdown content into Surgical Update UI or sends POST request to /api/resumes/<id>/surgical-update

### Business Value
Enables precise, safe resume updates that preserve data integrity while allowing rapid iteration on specific sections or employers

## 👤 User Story

**As a** Job Seeker  
**I want to** update specific parts of my resume (summary, competencies, or certain employers) without touching other sections  
**So that** I can make targeted updates efficiently without risking accidental changes to unrelated content

## 🛡️ Governance

### Policies

- `input-validation`
- `data-integrity`
- `selective-modification`
- `tag-promotion`

### Metrics

- `update-success-rate`
- `employers-replaced-count`
- `section-update-count`
- `tag-promotion-accuracy`

## 📡 Events

This sequence emits the following events in order:

1. `markdown.received`
2. `markdown.parsed`
3. `experiences.extracted`
4. `sections.extracted`
5. `resume.loaded`
6. `employers.identified`
7. `experiences.replaced`
8. `sections.updated`
9. `tags.promoted`
10. `resume.saved`

## 🎼 Movements

This sequence consists of 3 movements:

| # | Movement | Beats | Error Handling | Status |
|---|----------|-------|----------------|--------|
| 1 | Markdown Parsing and Extraction | 4 | `abort-sequence` | `active` |
| 2 | Resume Modification | 5 | `abort-sequence` | `active` |
| 3 | Finalization and Response | 1 | `abort-sequence` | `active` |

---

### Movement 1: Markdown Parsing and Extraction

Parse Markdown input to extract experiences and section updates

**Movement Properties:**

- **ID:** `mov-1-markdown-parsing`
- **Tempo:** 120 BPM
- **Error Handling:** `abort-sequence`
- **Status:** `active`

**User Story:**

**As a** Job Seeker, **I want to** have my Markdown input parsed into structured resume sections, **so that** the system understands exactly what I want to update

**Beats (4):**

#### Beat 1: Receive Markdown Input

**Receive Markdown or JSON Input**

Accept Markdown text, experiences JSON array, or both from the API request

| Property | Value |
|----------|-------|
| **Event** | `markdown.received` |
| **Dynamics** | `f` |
| **Timing** | `sync` |
| **Error Handling** | `abort-sequence` |

**Handler:**

- **Name:** `surgical_update_resume#receive_input`
- **Source:** `src/api/app.py`
- **Capabilities:** `validate`, `build`

**User Story:**

**As a** Job Seeker, **I want to** provide my updates via Markdown paste or JSON, **so that** I can use the format that's most convenient for me

**Acceptance Criteria:**

**Scenario 1:**

**Given:**
- Markdown text is provided in request body

**When:**
- API receives the surgical update request

**Then:**
- Markdown content is extracted from 'markdown' or 'markdown_input' field
- Request is validated to ensure it's not empty
- Input is ready for parsing

**Scenario 2:**

**Given:**
- Experiences JSON array is provided

**When:**
- API receives experiences instead of or in addition to Markdown

**Then:**
- JSON array is validated as well-formed
- Experiences are available for processing
- Markdown parsing can be skipped if preferred

**Tests:**

- **Test File:** `tests/test_surgical_update.py`
- **Test Case:** `test_receive_markdown_input`


#### Beat 2: Parse Markdown Content

**Parse Markdown Sections**

Parse Markdown to extract PROFESSIONAL SUMMARY, CORE COMPETENCIES, and RELEVANT EXPERIENCE sections

| Property | Value |
|----------|-------|
| **Event** | `markdown.parsed` |
| **Dynamics** | `f` |
| **Timing** | `sync` |
| **Error Handling** | `abort-sequence` |
| **Dependencies** | `markdown.received` |

**Handler:**

- **Name:** `markdown_resume_parser#parse_surgical_markdown`
- **Source:** `src/utils/markdown_resume_parser.py`
- **Capabilities:** `validate`, `build`

**User Story:**

**As a** Job Seeker, **I want to** have my Markdown parsed into structured sections, **so that** my paste is converted into actionable resume updates

**Acceptance Criteria:**

**Scenario 1:**

**Given:**
- Markdown contains ### **PROFESSIONAL SUMMARY** section

**When:**
- Parser processes the Markdown

**Then:**
- Summary text is extracted (content between header and next section)
- Text is trimmed and cleaned
- Summary is added to 'updates' dict with key 'summary'

**Scenario 2:**

**Given:**
- Markdown contains ### **CORE COMPETENCIES** section

**When:**
- Parser processes the Markdown

**Then:**
- Competencies are extracted as bullet list items
- Each competency line is parsed (format: 'Category: item1, item2')
- Competencies are added to 'updates' dict with key 'core_competencies'
- Competencies can be returned as list or newline-delimited string

**Scenario 3:**

**Given:**
- Markdown contains ### **RELEVANT EXPERIENCE** section with experiences

**When:**
- Parser processes the Markdown

**Then:**
- Each experience is identified by #### **Employer** | *Role* pattern
- Dates and location are extracted from italic line (*City, ST | Jan 2020 – Present*)
- Bullets are extracted (lines starting with *)
- Tech/skills tags are extracted from *Tech:* line
- Experience objects are created with employer, role, dates, location, bullets array
- Bullet-level tags are preserved in bullet objects
- All experiences are added to 'experiences' array

**Scenario 4:**

**Given:**
- Markdown parsing fails

**When:**
- Invalid Markdown format is detected

**Then:**
- Error is raised with descriptive message
- Request returns 400 status with error details
- No resume changes are applied

**Tests:**

- **Test File:** `tests/test_markdown_parser.py`
- **Test Case:** `test_parse_surgical_markdown`


#### Beat 3: Extract Experiences

**Extract and Validate Experiences**

Extract experiences from Markdown parse results or JSON input, validate structure, and identify target employers

| Property | Value |
|----------|-------|
| **Event** | `experiences.extracted` |
| **Dynamics** | `mf` |
| **Timing** | `sync` |
| **Error Handling** | `abort-sequence` |
| **Dependencies** | `markdown.parsed` |

**Handler:**

- **Name:** `surgical_update_resume#parse_experiences`
- **Source:** `src/api/app.py`
- **Capabilities:** `validate`, `build`

**User Story:**

**As a** Job Seeker, **I want to** have my experience entries validated and structured correctly, **so that** I know the system will replace the right employers' experiences

**Acceptance Criteria:**

**Scenario 1:**

**Given:**
- Experiences are provided as JSON array

**When:**
- System parses experiences input

**Then:**
- Array is validated as well-formed JSON
- Each experience is converted to dict
- Experience objects contain required fields (employer, role, dates, bullets)
- Bullet-level tags are promoted to experience-level tags

**Scenario 2:**

**Given:**
- Experiences are provided as JSON object with 'experiences' key

**When:**
- System parses experiences input

**Then:**
- Object is unwrapped to get experiences array
- Each experience is processed same as array format

**Scenario 3:**

**Given:**
- Experience has bullets with tags

**When:**
- System ensures tag promotion

**Then:**
- All bullet-level tags are collected
- Tags are merged with existing experience-level tags
- Duplicates are removed while preserving order
- Experience 'tags' field contains promoted tags

**Scenario 4:**

**Given:**
- Experiences input is invalid

**When:**
- System attempts to parse

**Then:**
- ValueError is raised with descriptive message
- Error indicates expected format (array or object with 'experiences')
- Request fails with 400 status

**Tests:**

- **Test File:** `tests/test_surgical_update.py`
- **Test Case:** `test_extract_experiences`


#### Beat 4: Extract Section Updates

**Extract Section Updates**

Extract summary and core competencies updates from Markdown parse results or explicit updates object

| Property | Value |
|----------|-------|
| **Event** | `sections.extracted` |
| **Dynamics** | `mf` |
| **Timing** | `sync` |
| **Error Handling** | `continue` |
| **Dependencies** | `markdown.parsed` |

**Handler:**

- **Name:** `surgical_update_resume#extract_section_updates`
- **Source:** `src/api/app.py`
- **Capabilities:** `build`

**User Story:**

**As a** Job Seeker, **I want to** have my summary and competencies updates identified, **so that** the system knows which non-experience sections to update

**Acceptance Criteria:**

**Scenario 1:**

**Given:**
- Markdown parse results contain 'summary' in updates dict

**When:**
- System extracts section updates

**Then:**
- Summary text is added to section updates
- Summary replaces existing resume summary when applied

**Scenario 2:**

**Given:**
- Markdown parse results contain 'core_competencies' in updates dict

**When:**
- System extracts section updates

**Then:**
- Core competencies are processed
- If competencies are newline-delimited string, they are split into list
- Competencies are added to section updates as list

**Scenario 3:**

**Given:**
- Explicit 'updates' object is provided in request body

**When:**
- System merges updates

**Then:**
- Markdown-derived updates are merged with explicit updates
- Explicit updates take precedence over Markdown updates
- Final updates dict contains all non-null updates

**Tests:**

- **Test File:** `tests/test_surgical_update.py`
- **Test Case:** `test_extract_section_updates`


---

### Movement 2: Resume Modification

Load target resume, identify employers to replace, and apply surgical updates

**Movement Properties:**

- **ID:** `mov-2-resume-modification`
- **Tempo:** 110 BPM
- **Error Handling:** `abort-sequence`
- **Status:** `active`

**User Story:**

**As a** Job Seeker, **I want to** have my resume updated with only the specified changes, **so that** all other resume content remains untouched and safe

**Beats (5):**

#### Beat 5: Load Target Resume

**Load Resume by ID**

Load the target resume data from storage using the provided resume ID

| Property | Value |
|----------|-------|
| **Event** | `resume.loaded` |
| **Dynamics** | `f` |
| **Timing** | `sync` |
| **Error Handling** | `abort-sequence` |
| **Dependencies** | `experiences.extracted`, `sections.extracted` |

**Handler:**

- **Name:** `resume_model#get`
- **Source:** `src/models/resume.py`
- **Capabilities:** `validate`

**User Story:**

**As a** Job Seeker, **I want to** have the system load my target resume, **so that** the system can apply updates to the correct resume

**Acceptance Criteria:**

**Scenario 1:**

**Given:**
- Resume ID is provided in URL path

**When:**
- System loads resume data

**Then:**
- Resume JSON is loaded from data/resumes/<id>.json
- Resume data is validated as well-formed
- Experience count before update is recorded
- Resume data is ready for modification

**Scenario 2:**

**Given:**
- Resume ID does not exist

**When:**
- System attempts to load resume

**Then:**
- 404 error is returned
- Error message indicates 'Resume not found'
- No modifications are attempted

**Tests:**

- **Test File:** `tests/test_surgical_update.py`
- **Test Case:** `test_load_target_resume`


#### Beat 6: Identify Target Employers

**Identify Employers to Replace**

Determine which employers to replace based on experiences array or explicit replace_employers list

| Property | Value |
|----------|-------|
| **Event** | `employers.identified` |
| **Dynamics** | `mf` |
| **Timing** | `sync` |
| **Error Handling** | `continue` |
| **Dependencies** | `resume.loaded` |

**Handler:**

- **Name:** `surgical_update_resume#identify_employers`
- **Source:** `src/api/app.py`
- **Capabilities:** `build`

**User Story:**

**As a** Job Seeker, **I want to** have the system identify which employers to replace, **so that** only the specified employers are updated, others remain unchanged

**Acceptance Criteria:**

**Scenario 1:**

**Given:**
- replace_employers list is provided in request

**When:**
- System identifies target employers

**Then:**
- Employer names are extracted from replace_employers
- Employer names are normalized (lowercase, dash variants)
- Duplicates are removed while preserving order
- Target employers list is created

**Scenario 2:**

**Given:**
- replace_employers list is NOT provided

**When:**
- System derives employers from experiences

**Then:**
- Employer field is extracted from each experience
- Empty employers are filtered out
- Employer names are normalized and deduplicated
- Target employers list is derived from experiences

**Scenario 3:**

**Given:**
- Employer names contain different dash types (–, —, -)

**When:**
- System normalizes employer names

**Then:**
- All dash variants are normalized to single hyphen
- Employer matching uses normalized names
- Different dash types in resume vs input don't cause mismatches

**Tests:**

- **Test File:** `tests/test_surgical_update.py`
- **Test Case:** `test_identify_target_employers`


#### Beat 7: Replace Employers Surgically

**Selective Experience Replacement**

Replace only the specified employers' experiences while preserving all other experience entries

| Property | Value |
|----------|-------|
| **Event** | `experiences.replaced` |
| **Dynamics** | `f` |
| **Timing** | `sync` |
| **Error Handling** | `abort-sequence` |
| **Dependencies** | `employers.identified` |

**Handler:**

- **Name:** `surgical_update_resume#replace_surgically`
- **Source:** `src/api/app.py`
- **Capabilities:** `build`

**User Story:**

**As a** Job Seeker, **I want to** have only the specified employers replaced in my resume, **so that** my other work experiences remain completely unchanged

**Acceptance Criteria:**

**Scenario 1:**

**Given:**
- Target employers list is identified
- New experiences are validated

**When:**
- System performs surgical replacement

**Then:**
- Existing experiences are filtered - those matching target employers are removed
- New experiences matching target employers are selected from input
- Experience array is reconstructed: new experiences first, then kept experiences
- Experience count after replacement is recorded
- List of replaced employers is returned
- List of missing employers (in targets but not in new experiences) is returned

**Scenario 2:**

**Given:**
- Target employer exists in resume but not in new experiences

**When:**
- System attempts replacement

**Then:**
- Employer is removed from resume (no replacement available)
- Employer is added to 'missing_employers' list
- Warning is included in response metadata

**Scenario 3:**

**Given:**
- Target employer exists in new experiences but not in resume

**When:**
- System performs replacement

**Then:**
- New experience is added to resume (addition, not replacement)
- No existing experience is removed
- Employer is included in 'replaced_employers' list

**Tests:**

- **Test File:** `tests/test_surgical_update.py`
- **Test Case:** `test_replace_employers_surgically`


#### Beat 8: Update Resume Sections

**Update Summary and Competencies**

Apply section updates (summary, core_competencies) to resume data

| Property | Value |
|----------|-------|
| **Event** | `sections.updated` |
| **Dynamics** | `mf` |
| **Timing** | `sync` |
| **Error Handling** | `continue` |
| **Dependencies** | `experiences.replaced` |

**Handler:**

- **Name:** `surgical_update_resume#update_sections`
- **Source:** `src/api/app.py`
- **Capabilities:** `build`

**User Story:**

**As a** Job Seeker, **I want to** have my summary and competencies updated if I provided them, **so that** I can update multiple sections in one surgical update

**Acceptance Criteria:**

**Scenario 1:**

**Given:**
- Section updates dict contains 'summary'

**When:**
- System updates sections

**Then:**
- Resume 'summary' field is replaced with new summary text
- Previous summary is overwritten
- Update is applied to resume data

**Scenario 2:**

**Given:**
- Section updates dict contains 'core_competencies' as string

**When:**
- System processes competencies

**Then:**
- String is split by newlines
- Each line is trimmed
- Empty lines are filtered out
- Result is set as list in resume 'core_competencies' field

**Scenario 3:**

**Given:**
- Section updates dict contains 'core_competencies' as list

**When:**
- System processes competencies

**Then:**
- List is used directly
- Resume 'core_competencies' field is replaced with list

**Scenario 4:**

**Given:**
- Section updates dict is empty

**When:**
- System attempts section updates

**Then:**
- No section changes are applied
- Resume sections remain unchanged
- Processing continues normally

**Tests:**

- **Test File:** `tests/test_surgical_update.py`
- **Test Case:** `test_update_resume_sections`


#### Beat 9: Promote Bullet Tags

**Promote Bullet-Level Tags to Experience-Level**

Ensure all bullet-level tags are promoted to experience-level tags for each updated experience

| Property | Value |
|----------|-------|
| **Event** | `tags.promoted` |
| **Dynamics** | `mf` |
| **Timing** | `sync` |
| **Error Handling** | `continue` |
| **Dependencies** | `sections.updated` |

**Handler:**

- **Name:** `surgical_update_resume#ensure_experience_level_tags`
- **Source:** `src/api/app.py`
- **Capabilities:** `build`

**User Story:**

**As a** Job Seeker, **I want to** have all my bullet tags automatically promoted to experience tags, **so that** my skills and technologies are properly categorized at the experience level

**Acceptance Criteria:**

**Scenario 1:**

**Given:**
- Experience bullets contain 'tags' fields

**When:**
- System promotes tags

**Then:**
- All tags from all bullets are collected
- Tags are merged with existing experience-level tags
- Duplicates are removed while preserving order
- Final tags list is set on experience 'tags' field

**Scenario 2:**

**Given:**
- Experience has no bullet tags

**When:**
- System promotes tags

**Then:**
- Existing experience-level tags are preserved
- No new tags are added
- Experience 'tags' field remains unchanged

**Scenario 3:**

**Given:**
- Experience has both bullet tags and experience tags

**When:**
- System promotes tags

**Then:**
- Existing experience tags come first in merged list
- Promoted bullet tags are appended
- Duplicates between the two sources are removed
- Order is preserved (experience tags first, then new bullet tags)

**Tests:**

- **Test File:** `tests/test_surgical_update.py`
- **Test Case:** `test_promote_bullet_tags`


---

### Movement 3: Finalization and Response

Save updated resume and return surgical update metadata

**Movement Properties:**

- **ID:** `mov-3-finalization`
- **Tempo:** 100 BPM
- **Error Handling:** `abort-sequence`
- **Status:** `active`

**User Story:**

**As a** Job Seeker, **I want to** have my changes saved and receive confirmation of what was updated, **so that** I know the update succeeded and can see exactly what changed

**Beats (1):**

#### Beat 10: Save Updated Resume

**Persist Resume Changes**

Save the surgically updated resume data to storage unless dry_run mode is enabled

| Property | Value |
|----------|-------|
| **Event** | `resume.saved` |
| **Dynamics** | `f` |
| **Timing** | `sync` |
| **Error Handling** | `abort-sequence` |
| **Dependencies** | `tags.promoted` |

**Handler:**

- **Name:** `resume_model#update`
- **Source:** `src/models/resume.py`
- **Capabilities:** `deploy`

**User Story:**

**As a** Job Seeker, **I want to** have my surgical updates saved to my resume, **so that** my changes are persisted and available for future use

**Acceptance Criteria:**

**Scenario 1:**

**Given:**
- dry_run is false or not specified

**When:**
- System saves resume

**Then:**
- Updated resume data is written to data/resumes/<id>.json
- File is saved with UTF-8 encoding
- Metadata is updated with last modified timestamp
- Success status is returned

**Scenario 2:**

**Given:**
- dry_run is true

**When:**
- System processes save operation

**Then:**
- Resume data is NOT written to disk
- Updated preview is included in response
- Response indicates dry_run mode was used
- Original resume remains unchanged

**Scenario 3:**

**Given:**
- Save operation fails

**When:**
- System attempts to persist changes

**Then:**
- 500 error is returned
- Error message indicates 'Failed to save updated resume'
- Resume remains in previous state

**Scenario 4:**

**Given:**
- Resume is successfully saved

**When:**
- System returns response

**Then:**
- Success: true is included
- Message: 'Surgical update applied' is included
- Metadata includes: replaced_employers, missing_employers, experience counts
- Response shows total_experience_before and total_experience_after

**Tests:**

- **Test File:** `tests/test_surgical_update.py`
- **Test Case:** `test_save_updated_resume`


---

---

*Report generated on 2025-12-07 21:35:17*
