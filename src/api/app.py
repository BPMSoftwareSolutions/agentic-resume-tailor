from typing import Any, Dict, List, Tuple
"""
Flask API for Resume Editor Web Interface

This API provides endpoints for managing resumes and job listings.
Supports single resume (backward compatibility) and multi-resume operations.

Endpoints:
- GET /api/resume - Read current/master resume data (backward compatibility)
- PUT /api/resume - Update master resume data (backward compatibility)
- POST /api/resume/validate - Validate resume JSON structure
- GET /api/resume/backup - Create backup of current resume
- GET /api/resume/backups - List all available backups
- POST /api/resume/restore - Restore from a backup

Multi-Resume Endpoints (Issue #6):
- GET /api/resumes - List all resumes
- POST /api/resumes - Create new resume
- GET /api/resumes/<id> - Get specific resume
- PUT /api/resumes/<id> - Update specific resume
- DELETE /api/resumes/<id> - Delete specific resume
- POST /api/resumes/<id>/duplicate - Duplicate resume
- POST /api/resumes/<id>/tailor - Tailor resume to job listing

Job Listing Endpoints (Issue #6):
- GET /api/job-listings - List all job listings
- POST /api/job-listings - Create new job listing
- GET /api/job-listings/<id> - Get specific job listing
- PUT /api/job-listings/<id> - Update specific job listing
- DELETE /api/job-listings/<id> - Delete specific job listing
- POST /api/job-listings/<id>/extract-keywords - Extract keywords from job description

Related to GitHub Issues #2 and #6
"""

import json
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.resume import Resume, ResumeMetadata
from models.job_listing import JobListing

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data"
RESUME_FILE = DATA_DIR / "master_resume.json"
BACKUP_DIR = DATA_DIR / "backups"

# Ensure backup directory exists
BACKUP_DIR.mkdir(exist_ok=True)

# Initialize models
resume_model = Resume(DATA_DIR)
job_listing_model = JobListing(DATA_DIR)


def validate_resume_structure(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate the structure of resume JSON data.
    
    Args:
        data: Resume data dictionary
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    # Required top-level fields
    required_fields = ["name", "title", "location", "contact", "summary"]
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")
    
    # Validate contact structure
    if "contact" in data:
        contact = data["contact"]
        if not isinstance(contact, dict):
            errors.append("'contact' must be an object")
        else:
            if "email" not in contact:
                errors.append("Missing 'email' in contact")
            if "phone" not in contact:
                errors.append("Missing 'phone' in contact")
    
    # Validate experience array
    if "experience" in data:
        if not isinstance(data["experience"], list):
            errors.append("'experience' must be an array")
        else:
            for idx, exp in enumerate(data["experience"]):
                if not isinstance(exp, dict):
                    errors.append(f"Experience entry {idx} must be an object")
                    continue
                
                exp_required = ["employer", "role", "dates", "bullets"]
                for field in exp_required:
                    if field not in exp:
                        errors.append(f"Experience entry {idx} missing '{field}'")
                
                if "bullets" in exp and not isinstance(exp["bullets"], list):
                    errors.append(f"Experience entry {idx} 'bullets' must be an array")
    
    # Validate education array
    if "education" in data:
        if not isinstance(data["education"], list):
            errors.append("'education' must be an array")
        else:
            for idx, edu in enumerate(data["education"]):
                if not isinstance(edu, dict):
                    errors.append(f"Education entry {idx} must be an object")
                    continue
                
                edu_required = ["institution", "degree"]
                for field in edu_required:
                    if field not in edu:
                        errors.append(f"Education entry {idx} missing '{field}'")
    
    # Validate certifications array if present
    if "certifications" in data:
        if not isinstance(data["certifications"], list):
            errors.append("'certifications' must be an array")
    
    return len(errors) == 0, errors


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})


