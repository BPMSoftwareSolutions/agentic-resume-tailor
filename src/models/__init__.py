"""
Data models for multi-resume support.

Related to GitHub Issue #6
"""

from .job_listing import JobListing
from .resume import Resume, ResumeMetadata

__all__ = ["Resume", "ResumeMetadata", "JobListing"]
