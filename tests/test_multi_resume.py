"""
Unit tests for multi-resume support.

Tests the Resume and JobListing models.

Related to GitHub Issue #6
"""

import json
import shutil
import sys
import tempfile
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest

from models.job_listing import JobListing
from models.resume import Resume, ResumeMetadata


@pytest.fixture
def temp_data_dir():
    """Create a temporary data directory for testing."""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    # Cleanup
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_resume_data():
    """Sample resume data for testing."""
    return {
        "name": "Test User",
        "title": "Software Engineer",
        "location": "Test City, ST",
        "contact": {"email": "test@example.com", "phone": "(123) 456-7890"},
        "summary": "Test summary",
        "experience": [
            {
                "employer": "Test Company",
                "role": "Software Engineer",
                "dates": "2020 - Present",
                "bullets": [
                    {"text": "Built CI/CD pipelines", "tags": ["CI/CD", "DevOps"]}
                ],
            }
        ],
        "education": [
            {
                "institution": "Test University",
                "degree": "BS Computer Science",
                "year": "2020",
            }
        ],
    }


class TestResumeModel:
    """Tests for Resume model."""

    def test_create_resume(self, temp_data_dir, sample_resume_data):
        """Test creating a new resume."""
        resume_model = Resume(temp_data_dir)

        metadata = resume_model.create(
            data=sample_resume_data, name="Test Resume", description="Test description"
        )

        assert metadata.name == "Test Resume"
        assert metadata.description == "Test description"
        assert metadata.id is not None
        assert metadata.is_master is False
        assert metadata.job_listing_id is None

    def test_create_master_resume(self, temp_data_dir, sample_resume_data):
        """Test creating a master resume."""
        resume_model = Resume(temp_data_dir)

        metadata = resume_model.create(
            data=sample_resume_data, name="Master Resume", is_master=True
        )

        assert metadata.is_master is True

        # Verify we can retrieve it as master
        master = resume_model.get_master()
        assert master is not None
        assert master["name"] == "Test User"

    def test_list_resumes(self, temp_data_dir, sample_resume_data):
        """Test listing all resumes."""
        resume_model = Resume(temp_data_dir)

        # Create multiple resumes
        resume_model.create(data=sample_resume_data, name="Resume 1")
        resume_model.create(data=sample_resume_data, name="Resume 2")
        resume_model.create(data=sample_resume_data, name="Resume 3")

        resumes = resume_model.list_all()
        assert len(resumes) == 3
        assert all(isinstance(r, ResumeMetadata) for r in resumes)

    def test_get_resume(self, temp_data_dir, sample_resume_data):
        """Test getting a specific resume."""
        resume_model = Resume(temp_data_dir)

        metadata = resume_model.create(data=sample_resume_data, name="Test Resume")

        # Get the resume
        data = resume_model.get(metadata.id)
        assert data is not None
        assert data["name"] == "Test User"
        assert data["title"] == "Software Engineer"

    def test_get_nonexistent_resume(self, temp_data_dir):
        """Test getting a resume that doesn't exist."""
        resume_model = Resume(temp_data_dir)

        data = resume_model.get("nonexistent-id")
        assert data is None

    def test_update_resume(self, temp_data_dir, sample_resume_data):
        """Test updating resume data."""
        resume_model = Resume(temp_data_dir)

        metadata = resume_model.create(data=sample_resume_data, name="Test Resume")

        # Update the resume
        updated_data = sample_resume_data.copy()
        updated_data["title"] = "Senior Software Engineer"

        success = resume_model.update(metadata.id, updated_data)
        assert success is True

        # Verify update
        data = resume_model.get(metadata.id)
        assert data["title"] == "Senior Software Engineer"

    def test_update_metadata(self, temp_data_dir, sample_resume_data):
        """Test updating resume metadata."""
        resume_model = Resume(temp_data_dir)

        metadata = resume_model.create(data=sample_resume_data, name="Test Resume")

        # Update metadata
        success = resume_model.update_metadata(
            metadata.id, name="Updated Resume Name", description="Updated description"
        )
        assert success is True

        # Verify update
        resumes = resume_model.list_all()
        updated = next(r for r in resumes if r.id == metadata.id)
        assert updated.name == "Updated Resume Name"
        assert updated.description == "Updated description"

    def test_delete_resume(self, temp_data_dir, sample_resume_data):
        """Test deleting a resume."""
        resume_model = Resume(temp_data_dir)

        metadata = resume_model.create(data=sample_resume_data, name="Test Resume")

        # Delete the resume
        success = resume_model.delete(metadata.id)
        assert success is True

        # Verify deletion
        data = resume_model.get(metadata.id)
        assert data is None

        resumes = resume_model.list_all()
        assert len(resumes) == 0

    def test_duplicate_resume(self, temp_data_dir, sample_resume_data):
        """Test duplicating a resume."""
        resume_model = Resume(temp_data_dir)

        original = resume_model.create(data=sample_resume_data, name="Original Resume")

        # Duplicate the resume
        duplicate = resume_model.duplicate(original.id, "Duplicated Resume")

        assert duplicate is not None
        assert duplicate.id != original.id
        assert duplicate.name == "Duplicated Resume"
        assert "Duplicated from" in duplicate.description

        # Verify both exist
        resumes = resume_model.list_all()
        assert len(resumes) == 2

        # Verify data is the same
        original_data = resume_model.get(original.id)
        duplicate_data = resume_model.get(duplicate.id)
        assert original_data["name"] == duplicate_data["name"]
        assert original_data["title"] == duplicate_data["title"]


