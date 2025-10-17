"""
Unit tests for resume unique name constraint.

Tests that the Resume model enforces unique resume names and prevents
duplicate names from being created or updated.

Related to GitHub Issue #XX (Duplicate Resume Names)
"""

import json
import pytest
import tempfile
from pathlib import Path

from src.models.resume import Resume


@pytest.fixture
def temp_data_dir():
    """Create a temporary data directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def resume_model(temp_data_dir):
    """Create a Resume model instance with temporary directory."""
    return Resume(temp_data_dir)


@pytest.fixture
def sample_resume_data():
    """Sample resume data for testing."""
    return {
        "name": "John Doe",
        "title": "Software Engineer",
        "location": "San Francisco, CA",
        "contact": {
            "email": "john@example.com",
            "phone": "555-1234",
        },
        "summary": "Experienced software engineer",
        "technical_proficiencies": {
            "languages": ["Python", "JavaScript"],
        },
        "areas_of_expertise": ["Web Development"],
        "experience": [],
        "education": [],
        "certifications": [],
    }


class TestUniqueNameConstraint:
    """Test suite for unique resume name constraint."""

    def test_create_resume_with_unique_name(self, resume_model, sample_resume_data):
        """Test creating a resume with a unique name succeeds."""
        metadata = resume_model.create(
            data=sample_resume_data,
            name="Unique Resume",
            description="Test resume",
        )

        assert metadata is not None
        assert metadata.name == "Unique Resume"
        assert metadata.id is not None

    def test_create_duplicate_resume_raises_error(
        self, resume_model, sample_resume_data
    ):
        """Test creating a resume with duplicate name raises ValueError."""
        # Create first resume
        resume_model.create(
            data=sample_resume_data,
            name="Duplicate Test",
            description="First resume",
        )

        # Try to create second resume with same name
        with pytest.raises(ValueError) as exc_info:
            resume_model.create(
                data=sample_resume_data,
                name="Duplicate Test",
                description="Second resume",
            )

        assert "already exists" in str(exc_info.value)

    def test_create_duplicate_resume_case_insensitive(
        self, resume_model, sample_resume_data
    ):
        """Test that duplicate name check is case-insensitive."""
        # Create first resume
        resume_model.create(
            data=sample_resume_data,
            name="Case Test",
            description="First resume",
        )

        # Try to create with different case
        with pytest.raises(ValueError) as exc_info:
            resume_model.create(
                data=sample_resume_data,
                name="CASE TEST",
                description="Second resume",
            )

        assert "already exists" in str(exc_info.value)

    def test_duplicate_resume_with_unique_name(
        self, resume_model, sample_resume_data
    ):
        """Test duplicating a resume with a unique new name succeeds."""
        # Create original resume
        original = resume_model.create(
            data=sample_resume_data,
            name="Original Resume",
            description="Original",
        )

        # Duplicate with unique name
        duplicate = resume_model.duplicate(original.id, "Duplicated Resume")

        assert duplicate is not None
        assert duplicate.name == "Duplicated Resume"
        assert duplicate.id != original.id

    def test_duplicate_resume_with_duplicate_name_raises_error(
        self, resume_model, sample_resume_data
    ):
        """Test duplicating a resume with duplicate name raises ValueError."""
        # Create original resume
        original = resume_model.create(
            data=sample_resume_data,
            name="Original Resume",
            description="Original",
        )

        # Try to duplicate with same name
        with pytest.raises(ValueError) as exc_info:
            resume_model.duplicate(original.id, "Original Resume")

        assert "already exists" in str(exc_info.value)

    def test_update_metadata_with_unique_name(self, resume_model, sample_resume_data):
        """Test updating resume metadata with unique name succeeds."""
        # Create resume
        metadata = resume_model.create(
            data=sample_resume_data,
            name="Original Name",
            description="Original",
        )

        # Update with unique name
        success = resume_model.update_metadata(metadata.id, name="Updated Name")

        assert success is True

        # Verify the name was updated
        all_resumes = resume_model.list_all()
        updated = next(r for r in all_resumes if r.id == metadata.id)
        assert updated.name == "Updated Name"

    def test_update_metadata_with_duplicate_name_raises_error(
        self, resume_model, sample_resume_data
    ):
        """Test updating resume metadata with duplicate name raises ValueError."""
        # Create two resumes
        resume1 = resume_model.create(
            data=sample_resume_data,
            name="Resume One",
            description="First",
        )

        resume2 = resume_model.create(
            data=sample_resume_data,
            name="Resume Two",
            description="Second",
        )

        # Try to update resume2 to have same name as resume1
        with pytest.raises(ValueError) as exc_info:
            resume_model.update_metadata(resume2.id, name="Resume One")

        assert "already exists" in str(exc_info.value)

    def test_update_metadata_same_name_allowed(
        self, resume_model, sample_resume_data
    ):
        """Test updating resume metadata with its own name is allowed."""
        # Create resume
        metadata = resume_model.create(
            data=sample_resume_data,
            name="My Resume",
            description="Original",
        )

        # Update with same name (should succeed)
        success = resume_model.update_metadata(metadata.id, name="My Resume")

        assert success is True

    def test_name_exists_helper_method(self, resume_model, sample_resume_data):
        """Test the _name_exists helper method."""
        # Create a resume
        resume_model.create(
            data=sample_resume_data,
            name="Test Resume",
            description="Test",
        )

        # Check that name exists
        assert resume_model._name_exists("Test Resume") is True
        assert resume_model._name_exists("test resume") is True  # Case insensitive
        assert resume_model._name_exists("Nonexistent") is False

    def test_name_exists_with_exclude_id(self, resume_model, sample_resume_data):
        """Test _name_exists with exclude_id parameter."""
        # Create a resume
        metadata = resume_model.create(
            data=sample_resume_data,
            name="Test Resume",
            description="Test",
        )

        # Check that name exists
        assert resume_model._name_exists("Test Resume") is True

        # Check that name doesn't exist when excluding the resume itself
        assert resume_model._name_exists("Test Resume", exclude_id=metadata.id) is False

