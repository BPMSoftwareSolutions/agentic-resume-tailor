"""
Shared pytest fixtures for test isolation and cleanup.

This module provides fixtures that ensure tests are isolated and don't
persist data to the actual data/resumes or data/job_listings directories.

Related to GitHub Issue #39: Fix Tests persisted data/resumes (anti-pattern)
"""

import json
import shutil
import sys
import tempfile
from pathlib import Path

import pytest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from models.job_listing import JobListing
from models.resume import Resume


@pytest.fixture
def temp_data_dir():
    """
    Create a temporary data directory for testing.
    
    This fixture ensures that all test data is isolated and cleaned up
    after each test, preventing data from persisting in the actual
    data/resumes or data/job_listings directories.
    
    Yields:
        Path: Temporary directory path
    """
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def resume_model(temp_data_dir):
    """
    Create a Resume model instance with a temporary directory.
    
    This fixture provides an isolated Resume model that writes to
    a temporary directory instead of the actual data/resumes directory.
    
    Args:
        temp_data_dir: Temporary directory fixture
        
    Returns:
        Resume: Resume model instance with isolated data directory
    """
    return Resume(temp_data_dir)


@pytest.fixture
def job_listing_model(temp_data_dir):
    """
    Create a JobListing model instance with a temporary directory.
    
    This fixture provides an isolated JobListing model that writes to
    a temporary directory instead of the actual data/job_listings directory.
    
    Args:
        temp_data_dir: Temporary directory fixture
        
    Returns:
        JobListing: JobListing model instance with isolated data directory
    """
    return JobListing(temp_data_dir)


@pytest.fixture
def sample_resume_data():
    """
    Provide sample resume data for testing.
    
    Returns:
        dict: Sample resume data structure
    """
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
def unique_resume_name():
    """
    Generate a unique resume name for testing.
    
    This fixture generates a unique name using timestamp to prevent
    conflicts when tests run multiple times or in parallel.
    
    Returns:
        str: Unique resume name
    """
    import time
    timestamp = int(time.time() * 1000)
    return f"Test_Resume_{timestamp}"


@pytest.fixture
def unique_job_listing_name():
    """
    Generate a unique job listing name for testing.
    
    This fixture generates a unique name using timestamp to prevent
    conflicts when tests run multiple times or in parallel.
    
    Returns:
        str: Unique job listing name
    """
    import time
    timestamp = int(time.time() * 1000)
    return f"Test_Job_{timestamp}"