class TestJobListingModel:
    """Tests for JobListing model."""

    def test_create_job_listing(self, temp_data_dir):
        """Test creating a new job listing."""
        job_model = JobListing(temp_data_dir)

        job_data = job_model.create(
            title="Software Engineer",
            company="Test Company",
            description="Test job description with Python and CI/CD",
            location="Remote",
            salary_range="$100k - $150k",
        )

        assert job_data["title"] == "Software Engineer"
        assert job_data["company"] == "Test Company"
        assert job_data["id"] is not None

    def test_list_job_listings(self, temp_data_dir):
        """Test listing all job listings."""
        job_model = JobListing(temp_data_dir)

        # Create multiple job listings
        job_model.create(
            title="Job 1", company="Company 1", description="Description 1"
        )
        job_model.create(
            title="Job 2", company="Company 2", description="Description 2"
        )

        listings = job_model.list_all()
        assert len(listings) == 2

    def test_get_job_listing(self, temp_data_dir):
        """Test getting a specific job listing."""
        job_model = JobListing(temp_data_dir)

        created = job_model.create(
            title="Software Engineer",
            company="Test Company",
            description="Test description",
        )

        # Get the job listing
        job_data = job_model.get(created["id"])
        assert job_data is not None
        assert job_data["title"] == "Software Engineer"

    def test_update_job_listing(self, temp_data_dir):
        """Test updating a job listing."""
        job_model = JobListing(temp_data_dir)

        created = job_model.create(
            title="Software Engineer",
            company="Test Company",
            description="Test description",
        )

        # Update the job listing
        success = job_model.update(
            created["id"], title="Senior Software Engineer", location="Remote"
        )
        assert success is True

        # Verify update
        job_data = job_model.get(created["id"])
        assert job_data["title"] == "Senior Software Engineer"
        assert job_data["location"] == "Remote"

    def test_delete_job_listing(self, temp_data_dir):
        """Test deleting a job listing."""
        job_model = JobListing(temp_data_dir)

        created = job_model.create(
            title="Software Engineer",
            company="Test Company",
            description="Test description",
        )

        # Delete the job listing
        success = job_model.delete(created["id"])
        assert success is True

        # Verify deletion
        job_data = job_model.get(created["id"])
        assert job_data is None

    def test_extract_keywords(self, temp_data_dir):
        """Test extracting keywords from job description."""
        job_model = JobListing(temp_data_dir)

        created = job_model.create(
            title="DevOps Engineer",
            company="Test Company",
            description="We need experience with Python, CI/CD, Kubernetes, and Docker",
        )

        # Extract keywords
        keywords = job_model.extract_keywords(created["id"])

        assert keywords is not None
        assert len(keywords) > 0
        # Should find some of the technical terms
        keywords_lower = [k.lower() for k in keywords]
        assert any("python" in k for k in keywords_lower)
