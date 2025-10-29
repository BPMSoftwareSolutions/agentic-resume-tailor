"""
TDD: Ensure tailoring replaces experience bullets with the selected (rewritten) bullets.

- Creates a simple resume with multiple bullets per job
- Creates a job listing whose keywords will be extracted (e.g., CI/CD)
- Calls POST /api/resumes/<id>/tailor
- Asserts the saved tailored resume's bullets are rewritten (not original)

Related to: Bullet normalization in tailoring pipeline
"""

import json
import sys
from pathlib import Path

import pytest

# Make src importable like other tests do
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from api.app import app


@pytest.fixture
def client(temp_data_dir, monkeypatch):
    """Flask test client with isolated data directory, mirroring other API tests."""
    import api.app as app_module
    from models.resume import Resume
    from models.job_listing import JobListing

    new_resume_model = Resume(temp_data_dir)
    new_job_listing_model = JobListing(temp_data_dir)

    monkeypatch.setattr(app_module, "DATA_DIR", temp_data_dir)
    monkeypatch.setattr(app_module, "resume_model", new_resume_model)
    monkeypatch.setattr(app_module, "job_listing_model", new_job_listing_model)

    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client


def test_tailor_replaces_bullets_with_selected_rewritten_bullets(client, unique_resume_name):
    """
    Create a resume with 1 experience and 3 simple bullets. After tailoring,
    the saved new resume should have bullets rewritten (e.g., with the heuristic
    suffix added), proving we replaced original bullets with the selected ones.
    """
    # Step 1: Create a simple resume via API
    sample_resume = {
        "name": "Candidate X",
        "title": "Engineer",
        "location": "Remote",
        "contact": {"email": "x@example.com", "phone": "(555) 123-4567"},
        "summary": "Experienced engineer.",
        "experience": [
            {
                "employer": "Acme",
                "role": "Engineer",
                "dates": "2023 - Present",
                "bullets": [
                    {"text": "Built CI/CD pipelines", "tags": ["CI/CD"]},
                    {"text": "Led team meetings", "tags": ["leadership"]},
                    {"text": "Managed deployments", "tags": ["deployment"]},
                ],
            }
        ],
    }

    payload = {"name": unique_resume_name, "data": sample_resume}
    resp = client.post("/api/resumes", data=json.dumps(payload), content_type="application/json")
    assert resp.status_code == 201, resp.data
    created = json.loads(resp.data)["resume"]
    source_resume_id = created["id"]

    # Step 2: Create a job listing that triggers relevant keywords
    job_payload = {
        "title": "DevOps Engineer",
        "company": "ExampleCo",
        "description": "We are seeking experience with CI/CD, pipelines, and automation.",
        "location": "Remote",
    }
    resp = client.post("/api/job-listings", data=json.dumps(job_payload), content_type="application/json")
    assert resp.status_code == 201, resp.data
    job_listing = json.loads(resp.data)["job_listing"]

    # Step 3: Tailor the resume
    tailor_payload = {
        "job_listing_id": job_listing["id"],
        "new_resume_name": f"{unique_resume_name}_Tailored",
        "use_rag": False,
        "use_llm_rewriting": False,
    }
    resp = client.post(
        f"/api/resumes/{source_resume_id}/tailor",
        data=json.dumps(tailor_payload),
        content_type="application/json",
    )
    assert resp.status_code == 201, resp.data
    tailored_meta = json.loads(resp.data)["resume"]

    # Step 4: Load the saved tailored resume and verify bullets are rewritten (not originals)
    import api.app as app_module

    tailored_json = app_module.resume_model.get(tailored_meta["id"])  # stored on disk
    assert tailored_json is not None
    assert "experience" in tailored_json
    exp = tailored_json["experience"][0]

    # The tailored bullets should be rewritten strings (heuristic appends impact suffix)
    bullets = exp.get("bullets", [])
    assert isinstance(bullets, list) and len(bullets) > 0

    # Each bullet should have the rewritten heuristic phrase appended by rewrite_star()
    for b in bullets:
        assert "text" in b
        assert b["text"].endswith("improved reliability and delivery speed.")

    # Optional: Ensure we didn't keep the original bullets verbatim
    original_texts = {"Built CI/CD pipelines", "Led team meetings", "Managed deployments"}
    for b in bullets:
        assert b["text"] not in original_texts

