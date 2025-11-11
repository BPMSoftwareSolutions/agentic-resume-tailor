#!/usr/bin/env python3
"""
Unit test: surgical_resume_update should only replace specified employers
and leave all other experiences untouched. It should also ensure that tags
exist at the EXPERIENCE level (promoting from bullet-level if needed).
"""

import copy
import json

from pathlib import Path

# Import functions from the script under test
import sys
sys.path.insert(0, str(Path(__file__).parent))
from surgical_resume_update import (
    replace_experiences_surgically,
    select_matching_new_experiences,
)


def make_resume():
    # 5 experiences baseline
    return {
        "name": "Test Resume",
        "title": "Engineer",
        "experience": [
            {
                "employer": "EmpA",
                "role": "RoleA",
                "dates": "2020-2021",
                "location": "CityA",
                "bullets": [{"text": "A1"}],
                "tags": ["KeepMeA"]
            },
            {
                "employer": "EmpB",
                "role": "RoleB",
                "dates": "2019-2020",
                "location": "CityB",
                "bullets": [{"text": "B1"}],
                "tags": ["OldB"]
            },
            {
                "employer": "EmpC",
                "role": "RoleC",
                "dates": "2018-2019",
                "location": "CityC",
                "bullets": [{"text": "C1"}],
                "tags": ["KeepMeC"]
            },
            {
                "employer": "EmpD",
                "role": "RoleD",
                "dates": "2017-2018",
                "location": "CityD",
                "bullets": [{"text": "D1"}],
                "tags": ["OldD"]
            },
            {
                "employer": "EmpE",
                "role": "RoleE",
                "dates": "2016-2017",
                "location": "CityE",
                "bullets": [{"text": "E1"}],
                "tags": ["KeepMeE"]
            },
        ]
    }


def make_new_experiences_source():
    # Source file style: two experiences to replace, tags on bullets only
    return [
        {
            "employer": "EmpB",
            "role": "RoleB-New",
            "dates": "2022-2023",
            "location": "CityB",
            "bullets": [
                {"text": "B-New1", "tags": ["NewB1", "NewB2"]},
                {"text": "B-New2", "tags": ["NewB2", "NewB3"]},
            ]
        },
        {
            "employer": "EmpD",
            "role": "RoleD-New",
            "dates": "2021-2022",
            "location": "CityD",
            "bullets": [
                {"text": "D-New1", "tags": ["NewD"]},
            ]
        },
        {
            "employer": "OtherUnrelated",
            "role": "ShouldNotBeInserted",
            "dates": "N/A",
            "location": "N/A",
            "bullets": [{"text": "Ignore me", "tags": ["Nope"]}],
        }
    ]


def test_surgical_only_replaces_specified():
    resume = make_resume()
    original = copy.deepcopy(resume)
    new_source = make_new_experiences_source()

    # Only replace EmpB and EmpD
    employers_to_replace = ["EmpB", "EmpD"]

    # Select matching new experiences (also promotes tags to experience-level)
    matching = select_matching_new_experiences(employers_to_replace, new_source)

    # Perform replacement (uses only matching ones internally as well)
    updated = replace_experiences_surgically(
        resume, new_source, employers_to_replace
    )

    # 1) Count unchanged except replaced ones (still total 5)
    assert len(updated["experience"]) == 5, f"Expected 5 experiences, got {len(updated['experience'])}"

    # 2) Other employers remain untouched (EmpA, EmpC, EmpE)
    kept_employers = [e["employer"] for e in updated["experience"] if e["employer"] in {"EmpA", "EmpC", "EmpE"}]
    assert set(kept_employers) == {"EmpA", "EmpC", "EmpE"}

    # Check content of one kept item remained identical
    kept_after = next(e for e in updated["experience"] if e["employer"] == "EmpA")
    assert kept_after == original["experience"][0], "EmpA should be unchanged"

    # 3) Replaced entries appear and have experience-level tags promoted
    repB = next(e for e in updated["experience"] if e["employer"] == "EmpB")
    repD = next(e for e in updated["experience"] if e["employer"] == "EmpD")

    assert repB["role"] == "RoleB-New"
    assert repD["role"] == "RoleD-New"

    # Experience-level tags should include union of bullet tags
    assert set(repB.get("tags", [])) == {"NewB1", "NewB2", "NewB3"}
    assert set(repD.get("tags", [])) == {"NewD"}

    print("\n✅ TEST PASSED: Surgical update only replaced specified employers and preserved others.\n")


if __name__ == "__main__":
    test_surgical_only_replaces_specified()

