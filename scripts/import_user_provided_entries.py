#!/usr/bin/env python3
"""Import user-provided experience entries into the ExperienceLog.

This script contains the entries provided in the user's last message and will add
an Experience entry per job section.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.experience_log import ExperienceLog, Experience


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


def main():
    log = ExperienceLog()
    added = 0
    for e in ENTRIES:
        exp = Experience(
            id="",
            employer=e['employer'],
            role=e['role'],
            dates=e['dates'],
            location=e.get('location',''),
            bullets=e['bullets'],
            skills=e.get('skills', []),
            technologies=[],
            techniques=[],
            principles=[],
            notes='Imported from user-provided entries'
        )
        try:
            log.add(exp)
            print(f"Added: {exp.employer} | {exp.role} | {len(exp.bullets)} bullets")
            added += 1
        except ValueError as ve:
            print(f"Skipped duplicate: {exp.employer} | {ve}")
    print(f"Done. Entries added: {added}")


if __name__ == '__main__':
    main()
