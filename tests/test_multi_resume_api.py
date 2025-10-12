"""
API tests for multi-resume support.

Tests the new API endpoints for resumes and job listings.

Related to GitHub Issue #6
"""

import json
import sys
import tempfile
import shutil
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

import pytest
from api.app import app, DATA_DIR, resume_model, job_listing_model


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def sample_resume_data():
    """Sample resume data for testing."""
    return {
        "name": "Test User",
        "title": "Software Engineer",
        "location": "Test City, ST",
        "contact": {
            "email": "test@example.com",
            "phone": "(123) 456-7890"
        },
        "summary": "Test summary",
        "experience": [
            {
                "employer": "Test Company",
                "role": "Software Engineer",
                "dates": "2020 - Present",
                "bullets": [
                    {
                        "text": "Built CI/CD pipelines",
                        "tags": ["CI/CD", "DevOps"]
                    }
                ]
            }
        ],
        "education": [
            {
                "institution": "Test University",
                "degree": "BS Computer Science",
                "year": "2020"
            }
        ]
    }


class TestResumeAPI:
    """Tests for resume API endpoints."""
    
    def test_list_resumes(self, client):
        """Test GET /api/resumes."""
        response = client.get('/api/resumes')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'resumes' in data
        assert isinstance(data['resumes'], list)
    
    def test_create_resume(self, client, sample_resume_data):
        """Test POST /api/resumes."""
        payload = {
            "name": "Test Resume",
            "data": sample_resume_data,
            "description": "Test description"
        }

        response = client.post(
            '/api/resumes',
            data=json.dumps(payload),
            content_type='application/json'
        )

        if response.status_code != 201:
            print(f"Error response: {response.data}")

        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'resume' in data
        assert data['resume']['name'] == "Test Resume"

        # Cleanup
        resume_id = data['resume']['id']
        resume_model.delete(resume_id)
    
    def test_create_resume_missing_name(self, client, sample_resume_data):
        """Test POST /api/resumes with missing name."""
        payload = {
            "data": sample_resume_data
        }
        
        response = client.post(
            '/api/resumes',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_get_resume(self, client, sample_resume_data):
        """Test GET /api/resumes/<id>."""
        # Create a resume first
        metadata = resume_model.create(
            data=sample_resume_data,
            name="Test Resume"
        )
        
        # Get the resume
        response = client.get(f'/api/resumes/{metadata.id}')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['name'] == "Test User"
        
        # Cleanup
        resume_model.delete(metadata.id)
    
    def test_get_nonexistent_resume(self, client):
        """Test GET /api/resumes/<id> with nonexistent ID."""
        response = client.get('/api/resumes/nonexistent-id')
        assert response.status_code == 404
    
    def test_update_resume(self, client, sample_resume_data):
        """Test PUT /api/resumes/<id>."""
        # Create a resume first
        metadata = resume_model.create(
            data=sample_resume_data,
            name="Test Resume"
        )
        
        # Update the resume
        updated_data = sample_resume_data.copy()
        updated_data['title'] = "Senior Software Engineer"
        
        payload = {
            "data": updated_data,
            "name": "Updated Resume"
        }
        
        response = client.put(
            f'/api/resumes/{metadata.id}',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        
        # Verify update
        resume_data = resume_model.get(metadata.id)
        assert resume_data['title'] == "Senior Software Engineer"
        
        # Cleanup
        resume_model.delete(metadata.id)
    
    def test_delete_resume(self, client, sample_resume_data):
        """Test DELETE /api/resumes/<id>."""
        # Create a resume first
        metadata = resume_model.create(
            data=sample_resume_data,
            name="Test Resume"
        )
        
        # Delete the resume
        response = client.delete(f'/api/resumes/{metadata.id}')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        
        # Verify deletion
        resume_data = resume_model.get(metadata.id)
        assert resume_data is None
    
    def test_duplicate_resume(self, client, sample_resume_data):
        """Test POST /api/resumes/<id>/duplicate."""
        # Create a resume first
        metadata = resume_model.create(
            data=sample_resume_data,
            name="Original Resume"
        )
        
        # Duplicate the resume
        payload = {"name": "Duplicated Resume"}
        
        response = client.post(
            f'/api/resumes/{metadata.id}/duplicate',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['resume']['name'] == "Duplicated Resume"
        
        # Cleanup
        resume_model.delete(metadata.id)
        resume_model.delete(data['resume']['id'])


class TestJobListingAPI:
    """Tests for job listing API endpoints."""
    
    def test_list_job_listings(self, client):
        """Test GET /api/job-listings."""
        response = client.get('/api/job-listings')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'job_listings' in data
    
    def test_create_job_listing(self, client):
        """Test POST /api/job-listings."""
        payload = {
            "title": "Software Engineer",
            "company": "Test Company",
            "description": "Test job description with Python and CI/CD",
            "location": "Remote"
        }
        
        response = client.post(
            '/api/job-listings',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['job_listing']['title'] == "Software Engineer"
        
        # Cleanup
        job_listing_model.delete(data['job_listing']['id'])
    
    def test_create_job_listing_missing_fields(self, client):
        """Test POST /api/job-listings with missing required fields."""
        payload = {
            "title": "Software Engineer"
            # Missing company and description
        }
        
        response = client.post(
            '/api/job-listings',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 400
    
    def test_get_job_listing(self, client):
        """Test GET /api/job-listings/<id>."""
        # Create a job listing first
        job_data = job_listing_model.create(
            title="Software Engineer",
            company="Test Company",
            description="Test description"
        )
        
        # Get the job listing
        response = client.get(f'/api/job-listings/{job_data["id"]}')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['job_listing']['title'] == "Software Engineer"
        
        # Cleanup
        job_listing_model.delete(job_data['id'])
    
    def test_update_job_listing(self, client):
        """Test PUT /api/job-listings/<id>."""
        # Create a job listing first
        job_data = job_listing_model.create(
            title="Software Engineer",
            company="Test Company",
            description="Test description"
        )
        
        # Update the job listing
        payload = {
            "title": "Senior Software Engineer",
            "location": "Remote"
        }
        
        response = client.put(
            f'/api/job-listings/{job_data["id"]}',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        
        # Cleanup
        job_listing_model.delete(job_data['id'])
    
    def test_delete_job_listing(self, client):
        """Test DELETE /api/job-listings/<id>."""
        # Create a job listing first
        job_data = job_listing_model.create(
            title="Software Engineer",
            company="Test Company",
            description="Test description"
        )
        
        # Delete the job listing
        response = client.delete(f'/api/job-listings/{job_data["id"]}')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True

