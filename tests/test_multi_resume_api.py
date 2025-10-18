"""
API tests for multi-resume support.

Tests the new API endpoints for resumes and job listings.

Related to GitHub Issue #6

Note: This test module uses isolated fixtures from conftest.py to prevent
persisting test data to the actual data/resumes or data/job_listings directories.
See GitHub Issue #39 for details on test isolation improvements.
"""

import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest

from api.app import app


@pytest.fixture
def client(temp_data_dir, monkeypatch):
    """
    Create a test client for the Flask app with isolated data directory.

    This fixture patches the app's DATA_DIR to use a temporary directory,
    ensuring that all test data is isolated and cleaned up after each test.

    Args:
        temp_data_dir: Temporary directory fixture from conftest.py
        monkeypatch: pytest monkeypatch fixture

    Yields:
        FlaskClient: Test client for the Flask app
    """
    # Import the app module using the same path as the app import in this file
    # (because of sys.path manipulation, we use 'api.app' not 'src.api.app')
    import api.app as app_module
    from models.resume import Resume
    from models.job_listing import JobListing

    # Create new models with temporary directory
    new_resume_model = Resume(temp_data_dir)
    new_job_listing_model = JobListing(temp_data_dir)

    # Patch the app module
    monkeypatch.setattr(app_module, "DATA_DIR", temp_data_dir)
    monkeypatch.setattr(app_module, "resume_model", new_resume_model)
    monkeypatch.setattr(app_module, "job_listing_model", new_job_listing_model)

    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client


