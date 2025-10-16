"""
Experience Parser

Parses markdown files containing work experience sections to extract:
- Employer name
- Role/title
- Dates (start and end)
- Location
- Bullet points/achievements
- Tags/skills

Supports multiple formats:
- Standard resume format with employer headers
- Tailored experience summaries
- Bullet-point lists

Usage:
    from parsers import ExperienceParser

    parser = ExperienceParser()
    experiences = parser.parse_file("data/experience.md")

    for exp in experiences:
        print(f"{exp['employer']} - {exp['role']}")
"""

import re
from pathlib import Path
from typing import Any, Dict, List, Optional


class ExperienceParser:
    """Parse markdown experience files to extract structured work history"""

    def __init__(self):
        self.content = ""
        self.lines = []

    def parse_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Parse an experience file and return list of experience entries"""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Experience file not found: {file_path}")

        with open(path, "r", encoding="utf-8") as f:
            self.content = f.read()

        # Normalize Unicode characters
        self.content = self.content.replace("\u2019", "'")
        self.content = self.content.replace("\u2018", "'")
        self.content = self.content.replace("\u201c", '"')
        self.content = self.content.replace("\u201d", '"')
        self.content = self.content.replace("\u2013", "-")
        self.content = self.content.replace("\u2014", "-")
        self.content = self.content.replace("\u2011", "-")

        self.lines = self.content.split("\n")

        return self._extract_experiences()

    def _extract_experiences(self) -> List[Dict[str, Any]]:
        """Extract all experience entries from the content"""
        experiences = []

        # Look for experience headers (### Employer - Role (Dates))
        # After normalization, all dashes should be regular hyphens
        pattern = r"^###\s+\*\*(.+?)\s+[-]\s+(.+?)\s+\((.+?)\)\*\*\s*$"

        i = 0
        while i < len(self.lines):
            line = self.lines[i].strip()
            match = re.match(pattern, line)

            if match:
                employer = match.group(1).strip()
                role = match.group(2).strip()
                dates = match.group(3).strip()

                # Extract bullets and tags for this experience
                bullets, tags, end_index = self._extract_bullets_and_tags(i + 1)

                # Try to parse location from role if present
                location = ""
                if "/" in role:
                    parts = role.split("/")
                    role = parts[0].strip()

                experiences.append(
                    {
                        "employer": employer,
                        "role": role,
                        "dates": dates,
                        "location": location,
                        "bullets": bullets,
                        "tags": tags,
                    }
                )

                i = end_index
            else:
                i += 1

        return experiences

    def _extract_bullets_and_tags(
        self, start_index: int
    ) -> tuple[List[str], List[str], int]:
        """Extract bullet points and tags from an experience section"""
        bullets = []
        tags = []
        i = start_index

        while i < len(self.lines):
            line = self.lines[i].strip()

            # Stop at next experience header or major section
            if line.startswith("###") or line.startswith("##"):
                break

            # Check for tags line
            if line.startswith("**Tags:**"):
                # Extract tags
                tags_text = line.replace("**Tags:**", "").strip()
                tags = [tag.strip() for tag in tags_text.split(",")]
                i += 1
                continue

            # Check for bullet point
            if line.startswith("*") or line.startswith("-"):
                # Remove bullet marker
                bullet = re.sub(r"^[\*\-]\s+", "", line)
                if bullet and len(bullet) > 10:  # Filter out very short bullets
                    bullets.append(bullet)

            i += 1

        return bullets, tags, i

    def parse_text(self, text: str) -> List[Dict[str, Any]]:
        """Parse experience text directly (useful for testing)"""
        self.content = text

        # Normalize Unicode characters
        self.content = self.content.replace("\u2019", "'")
        self.content = self.content.replace("\u2018", "'")
        self.content = self.content.replace("\u201c", '"')
        self.content = self.content.replace("\u201d", '"')
        self.content = self.content.replace("\u2013", "-")
        self.content = self.content.replace("\u2014", "-")
        self.content = self.content.replace("\u2011", "-")

        self.lines = self.content.split("\n")

        return self._extract_experiences()

    def format_for_crud(self, experiences: List[Dict[str, Any]]) -> str:
        """Format experiences for use with CRUD experience.py script"""
        output = []

        for exp in experiences:
            output.append(f"# {exp['employer']} - {exp['role']}")
            output.append(f"Dates: {exp['dates']}")
            if exp["location"]:
                output.append(f"Location: {exp['location']}")
            output.append("")

            for bullet in exp["bullets"]:
                output.append(f"- {bullet}")

            if exp["tags"]:
                output.append(f"\nTags: {', '.join(exp['tags'])}")

            output.append("\n---\n")

        return "\n".join(output)


def main():
    """Test the parser with a sample experience file"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python experience_parser.py <experience_file>")
        sys.exit(1)

    parser = ExperienceParser()
    experiences = parser.parse_file(sys.argv[1])

    print(f"=== Parsed {len(experiences)} Experience Entries ===\n")

    for i, exp in enumerate(experiences, 1):
        print(f"{i}. {exp['employer']}")
        print(f"   Role: {exp['role']}")
        print(f"   Dates: {exp['dates']}")
        if exp["location"]:
            print(f"   Location: {exp['location']}")
        print(f"   Bullets: {len(exp['bullets'])}")
        if exp["tags"]:
            print(
                f"   Tags: {', '.join(exp['tags'][:5])}{'...' if len(exp['tags']) > 5 else ''}"
            )
        print()

    # Show first experience in detail
    if experiences:
        print("=== First Experience Detail ===\n")
        exp = experiences[0]
        print(f"Employer: {exp['employer']}")
        print(f"Role: {exp['role']}")
        print(f"Dates: {exp['dates']}")
        print(f"\nBullets:")
        for bullet in exp["bullets"][:3]:
            print(f"  - {bullet}")
        if len(exp["bullets"]) > 3:
            print(f"  ... and {len(exp['bullets']) - 3} more")

        if exp["tags"]:
            print(f"\nTags: {', '.join(exp['tags'])}")


if __name__ == "__main__":
    main()
