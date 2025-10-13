"""
Resume Matcher

Compares job posting requirements with resume content to:
- Identify matching skills
- Find relevant experience bullets
- Calculate match scores
- Suggest which sections to update

Usage:
    from orchestrator import ResumeMatcher
    from parsers import JobPostingParser
    
    # Parse job posting
    job_parser = JobPostingParser()
    job_data = job_parser.parse_file("job.md")
    
    # Load resume
    with open("data/resumes/resume_id.json") as f:
        resume_data = json.load(f)
    
    # Match
    matcher = ResumeMatcher()
    match_result = matcher.match(job_data, resume_data)
    
    print(f"Match score: {match_result['score']}%")
    print(f"Missing skills: {match_result['missing_skills']}")
"""

import json
from typing import Dict, List, Any, Set
from pathlib import Path


class ResumeMatcher:
    """Match job requirements to resume content"""
    
    def __init__(self):
        self.job_data = {}
        self.resume_data = {}
    
    def match(self, job_data: Dict[str, Any], resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compare job requirements with resume content
        
        Returns:
            {
                'score': float (0-100),
                'matching_skills': list,
                'missing_skills': list,
                'relevant_experience': list,
                'suggestions': list,
                'details': dict
            }
        """
        self.job_data = job_data
        self.resume_data = resume_data
        
        # Extract resume skills
        resume_skills = self._extract_resume_skills()
        
        # Compare skills
        required_skills = set(s.lower() for s in job_data.get('required_skills', []))
        matching_skills = resume_skills.intersection(required_skills)
        missing_skills = required_skills - resume_skills
        
        # Find relevant experience
        relevant_experience = self._find_relevant_experience(job_data)
        
        # Calculate match score
        score = self._calculate_match_score(
            matching_skills,
            required_skills,
            relevant_experience,
            job_data
        )
        
        # Generate suggestions
        suggestions = self._generate_suggestions(
            missing_skills,
            relevant_experience,
            job_data
        )
        
        return {
            'score': round(score, 2),
            'matching_skills': sorted(list(matching_skills)),
            'missing_skills': sorted(list(missing_skills)),
            'relevant_experience': relevant_experience,
            'suggestions': suggestions,
            'details': {
                'total_required_skills': len(required_skills),
                'total_matching_skills': len(matching_skills),
                'skill_match_percentage': round(len(matching_skills) / len(required_skills) * 100, 2) if required_skills else 0,
                'relevant_experience_count': len(relevant_experience)
            }
        }
    
    def _extract_resume_skills(self) -> Set[str]:
        """Extract all skills from resume"""
        skills = set()
        
        # From technical_skills section
        tech_skills = self.resume_data.get('technical_skills', {})
        for category, skills_list in tech_skills.items():
            if isinstance(skills_list, str):
                # Split by comma and clean
                for skill in skills_list.split(','):
                    skills.add(skill.strip().lower())
            elif isinstance(skills_list, list):
                for skill in skills_list:
                    skills.add(skill.strip().lower())
        
        # From expertise section
        expertise = self.resume_data.get('expertise', [])
        for area in expertise:
            # Extract keywords from expertise areas
            words = area.lower().split()
            skills.update(words)
        
        # From experience bullets (extract technology mentions)
        experience = self.resume_data.get('experience', [])
        for exp in experience:
            bullets = exp.get('bullets', [])
            for bullet in bullets:
                # Simple keyword extraction (could be improved with NLP)
                bullet_lower = bullet.lower()
                # Check for common tech keywords
                tech_keywords = ['python', 'java', 'javascript', 'aws', 'azure', 'docker', 'kubernetes', 
                                'react', 'angular', 'node', 'sql', 'mongodb', 'ci/cd', 'microservices']
                for keyword in tech_keywords:
                    if keyword in bullet_lower:
                        skills.add(keyword)
        
        return skills
    
    def _find_relevant_experience(self, job_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find experience entries relevant to the job"""
        relevant = []
        
        required_skills = set(s.lower() for s in job_data.get('required_skills', []))
        responsibilities = [r.lower() for r in job_data.get('responsibilities', [])]
        
        experience = self.resume_data.get('experience', [])
        
        for exp in experience:
            relevance_score = 0
            matching_bullets = []
            
            bullets = exp.get('bullets', [])
            for bullet in bullets:
                bullet_lower = bullet.lower()
                
                # Check if bullet mentions required skills
                skill_matches = sum(1 for skill in required_skills if skill in bullet_lower)
                if skill_matches > 0:
                    relevance_score += skill_matches
                    matching_bullets.append({
                        'text': bullet,
                        'skill_matches': skill_matches
                    })
                
                # Check if bullet relates to job responsibilities
                resp_matches = sum(1 for resp in responsibilities if any(word in bullet_lower for word in resp.split()[:5]))
                if resp_matches > 0:
                    relevance_score += resp_matches * 0.5
            
            if relevance_score > 0:
                relevant.append({
                    'employer': exp.get('employer', ''),
                    'role': exp.get('role', ''),
                    'dates': exp.get('dates', ''),
                    'relevance_score': relevance_score,
                    'matching_bullets': matching_bullets,
                    'total_bullets': len(bullets)
                })
        
        # Sort by relevance score
        relevant.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return relevant
    
    def _calculate_match_score(self, matching_skills: Set[str], required_skills: Set[str], 
                               relevant_experience: List[Dict], job_data: Dict[str, Any]) -> float:
        """Calculate overall match score (0-100)"""
        
        # Skills match (50% weight)
        skill_score = (len(matching_skills) / len(required_skills) * 50) if required_skills else 0
        
        # Experience relevance (30% weight)
        exp_score = 0
        if relevant_experience:
            # Score based on number of relevant experiences and their relevance scores
            total_relevance = sum(exp['relevance_score'] for exp in relevant_experience)
            # Normalize to 0-30 range
            exp_score = min(30, total_relevance * 3)
        
        # Title match (10% weight)
        title_score = 0
        job_title = job_data.get('title', '').lower()
        resume_title = self.resume_data.get('basic_info', {}).get('title', '').lower()
        if job_title and resume_title:
            # Simple word overlap
            job_words = set(job_title.split())
            resume_words = set(resume_title.split())
            overlap = len(job_words.intersection(resume_words))
            title_score = min(10, overlap * 3)
        
        # Years of experience (10% weight)
        years_score = 0
        required_years = job_data.get('experience_years')
        if required_years:
            # Count years from experience section
            experience = self.resume_data.get('experience', [])
            total_years = len(experience) * 2  # Rough estimate
            if total_years >= required_years:
                years_score = 10
            else:
                years_score = (total_years / required_years) * 10
        else:
            years_score = 10  # No requirement, full score
        
        total_score = skill_score + exp_score + title_score + years_score
        
        return min(100, total_score)
    
    def _generate_suggestions(self, missing_skills: Set[str], relevant_experience: List[Dict], 
                             job_data: Dict[str, Any]) -> List[str]:
        """Generate suggestions for improving the resume"""
        suggestions = []
        
        # Missing skills suggestions
        if missing_skills:
            top_missing = sorted(list(missing_skills))[:5]
            suggestions.append(f"Add these missing skills: {', '.join(top_missing)}")
        
        # Title suggestion
        job_title = job_data.get('title', '')
        resume_title = self.resume_data.get('basic_info', {}).get('title', '')
        if job_title and job_title.lower() != resume_title.lower():
            suggestions.append(f"Consider updating title to match job: '{job_title}'")
        
        # Experience emphasis suggestion
        if relevant_experience:
            top_exp = relevant_experience[0]
            suggestions.append(f"Emphasize experience at {top_exp['employer']} - it has {len(top_exp['matching_bullets'])} relevant bullets")
        
        # Responsibilities alignment
        responsibilities = job_data.get('responsibilities', [])
        if responsibilities:
            suggestions.append(f"Align experience bullets with key responsibilities: {responsibilities[0][:100]}...")
        
        # Compliance requirements
        compliance = job_data.get('compliance_requirements', [])
        if compliance:
            suggestions.append(f"Highlight experience with: {', '.join(compliance)}")
        
        return suggestions


def main():
    """Test the matcher"""
    import sys
    from pathlib import Path

    # Add src to path
    sys.path.insert(0, str(Path(__file__).parent.parent))

    if len(sys.argv) < 3:
        print("Usage: python resume_matcher.py <job_posting_file> <resume_file>")
        sys.exit(1)

    from parsers.job_posting_parser import JobPostingParser
    
    # Parse job posting
    job_parser = JobPostingParser()
    job_data = job_parser.parse_file(sys.argv[1])
    
    # Load resume
    with open(sys.argv[2], 'r', encoding='utf-8') as f:
        resume_data = json.load(f)
    
    # Match
    matcher = ResumeMatcher()
    result = matcher.match(job_data, resume_data)
    
    print("=== Resume Match Analysis ===\n")
    print(f"Overall Match Score: {result['score']}%")
    print(f"\nSkill Match: {result['details']['skill_match_percentage']}%")
    print(f"  - Matching: {len(result['matching_skills'])} skills")
    print(f"  - Missing: {len(result['missing_skills'])} skills")
    
    if result['matching_skills']:
        print(f"\nMatching Skills:")
        for skill in result['matching_skills'][:10]:
            print(f"  ✓ {skill}")
    
    if result['missing_skills']:
        print(f"\nMissing Skills:")
        for skill in result['missing_skills'][:10]:
            print(f"  ✗ {skill}")
    
    if result['relevant_experience']:
        print(f"\nRelevant Experience ({len(result['relevant_experience'])} entries):")
        for exp in result['relevant_experience'][:3]:
            print(f"  - {exp['employer']} ({exp['role']})")
            print(f"    Relevance: {exp['relevance_score']:.1f}, Matching bullets: {len(exp['matching_bullets'])}")
    
    if result['suggestions']:
        print(f"\nSuggestions:")
        for i, suggestion in enumerate(result['suggestions'], 1):
            print(f"  {i}. {suggestion}")


if __name__ == '__main__':
    main()

