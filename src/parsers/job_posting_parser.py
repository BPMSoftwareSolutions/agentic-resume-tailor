"""
Job Posting Parser

Parses markdown job postings to extract:
- Job title and level
- Company name
- Location and work arrangement
- Required skills (technical and soft skills)
- Key responsibilities
- Experience requirements
- Preferred qualifications
- Company/industry context

Usage:
    from parsers import JobPostingParser

    parser = JobPostingParser()
    result = parser.parse_file("data/job_listings/job.md")

    print(result['title'])
    print(result['required_skills'])
"""

import re
from pathlib import Path
from typing import Any, Dict, List, Optional


class JobPostingParser:
    """Parse job postings to extract structured information"""

    # Common technical skill keywords
    TECH_SKILLS = {
        "languages": [
            "python",
            "java",
            "javascript",
            "typescript",
            "c++",
            "c#",
            "go",
            "rust",
            "ruby",
            "php",
            "swift",
            "kotlin",
        ],
        "frameworks": [
            "spring boot",
            "react",
            "angular",
            "vue",
            "django",
            "flask",
            "express",
            "node.js",
            ".net",
        ],
        "cloud": ["aws", "azure", "gcp", "google cloud", "cloud platform"],
        "databases": [
            "sql",
            "mysql",
            "postgresql",
            "mongodb",
            "redis",
            "dynamodb",
            "oracle",
        ],
        "devops": [
            "docker",
            "kubernetes",
            "jenkins",
            "ci/cd",
            "terraform",
            "ansible",
            "gitlab",
        ],
        "tools": ["git", "jira", "confluence", "datadog", "splunk", "grafana"],
        "billing": [
            "zuora",
            "stripe",
            "chargebee",
            "recurly",
            "revpro",
            "subscription billing",
        ],
        "methodologies": [
            "agile",
            "scrum",
            "kanban",
            "devops",
            "microservices",
            "api",
            "rest",
            "graphql",
        ],
    }

    # Soft skills keywords
    SOFT_SKILLS = [
        "leadership",
        "communication",
        "collaboration",
        "problem solving",
        "analytical",
        "mentorship",
        "stakeholder management",
        "strategic thinking",
        "team building",
    ]

    def __init__(self):
        self.content = ""
        self.lines = []

    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """Parse a job posting file and return structured data"""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Job posting file not found: {file_path}")

        with open(path, "r", encoding="utf-8") as f:
            self.content = f.read()

        # Normalize Unicode quotes and dashes to ASCII equivalents
        self.content = self.content.replace(
            "\u2019", "'"
        )  # Right single quotation mark
        self.content = self.content.replace("\u2018", "'")  # Left single quotation mark
        self.content = self.content.replace("\u201c", '"')  # Left double quotation mark
        self.content = self.content.replace(
            "\u201d", '"'
        )  # Right double quotation mark
        self.content = self.content.replace("\u2013", "-")  # En dash
        self.content = self.content.replace("\u2014", "-")  # Em dash
        self.content = self.content.replace("\u2011", "-")  # Non-breaking hyphen

        self.lines = self.content.split("\n")

        return {
            "title": self._extract_title(),
            "company": self._extract_company(),
            "location": self._extract_location(),
            "work_arrangement": self._extract_work_arrangement(),
            "required_skills": self._extract_required_skills(),
            "preferred_skills": self._extract_preferred_skills(),
            "responsibilities": self._extract_responsibilities(),
            "experience_years": self._extract_experience_years(),
            "management_experience": self._extract_management_experience(),
            "technical_requirements": self._extract_technical_requirements(),
            "soft_skills": self._extract_soft_skills(),
            "compliance_requirements": self._extract_compliance_requirements(),
            "raw_content": self.content,
        }

    def _extract_title(self) -> str:
        """Extract job title from the first line or title pattern"""
        if self.lines:
            # First line often contains the title
            first_line = self.lines[0].strip()
            # Remove common suffixes like "- job post"
            title = re.sub(r"\s*-\s*job post.*$", "", first_line, flags=re.IGNORECASE)
            return title.strip()
        return ""

    def _extract_company(self) -> str:
        """Extract company name"""
        # Look for company name in first few lines
        for i, line in enumerate(self.lines[:10]):
            line = line.strip()
            # Skip empty lines and the title
            if i == 0 or not line:
                continue
            # Company name is often on line 2 or 3
            if not any(
                keyword in line.lower()
                for keyword in ["out of", "stars", "full-time", "part-time"]
            ):
                # Check if it looks like a company name (not too long, not a rating)
                if len(line) < 50 and not re.match(r"^\d+\.?\d*$", line):
                    return line
        return ""

    def _extract_location(self) -> str:
        """Extract job location"""
        for line in self.lines[:15]:
            # Look for city, state patterns
            if re.search(r"[A-Z][a-z]+,\s*[A-Z]{2}", line):
                match = re.search(r"([A-Z][a-z]+,\s*[A-Z]{2})", line)
                if match:
                    return match.group(1)
        return ""

    def _extract_work_arrangement(self) -> str:
        """Extract work arrangement (remote, hybrid, on-site)"""
        content_lower = self.content.lower()
        if "hybrid" in content_lower:
            return "hybrid"
        elif "remote" in content_lower:
            return "remote"
        elif "on-site" in content_lower or "onsite" in content_lower:
            return "on-site"
        return "not specified"

    def _extract_required_skills(self) -> List[str]:
        """Extract required technical skills"""
        skills = set()
        content_lower = self.content.lower()

        # Extract from all technical skill categories
        for category, keywords in self.TECH_SKILLS.items():
            for keyword in keywords:
                if keyword in content_lower:
                    skills.add(keyword)

        # Look for skills in required qualifications section
        required_section = self._extract_section(
            ["required qualifications", "your skills & abilities", "requirements"]
        )
        if required_section:
            # Extract specific patterns like "5+ years of X"
            patterns = [
                r"experience (?:with|in) ([^.,\n]+)",
                r"proficiency in ([^.,\n]+)",
                r"knowledge of ([^.,\n]+)",
                r"hands[‑-]on (?:experience )?(?:with|in) ([^.,\n]+)",
            ]
            for pattern in patterns:
                matches = re.finditer(pattern, required_section.lower())
                for match in matches:
                    skill_text = match.group(1).strip()
                    # Extract individual skills from the text
                    for category, keywords in self.TECH_SKILLS.items():
                        for keyword in keywords:
                            if keyword in skill_text:
                                skills.add(keyword)

        return sorted(list(skills))

    def _extract_preferred_skills(self) -> List[str]:
        """Extract preferred/nice-to-have skills"""
        skills = set()
        preferred_section = self._extract_section(
            ["preferred qualifications", "competitive edge", "nice to have", "bonus"]
        )

        if preferred_section:
            content_lower = preferred_section.lower()
            for category, keywords in self.TECH_SKILLS.items():
                for keyword in keywords:
                    if keyword in content_lower:
                        skills.add(keyword)

        return sorted(list(skills))

    def _extract_responsibilities(self) -> List[str]:
        """Extract key responsibilities"""
        responsibilities = []
        resp_section = self._extract_section(
            ["what you'll do", "responsibilities", "key responsibilities", "duties"]
        )

        # Debug: print the section
        # print(f"DEBUG: Responsibilities section:\n{resp_section[:500]}\n")

        if resp_section:
            # Split by double newlines (paragraphs) or single newlines
            lines = resp_section.split("\n")
            for line in lines:
                line = line.strip()
                if not line:  # Skip empty lines
                    continue
                # Remove bullet points and numbering
                line = re.sub(r"^[\-\*\•]\s*", "", line)
                line = re.sub(r"^\d+[\.\)]\s*", "", line)
                # Filter out short lines and lines that look like section headers
                if len(line) > 30 and not line.isupper():
                    # Stop at next section
                    if any(
                        header in line.lower()
                        for header in [
                            "your skills",
                            "qualifications",
                            "requirements",
                            "what will give",
                        ]
                    ):
                        break
                    responsibilities.append(line)

        return responsibilities

    def _extract_experience_years(self) -> Optional[int]:
        """Extract required years of experience"""
        # Look for patterns like "5+ years", "3-5 years", "minimum 7 years"
        patterns = [
            r"(\d+)\+?\s*years",
            r"minimum\s+(\d+)\s+years",
            r"at least\s+(\d+)\s+years",
        ]

        for pattern in patterns:
            match = re.search(pattern, self.content.lower())
            if match:
                return int(match.group(1))

        return None

    def _extract_management_experience(self) -> Optional[int]:
        """Extract required management experience years"""
        # Look for management-specific experience
        patterns = [
            r"(\d+)\+?\s*years\s+of\s+managerial\s+experience",
            r"(\d+)\+?\s*years\s+managing",
            r"(\d+)\+?\s*years\s+of\s+leadership\s+experience",
        ]

        for pattern in patterns:
            match = re.search(pattern, self.content.lower())
            if match:
                return int(match.group(1))

        return None

    def _extract_technical_requirements(self) -> List[str]:
        """Extract specific technical requirements"""
        requirements = []

        # Look for implementation requirements
        impl_patterns = [
            r"(\d+)\+?\s+(?:full lifecycle )?implementations? of ([^.,\n]+)",
            r"experience implementing ([^.,\n]+)",
            r"deployed ([^.,\n]+)",
        ]

        for pattern in impl_patterns:
            matches = re.finditer(pattern, self.content.lower())
            for match in matches:
                if len(match.groups()) > 1:
                    requirements.append(
                        f"{match.group(1)} implementations of {match.group(2).strip()}"
                    )
                else:
                    requirements.append(match.group(1).strip())

        return requirements

    def _extract_soft_skills(self) -> List[str]:
        """Extract soft skills requirements"""
        skills = set()
        content_lower = self.content.lower()

        for skill in self.SOFT_SKILLS:
            if skill in content_lower:
                skills.add(skill)

        return sorted(list(skills))

    def _extract_compliance_requirements(self) -> List[str]:
        """Extract compliance and regulatory requirements"""
        compliance = []
        content_lower = self.content.lower()

        compliance_keywords = [
            "sox",
            "gdpr",
            "hipaa",
            "pci",
            "compliance",
            "audit",
            "security",
        ]

        for keyword in compliance_keywords:
            if keyword in content_lower:
                compliance.append(
                    keyword.upper()
                    if keyword in ["sox", "gdpr", "hipaa", "pci"]
                    else keyword
                )

        return list(set(compliance))

    def _extract_section(self, section_headers: List[str]) -> str:
        """Extract content from a specific section"""
        content_lower = self.content.lower()

        for header in section_headers:
            # Find the section header
            pattern = rf"^.*{re.escape(header)}.*$"
            match = re.search(pattern, content_lower, re.MULTILINE)

            if match:
                start_pos = match.end()
                # Find the next major section (usually starts with capital letter and is short)
                # Look for patterns like "Your Skills & Abilities" or "What Will Give You"
                next_section_pattern = (
                    r"\n\n(?:[A-Z][^\n]{10,60}\n|[A-Z][a-z]+ [A-Z][^\n]+\n)"
                )
                next_section = re.search(next_section_pattern, self.content[start_pos:])
                if next_section:
                    end_pos = start_pos + next_section.start()
                else:
                    end_pos = len(self.content)

                return self.content[start_pos:end_pos].strip()

        return ""


