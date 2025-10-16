"""Select top-N most relevant bullets per employer for a tailored resume.

Saves a pruned copy: data/tailored_westlaw_lead_software_engineer_ai.pruned.json

Usage: python scripts/select_relevant_bullets.py --max-per-employer 4
"""
import json
from pathlib import Path
import argparse
import re

ROOT = Path(__file__).parent.parent
TAIL = ROOT / 'data' / 'tailored_westlaw_lead_software_engineer_ai.json'
PRUNED = ROOT / 'data' / 'tailored_westlaw_lead_software_engineer_ai.pruned.json'
TAX = ROOT / 'data' / 'tags' / 'taxonomy.json'


def tokenize(s: str):
    if not s:
        return set()
    s = re.sub(r"[^a-z0-9]+"," ", s.lower())
    return set(w for w in s.split() if len(w) > 2)


def load_taxonomy():
    if not TAX.exists():
        return {}
    return json.loads(TAX.read_text(encoding='utf-8'))


def score_bullet(text: str, bullet_tags, keywords, taxonomy):
    t = text.lower()
    score = 0
    # keyword matches (exact token presence)
    for kw in keywords:
        if kw in t:
            score += 3
    # taxonomy label substring matches
    for k,meta in taxonomy.items():
        label = meta.get('label','').lower()
        if label and label in t:
            score += 2
    # existing tags contribute small boost
    score += 0.5 * len(bullet_tags)
    # favor medium-length bullets (not extremely short)
    ln = len(text.split())
    if 8 <= ln <= 40:
        score += 1
    return score


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-per-employer', type=int, default=4)
    args = parser.parse_args()

    tailored = json.loads(TAIL.read_text(encoding='utf-8'))
    taxonomy = load_taxonomy()

    # build keywords from title, summary, technical_proficiencies, areas
    kws = set()
    kws.update(tokenize(tailored.get('title','')))
    kws.update(tokenize(tailored.get('summary','')))
    for v in (tailored.get('technical_proficiencies') or {}).values():
        kws.update(tokenize(v))
    for a in tailored.get('areas_of_expertise',[]) or []:
        kws.update(tokenize(a))

    # also include simple tokens from taxonomy labels for stronger matches
    for k,meta in taxonomy.items():
        lab = meta.get('label','')
        kws.update(tokenize(lab))

    summary = {'employers': 0, 'before': 0, 'after': 0}
    pruned = dict(tailored)
    new_exp = []
    for e in tailored.get('experience',[]) or []:
        summary['employers'] += 1
        bullets = e.get('bullets',[]) or []
        scored = []
        for b in bullets:
            text = b.get('text') if isinstance(b, dict) else (b or '')
            tags = b.get('tags') if isinstance(b, dict) else []
            s = score_bullet(text, tags, kws, taxonomy)
            scored.append((s, text, tags, b))
        summary['before'] += len(scored)
        # sort descending
        scored.sort(key=lambda x: x[0], reverse=True)
        chosen = scored[:args.max_per_employer]
        summary['after'] += len(chosen)
        # build new entry
        new_bullets = []
        for s,text,tags,b in chosen:
            if isinstance(b, dict):
                nb = dict(b)
            else:
                nb = {'text': text, 'tags': tags}
            nb['_score'] = s
            new_bullets.append(nb)
        ne = dict(e)
        ne['bullets'] = new_bullets
        new_exp.append(ne)
    pruned['experience'] = new_exp
    PRUNED.write_text(json.dumps(pruned, indent=2, ensure_ascii=False), encoding='utf-8')
    print('Wrote pruned resume to', PRUNED)
    print('Employers:', summary['employers'], 'Bullets before:', summary['before'], 'Bullets after:', summary['after'])
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
