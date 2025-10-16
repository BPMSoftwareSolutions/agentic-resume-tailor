"""
Natural Language Command Parser

Parses natural language commands to identify:
- Intent (add, update, remove, list, show, create, duplicate)
- Entity type (skill, experience, certification, education, summary, etc.)
- Target resume
- Parameters and values

Maps commands to appropriate CRUD script calls.

Usage:
    from parsers import NLCommandParser

    parser = NLCommandParser()
    result = parser.parse("Add Python to my technical skills")

    print(result['intent'])  # 'add'
    print(result['entity'])  # 'technical_skills'
    print(result['command'])  # 'python src/crud/technical_skills.py ...'
"""

import re
from typing import Any, Dict, List, Optional


class NLCommandParser:
    """Parse natural language commands and map to CRUD operations"""

    # Intent keywords
    INTENTS = {
        "add": ["add", "append", "include", "insert"],
        "update": ["update", "change", "modify", "edit", "set"],
        "remove": ["remove", "delete", "drop"],
        "list": ["list", "show all", "display all"],
        "show": ["show", "display", "get", "view"],
        "create": ["create", "make", "generate", "build"],
        "duplicate": ["duplicate", "copy", "clone"],
    }

    # Entity keywords
    ENTITIES = {
        "technical_skills": ["technical skill", "skill", "technology", "tech stack"],
        "expertise": ["expertise", "area of expertise", "specialization"],
        "experience": ["experience", "work history", "job", "position", "role"],
        "education": ["education", "degree", "university", "college"],
        "certification": ["certification", "cert", "certificate"],
        "summary": ["summary", "profile", "about"],
        "basic_info": ["title", "name", "email", "phone", "location", "contact"],
        "achievements": ["achievement", "accomplishment"],
        "resume": ["resume", "cv"],
    }

    # CRUD script mapping
    CRUD_SCRIPTS = {
        "technical_skills": "src/crud/technical_skills.py",
        "expertise": "src/crud/expertise.py",
        "experience": "src/crud/experience.py",
        "education": "src/crud/education.py",
        "certification": "src/crud/certifications.py",
        "summary": "src/crud/summary.py",
        "basic_info": "src/crud/basic_info.py",
        "achievements": "src/crud/achievements.py",
    }

    def __init__(self):
        self.command_text = ""

    def parse(
        self, command: str, default_resume: str = "Master Resume"
    ) -> Dict[str, Any]:
        """Parse a natural language command and return structured result"""
        self.command_text = command.lower().strip()

        # Identify intent
        intent = self._identify_intent()

        # Identify entity type
        entity = self._identify_entity()

        # Extract resume name
        resume = self._extract_resume() or default_resume

        # Extract parameters based on intent and entity
        params = self._extract_parameters(intent, entity)

        # Generate CRUD command
        crud_command = self._generate_crud_command(intent, entity, resume, params)

        return {
            "intent": intent,
            "entity": entity,
            "resume": resume,
            "parameters": params,
            "command": crud_command,
            "original": command,
        }

    def _identify_intent(self) -> str:
        """Identify the intent from the command"""
        for intent, keywords in self.INTENTS.items():
            for keyword in keywords:
                if keyword in self.command_text:
                    return intent
        return "unknown"

    def _identify_entity(self) -> str:
        """Identify the entity type from the command"""
        for entity, keywords in self.ENTITIES.items():
            for keyword in keywords:
                if keyword in self.command_text:
                    return entity
        return "unknown"

    def _extract_resume(self) -> Optional[str]:
        """Extract resume name from command"""
        # Look for patterns like "in resume X", "to resume X", "for resume X"
        patterns = [
            r'(?:in|to|for|from)\s+(?:resume\s+)?["\']?([^"\']+?)["\']?\s+(?:resume)?',
            r'resume\s+["\']?([^"\']+?)["\']?',
            r"my\s+([A-Z][a-z]+)\s+resume",
        ]

        for pattern in patterns:
            match = re.search(pattern, self.command_text, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        return None

    def _extract_parameters(self, intent: str, entity: str) -> Dict[str, Any]:
        """Extract parameters based on intent and entity"""
        params = {}

        if entity == "technical_skills":
            params = self._extract_skill_params(intent)
        elif entity == "expertise":
            params = self._extract_expertise_params(intent)
        elif entity == "experience":
            params = self._extract_experience_params(intent)
        elif entity == "summary":
            params = self._extract_summary_params(intent)
        elif entity == "basic_info":
            params = self._extract_basic_info_params(intent)
        elif entity == "certification":
            params = self._extract_certification_params(intent)
        elif entity == "education":
            params = self._extract_education_params(intent)
        elif entity == "resume":
            params = self._extract_resume_params(intent)

        return params

    def _extract_skill_params(self, intent: str) -> Dict[str, Any]:
        """Extract parameters for technical skills commands"""
        params = {}

        # Extract skill names (words after "add", "append", etc.)
        if intent in ["add", "update"]:
            # Look for skill names after intent keyword
            pattern = r"(?:add|append|include)\s+(.+?)\s+(?:to|in)"
            match = re.search(pattern, self.command_text)
            if match:
                skills_text = match.group(1).strip()
                # Split by "and" or commas
                skills = re.split(r"\s+and\s+|,\s*", skills_text)
                params["skills"] = [s.strip() for s in skills if s.strip()]

            # Try to identify category
            categories = ["languages", "cloud", "databases", "devops", "ai", "security"]
            for cat in categories:
                if cat in self.command_text:
                    params["category"] = cat
                    break

        return params

    def _extract_expertise_params(self, intent: str) -> Dict[str, Any]:
        """Extract parameters for expertise commands"""
        params = {}

        if intent == "add":
            # Extract expertise area
            pattern = r"(?:add|include)\s+(.+?)(?:\s+to|\s+in|$)"
            match = re.search(pattern, self.command_text)
            if match:
                params["area"] = match.group(1).strip()

        return params

    def _extract_experience_params(self, intent: str) -> Dict[str, Any]:
        """Extract parameters for experience commands"""
        params = {}

        # This is complex - for now, just flag that it needs file input
        if "from file" in self.command_text or "with file" in self.command_text:
            pattern = r'(?:from|with)\s+file\s+["\']?([^"\']+)["\']?'
            match = re.search(pattern, self.command_text)
            if match:
                params["file"] = match.group(1).strip()

        return params

    def _extract_summary_params(self, intent: str) -> Dict[str, Any]:
        """Extract parameters for summary commands"""
        params = {}

        if "from file" in self.command_text:
            pattern = r'from\s+file\s+["\']?([^"\']+)["\']?'
            match = re.search(pattern, self.command_text)
            if match:
                params["file"] = match.group(1).strip()

        return params

    def _extract_basic_info_params(self, intent: str) -> Dict[str, Any]:
        """Extract parameters for basic info commands"""
        params = {}

        # Identify which field to update
        if "title" in self.command_text:
            params["field"] = "title"
            pattern = r'(?:title\s+to|title\s+as)\s+["\']?([^"\']+)["\']?'
            match = re.search(pattern, self.command_text)
            if match:
                params["value"] = match.group(1).strip()
        elif "email" in self.command_text:
            params["field"] = "email"
        elif "phone" in self.command_text:
            params["field"] = "phone"
        elif "location" in self.command_text:
            params["field"] = "location"

        return params

    def _extract_certification_params(self, intent: str) -> Dict[str, Any]:
        """Extract parameters for certification commands"""
        return {}

    def _extract_education_params(self, intent: str) -> Dict[str, Any]:
        """Extract parameters for education commands"""
        return {}

    def _extract_resume_params(self, intent: str) -> Dict[str, Any]:
        """Extract parameters for resume commands"""
        params = {}

        if intent == "duplicate":
            # Extract source and target names
            pattern = (
                r"duplicate\s+(?:the\s+)?(.+?)\s+(?:resume\s+)?(?:as|to|into)\s+(.+)"
            )
            match = re.search(pattern, self.command_text)
            if match:
                params["source"] = match.group(1).strip()
                params["target"] = match.group(2).strip()

        return params

    def _generate_crud_command(
        self, intent: str, entity: str, resume: str, params: Dict[str, Any]
    ) -> str:
        """Generate the CRUD command to execute"""

        # Handle resume duplication separately
        if entity == "resume" and intent == "duplicate":
            source = params.get("source", resume)
            target = params.get("target", "New Resume")
            return f'python src/duplicate_resume.py --resume "{source}" --new-name "{target}"'

        # Get the CRUD script
        script = self.CRUD_SCRIPTS.get(entity)
        if not script:
            return f"# Unknown entity: {entity}"

        # Build command based on intent and entity
        cmd = f'python {script} --resume "{resume}"'

        if entity == "technical_skills":
            if intent == "add" and "skills" in params:
                category = params.get("category", "languages")
                skills_str = ", ".join(params["skills"])
                cmd += f' --append-to-category "{category}" "{skills_str}"'
            elif intent == "list":
                cmd += " --list"

        elif entity == "expertise":
            if intent == "add" and "area" in params:
                cmd += f' --add "{params["area"]}"'
            elif intent == "list":
                cmd += " --list"

        elif entity == "summary":
            if intent == "update" and "file" in params:
                cmd += f' --from-file "{params["file"]}"'
            elif intent == "show":
                cmd += " --show"

        elif entity == "basic_info":
            if intent == "update" and "field" in params:
                field = params["field"]
                if "value" in params:
                    cmd += f' --update-{field} "{params["value"]}"'
            elif intent == "show":
                cmd += " --show"

        elif intent == "list":
            cmd += " --list"
        elif intent == "show":
            cmd += " --show"

        return cmd


def main():
    """Test the parser with sample commands"""
    parser = NLCommandParser()

    test_commands = [
        "Add Python to my technical skills",
        "Add Python and Stripe to my technical skills",
        "Update my title to Principal Architect",
        "List my certifications",
        "Show my summary",
        "Duplicate the Ford resume as GM_Resume",
        "Add AI/ML Engineering to my expertise",
        "Update resume with file C:\\path\\to\\experience.md",
    ]

    print("=== Natural Language Command Parser Test ===\n")

    for cmd in test_commands:
        print(f"Command: {cmd}")
        result = parser.parse(cmd)
        print(f"  Intent: {result['intent']}")
        print(f"  Entity: {result['entity']}")
        print(f"  Resume: {result['resume']}")
        if result["parameters"]:
            print(f"  Params: {result['parameters']}")
        print(f"  CRUD: {result['command']}")
        print()


if __name__ == "__main__":
    main()
