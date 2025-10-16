import json
import sys
import tempfile
from pathlib import Path
from pathlib import Path as _P

# Ensure repository root is on sys.path so tests can import `src` as a package
ROOT = _P(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.experience_log import Experience, ExperienceLog


def test_add_and_persist(tmp_path: Path):
    db = tmp_path / "experiences.json"
    log = ExperienceLog(path=db)

    e = Experience(
        id="",
        employer="Acme",
        role="Engineer",
        dates="2020-2022",
        skills=["Python", "Testing"],
        technologies=["Docker"],
        bullets=["Built API"],
    )

    added = log.add(e)
    assert added.id
    # reload
    other = ExperienceLog(path=db)
    assert len(other.list()) == 1
    assert other.list()[0].employer == "Acme"


def test_find_by_skill_and_technology(tmp_path: Path):
    db = tmp_path / "experiences.json"
    log = ExperienceLog(path=db)

    e1 = Experience(
        id="",
        employer="X",
        role="Dev",
        dates="2021",
        skills=["Python", "CI/CD"],
        technologies=["Kubernetes"],
    )
    e2 = Experience(
        id="",
        employer="Y",
        role="Ops",
        dates="2022",
        skills=["Monitoring"],
        technologies=["Prometheus", "Grafana"],
    )

    log.add(e1)
    log.add(e2)

    res = log.find_by_skill("python")
    assert len(res) == 1
    assert res[0].employer == "X"

    techs = log.find_by_technology("prometheus")
    assert len(techs) == 1
    assert techs[0].employer == "Y"
