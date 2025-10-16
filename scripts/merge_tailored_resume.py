"""Merge duplicate employers in the tailored resume and add education/certifications from backup.

Usage: python scripts/merge_tailored_resume.py
"""
import json
from pathlib import Path
import re

ROOT = Path(__file__).parent.parent
TAIL = ROOT / 'data' / 'tailored_westlaw_lead_software_engineer_ai.json'
BACKUP = ROOT / 'data' / 'backups' / 'master_resume_backup_20251011_175614.json'


def normalize_key(s: str) -> str:
    if not s:
        return ''
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return s


def bullet_text(b):
    if isinstance(b, dict):
        return (b.get('text') or '').strip()
    return (b or '').strip()


def bullet_tags(b):
    if isinstance(b, dict):
        return list(b.get('tags') or [])
    return []


def merge_employer_group(entries):
    # entries: list of dict
    # choose representative fields
    rep = {}
    rep['employer'] = entries[0].get('employer')
    # pick longest non-empty role
    roles = [e.get('role','') or '' for e in entries]
    rep['role'] = max(roles, key=lambda s: len(s)) if roles else ''
    dates = [e.get('dates','') or '' for e in entries]
    rep['dates'] = max(dates, key=lambda s: len(s)) if dates else ''
    locations = [e.get('location','') or '' for e in entries]
    rep['location'] = next((l for l in locations if l), '')

    # merge bullets preserving first-seen order, dedupe by text
    seen = {}
    ordered = []
    for e in entries:
        for b in e.get('bullets', []) or []:
            text = bullet_text(b)
            if not text:
                continue
            key = re.sub(r"\s+"," ", text).strip()
            if key in seen:
                # union tags
                seen[key]['tags'] = sorted(list(set(seen[key].get('tags',[]) + bullet_tags(b))))
            else:
                item = {'text': text, 'tags': bullet_tags(b)}
                seen[key] = item
                ordered.append(item)
    rep['bullets'] = ordered
    return rep


def main():
    if not TAIL.exists():
        print('Tailored resume not found at', TAIL)
        return 1
    tailored = json.loads(TAIL.read_text(encoding='utf-8'))

    # group by normalized employer
    groups = {}
    order = []
    for e in tailored.get('experience', []) or []:
        key = normalize_key(e.get('employer',''))
        if key not in groups:
            groups[key] = []
            order.append(key)
        groups[key].append(e)

    merged = []
    for key in order:
        entries = groups[key]
        merged_entry = merge_employer_group(entries)
        merged.append(merged_entry)

    tailored['experience'] = merged

    # load backup education/certifications if available
    if BACKUP.exists():
        backup = json.loads(BACKUP.read_text(encoding='utf-8'))
        # merge education: backup has array of objects
        b_edu = backup.get('education', []) or []
        # existing education in tailored
        t_edu = tailored.get('education', []) or []
        # combine and dedupe by degree+institution
        seenedu = {}
        combined_edu = []
        for item in (t_edu + b_edu):
            deg = item.get('degree','') if isinstance(item, dict) else str(item)
            inst = item.get('institution','') if isinstance(item, dict) else ''
            key = (deg.strip().lower(), inst.strip().lower())
            if key in seenedu:
                continue
            seenedu[key] = item
            combined_edu.append(item)
        tailored['education'] = combined_edu

        # certifications: copy backup certifications (as-is) but avoid duplicates
        b_certs = backup.get('certifications', []) or []
        t_certs = tailored.get('certifications', []) or []
        # normalize cert by name+issuer+date
        seen = set()
        combined = []
        for c in (t_certs + b_certs):
            if isinstance(c, dict):
                name = c.get('name','').strip()
                issuer = c.get('issuer','').strip()
                date = c.get('date','').strip()
                key = (name.lower(), issuer.lower(), date.lower())
            else:
                name = str(c).strip()
                key = (name.lower(), '', '')
            if key in seen:
                continue
            seen.add(key)
            combined.append(c)
        tailored['certifications'] = combined

    # write back
    TAIL.write_text(json.dumps(tailored, indent=2, ensure_ascii=False), encoding='utf-8')
    print('Updated tailored resume written to', TAIL)
    # summary
    print('Employers:', len(tailored.get('experience',[])))
    print('Education items:', len(tailored.get('education',[])))
    print('Certifications:', len(tailored.get('certifications',[])))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
