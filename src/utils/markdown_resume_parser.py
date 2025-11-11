"""
Markdown -> structured resume data parser for surgical updates.

Supports extracting:
- summary (from '### PROFESSIONAL SUMMARY')
- core_competencies (from '### CORE COMPETENCIES' bullet list)
- experiences (from '### RELEVANT EXPERIENCE' entries)

Design notes:
- We keep the text as-is but strip simple Markdown emphasis (**bold**, *italic*).
- Experiences are recognized by '#### ' headings, with the pattern:
  '#### **Employer** | *Role*' (format variations tolerated)
- The following line is expected to contain location and dates in italics:
  '*Location | Dates*' — but we tolerate missing pieces.
- Bullets start with '* ' lines until a separator or next heading.
- An optional technology/tags line starts with '*Tech:*'.

This is purposely conservative and tolerant to minor variations
in the authoring format the user shared.
"""
from __future__ import annotations

import re
from typing import Any, Dict, List, Tuple


_HEADING_RE = re.compile(r"^#{3,4}\s+")
_BULLET_RE = re.compile(r"^\s*([*\-])\s+")
_TECH_PREFIX_RE = re.compile(r"^\s*[*\-]\s*Tech\s*:\s*\*?\s*(.*)$", re.IGNORECASE)
_H4_EXPERIENCE_RE = re.compile(r"^\s*####\s+(.*)$")


def _strip_md_emphasis(s: str) -> str:
    # Remove simple emphasis markers while keeping inner text
    s = re.sub(r"\*\*(.*?)\*\*", r"\1", s)
    s = re.sub(r"\*(.*?)\*", r"\1", s)
    s = s.replace("`", "")
    return s.strip()


def _split_title_line(line: str) -> Tuple[str, str]:
    """Split an experience title line into (employer, role).
    Accepts forms like: 'Employer | Role' or with markdown emphasis.
    """
    clean = _strip_md_emphasis(line)
    parts = [p.strip() for p in clean.split("|")]
    if len(parts) >= 2:
        return parts[0], parts[1]
    # If no pipe, try an em dash between employer and role
    emdash_split = re.split(r"\s*[\u2013\u2014\-]{1,2}\s*", clean, maxsplit=1)
    if len(emdash_split) >= 2:
        return emdash_split[0].strip(), emdash_split[1].strip()
    return clean, ""


def _parse_location_dates(line: str) -> Tuple[str, str]:
    """Parse '*Location | Dates*' or similar."""
    clean = _strip_md_emphasis(line)
    parts = [p.strip() for p in clean.split("|")]
    if len(parts) >= 2:
        return parts[0], parts[1]
    return clean, ""


def parse_surgical_markdown(md_text: str) -> Dict[str, Any]:
    lines = md_text.splitlines()
    i = 0
    summary_lines: List[str] = []
    core_competencies: List[str] = []
    experiences: List[Dict[str, Any]] = []

    def skip_separators(j: int) -> int:
        # Skip '---' or blank lines
        while j < len(lines) and (lines[j].strip() == "" or lines[j].strip() == "---"):
            j += 1
        return j

    while i < len(lines):
        line = lines[i]
        # PROFESSIONAL SUMMARY
        if line.strip().lower().startswith("### ") and "professional summary" in line.lower():
            i += 1
            i = skip_separators(i)
            while i < len(lines):
                if lines[i].strip().lower().startswith("### ") or lines[i].strip() == "---":
                    break
                # treat as paragraph lines
                l = _strip_md_emphasis(lines[i])
                if l:
                    summary_lines.append(l)
                i += 1
            continue

        # CORE COMPETENCIES
        if line.strip().lower().startswith("### ") and "core competencies" in line.lower():
            i += 1
            i = skip_separators(i)
            while i < len(lines):
                if lines[i].strip().lower().startswith("### ") or lines[i].strip() == "---":
                    break
                m = _BULLET_RE.match(lines[i])
                if m:
                    text = _BULLET_RE.sub("", lines[i])
                    text = _strip_md_emphasis(text)
                    if text:
                        core_competencies.append(text)
                i += 1
            continue

        # RELEVANT EXPERIENCE
        if line.strip().lower().startswith("### ") and "relevant experience" in line.lower():
            i += 1
            i = skip_separators(i)
            # Parse each experience until next ### or end
            while i < len(lines):
                if lines[i].strip().lower().startswith("### "):
                    break
                # Expect an H4 heading for experience title
                h4m = _H4_EXPERIENCE_RE.match(lines[i])
                if not h4m:
                    i += 1
                    continue
                title_line = h4m.group(1)
                employer, role = _split_title_line(title_line)
                i += 1
                i = skip_separators(i)

                # Next could be location/dates in italics
                location, dates = "", ""
                if i < len(lines) and lines[i].strip().startswith("*"):
                    location, dates = _parse_location_dates(lines[i])
                    i += 1

                # Bullets until *Tech:* or next h4/section/separator
                bullets: List[Dict[str, str]] = []
                tags: List[str] = []
                while i < len(lines):
                    if lines[i].strip() == "---":
                        i += 1
                        break
                    if lines[i].strip().lower().startswith("###") or lines[i].strip().lower().startswith("####"):
                        break
                    techm = _TECH_PREFIX_RE.match(lines[i])
                    if techm:
                        tech_str = techm.group(1)
                        tags = [t.strip() for t in tech_str.split(",") if t.strip()]
                        i += 1
                        continue
                    m = _BULLET_RE.match(lines[i])
                    if m:
                        text = _BULLET_RE.sub("", lines[i])
                        text = _strip_md_emphasis(text)
                        if text:
                            bullets.append({"text": text})
                    i += 1

                exp: Dict[str, Any] = {
                    "employer": employer,
                    "role": role,
                    "dates": dates,
                    "location": location,
                    "bullets": bullets,
                }
                if tags:
                    exp["tags"] = tags
                experiences.append(exp)

                i = skip_separators(i)
            continue

        i += 1

    updates: Dict[str, Any] = {}
    if summary_lines:
        # Join paragraphs; preserve punctuation and spaces
        updates["summary"] = " ".join(s.strip() for s in summary_lines if s.strip())
    if core_competencies:
        updates["core_competencies"] = core_competencies

    return {"experiences": experiences, "updates": updates}

