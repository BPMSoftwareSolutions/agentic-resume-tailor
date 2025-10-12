# Multi-Resume Support

**Related to:** [GitHub Issue #6](https://github.com/BPMSoftwareSolutions/agentic-resume-tailor/issues/6)

## Overview

The multi-resume support feature allows users to create, manage, and export multiple tailored resumes, each linked to specific job listings. This enables efficient generation and tracking of resumes customized for different roles.

## Features

✅ **Multiple Resume Management** - Create, edit, duplicate, and delete multiple resumes  
✅ **Job Listing Management** - Add and manage job listings with automatic keyword extraction  
✅ **Resume Tailoring** - Automatically tailor resumes to job listings using AI-powered matching  
✅ **Dashboard UI** - Visual interface for managing all resumes and job listings  
✅ **Master Resume** - Maintain a master resume as the source of truth  
✅ **Export Support** - Export any resume in HTML/DOCX format  
✅ **Backup & Restore** - Automatic backups for all resume operations  

## Architecture

### Data Storage

```
data/
├── resumes/
│   ├── index.json              # Index of all resumes
│   ├── {resume-id}.json        # Individual resume files
│   └── ...
├── job_listings/
│   ├── index.json              # Index of all job listings
│   ├── {job-id}.json           # Individual job listing files
│   └── ...
└── backups/                    # Backup files
```

### Backend Components

#### Data Models (`src/models/`)

- **Resume Model** - Manages resume CRUD operations
  - Create, read, update, delete resumes
  - Duplicate resumes
  - Track master resume
  - Metadata management (name, description, job listing link)

- **JobListing Model** - Manages job listing CRUD operations
  - Create, read, update, delete job listings
  - Extract keywords from job descriptions
  - Link to tailored resumes

#### API Endpoints (`src/api/app.py`)

**Resume Endpoints:**
- `GET /api/resumes` - List all resumes
- `POST /api/resumes` - Create new resume
- `GET /api/resumes/<id>` - Get specific resume
- `PUT /api/resumes/<id>` - Update specific resume
- `DELETE /api/resumes/<id>` - Delete specific resume
- `POST /api/resumes/<id>/duplicate` - Duplicate resume
- `POST /api/resumes/<id>/tailor` - Tailor resume to job listing

**Job Listing Endpoints:**
- `GET /api/job-listings` - List all job listings
- `POST /api/job-listings` - Create new job listing
- `GET /api/job-listings/<id>` - Get specific job listing
- `PUT /api/job-listings/<id>` - Update specific job listing
- `DELETE /api/job-listings/<id>` - Delete specific job listing
- `POST /api/job-listings/<id>/extract-keywords` - Extract keywords

**Export Endpoints:**
- `GET /api/resume/docx` - Export master resume as DOCX (backward compatible)
- `POST /api/resume/docx` - Export specific resume as DOCX
  - Body: `{"resume_id": "uuid"}` or `{"resume_path": "path/to/resume.json"}`

**Legacy Endpoints (Backward Compatibility):**
- `GET /api/resume` - Get master resume
- `PUT /api/resume` - Update master resume
- All existing backup/restore endpoints

### Frontend Components

#### Dashboard (`src/web/dashboard.html` & `dashboard.js`)

- **Resume Management**
  - View all resumes in card layout
  - Create new resumes from scratch or duplicate existing ones
  - Edit resumes (opens in resume editor)
  - Delete resumes (except master)
  - Tailor resumes to job listings

- **Job Listing Management**
  - View all job listings
  - Add new job listings
  - View job details
  - Delete job listings

- **Statistics**
  - Total resumes count
  - Total job listings count
  - Tailored resumes count

#### Resume Editor (`src/web/index.html` & `app.js`)

- Updated to support loading specific resumes via URL parameter
- Example: `index.html?resume={resume-id}`
- Saves changes to the specific resume being edited
- Maintains backward compatibility with master resume editing

## Usage

### Starting the Application

1. **Start the API server:**
   ```bash
   python src/api/app.py
   ```

2. **Open the dashboard:**
   - Navigate to `src/web/dashboard.html` in your browser
   - Or use: `python -m http.server 8080` and go to `http://localhost:8080/dashboard.html`

### Migration

If you have an existing `master_resume.json`, migrate it to the new structure:

```bash
# Dry run to see what will happen
python src/migrate_to_multi_resume.py --dry-run

# Perform the migration
python src/migrate_to_multi_resume.py
```

This will:
- Create the master resume in `data/resumes/`
- Backup the original `master_resume.json`
- Create the index files

### Creating a New Resume

1. Open the dashboard
2. Click "Create New Resume"
3. Enter a name and optional description
4. Choose to start from scratch (uses master resume) or duplicate an existing resume
5. Click "Create Resume"
6. The new resume will appear in the dashboard

### Adding a Job Listing

1. Open the dashboard
2. Switch to the "Job Listings" tab
3. Click "Add Job Listing"
4. Fill in the job details:
   - Title (required)
   - Company (required)
   - Location (optional)
   - URL (optional)
   - Salary range (optional)
   - Description (required)
5. Click "Add Job Listing"
6. Keywords will be automatically extracted from the description

### Tailoring a Resume

1. Open the dashboard
2. Find the resume you want to tailor
3. Click the "Tailor" button
4. Select a job listing from the dropdown
5. Enter a name for the tailored resume
6. Click "Tailor Resume"
7. The system will:
   - Extract keywords from the job listing
   - Score and select the most relevant experience bullets
   - Rewrite bullets using STAR methodology
   - Create a new tailored resume

### Editing a Resume

1. Open the dashboard
2. Find the resume you want to edit
3. Click the "Edit" button
4. The resume editor will open with that specific resume loaded
5. Make your changes
6. Click "Save Changes"

### Exporting a Resume

#### From the Dashboard

1. Open the dashboard
2. Find the resume you want to export
3. Click the "Export DOCX" button
4. The DOCX file will be downloaded automatically

#### From the Resume Editor

1. Open a resume in the editor
2. Click the "Generate DOCX" button in the top navigation
3. The DOCX file will be downloaded automatically

#### From the Command Line

```bash
# Export a specific resume
python src/generate_hybrid_resume.py \
  --input data/resumes/{resume-id}.json \
  --output out/resume.html \
  --docx
```

#### Via API

```bash
# Export a specific resume by ID
curl -X POST http://localhost:5000/api/resume/docx \
  -H "Content-Type: application/json" \
  -d '{"resume_id": "{resume-id}"}' \
  --output resume.docx

# Export master resume (backward compatible)
curl http://localhost:5000/api/resume/docx --output resume.docx
```

## API Examples

### Create a New Resume

```bash
curl -X POST http://localhost:5000/api/resumes \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Software Engineer Resume",
    "description": "Tailored for software engineering roles",
    "data": { ... resume data ... }
  }'
```

### Tailor a Resume to a Job

```bash
curl -X POST http://localhost:5000/api/resumes/{resume-id}/tailor \
  -H "Content-Type: application/json" \
  -d '{
    "job_listing_id": "{job-id}",
    "new_resume_name": "Resume for Company X"
  }'
```

### Add a Job Listing

```bash
curl -X POST http://localhost:5000/api/job-listings \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Senior Software Engineer",
    "company": "Tech Company",
    "description": "We are looking for...",
    "location": "Remote",
    "url": "https://example.com/job"
  }'
```

## Testing

### Run Unit Tests

```bash
# Test data models
python -m pytest tests/test_multi_resume.py -v

# Test API endpoints
python -m pytest tests/test_multi_resume_api.py -v

# Run all tests
python -m pytest tests/ -v
```

### Test Coverage

- 15 unit tests for Resume and JobListing models
- 14 API integration tests
- 7 DOCX export tests
- **Total: 36 tests, all passing** ✅

## Future Enhancements

- [ ] Batch export of multiple resumes
- [ ] Resume templates
- [ ] Version history for resumes
- [ ] Resume comparison tool
- [ ] Job listing import from URLs
- [ ] Advanced keyword matching with ML
- [ ] Resume analytics and insights
- [ ] Collaborative resume editing
- [ ] Integration with job boards

## Troubleshooting

### "Failed to load resumes"
- Ensure the API server is running on port 5000
- Check that `data/resumes/index.json` exists
- Verify CORS is enabled in the API

### "Master resume not found"
- Run the migration script: `python src/migrate_to_multi_resume.py`
- Or manually create a master resume through the API

### "Keywords not extracted"
- Check that the job description contains technical terms
- Verify `src/jd_parser.py` is working correctly
- Keywords are extracted automatically when creating job listings

## Architecture Decisions

### Why Separate Files?
- Scalability: Each resume is independent
- Performance: Load only what's needed
- Backup: Easy to backup individual resumes
- Version control: Better git diffs

### Why Index Files?
- Fast listing without reading all files
- Metadata caching
- Easy to query and filter

### Why Keep Master Resume?
- Single source of truth
- Easy to create new resumes
- Maintains consistency

## Related Documentation

- [Resume Editor Web Interface](RESUME_EDITOR_WEB_INTERFACE.md)
- [CI/CD Pipeline](CI_CD_PIPELINE.md)
- [Hybrid HTML Resume Generation](HYBRID_HTML_RESUME_GENERATION.md)

