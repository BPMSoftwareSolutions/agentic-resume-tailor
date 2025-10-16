# Issue: Accurate per-bullet tagging for resumes

## Summary

Resume bullets currently inherit the employer-level skills list when the bullet is a plain string. This produces large, noisy tag lists per bullet and reduces the precision of search, matching, and highlighting features. We need a robust system to assign accurate, concise tags to each bullet that reflect the bullet's content.

## Goals / Acceptance Criteria

- Each bullet should have 1–5 high-precision tags directly relevant to the bullet text.
- Tags should be canonicalized (slug id, label, category) and normalized across the repository.
- Tag assignment should be automatable with a conservative default and allow optional manual curation via a CSV or UI.
- The system should support migration of existing entries and allow re-running with improved taxonomy or matching logic.
- Unit tests and integration tests should verify tag extraction behavior on representative bullets.

## Proposal

1. Taxonomy
   - Create `data/tags/taxonomy.json` containing canonical tags with optional synonyms and category.
   - Seed taxonomy automatically from existing `data/experiences.json` `skills` / `technologies` and curated common synonyms.

2. Tagging engine (scripts/assign_tags.py)
   - Conservative algorithm (v1): exact and phrase match from taxonomy and experience skills, limit to N tags/bullet (default N=4), preserve existing explicit tags.
   - Improved algorithm (v2): add fuzzy matching, entity extraction, and mapping using simple NLP rules (optional dependency: spacy) for higher recall.
   - Provide CLI flags: --dry-run, --force, --max-tags, --export-csv

3. Manual curation
   - Export suggested tags to CSV for review and re-import after edits.
   - Optionally, add a lightweight UI to accept/reject mappings (future).

4. Migration
   - Keep original `notes.provenance` and add `tags` metadata with `provenance` (auto/manual/timestamp).
   - Provide migration script `scripts/migrate_tags.py` to apply approved CSV changes to `data/experiences.json` and `data/<tailored>.json` files.

5. Tests
   - `tests/test_assign_tags.py` covering exact match, multi-word phrase, fallback behavior, and truncation.

6. Rollout plan
   - Phase 1: Implement taxonomy + conservative tagging, dry-run on all experiences, export CSV.
   - Phase 2: Curate CSV, import curated tags, run generator for QA.
   - Phase 3: Optionally add fuzzy/NLP and re-run.

## Implementation Tasks (rough estimates)

- Seed taxonomy script (seed_tags.py): 1–2 hours
- assign_tags.py (conservative): 2–3 hours
- CSV export/import: 1 hour
- Unit tests: 1 hour
- Integration test + run on full dataset: 30–60 mins
- Optional NLP/fuzzy: 4–8 hours (depends on tuning)

Total conservative path: ~6 hours. With optional NLP: ~12–16 hours.

## Risks & Mitigations

- False positives: mitigate by preferring exact/multiword matches and limiting tags per bullet.
- Missing tags for implicit concepts: provide CSV for manual curation and iterate with fuzzy/NLP later.
- Taxonomy drift: add scripts to reconcile synonyms and canonical merge rules.

## Output artifacts

- `data/tags/taxonomy.json` (seeded)
- `scripts/assign_tags.py` (CLI)
- `scripts/seed_tags.py` (helper)
- `scripts/export_tag_suggestions.py` (CSV export)
- `scripts/migrate_tags.py` (apply curated tags)
- `tests/test_assign_tags.py`

## Next steps (recommended)

1. Approve the proposal.
2. I will implement the conservative tagging engine (`assign_tags.py`) and `taxonomy.json` seed and run a dry-run export CSV for your review.
3. Review the CSV, approve or edit suggested tags, and I'll import the curated tags and regenerate the DOCX for final QA.

---

If this looks good I can open a PR with the scripts and the seeded taxonomy. If you'd like changes to the approach (e.g., immediate NLP), tell me which option you prefer and I'll adapt the plan.