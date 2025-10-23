import json
import os
import pytest
from cdp_maintainer import read_json, write_json, set_top5

def test_top_tech_stacks_added_to_all_best_practices(tmp_path):
    # Setup: minimal pipeline JSON with missing top_tech_stacks
    data = {
        "pipeline": {
            "name": "Continuous Delivery Pipeline",
            "aspects": [
                {
                    "name": "Continuous Integration",
                    "index": 2,
                    "key_activities": [
                        {
                            "name": "Develop",
                            "best_practices": [
                                {"name": "Breaking features into stories"},
                                {"name": "Continuous Integration"},
                                {"name": "Test Automation"}
                            ]
                        }
                    ]
                }
            ]
        }
    }
    test_json = tmp_path / "test.json"
    write_json(str(test_json), data)

    # Act: set top 5 for Continuous Integration and Test Automation
    set_top5(data, "Continuous Integration", "Develop", "Continuous Integration", [
        ("Python + FastAPI + GitHub Actions", "Used for backend microservices and API pipelines with automated testing and deployment."),
        ("Java + Spring Boot + Jenkins", "Common enterprise CI setup for monolithic and microservice Java systems."),
        ("Node.js + Docker + AWS CodePipeline", "Used in full-stack JavaScript applications and cloud-native pipelines."),
        (".NET Core + Azure DevOps + Terraform", "Typical Microsoft ecosystem CI/CD workflow with Infrastructure-as-Code."),
        ("Go + Kubernetes + ArgoCD", "Modern lightweight build/deploy pipeline for distributed services.")
    ], level="practice")
    set_top5(data, "Continuous Integration", "Develop", "Test Automation", [
        ("Python + PyTest + Selenium", "Used for functional and browser automation tests."),
        ("JavaScript + Cypress + GitHub Actions", "Modern UI testing framework for CI pipelines."),
        ("Java + JUnit + Jenkins", "Classic test automation combination in enterprise Java systems."),
        ("C# + NUnit + Azure Pipelines", "Used in Microsoft-based QA automation setups."),
        ("Playwright + Docker + GitLab CI", "Cross-browser testing with containerized runners.")
    ], level="practice")

    # Assert: all best practices have top_tech_stacks (even if empty)
    for aspect in data["pipeline"]["aspects"]:
        if aspect["name"] == "Continuous Integration":
            for activity in aspect["key_activities"]:
                if activity["name"] == "Develop":
                    for bp in activity["best_practices"]:
                        assert "top_tech_stacks" in bp, f"Missing top_tech_stacks in {bp['name']}"
                        assert isinstance(bp["top_tech_stacks"], list)

    # This should fail for 'Breaking features into stories' (no top_tech_stacks added)

if __name__ == "__main__":
    pytest.main([__file__])
