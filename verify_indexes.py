import json
from pathlib import Path

# Check if the resume file exists in the correct location
resume_id = '3dd6b4d2-4f14-4bf8-8dd5-5877c6d3d1ab'
resume_path = Path('data/resumes') / f'{resume_id}.json'
print(f'Resume file exists: {resume_path.exists()}')

# Check if the job listing file exists
job_id = '2ee2467f-f8a9-4485-a389-46a9a5ee7850'
job_path = Path('data/job_listings') / f'{job_id}.json'
print(f'Job listing file exists: {job_path.exists()}')

# Check if resume is in index
print()
print('Checking resume index...')
try:
    index = json.loads(Path('data/resumes/index.json').read_text(encoding='utf-8'))
    found = False
    for r in index['resumes']:
        if r['id'] == resume_id:
            print(f'✅ Resume found in index: {r["name"]}')
            print(f'   Job Listing ID: {r["job_listing_id"]}')
            found = True
            break
    if not found:
        print(f'❌ Resume NOT found in index')
except Exception as e:
    print(f'Error reading resume index: {e}')

# Check if job listing is in index
print()
print('Checking job listing index...')
try:
    index = json.loads(Path('data/job_listings/index.json').read_text(encoding='utf-8'))
    found = False
    for j in index['job_listings']:
        if j['id'] == job_id:
            print(f'✅ Job listing found in index: {j["title"]} at {j["company"]}')
            found = True
            break
    if not found:
        print(f'❌ Job listing NOT found in index')
except Exception as e:
    print(f'Error reading job listing index: {e}')

# Check bidirectional linking
print()
print('Checking bidirectional linking...')
try:
    job_data = json.loads(job_path.read_text(encoding='utf-8'))
    tailored_ids = job_data.get('tailored_resume_ids', [])
    if resume_id in tailored_ids:
        print(f'✅ Resume linked in job listing: {tailored_ids}')
    else:
        print(f'❌ Resume NOT linked in job listing. Tailored IDs: {tailored_ids}')
except Exception as e:
    print(f'Error checking job data: {e}')

