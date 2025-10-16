#!/usr/bin/env python3
"""Merge a set of user-provided entries into `data/experiences.json`.

For each provided entry, find an existing entry by employer (case-insensitive). If found,
append any bullets that don't already exist (exact match) and add any missing skills.
If no match is found, append the entry as new.
"""
from pathlib import Path
import json
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DATA_FILE = ROOT / 'data' / 'experiences.json'

ENTRIES = [
    {
        'employer': 'CGI – Daugherty / Edward Jones',
        'role': 'Principal Consultant / Platform Team Delivery Lead – Digital Client Experience',
        'dates': '2021–2024',
        'location': '',
        'bullets': [
            'Led modernization of the Online Access platform, transitioning from monolithic architecture to cloud-native microservices and micro-frontends using Java, Spring Boot, and Angular.',
            'Drove CI/CD platform maturity, evolving Azure DevOps pipelines into trunk-based development workflows supporting 13 Agile teams across web, API, mobile, and mainframe domains.',
            'Implemented feature-flag release strategies, short-lived branches, and automated test gates, enabling independent deployments and 50 % faster release cycles.',
            'Instituted Delivery Excellence workshops on value-stream mapping, continuous integration health checks, and test-driven development.',
            'Partnered with engineering managers to standardize observability (Dynatrace, Splunk) and delivery governance across trains.'
        ],
        'skills': ['Azure DevOps', 'Terraform', 'Jenkins', 'SonarQube', 'ESLint', 'Dynatrace', 'Spring Boot', 'Angular', 'SQL Server']
    },
    {
        'employer': 'Daugherty – Cox Communications',
        'role': 'Platform Architect – Cloud Infrastructure & Automation',
        'dates': '2023–2024',
        'location': '',
        'bullets': [
            'Architected and deployed CI/CD pipelines in GitHub Actions for API Gateway and AWS Lambda microservices using Terraform-based IaC modules.',
            'Transitioned teams from manual staging branches to trunk-based continuous integration, integrating linting, IaC validation, and security scans into the mainline workflow.',
            'Designed rollback workflows leveraging Terraform state management for fault-tolerant releases.',
            'Orchestrated KeeperSecurity-managed key rotation and encryption automation through Bitbucket pipelines to enforce DevSecOps standards.',
            'Reduced deployment friction across environments and achieved 100 % parity between staging and production builds.'
        ],
        'skills': ['AWS Lambda', 'API Gateway', 'Terraform', 'GitHub Actions', 'Python', 'KeeperSecurity']
    },
    {
        'employer': 'BPM Software Solutions',
        'role': 'Senior Software Architect / Engineering Lead',
        'dates': '2017–2021',
        'location': '',
        'bullets': [
            'Spearheaded cloud-first modernization initiatives across finance, healthcare, and analytics clients, transitioning legacy systems to Azure and AWS.',
            'Implemented Jenkins + Kubernetes-driven CI/CD pipelines that matured into trunk-based delivery for ETL, BI, and automation workloads.',
            'Established CI/CD governance playbooks and reusable pipeline modules, embedding security, observability, and rollback automation.',
            'Mentored engineers on short-lived branch strategies, feature toggles, and continuous merge practices, improving delivery reliability by 40 %.',
            'Architected unified BI platform on Azure integrating multiple ERP systems; automation raised enterprise valuation by $60 M in 18 months.'
        ],
        'skills': ['Azure Functions', 'Terraform', 'Jenkins', 'Docker', 'Kubernetes', 'SQL Server', 'Python', 'React']
    },
    {
        'employer': 'Soave Enterprises',
        'role': 'Technology Manager / Software Architect',
        'dates': '2015–2016',
        'location': '',
        'bullets': [
            'Directed modernization of enterprise infrastructure across 25 U.S. locations, migrating to hybrid AWS EC2 cloud.',
            'Introduced DevOps automation and early CI/CD pipelines, establishing repeatable build/test/deploy flows.',
            'Laid the groundwork for trunk-based development by implementing shared mainline branching and continuous integration for distributed teams.'
        ],
        'skills': ['AWS EC2', 'DevOps', 'CI/CD']
    },
    {
        'employer': 'Interactive Business Solutions',
        'role': 'Senior Software Engineering Consultant',
        'dates': '2016–2017',
        'location': '',
        'bullets': [
            'Engineered multi-system integrations (CRM, LMS, ERP) that increased month-end productivity 300 %.',
            'Built AWS-hosted CI/CD workflows for financial reporting systems, evolving toward trunk-based branching for faster client deliverables.',
            'Mentored developers on automation and continuous testing practices to maintain production quality at speed.'
        ],
        'skills': ['API Integration', 'Cloud Migration', 'CI/CD']
    },
    {
        'employer': 'John Deere Landscapes',
        'role': 'Software Development Lead / Solution Architect',
        'dates': '2010–2015',
        'location': '',
        'bullets': [
            'Led modernization of proprietary ERP system used by 400+ retail stores.',
            'Introduced automated build pipelines, unit-test enforcement, and continuous integration, paving the cultural path toward trunk-based development long before mainstream adoption.',
            'Oversaw transition to Microsoft Dynamics AX 2012 R2, incorporating modular architecture and early DevOps principles.'
        ],
        'skills': ['Microsoft Dynamics AX', 'TDD', 'CI/CD']
    }
]


def load_data():
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def find_match(data, employer, role=None, dates=None):
    e_lower = employer.strip().lower()
    for entry in data:
        if entry.get('employer','').strip().lower() == e_lower:
            # optional role/dates matching could be added
            return entry
    return None


def merge_entry(existing, new):
    added_bullets = 0
    added_skills = 0

    exist_bullets = existing.get('bullets', []) or []
    for b in new.get('bullets', []):
        if not any(b.strip() == eb.strip() for eb in exist_bullets):
            exist_bullets.append(b)
            added_bullets += 1

    existing['bullets'] = exist_bullets

    exist_skills = existing.get('skills', []) or []
    for s in new.get('skills', []):
        if not any(s.strip().lower() == es.strip().lower() for es in exist_skills):
            exist_skills.append(s)
            added_skills += 1

    existing['skills'] = exist_skills
    return added_bullets, added_skills


def main():
    data = load_data()
    added_new = 0
    merged_total = 0
    merged_skills_total = 0

    for n in ENTRIES:
        match = find_match(data, n['employer'], n.get('role'), n.get('dates'))
        if match:
            ab, as_ = merge_entry(match, n)
            if ab or as_:
                print(f"Merged into existing '{n['employer']}': +{ab} bullets, +{as_} skills")
                merged_total += ab
                merged_skills_total += as_
            else:
                print(f"No new data to merge for '{n['employer']}'")
        else:
            new_entry = {
                'id': str(uuid.uuid4()),
                'employer': n['employer'],
                'role': n['role'],
                'dates': n['dates'],
                'location': n.get('location',''),
                'bullets': n.get('bullets', []),
                'skills': n.get('skills', []),
                'technologies': [],
                'techniques': [],
                'principles': [],
                'notes': 'Imported/merged from user-provided entries'
            }
            data.append(new_entry)
            added_new += 1
            print(f"Added new entry for '{n['employer']}'")

    save_data(data)
    print(f"Done. New entries added: {added_new}. Bullets merged: {merged_total}. Skills merged: {merged_skills_total}.")


if __name__ == '__main__':
    main()
