#!/usr/bin/env python3
"""Import experiences from the Ford-tailored markdown file into ExperienceLog.

Creates one Experience entry per job section found in the markdown.
"""
from pathlib import Path
import re
import sys
import json

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.experience_log import ExperienceLog, Experience


MD_PATH = Path(r"c:\source\repos\bpm\internal\agentic-resume-tailor\data\job_listings\Tailored Experience Summary for Ford.md")


def parse_markdown(md_text: str):
    # Split into sections by '### ' headers
    sections = re.split(r"\n(?=### )", md_text)
    entries = []
    header_re = re.compile(r"###\s+\*\*(.+?)\s+—\s+(.+?)\s*\(([^)]+)\)\*\*")

    for sec in sections:
        m = header_re.search(sec)
        if not m:
            continue
        employer = m.group(1).strip()
        role = m.group(2).strip()
        dates = m.group(3).strip()

        # Extract bullets (lines starting with '* ')
        bullets = []
        tags = []
        for line in sec.splitlines():
            line = line.strip()
            if line.startswith("*") and not line.startswith("**"):
                # remove leading '*'
                text = line.lstrip('*').strip()
                if text:
                    bullets.append(text)
            # Tags line like '**Tags:** ...'
            if line.startswith('**Tags:**'):
                t = line.replace('**Tags:**', '').strip()
                tags = [x.strip() for x in t.split(',') if x.strip()]

        entries.append({
            'employer': employer,
            'role': role,
            'dates': dates,
            'bullets': bullets,
            'tags': tags,
        })

    return entries


def main():
    if not MD_PATH.exists():
        print(f"Markdown file not found: {MD_PATH}")
        return

    text = MD_PATH.read_text(encoding='utf-8')
    entries = parse_markdown(text)
    if not entries:
        print("No job sections parsed from markdown.")
        return

    log = ExperienceLog()
    added = 0
    for e in entries:
        exp = Experience(
            id="",
            employer=e['employer'],
            role=e['role'],
            dates=e['dates'],
            location="",
            bullets=e['bullets'],
            skills=e['tags'],
            technologies=[],
            techniques=[],
            principles=[],
            notes="Imported from Ford tailored markdown",
        )
        try:
            log.add(exp)
            print(f"Added: {exp.employer} | {exp.role} | {len(exp.bullets)} bullets")
            added += 1
        except ValueError as ve:
            print(f"Skipped duplicate: {exp.employer} | {exp.role} | {exp.dates} -> {ve}")
        except Exception as ex:
            print(f"Error adding entry for {exp.employer}: {ex}")

    print(f"Done. Entries added: {added}")


if __name__ == '__main__':
    main()