def main():
    """Test the parser with a sample job posting"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python job_posting_parser.py <job_posting_file>")
        sys.exit(1)

    parser = JobPostingParser()
    result = parser.parse_file(sys.argv[1])

    print("=== Job Posting Analysis ===\n")
    print(f"Title: {result['title']}")
    print(f"Company: {result['company']}")
    print(f"Location: {result['location']}")
    print(f"Work Arrangement: {result['work_arrangement']}")
    print(f"\nExperience Required: {result['experience_years']} years")
    if result["management_experience"]:
        print(f"Management Experience: {result['management_experience']} years")

    print(f"\nRequired Skills ({len(result['required_skills'])}):")
    for skill in result["required_skills"]:
        print(f"  - {skill}")

    if result["preferred_skills"]:
        print(f"\nPreferred Skills ({len(result['preferred_skills'])}):")
        for skill in result["preferred_skills"]:
            print(f"  - {skill}")

    print(f"\nKey Responsibilities ({len(result['responsibilities'])}):")
    for resp in result["responsibilities"][:5]:  # Show first 5
        print(f"  - {resp}")

    if result["technical_requirements"]:
        print(f"\nTechnical Requirements:")
        for req in result["technical_requirements"]:
            print(f"  - {req}")

    if result["soft_skills"]:
        print(f"\nSoft Skills:")
        for skill in result["soft_skills"]:
            print(f"  - {skill}")

    if result["compliance_requirements"]:
        print(f"\nCompliance Requirements:")
        for req in result["compliance_requirements"]:
            print(f"  - {req}")


if __name__ == "__main__":
    main()
