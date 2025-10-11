# Resume Editor Web Interface

A user-friendly web application for managing and editing the `master_resume.json` file. This interface provides a visual way to update resume content without manually editing JSON files.

**Related to:** [GitHub Issue #2](https://github.com/BPMSoftwareSolutions/agentic-resume-tailor/issues/2)

## Features

✅ **Visual Resume Editor** - Edit all resume sections through an intuitive web interface  
✅ **Real-time Validation** - Client and server-side validation to prevent malformed data  
✅ **Automatic Backups** - Creates backups before every save operation  
✅ **Backup Management** - View, restore, and manage backup history  
✅ **Responsive Design** - Works seamlessly on desktop, tablet, and mobile devices  
✅ **CRUD Operations** - Add, edit, and delete experience, education, and certifications  
✅ **Tag Management** - Manage technology tags for experience bullets  
✅ **RESTful API** - Clean API for programmatic access  

## Architecture

### Backend (Flask API)
- **Location:** `src/api/app.py`
- **Port:** 5000
- **Technology:** Python Flask with CORS support

### Frontend (Web Application)
- **Location:** `src/web/`
- **Files:**
  - `index.html` - Main HTML structure
  - `app.js` - JavaScript application logic
  - `styles.css` - Responsive CSS styling
- **Technology:** Vanilla JavaScript with Bootstrap 5

### Data Storage
- **Resume File:** `data/master_resume.json`
- **Backups:** `data/backups/`

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify installation:**
   ```bash
   python -m pytest tests/test_api.py -v
   ```

### Running the Application

1. **Start the Flask API server:**
   ```bash
   python src/api/app.py
   ```
   
   The API will be available at `http://localhost:5000`

2. **Open the web interface:**
   
   Open `src/web/index.html` in your web browser, or serve it using a simple HTTP server:
   
   ```bash
   # Using Python's built-in HTTP server
   cd src/web
   python -m http.server 8080
   ```
   
   Then navigate to `http://localhost:8080`

## User Guide

### Navigating the Interface

The interface is divided into sections accessible via the left sidebar:

- **Basic Info** - Name, title, location, contact information
- **Summary** - Professional summary
- **Technical Skills** - Technical proficiencies by category
- **Areas of Expertise** - Key areas of expertise
- **Experience** - Professional experience entries
- **Education** - Educational background
- **Certifications** - Professional certifications

### Editing Resume Content

#### Basic Information
1. Click "Basic Info" in the sidebar
2. Edit fields directly
3. Changes are tracked automatically

#### Adding Experience
1. Navigate to "Experience" section
2. Click "Add Experience" button
3. Fill in employer, role, dates, and location
4. Add accomplishment bullets
5. Tag bullets with relevant technologies

#### Managing Tags
- Click "Add Tag" on any bullet point
- Enter tag name in the prompt
- Click "×" on a tag to remove it

#### Saving Changes
1. Click "Save Changes" in the top navigation
2. System validates data before saving
3. Automatic backup is created
4. Success message confirms save

### Backup Management

#### Creating Manual Backups
- Click "Create Backup" button in top navigation
- Backup is created with timestamp

#### Viewing Backup History
1. Click "View Backups" button
2. Modal shows all available backups with:
   - Filename
   - Creation date/time
   - File size

#### Restoring from Backup
1. Open backup history modal
2. Click "Restore" on desired backup
3. Confirm restoration
4. Current state is backed up before restore
5. Page reloads with restored data

## API Documentation

### Base URL
```
http://localhost:5000/api
```

### Endpoints

#### Health Check
```http
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-11T12:00:00"
}
```

#### Get Resume Data
```http
GET /api/resume
```

**Response:**
```json
{
  "success": true,
  "data": { /* resume data */ }
}
```

#### Update Resume
```http
PUT /api/resume
Content-Type: application/json

{ /* complete resume data */ }
```

**Response:**
```json
{
  "success": true,
  "message": "Resume updated successfully",
  "backup": "master_resume_backup_20251011_120000.json"
}
```

#### Validate Resume
```http
POST /api/resume/validate
Content-Type: application/json

{ /* resume data to validate */ }
```

**Response:**
```json
{
  "valid": true,
  "errors": []
}
```

#### Create Backup
```http
POST /api/resume/backup
```

**Response:**
```json
{
  "success": true,
  "message": "Backup created successfully",
  "backup": "master_resume_backup_20251011_120000.json",
  "timestamp": "2025-10-11T12:00:00"
}
```

#### List Backups
```http
GET /api/resume/backups
```

**Response:**
```json
{
  "success": true,
  "backups": [
    {
      "filename": "master_resume_backup_20251011_120000.json",
      "size": 12345,
      "created": "2025-10-11T12:00:00"
    }
  ]
}
```

#### Restore Backup
```http
POST /api/resume/restore
Content-Type: application/json

{
  "filename": "master_resume_backup_20251011_120000.json"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Resume restored successfully",
  "restored_from": "master_resume_backup_20251011_120000.json",
  "current_backup": "master_resume_backup_20251011_120100.json"
}
```

## Validation Rules

The system validates resume data to ensure data integrity:

### Required Fields
- `name` - Full name
- `title` - Professional title
- `location` - Location
- `contact` - Contact object with `email` and `phone`
- `summary` - Professional summary

### Experience Entries
- `employer` - Company name
- `role` - Job title
- `dates` - Employment dates
- `bullets` - Array of accomplishment objects

### Education Entries
- `school` - Institution name
- `degree` - Degree or certification

### Data Types
- `experience` - Must be an array
- `education` - Must be an array
- `certifications` - Must be an array (if present)
- `contact` - Must be an object

## Testing

### Running Unit Tests
```bash
# Run all API tests
python -m pytest tests/test_api.py -v

# Run with coverage
python -m pytest tests/test_api.py --cov=src/api --cov-report=html
```

### Test Coverage
- Health check endpoint
- Resume CRUD operations
- Validation logic
- Backup creation and restoration
- Error handling
- Edge cases

## Troubleshooting

### API Server Won't Start
- Check if port 5000 is already in use
- Verify Python dependencies are installed
- Check file permissions for `data/` directory

### Cannot Save Changes
- Verify API server is running
- Check browser console for errors
- Ensure `data/master_resume.json` is writable

### Validation Errors
- Review error messages in the UI
- Check that all required fields are filled
- Verify data structure matches expected format

### Backup Restoration Fails
- Ensure backup file exists in `data/backups/`
- Verify backup file is valid JSON
- Check file permissions

## Security Considerations

### Current Implementation
- CORS enabled for local development
- No authentication (suitable for local use)
- File system access restricted to data directory

### Production Recommendations
- Add authentication/authorization
- Implement rate limiting
- Use HTTPS
- Restrict CORS to specific origins
- Add input sanitization
- Implement audit logging

## Future Enhancements

- [ ] User authentication
- [ ] Multi-user support
- [ ] Version control integration
- [ ] Export to multiple formats
- [ ] AI-powered content suggestions
- [ ] Collaborative editing
- [ ] Cloud storage integration
- [ ] Mobile app

## Contributing

When contributing to the resume editor:

1. Follow TDD principles - write tests first
2. Ensure all tests pass before committing
3. Update documentation for new features
4. Link commits to GitHub issues
5. Follow existing code style

## License

This project is part of the agentic-resume-tailor repository.

## Support

For issues or questions:
- Create a GitHub issue
- Reference issue #2 for context
- Include error messages and logs

