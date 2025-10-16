"""
Unit tests for duplicate_resume.py script.

Tests the CLI script for duplicating resumes.

Related to GitHub Issue #19
"""

import json
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest

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


@pytest.fixture
def setup_test_resumes(temp_data_dir, sample_resume_data):
    """Create test resumes for testing."""
    resume_model = Resume(temp_data_dir)

    # Create master resume
    master = resume_model.create(
        data=sample_resume_data,
        name="Master Resume",
        is_master=True,
        description="Master resume",
    )

    # Create Ford resume
    ford_data = sample_resume_data.copy()
    ford_data["title"] = "Senior Software Engineer"
    ford = resume_model.create(
        data=ford_data,
        name="Sidney_Jones_Senior_Software_Engineer_Ford",
        description="Ford resume",
    )

    return {"master": master, "ford": ford, "resume_model": resume_model}


class TestDuplicateResumeFunction:
    """Tests for duplicate_resume function."""

    def test_duplicate_by_name(self, temp_data_dir, setup_test_resumes):
        """Test duplicating a resume by name."""
        from duplicate_resume import duplicate_resume

        new_metadata = duplicate_resume(
            data_dir=temp_data_dir,
            source_identifier="Ford",
            new_name="Sidney_Jones_Senior_Engineer_NewCo",
        )

        assert new_metadata is not None
        assert new_metadata.name == "Sidney_Jones_Senior_Engineer_NewCo"
        assert new_metadata.is_master is False
        assert "Duplicated from" in new_metadata.description

    def test_duplicate_by_id(self, temp_data_dir, setup_test_resumes):
        """Test duplicating a resume by ID."""
        from duplicate_resume import duplicate_resume

        ford_id = setup_test_resumes["ford"].id

        new_metadata = duplicate_resume(
            data_dir=temp_data_dir,
            source_id=ford_id,
            new_name="Sidney_Jones_Senior_Engineer_NewCo",
        )

        assert new_metadata is not None
        assert new_metadata.name == "Sidney_Jones_Senior_Engineer_NewCo"

    def test_duplicate_with_description(self, temp_data_dir, setup_test_resumes):
        """Test duplicating a resume with custom description."""
        from duplicate_resume import duplicate_resume

        new_metadata = duplicate_resume(
            data_dir=temp_data_dir,
            source_identifier="Master Resume",
            new_name="Test Resume",
            description="Custom description",
        )

        assert new_metadata is not None
        assert new_metadata.description == "Custom description"

    def test_duplicate_nonexistent_resume(self, temp_data_dir, setup_test_resumes):
        """Test duplicating a non-existent resume."""
        from duplicate_resume import duplicate_resume

        with pytest.raises(FileNotFoundError):
            duplicate_resume(
                data_dir=temp_data_dir,
                source_identifier="NonExistent",
                new_name="Test Resume",
            )

    def test_duplicate_without_new_name(self, temp_data_dir, setup_test_resumes):
        """Test duplicating without providing new name."""
        from duplicate_resume import duplicate_resume

        with pytest.raises(ValueError):
            duplicate_resume(
                data_dir=temp_data_dir, source_identifier="Ford", new_name=""
            )

    def test_duplicate_without_source(self, temp_data_dir, setup_test_resumes):
        """Test duplicating without providing source."""
        from duplicate_resume import duplicate_resume

        with pytest.raises(ValueError):
            duplicate_resume(data_dir=temp_data_dir, new_name="Test Resume")

    def test_duplicate_data_integrity(self, temp_data_dir, setup_test_resumes):
        """Test that duplicated resume has same data as source."""
        from duplicate_resume import duplicate_resume

        resume_model = setup_test_resumes["resume_model"]
        ford_id = setup_test_resumes["ford"].id

        # Get original data
        original_data = resume_model.get(ford_id)

        # Duplicate
        new_metadata = duplicate_resume(
            data_dir=temp_data_dir, source_id=ford_id, new_name="Test Resume"
        )

        # Get duplicated data
        new_data = resume_model.get(new_metadata.id)

        # Verify data is the same
        assert new_data["name"] == original_data["name"]
        assert new_data["title"] == original_data["title"]
        assert new_data["summary"] == original_data["summary"]
        assert len(new_data["experience"]) == len(original_data["experience"])


class TestDuplicateResumeCLI:
    """Tests for duplicate_resume.py CLI script."""

    def test_cli_duplicate_by_name(self, temp_data_dir, setup_test_resumes):
        """Test CLI script with resume name."""
        result = subprocess.run(
            [
                sys.executable,
                "src/duplicate_resume.py",
                "--resume",
                "Ford",
                "--new-name",
                "Sidney_Jones_Senior_Engineer_NewCo",
                "--data-dir",
                str(temp_data_dir),
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "Successfully duplicated resume" in result.stdout
        assert "Sidney_Jones_Senior_Engineer_NewCo" in result.stdout

    def test_cli_duplicate_by_id(self, temp_data_dir, setup_test_resumes):
        """Test CLI script with resume ID."""
        ford_id = setup_test_resumes["ford"].id

        result = subprocess.run(
            [
                sys.executable,
                "src/duplicate_resume.py",
                "--resume-id",
                ford_id,
                "--new-name",
                "Test Resume",
                "--data-dir",
                str(temp_data_dir),
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "Successfully duplicated resume" in result.stdout

    def test_cli_duplicate_with_description(self, temp_data_dir, setup_test_resumes):
        """Test CLI script with description."""
        result = subprocess.run(
            [
                sys.executable,
                "src/duplicate_resume.py",
                "--resume",
                "Master Resume",
                "--new-name",
                "Test Resume",
                "--description",
                "Custom description",
                "--data-dir",
                str(temp_data_dir),
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "Successfully duplicated resume" in result.stdout
        assert "Custom description" in result.stdout

    def test_cli_missing_new_name(self, temp_data_dir, setup_test_resumes):
        """Test CLI script without new name."""
        result = subprocess.run(
            [
                sys.executable,
                "src/duplicate_resume.py",
                "--resume",
                "Ford",
                "--data-dir",
                str(temp_data_dir),
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode != 0

    def test_cli_nonexistent_resume(self, temp_data_dir, setup_test_resumes):
        """Test CLI script with non-existent resume."""
        result = subprocess.run(
            [
                sys.executable,
                "src/duplicate_resume.py",
                "--resume",
                "NonExistent",
                "--new-name",
                "Test Resume",
                "--data-dir",
                str(temp_data_dir),
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 2  # FileNotFoundError exit code
        assert (
            "no resume found" in result.stderr.lower()
            or "no resume found" in result.stdout.lower()
        )

    def test_cli_help(self):
        """Test CLI script help."""
        result = subprocess.run(
            [sys.executable, "src/duplicate_resume.py", "--help"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "duplicate" in result.stdout.lower()
        assert "--resume" in result.stdout
        assert "--new-name" in result.stdout