class TestResumeAPI:
    """Tests for resume API endpoints."""

    def test_list_resumes(self, client):
        """Test GET /api/resumes."""
        response = client.get("/api/resumes")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data["success"] is True
        assert "resumes" in data
        assert isinstance(data["resumes"], list)

    def test_create_resume(self, client, sample_resume_data, unique_resume_name):
        """Test POST /api/resumes."""
        payload = {
            "name": unique_resume_name,
            "data": sample_resume_data,
            "description": "Test description",
        }

        response = client.post(
            "/api/resumes", data=json.dumps(payload), content_type="application/json"
        )

        if response.status_code != 201:
            print(f"Error response: {response.data}")

        assert response.status_code == 201
        data = json.loads(response.data)
        assert data["success"] is True
        assert "resume" in data
        assert data["resume"]["name"] == unique_resume_name

        # Note: Cleanup is automatic via temp_data_dir fixture

    def test_create_resume_missing_name(self, client, sample_resume_data):
        """Test POST /api/resumes with missing name."""
        payload = {"data": sample_resume_data}

        response = client.post(
            "/api/resumes", data=json.dumps(payload), content_type="application/json"
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data

    def test_get_resume(self, client, sample_resume_data, unique_resume_name):
        """Test GET /api/resumes/<id>."""
        # Create a resume first using the API
        # Use the patched resume_model from the app module
        import api.app as app_module
        metadata = app_module.resume_model.create(data=sample_resume_data, name=unique_resume_name)

        # Get the resume
        response = client.get(f"/api/resumes/{metadata.id}")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data["success"] is True
        assert data["data"]["name"] == "Test User"

        # Note: Cleanup is automatic via temp_data_dir fixture

    def test_get_nonexistent_resume(self, client):
        """Test GET /api/resumes/<id> with nonexistent ID."""
        response = client.get("/api/resumes/nonexistent-id")
        assert response.status_code == 404

    def test_update_resume(self, client, sample_resume_data, unique_resume_name):
        """Test PUT /api/resumes/<id>."""
        # Create a resume first using the API
        # Use the patched resume_model from the app module
        import api.app as app_module
        metadata = app_module.resume_model.create(data=sample_resume_data, name=unique_resume_name)

        # Update the resume
        updated_data = sample_resume_data.copy()
        updated_data["title"] = "Senior Software Engineer"

        payload = {"data": updated_data, "name": f"{unique_resume_name}_Updated"}

        response = client.put(
            f"/api/resumes/{metadata.id}",
            data=json.dumps(payload),
            content_type="application/json",
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["success"] is True

        # Verify update
        resume_data = app_module.resume_model.get(metadata.id)
        assert resume_data["title"] == "Senior Software Engineer"

        # Note: Cleanup is automatic via temp_data_dir fixture

    def test_delete_resume(self, client, sample_resume_data, unique_resume_name):
        """Test DELETE /api/resumes/<id>."""
        # Create a resume first using the API
        # Use the patched resume_model from the app module
        import api.app as app_module
        metadata = app_module.resume_model.create(data=sample_resume_data, name=unique_resume_name)

        # Delete the resume
        response = client.delete(f"/api/resumes/{metadata.id}")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data["success"] is True

        # Verify deletion
        resume_data = app_module.resume_model.get(metadata.id)
        assert resume_data is None

    def test_duplicate_resume(self, client, sample_resume_data, unique_resume_name):
        """Test POST /api/resumes/<id>/duplicate."""
        # Create a resume first using the API
        # Use the patched resume_model from the app module
        import api.app as app_module
        metadata = app_module.resume_model.create(data=sample_resume_data, name=unique_resume_name)

        # Duplicate the resume
        payload = {"name": f"{unique_resume_name}_Duplicate"}

        response = client.post(
            f"/api/resumes/{metadata.id}/duplicate",
            data=json.dumps(payload),
            content_type="application/json",
        )

        assert response.status_code == 201
        data = json.loads(response.data)
        assert data["success"] is True
        assert data["resume"]["name"] == f"{unique_resume_name}_Duplicate"

        # Note: Cleanup is automatic via temp_data_dir fixture


class TestJobListingAPI:
    """Tests for job listing API endpoints."""

    def test_list_job_listings(self, client):
        """Test GET /api/job-listings."""
        response = client.get("/api/job-listings")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data["success"] is True
        assert "job_listings" in data

    def test_create_job_listing(self, client):
        """Test POST /api/job-listings."""
        payload = {
            "title": "Software Engineer",
            "company": "Test Company",
            "description": "Test job description with Python and CI/CD",
            "location": "Remote",
        }

        response = client.post(
            "/api/job-listings",
            data=json.dumps(payload),
            content_type="application/json",
        )

        assert response.status_code == 201
        data = json.loads(response.data)
        assert data["success"] is True
        assert data["job_listing"]["title"] == "Software Engineer"

        # Note: Cleanup is automatic via temp_data_dir fixture

    def test_create_job_listing_missing_fields(self, client):
        """Test POST /api/job-listings with missing required fields."""
        payload = {
            "title": "Software Engineer"
            # Missing company and description
        }

        response = client.post(
            "/api/job-listings",
            data=json.dumps(payload),
            content_type="application/json",
        )

        assert response.status_code == 400

    def test_get_job_listing(self, client):
        """Test GET /api/job-listings/<id>."""
        # Create a job listing first using the API
        from api.app import job_listing_model
        job_data = job_listing_model.create(
            title="Software Engineer",
            company="Test Company",
            description="Test description",
        )

        # Get the job listing
        response = client.get(f'/api/job-listings/{job_data["id"]}')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data["success"] is True
        assert data["job_listing"]["title"] == "Software Engineer"

        # Note: Cleanup is automatic via temp_data_dir fixture

    def test_update_job_listing(self, client):
        """Test PUT /api/job-listings/<id>."""
        # Create a job listing first using the API
        from api.app import job_listing_model
        job_data = job_listing_model.create(
            title="Software Engineer",
            company="Test Company",
            description="Test description",
        )

        # Update the job listing
        payload = {"title": "Senior Software Engineer", "location": "Remote"}

        response = client.put(
            f'/api/job-listings/{job_data["id"]}',
            data=json.dumps(payload),
            content_type="application/json",
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["success"] is True

        # Note: Cleanup is automatic via temp_data_dir fixture

    def test_delete_job_listing(self, client):
        """Test DELETE /api/job-listings/<id>."""
        # Create a job listing first using the API
        from api.app import job_listing_model
        job_data = job_listing_model.create(
            title="Software Engineer",
            company="Test Company",
            description="Test description",
        )

        # Delete the job listing
        response = client.delete(f'/api/job-listings/{job_data["id"]}')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data["success"] is True
