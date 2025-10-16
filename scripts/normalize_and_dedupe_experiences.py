#!/usr/bin/env python3
"""Normalize skills/technologies, extract tags from resume JSONs into Experience fields,
and perform global deduplication of bullets in data/experiences.json.

Behavior:
- Lowercase and dedupe skills/technologies lists.
- For entries that have notes like 'Imported from resume: ...', attempt to find the original
  resume JSON and merge bullet-level tags (if present) into the entry's skills/technologies.
- Remove duplicate bullets across the whole file (keep first occurrence).
"""
from pathlib import Path
import json
import sys
from typing import Set

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DATA_FILE = ROOT / 'data' / 'experiences.json'
RESUMES_DIR = ROOT / 'data' / 'resumes'

# Small heuristic technology keywords to classify tags -> technology vs skill
TECH_KEYWORDS = {
    'aws', 'azure', 'docker', 'kubernetes', 'jenkins', 'terraform', 'github actions',
    'python', 'java', 'c#', 'c++', 'node.js', 'node', 'react', 'flask', 'sql', 'mysql',
    'dynamodb', 's3', 'lambda', 'ec2', 'cloudwatch', 'sonarqube', 'prometheus', 'grafana'
}


def normalize_token(t: str) -> str:
    return t.strip()


def is_tech(tag: str) -> bool:
    k = tag.lower().strip()
    for kw in TECH_KEYWORDS:
        if kw in k:
            return True
    return False


def load_json(path: Path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(path: Path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main():
    if not DATA_FILE.exists():
        print(f"Data file missing: {DATA_FILE}")
        return

    data = load_json(DATA_FILE)

    # Map of seen bullets to first occurrence index
    seen_bullets: Set[str] = set()
    new_entries = []

    # Attempt to build a map from resume name -> resume JSON to extract bullet tags
    resume_map = {}
    idx_file = RESUMES_DIR / 'index.json'
    if idx_file.exists():
        idx = load_json(idx_file)
        for r in idx.get('resumes', []):
            resume_map[r.get('name')] = RESUMES_DIR / f"{r.get('id')}.json"

    for entry in data:
        # Normalize skills and technologies
        skills = entry.get('skills') or []
        techs = entry.get('technologies') or []

        norm_skills = []
        for s in skills:
            s_norm = normalize_token(s)
            if s_norm and s_norm not in norm_skills:
                norm_skills.append(s_norm)

        norm_techs = []
        for t in techs:
            t_norm = normalize_token(t)
            if t_norm and t_norm not in norm_techs:
                norm_techs.append(t_norm)

        # If entry came from a resume, try to extract bullet tags from that resume file
        notes = entry.get('notes','') or ''
        if notes.startswith('Imported from resume:'):
            name = notes.replace('Imported from resume:', '').strip()
            resume_path = resume_map.get(name)
            if resume_path and resume_path.exists():
                try:
                    rj = load_json(resume_path)
                    # Find a matching experience in the resume by employer+role+dates
                    for e in rj.get('experience', []):
                        if (e.get('employer','').strip().lower() == entry.get('employer','').strip().lower() and
                                e.get('role','').strip().lower() == entry.get('role','').strip().lower()):
                            # extract tags from bullets
                            for b in e.get('bullets', []):
                                if isinstance(b, dict):
                                    for tag in b.get('tags', []):
                                        if is_tech(tag):
                                            if tag not in norm_techs:
                                                norm_techs.append(tag)
                                        else:
                                            if tag not in norm_skills:
                                                norm_skills.append(tag)
                            break
                except Exception:
                    pass

        # Also try to pull tags from the experience's notes if present (Ford imports set skills already)

        # Normalize lists: strip and dedupe ignoring case
        def dedupe_preserve(items):
            out = []
            seen = set()
            for it in items:
                if not it:
                    continue
                key = it.strip()
                key_lower = key.lower()
                if key_lower not in seen:
                    seen.add(key_lower)
                    out.append(key)
            return out

        entry['skills'] = dedupe_preserve(norm_skills)
        entry['technologies'] = dedupe_preserve(norm_techs)

        # Deduplicate bullets globally (exact match). Keep first occurrence.
        new_bullets = []
        for b in entry.get('bullets', []):
            b_text = b.strip() if isinstance(b, str) else str(b).strip()
            if not b_text:
                continue
            if b_text in seen_bullets:
                # skip duplicate bullet
                continue
            seen_bullets.add(b_text)
            new_bullets.append(b_text)

        entry['bullets'] = new_bullets
        new_entries.append(entry)

    save_json(DATA_FILE, new_entries)
    print(f"Normalization and dedupe complete. Entries: {len(new_entries)}")


if __name__ == '__main__':
    main()
