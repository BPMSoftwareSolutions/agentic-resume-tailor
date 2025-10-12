"""
Job listing data model and storage management.

Related to GitHub Issue #6
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional


class JobListing:
    """Job listing data model with storage operations."""
    
    def __init__(self, data_dir: Path):
        """
        Initialize JobListing model.
        
        Args:
            data_dir: Base data directory path
        """
        self.data_dir = data_dir
        self.job_listings_dir = data_dir / "job_listings"
        self.job_listings_dir.mkdir(exist_ok=True)
        
        # Index file to track all job listings
        self.index_file = self.job_listings_dir / "index.json"
        self._ensure_index()
    
    def _ensure_index(self):
        """Ensure index file exists."""
        if not self.index_file.exists():
            self.index_file.write_text(json.dumps({"job_listings": []}, indent=2), encoding='utf-8')
    
    def _load_index(self) -> Dict[str, Any]:
        """Load job listing index."""
        return json.loads(self.index_file.read_text(encoding='utf-8'))
    
    def _save_index(self, index: Dict[str, Any]):
        """Save job listing index."""
        self.index_file.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding='utf-8')
    
    def _get_job_listing_path(self, job_id: str) -> Path:
        """Get path to job listing file."""
        return self.job_listings_dir / f"{job_id}.json"
    
    def list_all(self) -> List[Dict[str, Any]]:
        """
        List all job listings.
        
        Returns:
            List of job listing metadata
        """
        index = self._load_index()
        return index["job_listings"]
    
    def get(self, job_id: str) -> Optional[Dict[str, Any]]:
        """
        Get job listing by ID.
        
        Args:
            job_id: Job listing ID
            
        Returns:
            Job listing data or None if not found
        """
        job_path = self._get_job_listing_path(job_id)
        if not job_path.exists():
            return None
        
        return json.loads(job_path.read_text(encoding='utf-8'))
    
    def create(
        self,
        title: str,
        company: str,
        description: str,
        url: Optional[str] = None,
        location: Optional[str] = None,
        salary_range: Optional[str] = None,
        keywords: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Create a new job listing.
        
        Args:
            title: Job title
            company: Company name
            description: Job description
            url: Job posting URL
            location: Job location
            salary_range: Salary range
            keywords: Extracted keywords
            
        Returns:
            Job listing metadata
        """
        job_id = str(uuid.uuid4())
        now = datetime.now().isoformat()
        
        # Create job listing data
        job_data = {
            "id": job_id,
            "title": title,
            "company": company,
            "description": description,
            "url": url,
            "location": location,
            "salary_range": salary_range,
            "keywords": keywords or [],
            "created_at": now,
            "updated_at": now
        }
        
        # Save job listing data
        job_path = self._get_job_listing_path(job_id)
        job_path.write_text(json.dumps(job_data, indent=2, ensure_ascii=False), encoding='utf-8')
        
        # Update index
        index = self._load_index()
        index["job_listings"].append({
            "id": job_id,
            "title": title,
            "company": company,
            "location": location,
            "created_at": now,
            "updated_at": now
        })
        self._save_index(index)
        
        return job_data
    
    def update(self, job_id: str, **kwargs) -> bool:
        """
        Update job listing.
        
        Args:
            job_id: Job listing ID
            **kwargs: Fields to update
            
        Returns:
            True if successful, False if job listing not found
        """
        job_path = self._get_job_listing_path(job_id)
        if not job_path.exists():
            return False
        
        # Load and update job data
        job_data = json.loads(job_path.read_text(encoding='utf-8'))
        
        # Update allowed fields
        allowed_fields = ["title", "company", "description", "url", "location", "salary_range", "keywords"]
        for key in allowed_fields:
            if key in kwargs:
                job_data[key] = kwargs[key]
        
        job_data["updated_at"] = datetime.now().isoformat()
        
        # Save updated data
        job_path.write_text(json.dumps(job_data, indent=2, ensure_ascii=False), encoding='utf-8')
        
        # Update index
        index = self._load_index()
        for job in index["job_listings"]:
            if job["id"] == job_id:
                if "title" in kwargs:
                    job["title"] = kwargs["title"]
                if "company" in kwargs:
                    job["company"] = kwargs["company"]
                if "location" in kwargs:
                    job["location"] = kwargs["location"]
                job["updated_at"] = datetime.now().isoformat()
                break
        self._save_index(index)
        
        return True
    
    def delete(self, job_id: str) -> bool:
        """
        Delete a job listing.
        
        Args:
            job_id: Job listing ID
            
        Returns:
            True if successful, False if job listing not found
        """
        job_path = self._get_job_listing_path(job_id)
        if not job_path.exists():
            return False
        
        # Delete job listing file
        job_path.unlink()
        
        # Update index
        index = self._load_index()
        index["job_listings"] = [j for j in index["job_listings"] if j["id"] != job_id]
        self._save_index(index)
        
        return True
    
    def extract_keywords(self, job_id: str) -> Optional[List[str]]:
        """
        Extract keywords from job listing description.
        
        Args:
            job_id: Job listing ID
            
        Returns:
            List of keywords or None if job listing not found
        """
        job_data = self.get(job_id)
        if not job_data:
            return None
        
        # Use existing jd_parser to extract keywords
        from jd_parser import extract_keywords
        
        description = job_data.get("description", "")
        keywords = extract_keywords(description)
        
        # Update job listing with keywords
        self.update(job_id, keywords=keywords)
        
        return keywords

