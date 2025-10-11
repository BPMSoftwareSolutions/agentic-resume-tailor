"""
Flask API for Resume Editor Web Interface

This API provides endpoints for managing the master_resume.json file.
Supports reading, updating, validating, and backing up resume data.

Endpoints:
- GET /api/resume - Read current resume data
- PUT /api/resume - Update resume data
- POST /api/resume/validate - Validate resume JSON structure
- GET /api/resume/backup - Create backup of current resume
- GET /api/resume/backups - List all available backups
- POST /api/resume/restore - Restore from a backup

Related to GitHub Issue #2
"""

import json
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data"
RESUME_FILE = DATA_DIR / "master_resume.json"
BACKUP_DIR = DATA_DIR / "backups"

# Ensure backup directory exists
BACKUP_DIR.mkdir(exist_ok=True)


def validate_resume_structure(data: Dict[str, Any]) -> tuple[bool, List[str]]:
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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

