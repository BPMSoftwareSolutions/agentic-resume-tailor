"""
Hybrid Resume Processor - Generate semantic HTML from resume JSON.

This module generates semantic HTML structure with data attributes for
programmatic access and transformation. Part of the hybrid HTML+SVG
resume generation pipeline.
"""

import json
from pathlib import Path
from typing import Dict, Any, List


class HybridResumeProcessor:
    """
    Generate semantic HTML from resume JSON with data attributes
    for programmatic access and transformation.
    """
    
    def __init__(self, resume_json_path: str, theme: str = "professional"):
        """
        Initialize the hybrid resume processor.
        
        Args:
            resume_json_path: Path to resume JSON file
            theme: Theme name (professional, modern, executive, creative)
        """
        self.resume_data = self._load_resume_data(resume_json_path)
        self.theme = theme
        
        # Sort experiences by date (most recent first)
        if 'experience' in self.resume_data:
            self.resume_data['experience'] = self._sort_experiences_by_date(self.resume_data['experience'])
    
    def _load_resume_data(self, json_path: str) -> Dict[str, Any]:
        """Load resume data from JSON file."""
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _sanitize_id(self, text: str) -> str:
        """
        Sanitize text for use as an element ID or data attribute.
        Replace spaces and special characters with underscores.
        """
        return text.lower().replace(' ', '_').replace('-', '_').replace('/', '_').replace('.', '_').replace(',', '').replace('&', 'and').replace('#', '')
    
    def _sort_experiences_by_date(self, experiences: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Sort experiences by end date (most recent first), then by start date.
        Handles date ranges like "2022 – 2024" or "2010 – Present".
        
        Args:
            experiences: List of experience dictionaries with 'dates' field
            
        Returns:
            Sorted list of experiences (most recent to oldest)
        """
        def get_date_tuple(exp: Dict[str, Any]) -> tuple:
            """Extract (end_year, start_year) from dates field for sorting."""
            dates = exp.get('dates', '')
            
            # Handle "Present" or current job
            if 'Present' in dates or 'Current' in dates:
                end_year = 9999  # Put current jobs at the top
                # Try to get start year
                parts = dates.replace('–', '-').replace('—', '-').split('-')
                if len(parts) >= 1:
                    start_str = ''.join(filter(str.isdigit, parts[0].strip()))[:4]
                    start_year = int(start_str) if start_str else 0
                else:
                    start_year = 0
                return (end_year, start_year)
            
            # Split by dash/hyphen to get start and end dates
            parts = dates.replace('–', '-').replace('—', '-').split('-')
            if len(parts) >= 2:
                # Extract end year
                end_str = ''.join(filter(str.isdigit, parts[-1].strip()))[:4]
                end_year = int(end_str) if end_str else 0
                
                # Extract start year
                start_str = ''.join(filter(str.isdigit, parts[0].strip()))[:4]
                start_year = int(start_str) if start_str else 0
                
                return (end_year, start_year)
            
            # If we can't parse it, return (0, 0) to put it at the end
            return (0, 0)
        
        # Sort by end year descending, then start year descending
        # This ensures most recent jobs come first, and if end dates match, most recent start date wins
        return sorted(experiences, key=get_date_tuple, reverse=True)
    
    def generate_html(self) -> str:
        """
        Generate HTML structure with semantic tags and data attributes.
        
        Returns HTML string with:
        - Semantic HTML5 tags (header, section, article)
        - Data attributes for each content piece
        - CSS classes for styling hooks
        - SVG placeholders for graphics
        """
        html_parts = []
        
        # Generate header section
        html_parts.append(self._generate_header_html())
        
        # Generate summary section
        html_parts.append(self._generate_summary_html())
        
        # Generate skills section
        html_parts.append(self._generate_skills_html())
        
        # Generate experience section
        html_parts.append(self._generate_experience_html())
        
        # Generate education section
        html_parts.append(self._generate_education_html())
        
        return '\n'.join(html_parts)
    
    def _generate_header_html(self) -> str:
        """Generate header with contact information."""
        name = self.resume_data.get('name', '')
        title = self.resume_data.get('title', '')
        location = self.resume_data.get('location', '')
        contact = self.resume_data.get('contact', {})
        email = contact.get('email', '')
        phone = contact.get('phone', '')
        
        return f'''    <div class="header" data-section="header">
      <div class="header-content">
        <div class="personal-info" data-section="personal_info">
          <h1 data-field="name">{name}</h1>
          <div class="title" data-field="title">{title}</div>
        </div>
        <div class="contact-info" data-section="contact_info">
          <div class="contact-item" data-field="location">{location}</div>
          <div class="contact-item" data-field="email">{email}</div>
          <div class="contact-item" data-field="phone">{phone}</div>
        </div>
      </div>
    </div>'''
    
    def _generate_summary_html(self) -> str:
        """Generate summary section."""
        summary = self.resume_data.get('summary', '')
        
        return f'''    <section class="section" data-section="summary">
      <h2 class="section-heading">PROFESSIONAL SUMMARY</h2>
      <p class="summary-text" data-field="summary_text">{summary}</p>
    </section>'''
    
    def _generate_skills_html(self) -> str:
        """Generate two-column skills section."""
        tech_prof = self.resume_data.get('technical_proficiencies', {})
        expertise = self.resume_data.get('areas_of_expertise', [])
        
        # Generate technical proficiencies (left column)
        tech_html = ['        <div class="skills-column" data-section="technical_proficiencies">']
        tech_html.append('          <h3 class="subsection-heading">TECHNICAL PROFICIENCIES</h3>')
        
        for category, skills in tech_prof.items():
            category_id = self._sanitize_id(category)
            category_display = category.replace('_', ' ').upper()
            tech_html.append(f'          <div class="skill-category" data-category="{category_id}">')
            tech_html.append(f'            <div class="skill-label">{category_display}:</div>')
            tech_html.append(f'            <div class="skill-value">{skills}</div>')
            tech_html.append('          </div>')
        
        tech_html.append('        </div>')
        
        # Generate areas of expertise (right column)
        expertise_html = ['        <div class="skills-column" data-section="areas_of_expertise">']
        expertise_html.append('          <h3 class="subsection-heading">AREAS OF EXPERTISE</h3>')
        expertise_html.append('          <ul class="expertise-list">')
        
        for idx, area in enumerate(expertise):
            expertise_html.append(f'            <li class="expertise-item" data-item="{idx}">{area}</li>')
        
        expertise_html.append('          </ul>')
        expertise_html.append('        </div>')
        
        return f'''    <section class="section" data-section="skills">
      <h2 class="section-heading">CORE COMPETENCIES</h2>
      <div class="two-column">
{chr(10).join(tech_html)}
{chr(10).join(expertise_html)}
      </div>
    </section>'''
    
    def _generate_experience_html(self) -> str:
        """Generate experience section with bullets."""
        experience = self.resume_data.get('experience', [])
        
        exp_html = ['    <section class="section" data-section="experience">']
        exp_html.append('      <h2 class="section-heading">PROFESSIONAL EXPERIENCE</h2>')
        
        for idx, job in enumerate(experience):
            employer = job.get('employer', '')
            location = job.get('location', '')
            dates = job.get('dates', '')
            role = job.get('role', '')
            bullets = job.get('bullets', job.get('selected_bullets', []))
            
            company_id = self._sanitize_id(employer)
            
            exp_html.append(f'      <div class="experience-item" data-position="{idx}" data-company="{company_id}">')
            exp_html.append('        <div class="experience-header">')
            exp_html.append('          <div class="experience-left">')
            exp_html.append(f'            <div class="employer" data-field="employer">{employer}</div>')
            exp_html.append(f'            <div class="role" data-field="role">{role}</div>')
            exp_html.append('          </div>')
            exp_html.append('          <div class="experience-right">')
            exp_html.append(f'            <div class="location" data-field="location">{location}</div>')
            exp_html.append(f'            <div class="dates" data-field="dates">{dates}</div>')
            exp_html.append('          </div>')
            exp_html.append('        </div>')
            
            # Generate bullets
            for bullet_idx, bullet in enumerate(bullets):
                # Handle both string and dict formats
                bullet_text = bullet if isinstance(bullet, str) else bullet.get('text', '')
                
                exp_html.append(f'        <div class="bullet-item" data-bullet="{bullet_idx}">')
                exp_html.append(f'          <div class="bullet-text">• {bullet_text}</div>')
                exp_html.append('        </div>')
            
            exp_html.append('      </div>')
        
        exp_html.append('    </section>')
        
        return '\n'.join(exp_html)
    
    def _generate_education_html(self) -> str:
        """Generate education and certifications section."""
        education = self.resume_data.get('education', [])
        certifications = self.resume_data.get('certifications', [])
        achievements = self.resume_data.get('achievements', [])
        
        edu_html = ['    <section class="section" data-section="education">']
        edu_html.append('      <h2 class="section-heading">EDUCATION & PROFESSIONAL DEVELOPMENT</h2>')
        
        # Education items
        for idx, edu in enumerate(education):
            degree = edu.get('degree', '')
            institution = edu.get('institution', '')
            location = edu.get('location', '')
            
            edu_html.append(f'      <div class="education-item" data-position="{idx}">')
            edu_html.append(f'        <div class="degree" data-field="degree">{degree} | {institution}, {location}</div>')
            edu_html.append('      </div>')
        
        # Certifications
        if certifications:
            for idx, cert in enumerate(certifications):
                edu_html.append(f'      <div class="certification-item" data-position="{idx}">• {cert}</div>')
        
        # Achievements
        if achievements:
            for idx, achievement in enumerate(achievements):
                edu_html.append(f'      <div class="achievement-item" data-position="{idx}">• {achievement}</div>')
        
        edu_html.append('    </section>')
        
        return '\n'.join(edu_html)

