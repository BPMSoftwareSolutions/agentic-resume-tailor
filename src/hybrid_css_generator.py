"""
Hybrid CSS Generator - Generate CSS for professional resume styling.

This module generates CSS stylesheets for resume themes,
including layout, typography, colors, and print styles.
"""

from typing import Dict, Any


class HybridCSSGenerator:
    """
    Generate CSS for resume themes.
    """
    
    THEMES = {
        'professional': {
            'colors': {
                'primary': '#2C3E50',
                'secondary': '#34495E',
                'accent': '#3498DB',
                'text': '#2C3E50',
                'text_light': '#7F8C8D',
                'background': '#ECF0F1',
                'section_bg': '#FFFFFF'
            },
            'typography': {
                'fontFamily': 'Calibri, Arial, sans-serif',
                'baseFontSize': '10pt',
                'headingFontSize': '11pt',
                'nameFontSize': '18pt'
            }
        },
        'modern': {
            'colors': {
                'primary': '#1A237E',
                'secondary': '#283593',
                'accent': '#3F51B5',
                'text': '#212121',
                'text_light': '#757575',
                'background': '#FAFAFA',
                'section_bg': '#FFFFFF'
            },
            'typography': {
                'fontFamily': 'Calibri, Arial, sans-serif',
                'baseFontSize': '10pt',
                'headingFontSize': '11pt',
                'nameFontSize': '18pt'
            }
        },
        'executive': {
            'colors': {
                'primary': '#1B1B1B',
                'secondary': '#424242',
                'accent': '#757575',
                'text': '#1B1B1B',
                'text_light': '#757575',
                'background': '#F5F5F5',
                'section_bg': '#FFFFFF'
            },
            'typography': {
                'fontFamily': 'Calibri, Georgia, serif',
                'baseFontSize': '10pt',
                'headingFontSize': '11pt',
                'nameFontSize': '18pt'
            }
        }
    }
    
    def __init__(self, theme: str = "professional"):
        """
        Initialize the CSS generator.
        
        Args:
            theme: Theme name (professional, modern, executive)
        """
        self.theme = theme
        self.theme_config = self.THEMES.get(theme, self.THEMES['professional'])
    
    def generate_css(self) -> str:
        """Generate complete CSS stylesheet."""
        css_parts = []
        
        # Base styles
        css_parts.append(self._generate_base_css())
        
        # Layout styles
        css_parts.append(self._generate_layout_css())
        
        # Typography styles
        css_parts.append(self._generate_typography_css())
        
        # Component styles
        css_parts.append(self._generate_component_css())
        
        # Print styles
        css_parts.append(self._generate_print_css())
        
        return '\n\n'.join(css_parts)
    
    def _generate_base_css(self) -> str:
        """Generate base CSS reset and page setup."""
        colors = self.theme_config['colors']
        typo = self.theme_config['typography']
        
        return f'''/* Base Styles */
* {{
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}}

body {{
  font-family: {typo['fontFamily']};
  background-color: {colors['background']};
  color: {colors['text']};
  line-height: 1.6;
  font-size: {typo['baseFontSize']};
}}

.resume-container {{
  max-width: 8.5in;
  margin: 0 auto;
  background: white;
  padding: 0.5in;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
}}'''
    
    def _generate_layout_css(self) -> str:
        """Generate layout CSS using CSS Grid/Flexbox."""
        colors = self.theme_config['colors']
        
        return f'''/* Layout Styles */
.header {{
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 2px solid {colors['primary']};
}}

.header-content {{
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}}

.personal-info {{
  flex: 1;
}}

.contact-info {{
  text-align: right;
  font-size: 9pt;
  color: {colors['text_light']};
}}

.contact-item {{
  margin-bottom: 3px;
}}

.section {{
  margin-bottom: 20px;
}}

.section-heading {{
  font-size: {self.theme_config['typography']['headingFontSize']};
  font-weight: bold;
  color: {colors['primary']};
  margin-bottom: 10px;
  padding-bottom: 5px;
  border-bottom: 1px solid {colors['accent']};
  text-transform: uppercase;
  letter-spacing: 0.5px;
}}

.subsection-heading {{
  font-size: 10pt;
  font-weight: bold;
  color: {colors['secondary']};
  margin-bottom: 8px;
  text-transform: uppercase;
}}

.two-column {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}}

.experience-item {{
  margin-bottom: 15px;
}}

.experience-header {{
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}}

.experience-left {{
  flex: 1;
}}

.experience-right {{
  text-align: right;
  font-size: 9pt;
  color: {colors['text_light']};
}}'''
    
    def _generate_typography_css(self) -> str:
        """Generate typography styles."""
        colors = self.theme_config['colors']
        typo = self.theme_config['typography']
        
        return f'''/* Typography Styles */
h1 {{
  font-size: {typo['nameFontSize']};
  font-weight: bold;
  color: {colors['primary']};
  margin-bottom: 5px;
}}

.title {{
  font-size: {typo['headingFontSize']};
  font-weight: bold;
  color: {colors['secondary']};
  margin-bottom: 5px;
}}

.summary-text {{
  text-align: justify;
  line-height: 1.5;
}}

.employer {{
  font-weight: bold;
  font-size: 10pt;
  color: {colors['primary']};
}}

.role {{
  font-weight: bold;
  font-size: 10pt;
  color: {colors['secondary']};
  margin-top: 2px;
}}

.location, .dates {{
  font-size: 9pt;
  color: {colors['text_light']};
}}

.bullet-item {{
  margin-bottom: 5px;
  margin-left: 15px;
}}

.bullet-text {{
  line-height: 1.4;
}}

.skill-category {{
  margin-bottom: 8px;
}}

.skill-label {{
  font-weight: bold;
  color: {colors['secondary']};
  display: inline;
}}

.skill-value {{
  display: inline;
  margin-left: 5px;
}}

.expertise-list {{
  list-style-type: none;
  padding-left: 0;
}}

.expertise-item {{
  margin-bottom: 5px;
  padding-left: 15px;
  position: relative;
}}

.expertise-item::before {{
  content: "•";
  position: absolute;
  left: 0;
  color: {colors['accent']};
  font-weight: bold;
}}

.education-item, .certification-item, .achievement-item {{
  margin-bottom: 5px;
}}

.degree {{
  font-weight: bold;
}}'''
    
    def _generate_component_css(self) -> str:
        """Generate component-specific styles."""
        return '''/* Component Styles */
.skills-column {
  break-inside: avoid;
}

.experience-item {
  break-inside: avoid;
}

.education-item {
  break-inside: avoid;
}'''
    
    def _generate_print_css(self) -> str:
        """Generate print-specific styles."""
        return '''/* Print Styles */
@media print {
  body {
    background: white;
  }
  
  .resume-container {
    box-shadow: none;
    padding: 0;
    max-width: 100%;
  }
  
  .section {
    page-break-inside: avoid;
  }
  
  .experience-item {
    page-break-inside: avoid;
  }
}

@page {
  size: letter;
  margin: 0.5in;
}'''

