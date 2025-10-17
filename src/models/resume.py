"""
Resume data model and storage management.

Related to GitHub Issue #6
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class ResumeMetadata:
    """Metadata for a resume."""

    def __init__(
        self,
        id: str,
        name: str,
        created_at: str,
        updated_at: str,
        job_listing_id: Optional[str] = None,
        is_master: bool = False,
        description: str = "",
    ):
        self.id = id
        self.name = name
        self.created_at = created_at
        self.updated_at = updated_at
        self.job_listing_id = job_listing_id
        self.is_master = is_master
        self.description = description

    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "job_listing_id": self.job_listing_id,
            "is_master": self.is_master,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ResumeMetadata":
        """Create metadata from dictionary."""
        return cls(
            id=data["id"],
            name=data["name"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
            job_listing_id=data.get("job_listing_id"),
            is_master=data.get("is_master", False),
            description=data.get("description", ""),
        )


class Resume:
    """Resume data model with storage operations."""

    def __init__(self, data_dir: Path):
        """
        Initialize Resume model.

        Args:
            data_dir: Base data directory path
        """
        self.data_dir = data_dir
        self.resumes_dir = data_dir / "resumes"
        self.resumes_dir.mkdir(exist_ok=True)

        # Index file to track all resumes
        self.index_file = self.resumes_dir / "index.json"
        self._ensure_index()

    def _ensure_index(self):
        """Ensure index file exists."""
        if not self.index_file.exists():
            self.index_file.write_text(
                json.dumps({"resumes": []}, indent=2), encoding="utf-8"
            )

    def _load_index(self) -> Dict[str, Any]:
        """Load resume index."""
        return json.loads(self.index_file.read_text(encoding="utf-8"))

    def _save_index(self, index: Dict[str, Any]):
        """Save resume index."""
        self.index_file.write_text(
            json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    def _get_resume_path(self, resume_id: str) -> Path:
        """Get path to resume file."""
        return self.resumes_dir / f"{resume_id}.json"

    def _name_exists(self, name: str, exclude_id: Optional[str] = None) -> bool:
        """
        Check if a resume with the given name already exists.

        Args:
            name: Resume name to check
            exclude_id: Optional resume ID to exclude from check (for updates)

        Returns:
            True if name exists, False otherwise
        """
        index = self._load_index()
        for resume in index["resumes"]:
            if resume["id"] != exclude_id and resume["name"].lower() == name.lower():
                return True
        return False

    def list_all(self) -> List[ResumeMetadata]:
        """
        List all resumes.

        Returns:
            List of resume metadata
        """
        index = self._load_index()
        return [ResumeMetadata.from_dict(r) for r in index["resumes"]]

    def get(self, resume_id: str) -> Optional[Dict[str, Any]]:
        """
        Get resume by ID.

        Args:
            resume_id: Resume ID

        Returns:
            Resume data or None if not found
        """
        resume_path = self._get_resume_path(resume_id)
        if not resume_path.exists():
            return None

        return json.loads(resume_path.read_text(encoding="utf-8"))

    def create(
        self,
        data: Dict[str, Any],
        name: str,
        job_listing_id: Optional[str] = None,
        is_master: bool = False,
        description: str = "",
    ) -> ResumeMetadata:
        """
        Create a new resume.

        Args:
            data: Resume data
            name: Resume name
            job_listing_id: Optional job listing ID
            is_master: Whether this is the master resume
            description: Resume description

        Returns:
            Resume metadata

        Raises:
            ValueError: If a resume with the same name already exists
        """
        # Check for duplicate name
        if self._name_exists(name):
            raise ValueError(f"A resume with the name '{name}' already exists. Please use a different name.")

        resume_id = str(uuid.uuid4())
        now = datetime.now().isoformat()

        # Create metadata
        metadata = ResumeMetadata(
            id=resume_id,
            name=name,
            created_at=now,
            updated_at=now,
            job_listing_id=job_listing_id,
            is_master=is_master,
            description=description,
        )

        # Save resume data
        resume_path = self._get_resume_path(resume_id)
        resume_path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        # Update index
        index = self._load_index()
        index["resumes"].append(metadata.to_dict())
        self._save_index(index)

        return metadata

    def update(self, resume_id: str, data: Dict[str, Any]) -> bool:
        """
        Update resume data.

        Args:
            resume_id: Resume ID
            data: Updated resume data

        Returns:
            True if successful, False if resume not found
        """
        resume_path = self._get_resume_path(resume_id)
        if not resume_path.exists():
            return False

        # Update resume data
        resume_path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        # Update metadata timestamp
        index = self._load_index()
        for resume in index["resumes"]:
            if resume["id"] == resume_id:
                resume["updated_at"] = datetime.now().isoformat()
                break
        self._save_index(index)

        return True

    def update_metadata(self, resume_id: str, **kwargs) -> bool:
        """
        Update resume metadata.

        Args:
            resume_id: Resume ID
            **kwargs: Metadata fields to update

        Returns:
            True if successful, False if resume not found

        Raises:
            ValueError: If updating name to a name that already exists
        """
        index = self._load_index()

        for resume in index["resumes"]:
            if resume["id"] == resume_id:
                # Check for duplicate name if updating name
                if "name" in kwargs:
                    new_name = kwargs["name"]
                    if self._name_exists(new_name, exclude_id=resume_id):
                        raise ValueError(f"A resume with the name '{new_name}' already exists. Please use a different name.")

                # Update allowed fields
                for key in ["name", "job_listing_id", "description"]:
                    if key in kwargs:
                        resume[key] = kwargs[key]
                resume["updated_at"] = datetime.now().isoformat()
                self._save_index(index)
                return True

        return False

    def delete(self, resume_id: str) -> bool:
        """
        Delete a resume.

        Args:
            resume_id: Resume ID

        Returns:
            True if successful, False if resume not found
        """
        resume_path = self._get_resume_path(resume_id)
        if not resume_path.exists():
            return False

        # Delete resume file
        resume_path.unlink()

        # Update index
        index = self._load_index()
        index["resumes"] = [r for r in index["resumes"] if r["id"] != resume_id]
        self._save_index(index)

        return True

    def duplicate(self, resume_id: str, new_name: str) -> Optional[ResumeMetadata]:
        """
        Duplicate a resume.

        Args:
            resume_id: Source resume ID
            new_name: Name for the duplicated resume

        Returns:
            Metadata for new resume or None if source not found
        """
        # Get source resume
        source_data = self.get(resume_id)
        if not source_data:
            return None

        # Get source metadata
        index = self._load_index()
        source_metadata = None
        for r in index["resumes"]:
            if r["id"] == resume_id:
                source_metadata = r
                break

        # Create duplicate
        return self.create(
            data=source_data,
            name=new_name,
            job_listing_id=(
                source_metadata.get("job_listing_id") if source_metadata else None
            ),
            is_master=False,
            description=(
                f"Duplicated from {source_metadata.get('name', 'Unknown')}"
                if source_metadata
                else ""
            ),
        )

    def get_master(self) -> Optional[Dict[str, Any]]:
        """
        Get the master resume.

        Returns:
            Master resume data or None if not found
        """
        index = self._load_index()
        for resume in index["resumes"]:
            if resume.get("is_master", False):
                return self.get(resume["id"])
        return None

    def get_master_metadata(self) -> Optional[ResumeMetadata]:
        """
        Get the master resume metadata.

        Returns:
            Master resume metadata or None if not found
        """
        index = self._load_index()
        for resume in index["resumes"]:
            if resume.get("is_master", False):
                return ResumeMetadata.from_dict(resume)
        return None
