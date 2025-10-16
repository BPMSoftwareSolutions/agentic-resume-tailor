#!/usr/bin/env python3
"""Small CLI to interact with the ExperienceLog for demos and manual use."""
import argparse
from pathlib import Path
from src.experience_log import ExperienceLog, Experience


def main():
    parser = argparse.ArgumentParser(description="Experience Log CLI")
    parser.add_argument("--add", action="store_true", help="Add a sample experience")
    parser.add_argument("--list", action="store_true", help="List experiences")
    parser.add_argument("--skill", type=str, help="Search by skill")
    args = parser.parse_args()

    log = ExperienceLog()

    if args.add:
        exp = Experience(
            id="",
            employer="ExampleCorp",
            role="Senior Engineer",
            dates="2019-2024",
            location="Remote",
            bullets=["Improved deployment pipeline", "Mentored junior engineers"],
            skills=["CI/CD", "Mentoring"],
            technologies=["Docker", "Kubernetes", "GitHub Actions"],
            techniques=["Infrastructure as Code", "Blue/Green deployments"],
            principles=["DRY", "YAGNI"],
            notes="Imported from CLI sample"
        )
        try:
            added = log.add(exp)
            print(f"Added experience id={added.id}")
        except Exception as e:
            print(f"Could not add experience: {e}")

    if args.list:
        for e in log.list():
            print(f"- {e.employer} | {e.role} | {e.dates} | skills={', '.join(e.skills)}")

    if args.skill:
        matches = log.find_by_skill(args.skill)
        print(f"Found {len(matches)} matches for skill '{args.skill}':")
        for e in matches:
            print(f"  - {e.employer} | {e.role} | {e.dates}")


if __name__ == "__main__":
    main()
