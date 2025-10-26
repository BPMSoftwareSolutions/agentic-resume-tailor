#!/usr/bin/env python3
"""
Test resume-job linking functionality.

This script verifies:
1. Resumes have job_listing_id field set
2. Job listings have tailored_resume_ids array
3. Bidirectional linking is consistent
4. Timestamps are in ISO 8601 format with Z suffix
"""

import json
from pathlib import Path


def test_resume_job_linking():
    """Test resume-job linking."""
    print("=" * 80)
    print("TEST RESUME-JOB LINKING")
    print("=" * 80 + "\n")
    
    # Load resume index
    resume_index_path = Path("data/resumes/index.json")
    if not resume_index_path.exists():
        print("❌ Resume index not found")
        return False
    
    with open(resume_index_path, 'r', encoding='utf-8') as f:
        resume_index = json.load(f)
    
    # Load job listing index
    job_index_path = Path("data/job_listings/index.json")
    if not job_index_path.exists():
        print("❌ Job listing index not found")
        return False
    
    with open(job_index_path, 'r', encoding='utf-8') as f:
        job_index = json.load(f)
    
    print(f"Found {len(resume_index.get('resumes', []))} resumes")
    print(f"Found {len(job_index.get('job_listings', []))} job listings\n")
    
    # Test 1: Check resume fields
    print("TEST 1: Resume Fields")
    print("-" * 80)
    resumes_with_job_link = 0
    for resume in resume_index.get('resumes', []):
        resume_id = resume.get('id')
        job_listing_id = resume.get('job_listing_id')
        created_at = resume.get('created_at', '')
        updated_at = resume.get('updated_at', '')
        
        # Check timestamp format
        if created_at and not created_at.endswith('Z'):
            print(f"⚠️  Resume {resume_id}: created_at not in ISO 8601 format: {created_at}")
        if updated_at and not updated_at.endswith('Z'):
            print(f"⚠️  Resume {resume_id}: updated_at not in ISO 8601 format: {updated_at}")
        
        if job_listing_id:
            resumes_with_job_link += 1
            print(f"✅ Resume {resume_id}: linked to job {job_listing_id}")
    
    print(f"\n✅ {resumes_with_job_link} resumes have job_listing_id set\n")
    
    # Test 2: Check job listing fields
    print("TEST 2: Job Listing Fields")
    print("-" * 80)
    jobs_with_resume_links = 0
    for job in job_index.get('job_listings', []):
        job_id = job.get('id')
        tailored_resume_ids = job.get('tailored_resume_ids', [])
        created_at = job.get('created_at', '')
        updated_at = job.get('updated_at', '')
        
        # Check timestamp format
        if created_at and not created_at.endswith('Z'):
            print(f"⚠️  Job {job_id}: created_at not in ISO 8601 format: {created_at}")
        if updated_at and not updated_at.endswith('Z'):
            print(f"⚠️  Job {job_id}: updated_at not in ISO 8601 format: {updated_at}")
        
        if tailored_resume_ids:
            jobs_with_resume_links += 1
            print(f"✅ Job {job_id}: linked to {len(tailored_resume_ids)} resume(s)")
    
    print(f"\n✅ {jobs_with_resume_links} job listings have tailored_resume_ids set\n")
    
    # Test 3: Check bidirectional consistency
    print("TEST 3: Bidirectional Linking Consistency")
    print("-" * 80)
    
    # Build maps
    resume_to_job = {}
    for resume in resume_index.get('resumes', []):
        if resume.get('job_listing_id'):
            resume_to_job[resume['id']] = resume['job_listing_id']
    
    job_to_resumes = {}
    for job in job_index.get('job_listings', []):
        if job.get('tailored_resume_ids'):
            job_to_resumes[job['id']] = job['tailored_resume_ids']
    
    # Check consistency
    inconsistencies = 0
    for resume_id, job_id in resume_to_job.items():
        if job_id not in job_to_resumes or resume_id not in job_to_resumes[job_id]:
            print(f"❌ Resume {resume_id} links to job {job_id}, but job doesn't link back")
            inconsistencies += 1
        else:
            print(f"✅ Resume {resume_id} <-> Job {job_id} (bidirectional)")
    
    for job_id, resume_ids in job_to_resumes.items():
        for resume_id in resume_ids:
            if resume_id not in resume_to_job or resume_to_job[resume_id] != job_id:
                print(f"❌ Job {job_id} links to resume {resume_id}, but resume doesn't link back")
                inconsistencies += 1
    
    if inconsistencies == 0:
        print(f"\n✅ All bidirectional links are consistent\n")
    else:
        print(f"\n❌ Found {inconsistencies} inconsistencies\n")
    
    # Test 4: Check required fields
    print("TEST 4: Required Fields in Indexes")
    print("-" * 80)
    
    required_resume_fields = ['id', 'name', 'created_at', 'updated_at']
    required_job_fields = ['id', 'title', 'company', 'created_at', 'updated_at']
    
    missing_resume_fields = 0
    for resume in resume_index.get('resumes', []):
        for field in required_resume_fields:
            if field not in resume:
                print(f"❌ Resume {resume.get('id')}: missing field '{field}'")
                missing_resume_fields += 1
    
    missing_job_fields = 0
    for job in job_index.get('job_listings', []):
        for field in required_job_fields:
            if field not in job:
                print(f"❌ Job {job.get('id')}: missing field '{field}'")
                missing_job_fields += 1
    
    if missing_resume_fields == 0:
        print(f"✅ All resumes have required fields")
    if missing_job_fields == 0:
        print(f"✅ All job listings have required fields")
    
    print()
    
    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"✅ Resumes with job links: {resumes_with_job_link}")
    print(f"✅ Jobs with resume links: {jobs_with_resume_links}")
    print(f"✅ Bidirectional inconsistencies: {inconsistencies}")
    print(f"✅ Missing resume fields: {missing_resume_fields}")
    print(f"✅ Missing job fields: {missing_job_fields}")
    
    success = inconsistencies == 0 and missing_resume_fields == 0 and missing_job_fields == 0
    if success:
        print("\n✅ ALL TESTS PASSED")
    else:
        print("\n❌ SOME TESTS FAILED")
    
    return success


if __name__ == "__main__":
    test_resume_job_linking()

