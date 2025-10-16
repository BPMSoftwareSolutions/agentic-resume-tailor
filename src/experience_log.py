#!/usr/bin/env python3
"""
Experience Log

Small manager to store and query professional experiences with rich metadata
for building tailored resumes.

Data is stored in JSON at project `data/experiences.json` by default.
"""
from __future__ import annotations

import json
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class Experience:
    id: str
    employer: str
    role: str
    dates: str
    location: Optional[str] = ""
    bullets: List[str] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)
    technologies: List[str] = field(default_factory=list)
    techniques: List[str] = field(default_factory=list)
    principles: List[str] = field(default_factory=list)
    notes: Optional[str] = ""

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Experience":
        return Experience(
            id=d.get("id") or str(uuid.uuid4()),
            employer=d.get("employer", ""),
            role=d.get("role", ""),
            dates=d.get("dates", ""),
            location=d.get("location", ""),
            bullets=d.get("bullets", []) or [],
            skills=d.get("skills", []) or [],
            technologies=d.get("technologies", []) or [],
            techniques=d.get("techniques", []) or [],
            principles=d.get("principles", []) or [],
            notes=d.get("notes", ""),
        )


class ExperienceLog:
    def __init__(self, path: Optional[Path] = None):
        self.path = (
            Path(path)
            if path
            else Path(__file__).parent.parent / "data" / "experiences.json"
        )
        self._experiences: List[Experience] = []
        self.load()

    def load(self) -> None:
        if not self.path.exists():
            self._experiences = []
            return

        with open(self.path, "r", encoding="utf-8") as f:
            try:
                raw = json.load(f)
            except json.JSONDecodeError:
                raw = []

        self._experiences = [Experience.from_dict(d) for d in raw]

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(
                [asdict(e) for e in self._experiences], f, indent=2, ensure_ascii=False
            )

    def list(self) -> List[Experience]:
        return list(self._experiences)

    def add(self, exp: Experience) -> Experience:
        # Ensure unique id
        if not exp.id:
            exp.id = str(uuid.uuid4())

        # Prevent duplicates by employer+role+dates
        for existing in self._experiences:
            if (
                existing.employer.lower() == exp.employer.lower()
                and existing.role.lower() == exp.role.lower()
                and existing.dates == exp.dates
            ):
                raise ValueError("Duplicate experience entry detected")

        self._experiences.append(exp)
        self.save()
        return exp

    def find_by_skill(self, skill: str) -> List[Experience]:
        skill_lower = skill.lower()
        matches = []
        for e in self._experiences:
            if any(skill_lower == s.lower() for s in e.skills):
                matches.append(e)
                continue

            # also search bullets, technologies, techniques, principles
            text_fields = " ".join(
                e.bullets + e.technologies + e.techniques + e.principles
            )
            if skill_lower in text_fields.lower():
                matches.append(e)

        return matches

    def find_by_technology(self, tech: str) -> List[Experience]:
        tech_lower = tech.lower()
        return [
            e
            for e in self._experiences
            if any(tech_lower == t.lower() for t in e.technologies)
        ]

    def to_json(self) -> List[Dict[str, Any]]:
        return [asdict(e) for e in self._experiences]
