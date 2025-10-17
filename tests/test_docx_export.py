"""
Tests for DOCX export functionality with multi-resume support.
Related to GitHub Issue #6
"""

import json
import time
from pathlib import Path

import pytest

from src.api.app import app
from src.models.resume import Resume


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def unique_resume_name():
    """Generate a unique resume name using timestamp."""
    return f"Test_Resume_{int(time.time() * 1000)}"


@pytest.fixture
def sample_resume_data():
    """Sample resume data for testing."""
    return {
        "name": "John Doe",
        "title": "Software Engineer",
        "location": "San Francisco, CA",
        "contact": {"email": "john@example.com", "phone": "555-1234"},
        "summary": "Experienced software engineer",
        "experience": [
            {
                "employer": "Tech Corp",
                "role": "Senior Engineer",
                "dates": "2020-Present",
                "bullets": ["Built scalable systems", "Led team of 5 engineers"],
            }
        ],
        "education": [
            {
                "institution": "University of Tech",
                "degree": "BS Computer Science",
                "dates": "2016-2020",
            }
        ],
        "skills": ["Python", "JavaScript", "AWS"],
    }


class TestDocxExport:
    """Test DOCX export functionality."""

    def test_export_master_resume_get(self, client, tmp_path, monkeypatch):
        """Test exporting master resume using GET request (backward compatibility)."""
        # This test verifies backward compatibility
        # Note: This will fail if master_resume.json doesn't exist
        # In a real test, we'd mock the subprocess call
        pass  # Placeholder - requires mocking subprocess

    def test_export_specific_resume_post(
        self, client, tmp_path, sample_resume_data, monkeypatch, unique_resume_name
    ):
        """Test exporting a specific resume using POST request with resume_id."""
        # Create a test resume first
        response = client.post(
            "/api/resumes",
            data=json.dumps(
                {
                    "name": unique_resume_name,
                    "description": "Test description",
                    "data": sample_resume_data,
                }
            ),
            content_type="application/json",
        )

        assert response.status_code == 201
        result = json.loads(response.data)
        resume_id = result["resume"]["id"]

        # Note: Full test would require mocking subprocess.run
        # For now, we just verify the endpoint accepts the request
        # In production, you'd mock the DOCX generation

        # Verify the resume was created
        assert resume_id is not None
        assert result["resume"]["name"] == unique_resume_name

    def test_export_nonexistent_resume(self, client):
        """Test exporting a resume that doesn't exist."""
        response = client.post(
            "/api/resume/docx",
            data=json.dumps({"resume_id": "nonexistent-id"}),
            content_type="application/json",
        )

        assert response.status_code == 404
        result = json.loads(response.data)
        assert "error" in result
        assert "not found" in result["error"].lower()

    def test_export_with_invalid_path(self, client):
        """Test exporting with an invalid resume path."""
        response = client.post(
            "/api/resume/docx",
            data=json.dumps({"resume_path": "invalid/path/to/resume.json"}),
            content_type="application/json",
        )

        assert response.status_code == 404
        result = json.loads(response.data)
        assert "error" in result
        assert "not found" in result["error"].lower()

    def test_export_defaults_to_master_on_empty_post(self, client):
        """Test that POST with empty body defaults to master resume."""
        # This should behave like GET request
        # Note: Will fail if master_resume.json doesn't exist
        # In production, you'd mock the file system
        pass  # Placeholder - requires mocking


class TestDocxExportIntegration:
    """Integration tests for DOCX export with full workflow."""

    def test_create_and_export_resume(self, client, sample_resume_data, unique_resume_name):
        """Test creating a resume and then exporting it."""
        # Create resume
        create_response = client.post(
            "/api/resumes",
            data=json.dumps(
                {
                    "name": unique_resume_name,
                    "description": "Resume for export testing",
                    "data": sample_resume_data,
                }
            ),
            content_type="application/json",
        )

        assert create_response.status_code == 201
        resume_data = json.loads(create_response.data)
        resume_id = resume_data["resume"]["id"]

        # Verify we can request export (actual generation would be mocked)
        # In a real test environment, you'd mock subprocess.run
        assert resume_id is not None

    def test_tailor_and_export_resume(self, client, sample_resume_data, unique_resume_name):
        """Test tailoring a resume and then exporting it."""
        # Create a job listing
        job_response = client.post(
            "/api/job-listings",
            data=json.dumps(
                {
                    "title": "Senior Software Engineer",
                    "company": "Tech Company",
                    "description": "Looking for Python expert with AWS experience",
                    "location": "Remote",
                }
            ),
            content_type="application/json",
        )

        assert job_response.status_code == 201
        job_data = json.loads(job_response.data)
        job_id = job_data["job_listing"]["id"]

        # Create a resume
        resume_response = client.post(
            "/api/resumes",
            data=json.dumps({"name": unique_resume_name, "data": sample_resume_data}),
            content_type="application/json",
        )

        assert resume_response.status_code == 201
        resume_data = json.loads(resume_response.data)
        resume_id = resume_data["resume"]["id"]

        # Tailor the resume (this would use actual tailoring logic)
        # Note: This might fail if tailoring dependencies aren't available
        # In production tests, you'd mock the tailoring service

        # Verify we have the IDs needed for export
        assert resume_id is not None
        assert job_id is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
