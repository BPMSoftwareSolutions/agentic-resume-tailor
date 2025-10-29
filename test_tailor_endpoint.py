import requests
import json

# Sample job description
job_description = '''
Sr. DevOps Engineer (Azure) - Remote

Responsibilities:
- Design and implement CI/CD pipelines using Azure DevOps
- Manage and optimize cloud infrastructure on Azure
- Implement infrastructure as code using Terraform
- Monitor and troubleshoot production systems
- Collaborate with development teams on deployment strategies
- Implement security best practices and compliance measures

Requirements:
- 5+ years of DevOps experience
- Strong knowledge of Azure cloud platform
- Experience with CI/CD tools (Jenkins, GitLab CI, Azure Pipelines)
- Proficiency in scripting (Python, Bash, PowerShell)
- Experience with containerization (Docker, Kubernetes)
- Strong Linux/Unix administration skills
- Experience with monitoring tools (Prometheus, ELK, Datadog)
- Excellent problem-solving and communication skills
'''

payload = {
    'job_title': 'Sr. DevOps Engineer (Azure)',
    'company': 'Tech Company',
    'job_description': job_description,
    'url': 'https://www.indeed.com/viewjob?jk=fcd29f6d7f5168f9',
    'use_rag': False,
    'use_llm_rewriting': False,
    'theme': 'professional'
}

print('Testing /api/tailor-from-job-description endpoint...')
print()

response = requests.post('http://localhost:5000/api/tailor-from-job-description', json=payload)
print(f'Status Code: {response.status_code}')
print()

if response.status_code == 201:
    result = response.json()
    print('✅ SUCCESS!')
    print()
    print(f'Resume ID: {result["resume"]["id"]}')
    print(f'Resume Name: {result["resume"]["name"]}')
    print(f'Job Listing ID: {result["job_listing"]["id"]}')
    print(f'Job Title: {result["job_listing"]["title"]}')
    print(f'Company: {result["job_listing"]["company"]}')
    print(f'Keywords: {len(result["job_listing"]["keywords"])} extracted')
else:
    print('❌ FAILED')
    print(response.json())

