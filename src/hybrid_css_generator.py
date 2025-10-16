"""
Hybrid CSS Generator - Generate CSS from theme configuration.

This module generates CSS stylesheets from theme configuration files,
including layout, typography, colors, and print styles.
"""

import json
from pathlib import Path
from typing import Any, Dict


class HybridCSSGenerator:
    """
    Generate CSS from theme configuration.
    """

    def __init__(self, theme: str = "creative"):
        """
        Initialize the CSS generator.

        Args:
            theme: Theme name (professional, modern, executive, creative)
        """
        self.theme = theme
        self.theme_config = self._load_theme_config(theme)

    def _load_theme_config(self, theme: str) -> Dict[str, Any]:
        """Load theme configuration."""
        theme_path = (
            Path(__file__).parent.parent
            / "config"
            / "resume_themes"
            / theme
            / "theme.json"
        )
        with open(theme_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def generate_css(self) -> str:
        """
        Generate CSS with:
        - Page layout (@page, body, container)
        - Typography (fonts, sizes, weights from theme)
        - Colors (from theme palette)
        - Layout (grid, flexbox for responsive)
        - Print styles (@media print)
        """
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

        return "\n\n".join(css_parts)

    def _generate_base_css(self) -> str:
        """Generate base CSS reset and page setup."""
        colors = self.theme_config["colors"]
        typo = self.theme_config["typography"]

        return f"""/* Base Styles */
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
}}

.resume-container {{
  width: 1200px;
  margin: 0 auto;
  background: white;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
}}"""

    def _generate_layout_css(self) -> str:
        """
        Generate layout CSS using CSS Grid/Flexbox.

        Key classes:
        - .resume-container { width: 1200px; margin: 0 auto; }
        - .two-column { display: grid; grid-template-columns: 1fr 1fr; }
        - .experience-header { display: flex; justify-content: space-between; }
        """
        layout = self.theme_config["layout"]
        colors = self.theme_config["colors"]

        return f"""/* Layout Styles */
.header {{
  position: relative;
  height: {layout['header']['height']}px;
  overflow: hidden;
}}

.header-bg {{
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
}}

.header-content {{
  position: relative;
  z-index: 2;
  padding: {layout['header']['padding']}px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: 100%;
}}

.section {{
  padding: {layout['section']['padding']}px {layout['margins']['left']}px;
  margin-top: {layout['section']['marginTop']}px;
}}

.two-column {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: {layout['columns']['gap']}px;
}}

.skills-column {{
  display: flex;
  flex-direction: column;
}}

.experience-header {{
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
}}

.experience-left {{
  flex: 1;
}}

.experience-right {{
  text-align: right;
}}"""

    def _generate_typography_css(self) -> str:
        """
        Generate typography CSS from theme.typography.

        Maps theme config to CSS:
        - theme.typography.name.size → .personal-info h1 { font-size: 38px; }
        - theme.typography.body.color → .bullet-text { color: #1f2937; }
        """
        typo = self.theme_config["typography"]
        colors = self.theme_config["colors"]

        return f"""/* Typography Styles */
.personal-info h1 {{
  font-size: {typo['name']['size']}px;
  font-weight: {typo['name']['weight']};
  color: {typo['name']['color']};
  margin-bottom: 10px;
}}

.title {{
  font-size: {typo['title']['size']}px;
  font-weight: {typo['title']['weight']};
  color: {typo['title']['color']};
}}

.section-heading {{
  font-size: {typo['heading']['size']}px;
  font-weight: {typo['heading']['weight']};
  color: {typo['heading']['color']};
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid {colors['primary']};
}}

.subsection-heading {{
  font-size: {typo['subheading']['size']}px;
  font-weight: {typo['subheading']['weight']};
  color: {typo['subheading']['color']};
  margin-bottom: 15px;
}}

.summary-text {{
  font-size: {typo['body']['size']}px;
  color: {typo['body']['color']};
  text-align: justify;
  line-height: 1.8;
}}

.bullet-text {{
  font-size: {typo['body']['size']}px;
  color: {typo['body']['color']};
  line-height: 1.7;
  text-align: justify;
}}

.contact-item {{
  font-size: {typo['small']['size']}px;
  color: {colors['headerTextLight']};
  margin-bottom: 5px;
}}"""

    def _generate_component_css(self) -> str:
        """Generate component-specific CSS."""
        colors = self.theme_config["colors"]
        typo = self.theme_config["typography"]

        return f"""/* Component Styles */
.contact-info {{
  margin-top: 20px;
}}

.skill-category {{
  margin-bottom: 12px;
}}

.skill-label {{
  font-weight: 600;
  color: {colors['text']};
  font-size: {typo['small']['size']}px;
  margin-bottom: 4px;
}}

.skill-value {{
  font-size: {typo['small']['size']}px;
  color: {colors['textLight']};
  line-height: 1.6;
}}

.expertise-list {{
  list-style: none;
  display: grid;
  grid-template-columns: 1fr;
  gap: 8px;
}}

.expertise-item {{
  font-size: {typo['small']['size']}px;
  color: {colors['text']};
  padding-left: 20px;
  position: relative;
}}

.expertise-item::before {{
  content: "▸";
  position: absolute;
  left: 0;
  color: {colors['primary']};
  font-weight: bold;
}}

.experience-item {{
  margin-bottom: 30px;
}}

.employer {{
  font-size: {typo['subheading']['size']}px;
  font-weight: {typo['subheading']['weight']};
  color: {colors['text']};
}}

.role {{
  font-size: {typo['body']['size']}px;
  color: {colors['textLight']};
  font-style: italic;
}}

.location,
.dates {{
  font-size: {typo['small']['size']}px;
  color: {colors['textLight']};
}}

.bullet-item {{
  margin-bottom: 15px;
  padding-left: 20px;
  position: relative;
}}

.bullet-item::before {{
  content: "•";
  position: absolute;
  left: 0;
  color: {colors['primary']};
  font-weight: bold;
  font-size: 18px;
}}

.tags {{
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 8px;
}}

.tag {{
  display: inline-block;
  padding: 3px 8px;
  background-color: {colors['accent']}20;
  color: {typo['tag']['color']};
  font-size: {typo['tag']['size']}px;
  font-weight: {typo['tag']['weight']};
  border-radius: 3px;
  border: 1px solid {colors['accent']}40;
}}

.education-item {{
  margin-bottom: 15px;
}}

.degree {{
  font-size: {typo['subheading']['size']}px;
  font-weight: {typo['subheading']['weight']};
  color: {colors['text']};
}}

.institution {{
  font-size: {typo['small']['size']}px;
  color: {colors['textLight']};
}}

.certifications {{
  margin-top: 20px;
}}

.certification-item {{
  font-size: {typo['small']['size']}px;
  color: {colors['text']};
  margin-bottom: 8px;
  padding-left: 20px;
  position: relative;
}}

.certification-item::before {{
  content: "✓";
  position: absolute;
  left: 0;
  color: {colors['primary']};
  font-weight: bold;
}}"""

    def _generate_print_css(self) -> str:
        """
        Generate print-specific CSS.

        @media print {
          @page { margin: 0; size: A4; }
          body { margin: 0; padding: 0; }
          .resume-container { box-shadow: none; }
        }
        """
        return """/* Print Styles */
@media print {
  @page {
    margin: 0;
    size: letter;
  }
  
  body {
    margin: 0;
    padding: 0;
  }
  
  .resume-container {
    width: 100%;
    box-shadow: none;
    margin: 0;
  }
  
  .section {
    page-break-inside: avoid;
  }
  
  .experience-item {
    page-break-inside: avoid;
  }
}"""
