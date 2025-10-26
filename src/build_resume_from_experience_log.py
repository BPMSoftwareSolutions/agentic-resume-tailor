#!/usr/bin/env python3
"""
Build Resume from Experience Log

This module builds a complete resume from the experience log (data/experiences.json),
which is the source of truth for all resume data.

The experience log contains:
- Experience entries (employer, role, dates, location, bullets, skills, technologies, techniques, principles)
- Education entries (id starts with 'edu-')
- Certification entries (id starts with 'cert-')

This replaces the need for master_resume.json as the primary source.
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional


def build_resume_from_experience_log(
    experience_log_path: str = "data/experiences.json",
    personal_info: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """
    Build a complete resume from the experience log.

    Args:
        experience_log_path: Path to experiences.json
        personal_info: Optional personal info (name, email, phone, location, title, summary)
                      If not provided, uses defaults

    Returns:
        Complete resume dictionary ready for HTML generation
    """
    # Load experience log
    exp_log_path = Path(experience_log_path)
    if not exp_log_path.exists():
        raise FileNotFoundError(f"Experience log not found: {experience_log_path}")

    with open(exp_log_path, 'r', encoding='utf-8') as f:
        experiences = json.load(f)

    # Default personal info
    default_personal_info = {
        "name": "Sidney Jones",
        "title": "Senior DevOps Software Engineer",
        "location": "West Bloomfield, MI",
        "email": "sjones@bpmsoftwaresolutions.com",
        "phone": "(248) 802-1847",
        "summary": "Accomplished technology leader with extensive experience in driving software engineering management, enterprise architecture, and large-scale transformation initiatives.",
    }

    # Merge with provided personal info
    if personal_info:
        default_personal_info.update(personal_info)

    # Initialize resume structure
    resume = {
        "name": default_personal_info.get("name", ""),
        "title": default_personal_info.get("title", ""),
        "location": default_personal_info.get("location", ""),
        # Keep backward-compatible root fields
        "email": default_personal_info.get("email", ""),
        "phone": default_personal_info.get("phone", ""),
        # New structured contact object for HTML generator
        "contact": {
            "email": default_personal_info.get("email", ""),
            "phone": default_personal_info.get("phone", ""),
        },
        "summary": default_personal_info.get("summary", ""),
        "experience": [],
        "education": [],
        "certifications": [],
        "technical_proficiencies": {},
        "areas_of_expertise": [],
    }

    # Separate entries by type
    experience_entries = []
    education_entries = []
    certification_entries = []

    for entry in experiences:
        entry_id = entry.get("id", "")

        if entry_id.startswith("edu-"):
            education_entries.append(entry)
        elif entry_id.startswith("cert-"):
            certification_entries.append(entry)
        else:
            experience_entries.append(entry)

    # Process experience entries
    print(f"📝 Processing {len(experience_entries)} experience entries...")
    for exp in experience_entries:
        # Combine all tags for this experience
        all_tags = []
        all_tags.extend(exp.get("skills", []) or [])
        all_tags.extend(exp.get("technologies", []) or [])
        all_tags.extend(exp.get("techniques", []) or [])
        all_tags.extend(exp.get("principles", []) or [])

        # Remove duplicates while preserving order
        seen = set()
        unique_tags = []
        for tag in all_tags:
            if tag and tag.lower() not in seen:
                seen.add(tag.lower())
                unique_tags.append(tag)

        # Normalize bullets to list of dicts expected by scorer/generator
        raw_bullets = exp.get("bullets", []) or []
        norm_bullets = []
        for b in raw_bullets:
            if isinstance(b, dict):
                # Ensure text key exists
                text_val = b.get("text") if isinstance(b.get("text"), str) else str(b.get("text", ""))
                tags_val = b.get("tags") if isinstance(b.get("tags"), list) else []
                # Augment with experience-level tags if not present
                if not tags_val and unique_tags:
                    tags_val = unique_tags
                norm_bullets.append({"text": text_val, "tags": tags_val})
            else:
                # Simple string bullet
                norm_bullets.append({"text": str(b), "tags": unique_tags})

        experience_item = {
            "employer": exp.get("employer", ""),
            "role": exp.get("role", ""),
            "dates": exp.get("dates", ""),
            "location": exp.get("location", ""),
            "bullets": norm_bullets,
            "skills": exp.get("skills", []),
            "technologies": exp.get("technologies", []),
            "techniques": exp.get("techniques", []),
            "principles": exp.get("principles", []),
        }

        if unique_tags:
            experience_item["tags"] = unique_tags

        resume["experience"].append(experience_item)

    # Process education entries
    print(f"🎓 Processing {len(education_entries)} education entries...")
    for edu in education_entries:
        education_item = {
            "degree": edu.get("role", ""),
            "institution": edu.get("employer", ""),
            "location": edu.get("location", ""),
            "year": edu.get("dates", ""),
        }
        resume["education"].append(education_item)

    # Process certification entries
    print(f"🏆 Processing {len(certification_entries)} certification entries...")
    for cert in certification_entries:
        certification_item = {
            "name": cert.get("role", ""),
            "issuer": cert.get("employer", ""),
            "date": cert.get("dates", ""),
        }
        resume["certifications"].append(certification_item)

    # Extract technical proficiencies from all skills/technologies
    print("🔧 Extracting technical proficiencies...")
    all_skills = set()
    all_techs = set()

    for exp in experience_entries:
        all_skills.update(exp.get("skills", []) or [])
        all_techs.update(exp.get("technologies", []) or [])

    # Group by category (simple heuristic)
    # Join lists into display strings for HTML generator
    resume["technical_proficiencies"] = {
        "skills": ", ".join(sorted(list(all_skills))) if all_skills else "",
        "technologies": ", ".join(sorted(list(all_techs))) if all_techs else "",
    }

    # Extract areas of expertise (from principles or techniques)
    print("💡 Extracting areas of expertise...")
    all_principles = set()
    for exp in experience_entries:
        all_principles.update(exp.get("principles", []) or [])
        all_principles.update(exp.get("techniques", []) or [])

    resume["areas_of_expertise"] = sorted(list(all_principles)) if all_principles else [
        "Enterprise Architecture & Cloud Transformation",
        "Revenue Growth & Cost Optimization",
        "SaaS Solution Development",
        "Security & Data Protection",
        "AI Adoption & Scaling",
        "Data-Driven Analytics",
        "Process Automation",
        "Relationship Building",
        "Innovation & Product Development",
        "Business Strategy & Value Delivery",
        "Team Leadership & Agile Coaching",
        "Cybersecurity & Compliance",
    ]

    print(f"✅ Resume built successfully!")
    print(f"   - {len(resume['experience'])} experience entries")
    print(f"   - {len(resume['education'])} education entries")
    print(f"   - {len(resume['certifications'])} certification entries")
    print(f"   - {len(all_skills)} unique skills")
    print(f"   - {len(all_techs)} unique technologies")

    return resume


def save_resume_json(resume: Dict[str, Any], output_path: str) -> None:
    """Save resume to JSON file."""
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(resume, f, indent=2, ensure_ascii=False)

    print(f"✅ Resume saved to {output_path}")


if __name__ == "__main__":
    import sys

    # Build resume from experience log
    resume = build_resume_from_experience_log()

    # Save to file
    output_path = "data/resume_from_experience_log.json"
    save_resume_json(resume, output_path)

    print(f"\n✅ Resume built from experience log!")
    print(f"   Output: {output_path}")

