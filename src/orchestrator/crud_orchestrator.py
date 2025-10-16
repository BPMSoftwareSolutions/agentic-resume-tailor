"""
CRUD Orchestrator

Generates and executes sequences of CRUD operations to update resumes based on:
- Job posting analysis
- Resume match results
- User intent

The orchestrator:
1. Analyzes job requirements and resume gaps
2. Generates a sequence of CRUD operations
3. Executes operations in the correct order
4. Validates each operation
5. Provides progress feedback

Usage:
    from orchestrator import CRUDOrchestrator, ResumeMatcher
    from parsers import JobPostingParser

    # Parse job and match resume
    job_parser = JobPostingParser()
    job_data = job_parser.parse_file("job.md")

    matcher = ResumeMatcher()
    match_result = matcher.match(job_data, resume_data)

    # Orchestrate updates
    orchestrator = CRUDOrchestrator()
    operations = orchestrator.generate_operations(job_data, match_result, resume_name="Ford")
    results = orchestrator.execute_operations(operations)
"""

import json
import subprocess
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional


class CRUDOrchestrator:
    """Generate and execute CRUD operation sequences"""

    def __init__(self, data_dir: str = "data", dry_run: bool = False):
        self.data_dir = Path(data_dir)
        self.dry_run = dry_run
        self.progress_callback = None

    def set_progress_callback(self, callback: Callable[[str], None]):
        """Set callback function for progress updates"""
        self.progress_callback = callback

    def _log_progress(self, message: str):
        """Log progress message"""
        if self.progress_callback:
            self.progress_callback(message)
        else:
            print(f"[ORCHESTRATOR] {message}")

    def generate_operations(
        self,
        job_data: Dict[str, Any],
        match_result: Dict[str, Any],
        resume_name: str,
        intent: str = "tailor",
    ) -> List[Dict[str, Any]]:
        """
        Generate sequence of CRUD operations based on job analysis and match results

        Args:
            job_data: Parsed job posting data
            match_result: Resume match analysis
            resume_name: Target resume name
            intent: Operation intent (tailor, update, create)

        Returns:
            List of operation dictionaries with command, description, priority
        """
        operations = []

        # Priority 1: Update title to match job
        if intent == "tailor":
            job_title = job_data.get("title", "")
            if job_title:
                operations.append(
                    {
                        "command": f'python src/crud/basic_info.py --resume "{resume_name}" --update-title "{job_title}"',
                        "description": f"Update title to: {job_title}",
                        "priority": 1,
                        "type": "basic_info",
                    }
                )

        # Priority 2: Add missing critical skills
        missing_skills = match_result.get("missing_skills", [])
        if missing_skills:
            # Group skills by likely category
            skill_categories = self._categorize_skills(missing_skills)

            for category, skills in skill_categories.items():
                if skills:
                    skills_str = ", ".join(skills[:5])  # Limit to 5 per operation
                    operations.append(
                        {
                            "command": f'python src/crud/technical_skills.py --resume "{resume_name}" --append-to-category "{category}" "{skills_str}"',
                            "description": f"Add {category} skills: {skills_str}",
                            "priority": 2,
                            "type": "technical_skills",
                        }
                    )

        # Priority 3: Update summary to emphasize relevant experience
        if intent == "tailor":
            relevant_exp = match_result.get("relevant_experience", [])
            if relevant_exp:
                # Generate summary emphasizing top relevant experience
                summary_hint = self._generate_summary_hint(job_data, relevant_exp)
                operations.append(
                    {
                        "command": f"# Manual: Update summary to emphasize: {summary_hint}",
                        "description": f"Update summary to highlight: {summary_hint}",
                        "priority": 3,
                        "type": "summary",
                        "manual": True,
                    }
                )

        # Priority 4: Add relevant expertise areas
        responsibilities = job_data.get("responsibilities", [])
        if responsibilities:
            # Extract key expertise areas from responsibilities
            expertise_areas = self._extract_expertise_from_responsibilities(
                responsibilities
            )
            for area in expertise_areas[:3]:  # Top 3
                operations.append(
                    {
                        "command": f'python src/crud/expertise.py --resume "{resume_name}" --add "{area}"',
                        "description": f"Add expertise: {area}",
                        "priority": 4,
                        "type": "expertise",
                    }
                )

        # Priority 5: Highlight compliance experience if required
        compliance = job_data.get("compliance_requirements", [])
        if compliance:
            compliance_str = ", ".join(compliance)
            operations.append(
                {
                    "command": f"# Manual: Emphasize {compliance_str} experience in relevant bullets",
                    "description": f"Highlight compliance experience: {compliance_str}",
                    "priority": 5,
                    "type": "experience",
                    "manual": True,
                }
            )

        # Sort by priority
        operations.sort(key=lambda x: x["priority"])

        return operations

    def execute_operations(self, operations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Execute a sequence of CRUD operations

        Returns:
            {
                'total': int,
                'successful': int,
                'failed': int,
                'skipped': int,
                'results': list of result dicts
            }
        """
        results = {
            "total": len(operations),
            "successful": 0,
            "failed": 0,
            "skipped": 0,
            "results": [],
        }

        for i, operation in enumerate(operations, 1):
            self._log_progress(f"[{i}/{len(operations)}] {operation['description']}")

            # Skip manual operations
            if operation.get("manual", False):
                self._log_progress(f"  → Skipped (manual operation)")
                results["skipped"] += 1
                results["results"].append(
                    {
                        "operation": operation,
                        "status": "skipped",
                        "message": "Manual operation",
                    }
                )
                continue

            # Execute command
            if self.dry_run:
                self._log_progress(f"  → DRY RUN: {operation['command']}")
                results["successful"] += 1
                results["results"].append(
                    {
                        "operation": operation,
                        "status": "dry_run",
                        "message": "Dry run mode",
                    }
                )
            else:
                result = self._execute_command(operation["command"])
                if result["success"]:
                    self._log_progress(f"  ✓ Success")
                    results["successful"] += 1
                else:
                    self._log_progress(f"  ✗ Failed: {result['error']}")
                    results["failed"] += 1

                results["results"].append(
                    {
                        "operation": operation,
                        "status": "success" if result["success"] else "failed",
                        "message": result.get("output", result.get("error", "")),
                    }
                )

        return results

    def _execute_command(self, command: str) -> Dict[str, Any]:
        """Execute a single command"""
        try:
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True, timeout=30
            )

            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr if result.returncode != 0 else None,
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Command timed out"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _categorize_skills(self, skills: List[str]) -> Dict[str, List[str]]:
        """Categorize skills into technical skill categories"""
        categories = {
            "languages": [],
            "cloud": [],
            "databases": [],
            "devops": [],
            "billing": [],
            "ai": [],
        }

        # Categorization rules
        language_keywords = [
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
        ]
        cloud_keywords = ["aws", "azure", "gcp", "cloud platform", "google cloud"]
        database_keywords = [
            "sql",
            "mysql",
            "postgresql",
            "mongodb",
            "redis",
            "dynamodb",
        ]
        devops_keywords = [
            "docker",
            "kubernetes",
            "jenkins",
            "ci/cd",
            "terraform",
            "ansible",
            "git",
            "datadog",
        ]
        billing_keywords = [
            "zuora",
            "stripe",
            "chargebee",
            "subscription billing",
            "revpro",
        ]
        ai_keywords = ["ai", "ml", "machine learning", "tensorflow", "pytorch"]

        for skill in skills:
            skill_lower = skill.lower()
            if any(kw in skill_lower for kw in language_keywords):
                categories["languages"].append(skill)
            elif any(kw in skill_lower for kw in cloud_keywords):
                categories["cloud"].append(skill)
            elif any(kw in skill_lower for kw in database_keywords):
                categories["databases"].append(skill)
            elif any(kw in skill_lower for kw in devops_keywords):
                categories["devops"].append(skill)
            elif any(kw in skill_lower for kw in billing_keywords):
                categories["billing"].append(skill)
            elif any(kw in skill_lower for kw in ai_keywords):
                categories["ai"].append(skill)
            else:
                # Default to languages if unsure
                categories["languages"].append(skill)

        # Remove empty categories
        return {k: v for k, v in categories.items() if v}

    def _generate_summary_hint(
        self, job_data: Dict[str, Any], relevant_exp: List[Dict]
    ) -> str:
        """Generate hint for summary update"""
        if not relevant_exp:
            return "relevant experience"

        top_exp = relevant_exp[0]
        job_title = job_data.get("title", "this role")

        return f"{top_exp['employer']} experience for {job_title}"

    def _extract_expertise_from_responsibilities(
        self, responsibilities: List[str]
    ) -> List[str]:
        """Extract expertise areas from job responsibilities"""
        expertise = []

        # Common expertise patterns
        patterns = [
            "leadership",
            "architecture",
            "microservices",
            "cloud",
            "devops",
            "billing",
            "subscription",
            "revenue",
            "compliance",
            "sox",
        ]

        for resp in responsibilities:
            resp_lower = resp.lower()
            for pattern in patterns:
                if pattern in resp_lower and pattern not in [
                    e.lower() for e in expertise
                ]:
                    # Capitalize properly
                    if pattern == "sox":
                        expertise.append("SOX Compliance")
                    elif pattern == "devops":
                        expertise.append("DevOps")
                    else:
                        expertise.append(pattern.title())

        return expertise


def main():
    """Test the orchestrator"""
    import sys
    from pathlib import Path

    # Add src to path
    sys.path.insert(0, str(Path(__file__).parent.parent))

    if len(sys.argv) < 3:
        print(
            "Usage: python crud_orchestrator.py <job_posting_file> <resume_file> [resume_name]"
        )
        sys.exit(1)

    from orchestrator.resume_matcher import ResumeMatcher
    from parsers.job_posting_parser import JobPostingParser

    # Parse job posting
    job_parser = JobPostingParser()
    job_data = job_parser.parse_file(sys.argv[1])

    # Load resume
    with open(sys.argv[2], "r", encoding="utf-8") as f:
        resume_data = json.load(f)

    # Match
    matcher = ResumeMatcher()
    match_result = matcher.match(job_data, resume_data)

    # Generate operations
    resume_name = sys.argv[3] if len(sys.argv) > 3 else "Test Resume"
    orchestrator = CRUDOrchestrator(dry_run=True)
    operations = orchestrator.generate_operations(job_data, match_result, resume_name)

    print("=== CRUD Orchestration Plan ===\n")
    print(f"Resume: {resume_name}")
    print(f"Job: {job_data['title']} at {job_data['company']}")
    print(f"Match Score: {match_result['score']}%\n")
    print(f"Generated {len(operations)} operations:\n")

    for i, op in enumerate(operations, 1):
        manual_flag = " [MANUAL]" if op.get("manual") else ""
        print(f"{i}. {op['description']}{manual_flag}")
        print(f"   Command: {op['command']}")
        print()

    # Execute in dry run mode
    print("\n=== Executing Operations (DRY RUN) ===\n")
    results = orchestrator.execute_operations(operations)

    print(f"\nResults:")
    print(f"  Total: {results['total']}")
    print(f"  Successful: {results['successful']}")
    print(f"  Failed: {results['failed']}")
    print(f"  Skipped: {results['skipped']}")


if __name__ == "__main__":
    main()
