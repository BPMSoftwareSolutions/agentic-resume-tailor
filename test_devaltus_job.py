import requests
import json

# Read the job listing file
with open(r'data/job_listings/DevAltus - Sr. DevOps Engineer (Azure).txt', 'r') as f:
    job_description = f.read()

payload = {
    'job_title': 'Sr. DevOps Engineer (Azure)',
    'company': 'DevAltus',
    'job_description': job_description,
    'url': '',
    'use_rag': False,
    'use_llm_rewriting': False,
    'theme': 'professional'
}

print('=' * 80)
print('Testing /api/tailor-from-job-description with DevAltus Job Listing')
print('=' * 80)
print()
print(f'Job Title: {payload["job_title"]}')
print(f'Company: {payload["company"]}')
print(f'Job Description Length: {len(job_description)} characters')
print()

response = requests.post('http://localhost:5000/api/tailor-from-job-description', json=payload)
print(f'Status Code: {response.status_code}')
print()

if response.status_code == 201:
    result = response.json()
    print('✅ SUCCESS!')
    print()
    print('Resume Created:')
    print(f'  ID: {result["resume"]["id"]}')
    print(f'  Name: {result["resume"]["name"]}')
    print(f'  Job Listing ID: {result["resume"]["job_listing_id"]}')
    print()
    print('Job Listing Created:')
    print(f'  ID: {result["job_listing"]["id"]}')
    print(f'  Title: {result["job_listing"]["title"]}')
    print(f'  Company: {result["job_listing"]["company"]}')
    print(f'  Keywords Extracted: {len(result["job_listing"]["keywords"])}')
    print()
    print('Keywords:')
    for i, kw in enumerate(result["job_listing"]["keywords"][:15], 1):
        print(f'  {i}. {kw}')
    if len(result["job_listing"]["keywords"]) > 15:
        print(f'  ... and {len(result["job_listing"]["keywords"]) - 15} more')
    print()
    print('Message:', result["message"])
else:
    print('❌ FAILED')
    print(f'Error: {response.json()}')

