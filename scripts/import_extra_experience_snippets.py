#!/usr/bin/env python3
"""Import two extra experience snippets (Snap-On and Compuware) into ExperienceLog.

This script contains the snippets inline and will add one Experience per snippet.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.experience_log import ExperienceLog, Experience


SNAPON = {
    'employer': 'Snap-On Technologies',
    'role': 'Senior Software Engineer',
    'dates': '2000 – 2006',
    'location': 'Troy, MI',
    'bullets': [
        'Invented a data-driven orchestration framework for ECM communication on vehicle networks, enabling adaptive protocol handling across J1850-VPW, PWM, J1939, CAN/GM LAN, and ISO standards.',
        'Designed a dynamic diagnostic communication module capable of learning and adapting to new OEM protocols without reengineering core components.',
        'Developed calibration and service applications used by ISUZU, Harley-Davidson, Freightliner, Detroit Diesel, Mac, Eaton, and Penske, improving diagnostic accuracy and time-to-market for new vehicle platforms.',
        'Collaborated with embedded firmware engineers and field technicians to validate communication layers over the 9-pin Deutsch vehicle interface and OBD-II connectors.'
    ],
    'skills': ['Embedded Systems', 'Vehicle Diagnostics', 'Data-Driven Architecture', 'ECM Communication', 'J1850', 'J1939', 'CAN', 'ISO Protocols', 'C/C++', 'Automotive Innovation']
}

COMPUWARE = {
    'employer': 'Compuware',
    'role': 'Senior Software Developer',
    'dates': '2006 – 2010',
    'location': 'Detroit, MI',
    'bullets': [
        'Developed enterprise QA automation and load-testing frameworks (QALoad, QADirector) for large-scale clients including Ford, GM, Blue Cross Blue Shield, and EDS, improving reliability and scalability of distributed systems.',
        'Engineered E2E test automation frameworks in C++ and Java, integrating performance testing directly into early DevOps pipelines.',
        'Collaborated with product and QA teams to design automated defect-tracking systems, optimizing regression cycles and standardizing test execution across enterprise environments.',
        'Contributed to internal tooling for performance benchmarking, which later influenced commercial QA product lines adopted globally.'
    ],
    'skills': ['QA Automation', 'Performance Testing', 'E2E Frameworks', 'DevOps', 'Enterprise Software', 'C/C++', 'Java', 'Automotive and Healthcare Clients']
}


def main():
    log = ExperienceLog()
    for src in (SNAPON, COMPUWARE):
        exp = Experience(
            id="",
            employer=src['employer'],
            role=src['role'],
            dates=src['dates'],
            location=src.get('location',''),
            bullets=src['bullets'],
            skills=src.get('skills', []),
            technologies=[],
            techniques=[],
            principles=[],
            notes='Imported from user-provided snippets'
        )
        try:
            log.add(exp)
            print(f"Added: {exp.employer} | {exp.role} | {len(exp.bullets)} bullets")
        except ValueError as ve:
            print(f"Skipped duplicate: {exp.employer} | {ve}")
        except Exception as e:
            print(f"Error adding {exp.employer}: {e}")


if __name__ == '__main__':
    main()
