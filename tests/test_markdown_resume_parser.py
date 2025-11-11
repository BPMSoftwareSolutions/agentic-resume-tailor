import sys
from pathlib import Path

# Add src to path for utils import
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils.markdown_resume_parser import parse_surgical_markdown  # noqa: E402


def test_parse_surgical_markdown_basic():
    md = (
        "### **PROFESSIONAL SUMMARY**\n\n"
        "Engineering leader building scalable systems.\n\n"
        "---\n\n"
        "### **CORE COMPETENCIES**\n"
        "* **Languages & Frameworks:** Go, Python\n"
        "* **Cloud & DevOps:** AWS, Terraform\n\n"
        "---\n\n"
        "### **RELEVANT EXPERIENCE**\n"
        "#### **Acme Corp** | *Senior Engineer*\n\n"
        "*Springfield, IL | Jan 2020 – Present*\n"
        "* Built APIs\n"
        "* Deployed on AWS\n\n"
        "*Tech:* Go, AWS, Terraform\n"
    )

    parsed = parse_surgical_markdown(md)

    assert "updates" in parsed
    assert "experiences" in parsed

    assert "Engineering leader" in parsed["updates"]["summary"]
    assert any("Go" in item for item in parsed["updates"]["core_competencies"])  # bullet kept

    assert len(parsed["experiences"]) == 1
    exp = parsed["experiences"][0]
    assert exp["employer"] == "Acme Corp"
    assert exp["role"] == "Senior Engineer"
    assert exp["location"].startswith("Springfield")
    assert "2020" in exp["dates"]
    assert any("Built APIs" in b["text"] for b in exp["bullets"])  # bullet captured
    assert "Go" in exp.get("tags", [])


def test_parse_surgical_markdown_multiple_experiences():
    md = (
        "### **RELEVANT EXPERIENCE**\n"
        "#### **Foo Inc** | *Architect*\n\n"
        "*Remote | 2021 – 2023*\n"
        "* Designed systems\n\n"
        "*Tech:* Python, Docker\n\n"
        "#### **Bar LLC** | *Lead*\n\n"
        "*NYC, NY | 2019 – 2021*\n"
        "* Built teams\n\n"
        "*Tech:* Go, Kubernetes\n"
    )

    parsed = parse_surgical_markdown(md)
    exps = parsed["experiences"]
    assert [e["employer"] for e in exps] == ["Foo Inc", "Bar LLC"]
    assert "Kubernetes" in exps[1].get("tags", [])

