"""
Tests for surgical update endpoint using Markdown input.
"""
import json
import sys
from pathlib import Path

import pytest

# Add src to path for API import
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from api.app import app  # noqa: E402


@pytest.fixture
def client(temp_data_dir, monkeypatch):
    """
    Create a test client for the Flask app with isolated data directory,
    mirroring tests/test_multi_resume_api.py.
    """
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


def test_surgical_update_from_markdown_dry_run(client, sample_resume_data, unique_resume_name):
    # Create a resume first using the patched model
    import api.app as app_module
    meta = app_module.resume_model.create(data=sample_resume_data, name=unique_resume_name)

    md = (
        "### **PROFESSIONAL SUMMARY**\n\n"
        "New summary with distributed systems focus.\n\n"
        "---\n\n"
        "### **CORE COMPETENCIES**\n"
        "* Languages: Go, Python\n"
        "* Cloud: AWS, Azure\n\n"
        "---\n\n"
        "### **RELEVANT EXPERIENCE**\n"
        "#### **Test Company** | *Principal Engineer*\n\n"
        "*Test City, ST | 2022 - Present*\n"
        "* Built low-latency APIs\n"
        "* Implemented IaC\n\n"
        "*Tech:* Go, AWS, Terraform\n"
    )

    payload = {"markdown": md, "dry_run": True}
    resp = client.post(
        f"/api/resumes/{meta.id}/surgical-update",
        data=json.dumps(payload),
        content_type="application/json",
    )

    assert resp.status_code == 200, resp.data
    data = json.loads(resp.data)
    assert data.get("success") is True and data.get("dry_run") is True
    meta_info = data.get("meta", {})
    assert "Test Company" in meta_info.get("replaced_employers", [])

    updated = data.get("updated_preview", {})
    assert updated.get("summary", "").startswith("New summary")

    # Find replaced experience
    exps = updated.get("experience", [])
    tc = next((e for e in exps if e.get("employer") == "Test Company"), None)
    assert tc is not None
    assert tc.get("role") == "Principal Engineer"
    # Tags should be at experience level
    assert "Go" in (tc.get("tags") or [])