@app.route('/api/resume', methods=['GET'])
def get_resume():
    """
    Get the current resume data.
    
    Returns:
        JSON response with resume data or error
    """
    try:
        if not RESUME_FILE.exists():
            return jsonify({"error": "Resume file not found"}), 404
        
        with open(RESUME_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return jsonify({"success": True, "data": data})
    
    except json.JSONDecodeError as e:
        return jsonify({"error": f"Invalid JSON in resume file: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Failed to read resume: {str(e)}"}), 500


@app.route('/api/resume', methods=['PUT'])
def update_resume():
    """
    Update the resume data.
    Creates a backup before updating.

    Request body should contain the complete resume JSON.

    Returns:
        JSON response with success status or error
    """
    try:
        data = request.get_json(force=True)

        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Validate structure
        is_valid, errors = validate_resume_structure(data)
        if not is_valid:
            return jsonify({"error": "Validation failed", "details": errors}), 400

        # Create backup before updating
        backup_path = create_backup()

        # Write updated data
        with open(RESUME_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return jsonify({
            "success": True,
            "message": "Resume updated successfully",
            "backup": str(backup_path.name)
        })

    except (json.JSONDecodeError, ValueError) as e:
        return jsonify({"error": "No data provided or invalid JSON"}), 400
    except Exception as e:
        return jsonify({"error": f"Failed to update resume: {str(e)}"}), 500


@app.route('/api/resume/validate', methods=['POST'])
def validate_resume():
    """
    Validate resume JSON structure without saving.

    Request body should contain the resume JSON to validate.

    Returns:
        JSON response with validation results
    """
    try:
        data = request.get_json(force=True)

        if not data:
            return jsonify({"error": "No data provided"}), 400

        is_valid, errors = validate_resume_structure(data)

        return jsonify({
            "valid": is_valid,
            "errors": errors
        })

    except (json.JSONDecodeError, ValueError) as e:
        return jsonify({"error": "No data provided or invalid JSON"}), 400
    except Exception as e:
        return jsonify({"error": f"Validation failed: {str(e)}"}), 500


def create_backup() -> Path:
    """
    Create a backup of the current resume file.
    
    Returns:
        Path to the backup file
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"master_resume_backup_{timestamp}.json"
    backup_path = BACKUP_DIR / backup_filename
    
    shutil.copy2(RESUME_FILE, backup_path)
    
    return backup_path


@app.route('/api/resume/backup', methods=['POST'])
def backup_resume():
    """
    Create a manual backup of the current resume.
    
    Returns:
        JSON response with backup file information
    """
    try:
        backup_path = create_backup()
        
        return jsonify({
            "success": True,
            "message": "Backup created successfully",
            "backup": str(backup_path.name),
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({"error": f"Failed to create backup: {str(e)}"}), 500


@app.route('/api/resume/backups', methods=['GET'])
def list_backups():
    """
    List all available backup files.
    
    Returns:
        JSON response with list of backup files
    """
    try:
        backups = []
        
        for backup_file in sorted(BACKUP_DIR.glob("master_resume_backup_*.json"), reverse=True):
            stat = backup_file.stat()
            backups.append({
                "filename": backup_file.name,
                "size": stat.st_size,
                "created": datetime.fromtimestamp(stat.st_mtime).isoformat()
            })
        
        return jsonify({
            "success": True,
            "backups": backups
        })
    
    except Exception as e:
        return jsonify({"error": f"Failed to list backups: {str(e)}"}), 500


@app.route('/api/resume/restore', methods=['POST'])
def restore_backup():
    """
    Restore resume from a backup file.
    
    Request body should contain:
        {"filename": "backup_filename.json"}
    
    Returns:
        JSON response with success status or error
    """
    try:
        data = request.get_json()
        
        if not data or "filename" not in data:
            return jsonify({"error": "Backup filename not provided"}), 400
        
        backup_filename = data["filename"]
        backup_path = BACKUP_DIR / backup_filename
        
        if not backup_path.exists():
            return jsonify({"error": "Backup file not found"}), 404
        
        # Validate backup file before restoring
        with open(backup_path, 'r', encoding='utf-8') as f:
            backup_data = json.load(f)
        
        is_valid, errors = validate_resume_structure(backup_data)
        if not is_valid:
            return jsonify({"error": "Backup file has invalid structure", "details": errors}), 400
        
        # Create backup of current file before restoring
        current_backup = create_backup()
        
        # Restore from backup
        shutil.copy2(backup_path, RESUME_FILE)
        
        return jsonify({
            "success": True,
            "message": "Resume restored successfully",
            "restored_from": backup_filename,
            "current_backup": str(current_backup.name)
        })
    
    except json.JSONDecodeError as e:
        return jsonify({"error": f"Invalid JSON in backup file: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Failed to restore backup: {str(e)}"}), 500


@app.route('/api/resume/docx', methods=['GET'])
def generate_docx():
    """
    Generate and return the resume DOCX file for download.

    This endpoint generates a DOCX file from the resume JSON
    and returns it as a downloadable file.

    Returns:
        DOCX file download or error response
    """
    import subprocess
    import traceback

    # Paths
    generate_script = BASE_DIR / 'src' / 'generate_hybrid_resume.py'
    resume_json_path = DATA_DIR / 'master_resume.json'
    output_html_path = DATA_DIR / 'resume.html'
    docx_path = DATA_DIR / 'resume.docx'

    # Generate HTML and DOCX from resume JSON
    try:
    # ...existing code...

        result = subprocess.run([
            sys.executable,
            str(generate_script),
            '--input', str(resume_json_path),
            '--output', str(output_html_path),
            '--docx'
        ], capture_output=True, text=True)

    # ...existing code...

        if result.returncode != 0:
            return jsonify({'error': f'Failed to generate DOCX: {result.stderr or result.stdout}'}), 500

        # The DOCX file should be created alongside the HTML file
        if not docx_path.exists():
            return jsonify({'error': f'DOCX file was not created at {docx_path}. Output: {result.stdout}'}), 500

        return send_file(docx_path, as_attachment=True, download_name='resume.docx')

    except Exception as e:
        error_msg = f'Failed to generate DOCX: {str(e)}\n{traceback.format_exc()}'
    # ...existing code...
        return jsonify({'error': error_msg}), 500


# ============================================================================
# Multi-Resume API Endpoints (Issue #6)
# ============================================================================

@app.route('/api/resumes', methods=['GET'])
def list_resumes():
    """
    List all resumes.

    Returns:
        JSON response with list of resumes
    """
    try:
        resumes = resume_model.list_all()
        return jsonify({
            "success": True,
            "resumes": [r.to_dict() for r in resumes]
        })
    except Exception as e:
        return jsonify({"error": f"Failed to list resumes: {str(e)}"}), 500


@app.route('/api/resumes', methods=['POST'])
def create_resume():
    """
    Create a new resume.

    Request body:
        {
            "name": "Resume name",
            "data": { resume data },
            "job_listing_id": "optional job listing ID",
            "description": "optional description"
        }

    Returns:
        JSON response with created resume metadata
    """
    try:
        body = request.get_json(force=True)

        if not body:
            return jsonify({"error": "No data provided"}), 400

        name = body.get("name")
        data = body.get("data")
        job_listing_id = body.get("job_listing_id")
        description = body.get("description", "")

        if not name:
            return jsonify({"error": "Resume name is required"}), 400

        if not data:
            return jsonify({"error": "Resume data is required"}), 400

        # Validate resume structure
        is_valid, errors = validate_resume_structure(data)
        if not is_valid:
            return jsonify({"error": "Validation failed", "details": errors}), 400

        # Create resume
        metadata = resume_model.create(
            data=data,
            name=name,
            job_listing_id=job_listing_id,
            description=description
        )

        return jsonify({
            "success": True,
            "message": "Resume created successfully",
            "resume": metadata.to_dict()
        }), 201

    except Exception as e:
        return jsonify({"error": f"Failed to create resume: {str(e)}"}), 500


@app.route('/api/resumes/<resume_id>', methods=['GET'])
def get_resume_by_id(resume_id: str):
    """
    Get a specific resume by ID.

    Args:
        resume_id: Resume ID

    Returns:
        JSON response with resume data
    """
    try:
        data = resume_model.get(resume_id)

        if not data:
            return jsonify({"error": "Resume not found"}), 404

        return jsonify({
            "success": True,
            "data": data
        })

    except Exception as e:
        return jsonify({"error": f"Failed to get resume: {str(e)}"}), 500


@app.route('/api/resumes/<resume_id>', methods=['PUT'])
def update_resume_by_id(resume_id: str):
    """
    Update a specific resume.

    Args:
        resume_id: Resume ID

    Request body:
        {
            "data": { updated resume data },
            "name": "optional new name",
            "description": "optional new description"
        }

    Returns:
        JSON response with success status
    """
    try:
        body = request.get_json(force=True)

        if not body:
            return jsonify({"error": "No data provided"}), 400

        # Update resume data if provided
        if "data" in body:
            data = body["data"]

            # Validate resume structure
            is_valid, errors = validate_resume_structure(data)
            if not is_valid:
                return jsonify({"error": "Validation failed", "details": errors}), 400

            success = resume_model.update(resume_id, data)
            if not success:
                return jsonify({"error": "Resume not found"}), 404

        # Update metadata if provided
        metadata_updates = {}
        if "name" in body:
            metadata_updates["name"] = body["name"]
        if "description" in body:
            metadata_updates["description"] = body["description"]
        if "job_listing_id" in body:
            metadata_updates["job_listing_id"] = body["job_listing_id"]

        if metadata_updates:
            resume_model.update_metadata(resume_id, **metadata_updates)

        return jsonify({
            "success": True,
            "message": "Resume updated successfully"
        })

    except Exception as e:
        return jsonify({"error": f"Failed to update resume: {str(e)}"}), 500


@app.route('/api/resumes/<resume_id>', methods=['DELETE'])
def delete_resume_by_id(resume_id: str):
    """
    Delete a specific resume.

    Args:
        resume_id: Resume ID

    Returns:
        JSON response with success status
    """
    try:
        success = resume_model.delete(resume_id)

        if not success:
            return jsonify({"error": "Resume not found"}), 404

        return jsonify({
            "success": True,
            "message": "Resume deleted successfully"
        })

    except Exception as e:
        return jsonify({"error": f"Failed to delete resume: {str(e)}"}), 500


@app.route('/api/resumes/<resume_id>/duplicate', methods=['POST'])
def duplicate_resume(resume_id: str):
    """
    Duplicate a resume.

    Args:
        resume_id: Source resume ID

    Request body:
        {
            "name": "New resume name"
        }

    Returns:
        JSON response with new resume metadata
    """
    try:
        body = request.get_json(force=True)

        if not body or "name" not in body:
            return jsonify({"error": "Resume name is required"}), 400

        new_name = body["name"]

        metadata = resume_model.duplicate(resume_id, new_name)

        if not metadata:
            return jsonify({"error": "Source resume not found"}), 404

        return jsonify({
            "success": True,
            "message": "Resume duplicated successfully",
            "resume": metadata.to_dict()
        }), 201

    except Exception as e:
        return jsonify({"error": f"Failed to duplicate resume: {str(e)}"}), 500


@app.route('/api/resumes/<resume_id>/tailor', methods=['POST'])
def tailor_resume(resume_id: str):
    """
    Tailor a resume to a job listing.

    Args:
        resume_id: Resume ID to tailor

    Request body:
        {
            "job_listing_id": "Job listing ID",
            "new_resume_name": "Name for tailored resume"
        }

    Returns:
        JSON response with tailored resume metadata
    """
    try:
        body = request.get_json(force=True)

        if not body:
            return jsonify({"error": "No data provided"}), 400

        job_listing_id = body.get("job_listing_id")
        new_resume_name = body.get("new_resume_name")

        if not job_listing_id:
            return jsonify({"error": "Job listing ID is required"}), 400

        if not new_resume_name:
            return jsonify({"error": "New resume name is required"}), 400

        # Get source resume
        source_data = resume_model.get(resume_id)
        if not source_data:
            return jsonify({"error": "Source resume not found"}), 404

        # Get job listing
        job_listing = job_listing_model.get(job_listing_id)
        if not job_listing:
            return jsonify({"error": "Job listing not found"}), 404

        # Extract keywords from job listing if not already done
        keywords = job_listing.get("keywords", [])
        if not keywords:
            keywords = job_listing_model.extract_keywords(job_listing_id)

        # Tailor the resume using existing logic
        from tailor import select_and_rewrite

        tailored_data = source_data.copy()
        if "experience" in tailored_data:
            tailored_data["experience"] = select_and_rewrite(
                tailored_data["experience"],
                keywords
            )

        # Create new tailored resume
        metadata = resume_model.create(
            data=tailored_data,
            name=new_resume_name,
            job_listing_id=job_listing_id,
            description=f"Tailored for {job_listing.get('title', 'Unknown')} at {job_listing.get('company', 'Unknown')}"
        )

        return jsonify({
            "success": True,
            "message": "Resume tailored successfully",
            "resume": metadata.to_dict(),
            "keywords_used": keywords[:10]  # Return first 10 keywords
        }), 201

    except Exception as e:
        import traceback
        return jsonify({
            "error": f"Failed to tailor resume: {str(e)}",
            "traceback": traceback.format_exc()
        }), 500


# ============================================================================
# Job Listing API Endpoints (Issue #6)
# ============================================================================

@app.route('/api/job-listings', methods=['GET'])
def list_job_listings():
    """
    List all job listings.

    Returns:
        JSON response with list of job listings
    """
    try:
        job_listings = job_listing_model.list_all()
        return jsonify({
            "success": True,
            "job_listings": job_listings
        })
    except Exception as e:
        return jsonify({"error": f"Failed to list job listings: {str(e)}"}), 500


@app.route('/api/job-listings', methods=['POST'])
def create_job_listing():
    """
    Create a new job listing.

    Request body:
        {
            "title": "Job title",
            "company": "Company name",
            "description": "Job description",
            "url": "optional URL",
            "location": "optional location",
            "salary_range": "optional salary range"
        }

    Returns:
        JSON response with created job listing
    """
    try:
        body = request.get_json(force=True)

        if not body:
            return jsonify({"error": "No data provided"}), 400

        title = body.get("title")
        company = body.get("company")
        description = body.get("description")

        if not title:
            return jsonify({"error": "Job title is required"}), 400

        if not company:
            return jsonify({"error": "Company name is required"}), 400

        if not description:
            return jsonify({"error": "Job description is required"}), 400

        # Create job listing
        job_data = job_listing_model.create(
            title=title,
            company=company,
            description=description,
            url=body.get("url"),
            location=body.get("location"),
            salary_range=body.get("salary_range")
        )

        # Extract keywords automatically
        job_listing_model.extract_keywords(job_data["id"])

        return jsonify({
            "success": True,
            "message": "Job listing created successfully",
            "job_listing": job_data
        }), 201

    except Exception as e:
        return jsonify({"error": f"Failed to create job listing: {str(e)}"}), 500


@app.route('/api/job-listings/<job_id>', methods=['GET'])
def get_job_listing(job_id: str):
    """
    Get a specific job listing by ID.

    Args:
        job_id: Job listing ID

    Returns:
        JSON response with job listing data
    """
    try:
        job_data = job_listing_model.get(job_id)

        if not job_data:
            return jsonify({"error": "Job listing not found"}), 404

        return jsonify({
            "success": True,
            "job_listing": job_data
        })

    except Exception as e:
        return jsonify({"error": f"Failed to get job listing: {str(e)}"}), 500


@app.route('/api/job-listings/<job_id>', methods=['PUT'])
def update_job_listing(job_id: str):
    """
    Update a specific job listing.

    Args:
        job_id: Job listing ID

    Request body: Fields to update

    Returns:
        JSON response with success status
    """
    try:
        body = request.get_json(force=True)

        if not body:
            return jsonify({"error": "No data provided"}), 400

        success = job_listing_model.update(job_id, **body)

        if not success:
            return jsonify({"error": "Job listing not found"}), 404

        return jsonify({
            "success": True,
            "message": "Job listing updated successfully"
        })

    except Exception as e:
        return jsonify({"error": f"Failed to update job listing: {str(e)}"}), 500


@app.route('/api/job-listings/<job_id>', methods=['DELETE'])
def delete_job_listing(job_id: str):
    """
    Delete a specific job listing.

    Args:
        job_id: Job listing ID

    Returns:
        JSON response with success status
    """
    try:
        success = job_listing_model.delete(job_id)

        if not success:
            return jsonify({"error": "Job listing not found"}), 404

        return jsonify({
            "success": True,
            "message": "Job listing deleted successfully"
        })

    except Exception as e:
        return jsonify({"error": f"Failed to delete job listing: {str(e)}"}), 500


@app.route('/api/job-listings/<job_id>/extract-keywords', methods=['POST'])
def extract_job_keywords(job_id: str):
    """
    Extract keywords from job listing description.

    Args:
        job_id: Job listing ID

    Returns:
        JSON response with extracted keywords
    """
    try:
        keywords = job_listing_model.extract_keywords(job_id)

        if keywords is None:
            return jsonify({"error": "Job listing not found"}), 404

        return jsonify({
            "success": True,
            "keywords": keywords
        })

    except Exception as e:
        return jsonify({"error": f"Failed to extract keywords: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

