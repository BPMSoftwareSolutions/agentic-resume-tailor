"""
Data models for multi-resume support.

Related to GitHub Issue #6
"""

from .resume import Resume, ResumeMetadata
from .job_listing import JobListing

__all__ = ['Resume', 'ResumeMetadata', 'JobListing']

