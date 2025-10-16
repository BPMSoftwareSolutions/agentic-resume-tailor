"""Seed a basic taxonomy at data/tags/taxonomy.json using skills/technologies from experiences.json

Usage: python scripts/seed_tags.py
"""
import json
from pathlib import Path
import re

ROOT = Path(__file__).parent.parent
EXP = ROOT / 'data' / 'experiences.json'
TAX = ROOT / 'data' / 'tags' / 'taxonomy.json'

def slug(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s

def main():
    TAX.parent.mkdir(parents=True, exist_ok=True)
    if not EXP.exists():
        print('No experiences.json found at', EXP)
        return
    data = json.loads(EXP.read_text(encoding='utf-8'))
    tags = {}
    for e in data:
        for t in e.get('technologies', []) or []:
            key = slug(t)
            tags[key] = {'label': t, 'category': 'technology', 'synonyms': []}
        for s in e.get('skills', []) or []:
            key = slug(s)
            # avoid overwriting technology labels
            if key in tags and tags[key]['category'] == 'technology':
                continue
            tags.setdefault(key, {'label': s, 'category': 'skill', 'synonyms': []})

    # Basic manual additions useful for resumes
    extras = ['FastAPI','PostgreSQL','OpenSearch','RAG','LLM','Terraform','Kubernetes','Docker','CI/CD','GitHub Actions','Jenkins']
    for ex in extras:
        k = slug(ex)
        tags.setdefault(k, {'label': ex, 'category': 'technology' if any(c.isupper() for c in ex) else 'skill', 'synonyms': []})

    TAX.write_text(json.dumps(tags, indent=2), encoding='utf-8')
    print('Seeded taxonomy with', len(tags), 'entries to', TAX)

if __name__ == '__main__':
    main()
