"""Assign tags to bullets conservatively and export suggestions to CSV.

Usage examples:
  # dry-run and export suggestions
  python scripts/assign_tags.py --dry-run --output resume_output/tag_suggestions.csv --max-tags 4

  # apply changes in-place
  python scripts/assign_tags.py --apply --max-tags 4
"""
import json
from pathlib import Path
import csv
import argparse
import re

ROOT = Path(__file__).parent.parent
EXP = ROOT / 'data' / 'experiences.json'
TAIL = ROOT / 'data' / 'tailored_westlaw_lead_software_engineer_ai.json'
TAX = ROOT / 'data' / 'tags' / 'taxonomy.json'

def slug(s: str) -> str:
    return re.sub(r'[^a-z0-9]+','', s.lower())

def load_taxonomy():
    if not TAX.exists():
        return {}
    return json.loads(TAX.read_text(encoding='utf-8'))

def find_matches(text: str, candidates):
    text_l = text.lower()
    hits = []
    for key, meta in candidates.items():
        label = meta.get('label','').lower()
        if label and label in text_l:
            hits.append((key, meta['label']))
        # synonyms
        for syn in meta.get('synonyms',[]):
            if syn.lower() in text_l:
                hits.append((key, meta['label']))
    return hits

def suggest_tags_for_experience(exp, taxonomy, max_tags=4):
    skills = exp.get('skills',[]) or []
    suggestions = []
    for b in exp.get('bullets',[]):
        if isinstance(b, dict):
            text = b.get('text','')
            existing = b.get('tags', [])
        else:
            text = b
            existing = []
        matches = find_matches(text, taxonomy)
        # Also check experience skills as fallback (exact substring)
        for s in skills:
            if s.lower() in text.lower():
                k = re.sub(r'[^a-z0-9]+','', s.lower())
                if k not in [m[0] for m in matches]:
                    matches.append((k, s))

        # dedupe and limit
        seen = set()
        tags = []
        for k,label in matches:
            if k in seen: continue
            tags.append({'id': k, 'label': label})
            seen.add(k)
            if len(tags) >= max_tags: break

        # if no matches, keep existing or fallback to top skills
        if not tags and existing:
            tags = [{'id': re.sub(r'[^a-z0-9]+','', t.lower()), 'label': t} for t in existing[:max_tags]]
        if not tags and skills:
            tags = [{'id': re.sub(r'[^a-z0-9]+','', s.lower()), 'label': s} for s in skills[:max_tags]]

        suggestions.append({'text': text, 'suggested_tags': tags})
    return suggestions

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true', default=False)
    parser.add_argument('--apply', action='store_true', default=False)
    parser.add_argument('--output', default='resume_output/tag_suggestions.csv')
    parser.add_argument('--max-tags', type=int, default=4)
    args = parser.parse_args()

    taxonomy = load_taxonomy()
    experiences = json.loads(EXP.read_text(encoding='utf-8'))

    rows = []
    for e in experiences:
        sugg = suggest_tags_for_experience(e, taxonomy, max_tags=args.max_tags)
        for i, s in enumerate(sugg):
            rows.append({
                'employer': e.get('employer'),
                'role': e.get('role'),
                'dates': e.get('dates'),
                'bullet_index': i,
                'text': s['text'],
                'suggested_tags': ';'.join([t['label'] for t in s['suggested_tags']])
            })

    outp = Path(args.output)
    outp.parent.mkdir(parents=True, exist_ok=True)
    with outp.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['employer','role','dates','bullet_index','text','suggested_tags'])
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

    print('Wrote suggestions to', outp)

    if args.apply:
        # apply suggestions into the tailored resume (use taxonomy ids)
        tailored = json.loads(TAIL.read_text(encoding='utf-8'))
        # mapping experiences by employer+role
        keymap = {(e['employer'], e.get('role','')): e for e in experiences}
        # apply to tailored resume entries if matched
        for tre in tailored.get('experience', []):
            key = (tre.get('employer'), tre.get('role',''))
            src = keymap.get(key)
            if not src:
                continue
            sugg = suggest_tags_for_experience(src, taxonomy, max_tags=args.max_tags)
            # overwrite tags for each bullet in tailored entry
            new_bullets = []
            for sb, orig in zip(sugg, tre.get('bullets', [])):
                tags = [t['label'] for t in sb['suggested_tags']]
                if isinstance(orig, dict):
                    orig['tags'] = tags
                    new_bullets.append(orig)
                else:
                    new_bullets.append({'text': orig, 'tags': tags})
            tre['bullets'] = new_bullets
        TAIL.write_text(json.dumps(tailored, indent=2), encoding='utf-8')
        print('Applied suggested tags to', TAIL)

if __name__ == '__main__':
    main()
