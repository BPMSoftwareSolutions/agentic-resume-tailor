"""
Generate Interactive HTML Presentations for Musical Sequences

This script generates interactive, collapsible HTML presentations from musical sequence JSON files.
It provides a progressive disclosure experience where users can expand movements, beats, and
detailed information step-by-step during presentations.

Usage:
    python scripts/generate_sequence_presentation.py sequences/hybrid-resume-generation.sequence.json
    python scripts/generate_sequence_presentation.py sequences/*.sequence.json --output-dir presentations
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime


class SequencePresentationGenerator:
    """Generate interactive HTML presentations from musical sequence definitions."""

    def __init__(self, sequence_path: Path, output_dir: Optional[Path] = None):
        """
        Initialize the presentation generator.

        Args:
            sequence_path: Path to the sequence JSON file
            output_dir: Optional output directory for the presentation
        """
        self.sequence_path = sequence_path
        self.output_dir = output_dir or sequence_path.parent.parent / "presentations"
        self.sequence_data: Dict[str, Any] = {}

    def load_sequence(self) -> None:
        """Load the sequence JSON file."""
        with open(self.sequence_path, "r", encoding="utf-8") as f:
            self.sequence_data = json.load(f)

    def generate_css(self) -> str:
        """Generate CSS styles for the presentation."""
        return """
        :root {
            --primary-color: #2563eb;
            --secondary-color: #7c3aed;
            --success-color: #059669;
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --text-primary: #f1f5f9;
            --text-secondary: #94a3b8;
            --border-color: #334155;
            --accent-color: #f59e0b;
            --hover-bg: #334155;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: var(--bg-color);
            color: var(--text-primary);
            line-height: 1.6;
            padding: 2rem;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        /* Header Styles */
        .header {
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            padding: 2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }

        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            color: white;
        }

        .header .subtitle {
            font-size: 1.2rem;
            opacity: 0.9;
            margin-bottom: 1rem;
        }

        .header .description {
            opacity: 0.8;
            font-size: 1rem;
        }

        /* Metadata Grid */
        .metadata-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin: 2rem 0;
        }

        .metadata-card {
            background: var(--card-bg);
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid var(--border-color);
        }

        .metadata-label {
            font-size: 0.875rem;
            color: var(--text-secondary);
            margin-bottom: 0.25rem;
        }

        .metadata-value {
            font-size: 1.125rem;
            font-weight: 600;
            color: var(--text-primary);
        }

        .metadata-value code {
            background: rgba(99, 102, 241, 0.2);
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            font-size: 0.9rem;
        }

        /* Collapsible Sections */
        .collapsible {
            background: var(--card-bg);
            border: 2px solid var(--border-color);
            border-radius: 8px;
            margin-bottom: 1rem;
            overflow: hidden;
            transition: all 0.3s ease;
        }

        .collapsible.expanded {
            border-color: var(--primary-color);
            box-shadow: 0 4px 20px rgba(37, 99, 235, 0.2);
        }

        .collapsible-header {
            padding: 1.25rem;
            cursor: pointer;
            user-select: none;
            display: flex;
            align-items: center;
            justify-content: space-between;
            transition: background 0.2s ease;
        }

        .collapsible-header:hover {
            background: var(--hover-bg);
        }

        .collapsible-title {
            display: flex;
            align-items: center;
            gap: 1rem;
            flex: 1;
        }

        .collapsible-icon {
            font-size: 1.5rem;
            transition: transform 0.3s ease;
        }

        .collapsible.expanded .collapsible-icon {
            transform: rotate(90deg);
        }

        .collapsible-content {
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.4s ease, padding 0.4s ease;
        }

        .collapsible.expanded .collapsible-content {
            max-height: 5000px;
            padding: 1.25rem;
            border-top: 1px solid var(--border-color);
        }

        /* Movement Styles */
        .movement-number {
            font-size: 2rem;
            font-weight: bold;
            color: var(--primary-color);
            min-width: 3rem;
        }

        .movement-name {
            font-size: 1.5rem;
            font-weight: 600;
        }

        .movement-badge {
            background: var(--primary-color);
            color: white;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.875rem;
        }

        .movement-description {
            color: var(--text-secondary);
            margin-bottom: 1rem;
        }

        .movement-meta {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 0.75rem;
            margin-bottom: 1.5rem;
        }

        .meta-item {
            font-size: 0.875rem;
        }

        .meta-label {
            color: var(--text-secondary);
        }

        .meta-value {
            color: var(--text-primary);
            font-weight: 500;
        }

        /* Beat Styles */
        .beats-container {
            margin-left: 1rem;
        }

        .beat {
            margin-bottom: 0.75rem;
        }

        .beat-number {
            font-size: 1.25rem;
            font-weight: bold;
            color: var(--accent-color);
            min-width: 2.5rem;
        }

        .beat-name {
            font-size: 1.125rem;
            font-weight: 500;
        }

        .beat-event {
            background: rgba(245, 158, 11, 0.2);
            color: var(--accent-color);
            padding: 0.2rem 0.6rem;
            border-radius: 4px;
            font-size: 0.85rem;
            font-family: 'Courier New', monospace;
        }

        .beat-description {
            color: var(--text-secondary);
            margin: 0.5rem 0;
            padding-left: 3rem;
        }

        /* Detail Sections */
        .detail-section {
            background: rgba(30, 41, 59, 0.5);
            padding: 1rem;
            border-radius: 6px;
            margin-top: 0.75rem;
            margin-left: 3rem;
            border-left: 3px solid var(--secondary-color);
        }

        .detail-heading {
            font-size: 0.9rem;
            font-weight: 600;
            color: var(--secondary-color);
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .detail-content {
            font-size: 0.95rem;
            color: var(--text-secondary);
        }

        .detail-content code {
            background: rgba(99, 102, 241, 0.2);
            padding: 0.15rem 0.4rem;
            border-radius: 3px;
            font-size: 0.85rem;
            color: var(--text-primary);
        }

        .detail-list {
            list-style: none;
            padding-left: 1rem;
        }

        .detail-list li {
            padding: 0.25rem 0;
        }

        .detail-list li:before {
            content: "→ ";
            color: var(--secondary-color);
            margin-right: 0.5rem;
        }

        /* User Story */
        .user-story {
            background: linear-gradient(135deg, rgba(37, 99, 235, 0.15), rgba(124, 58, 237, 0.15));
            padding: 1rem;
            border-radius: 6px;
            margin: 0.75rem 0;
            border-left: 3px solid var(--primary-color);
        }

        .user-story-line {
            margin: 0.25rem 0;
            font-size: 0.95rem;
        }

        .user-story-label {
            font-weight: 600;
            color: var(--primary-color);
        }

        /* Acceptance Criteria */
        .criteria {
            background: rgba(5, 150, 105, 0.1);
            padding: 1rem;
            border-radius: 6px;
            margin: 0.75rem 0;
            border-left: 3px solid var(--success-color);
        }

        .criteria-scenario {
            margin-bottom: 1rem;
        }

        .criteria-label {
            font-weight: 600;
            color: var(--success-color);
            margin-bottom: 0.25rem;
        }

        .criteria-items {
            list-style: none;
            padding-left: 1.25rem;
        }

        .criteria-items li {
            padding: 0.2rem 0;
            color: var(--text-secondary);
        }

        .criteria-items li:before {
            content: "✓ ";
            color: var(--success-color);
            margin-right: 0.5rem;
        }

        /* Governance */
        .governance-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
            margin: 1rem 0;
        }

        .governance-section {
            background: var(--card-bg);
            padding: 1rem;
            border-radius: 6px;
            border: 1px solid var(--border-color);
        }

        .governance-section h4 {
            color: var(--primary-color);
            margin-bottom: 0.5rem;
        }

        .tag-list {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin: 0.5rem 0;
        }

        .tag {
            background: rgba(37, 99, 235, 0.2);
            color: var(--primary-color);
            padding: 0.25rem 0.75rem;
            border-radius: 15px;
            font-size: 0.875rem;
            border: 1px solid var(--primary-color);
        }

        /* Events */
        .events-list {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 0.5rem;
            margin: 1rem 0;
        }

        .event-item {
            background: rgba(245, 158, 11, 0.1);
            padding: 0.5rem 0.75rem;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-size: 0.85rem;
            color: var(--accent-color);
            border: 1px solid rgba(245, 158, 11, 0.3);
        }

        /* Footer */
        .footer {
            text-align: center;
            color: var(--text-secondary);
            margin-top: 3rem;
            padding: 2rem;
            border-top: 1px solid var(--border-color);
        }

        /* Responsive */
        @media (max-width: 768px) {
            body {
                padding: 1rem;
            }

            .header h1 {
                font-size: 1.75rem;
            }

            .metadata-grid {
                grid-template-columns: 1fr;
            }

            .governance-grid {
                grid-template-columns: 1fr;
            }
        }
        """

    def generate_javascript(self) -> str:
        """Generate JavaScript for interactive functionality."""
        return """
        // Toggle collapsible sections
        function toggleCollapsible(element) {
            const collapsible = element.closest('.collapsible');
            const wasExpanded = collapsible.classList.contains('expanded');

            // Collapse all siblings at the same level
            const parent = collapsible.parentElement;
            const siblings = parent.querySelectorAll(':scope > .collapsible');
            siblings.forEach(sibling => {
                if (sibling !== collapsible) {
                    sibling.classList.remove('expanded');
                }
            });

            // Toggle current
            collapsible.classList.toggle('expanded');

            // If we're expanding, scroll into view after animation
            if (!wasExpanded) {
                setTimeout(() => {
                    collapsible.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                }, 100);
            }
        }

        // Expand all movements
        function expandAll() {
            document.querySelectorAll('.collapsible').forEach(el => {
                el.classList.add('expanded');
            });
        }

        // Collapse all movements
        function collapseAll() {
            document.querySelectorAll('.collapsible').forEach(el => {
                el.classList.remove('expanded');
            });
        }

        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                collapseAll();
            }
        });

        // Auto-expand first movement on load
        window.addEventListener('load', () => {
            const firstMovement = document.querySelector('.movement');
            if (firstMovement) {
                setTimeout(() => {
                    firstMovement.classList.add('expanded');
                }, 500);
            }
        });
        """

    def format_user_story(self, user_story: Dict[str, str]) -> str:
        """Format a user story as HTML."""
        if not user_story:
            return ""

        persona = user_story.get('persona', 'User')
        goal = user_story.get('goal', 'achieve a goal')
        benefit = user_story.get('benefit', 'receive value')

        return f"""
        <div class="user-story">
            <div class="user-story-line">
                <span class="user-story-label">As a</span> {persona}
            </div>
            <div class="user-story-line">
                <span class="user-story-label">I want to</span> {goal}
            </div>
            <div class="user-story-line">
                <span class="user-story-label">So that</span> {benefit}
            </div>
        </div>
        """

    def format_acceptance_criteria(self, criteria: List[Dict[str, Any]]) -> str:
        """Format acceptance criteria as HTML."""
        if not criteria:
            return ""

        html = '<div class="criteria">'

        for idx, scenario in enumerate(criteria, 1):
            if len(criteria) > 1:
                html += f'<div class="criteria-scenario"><strong>Scenario {idx}:</strong></div>'

            for section in ['given', 'when', 'then', 'and']:
                items = scenario.get(section, [])
                if items:
                    html += f'<div class="criteria-label">{section.title()}:</div>'
                    html += '<ul class="criteria-items">'
                    for item in items:
                        html += f'<li>{item}</li>'
                    html += '</ul>'

        html += '</div>'
        return html

    def generate_beat_html(self, beat: Dict[str, Any]) -> str:
        """Generate HTML for a single beat."""
        beat_number = beat.get('beat', '?')
        beat_name = beat.get('name', 'Unnamed Beat')
        event = beat.get('event', 'N/A')
        description = beat.get('description', '')

        html = f"""
        <div class="collapsible beat">
            <div class="collapsible-header" onclick="toggleCollapsible(this)">
                <div class="collapsible-title">
                    <span class="collapsible-icon">▶</span>
                    <span class="beat-number">{beat_number}</span>
                    <span class="beat-name">{beat_name}</span>
                    <span class="beat-event">{event}</span>
                </div>
            </div>
            <div class="collapsible-content">
        """

        if description:
            html += f'<div class="beat-description">{description}</div>'

        # Handler information
        handler = beat.get('handler')
        if handler:
            html += '<div class="detail-section">'
            html += '<div class="detail-heading">Handler</div>'
            html += '<div class="detail-content">'

            if isinstance(handler, str):
                html += f'<code>{handler}</code>'
            else:
                handler_name = handler.get('name', 'N/A')
                source_path = handler.get('sourcePath', 'N/A')
                capabilities = handler.get('handlerCapabilities', [])

                html += f'<div><strong>Name:</strong> <code>{handler_name}</code></div>'
                html += f'<div><strong>Source:</strong> <code>{source_path}</code></div>'

                if capabilities:
                    caps_html = ', '.join(f'<code>{cap}</code>' for cap in capabilities)
                    html += f'<div><strong>Capabilities:</strong> {caps_html}</div>'

            html += '</div></div>'

        # User story
        user_story = beat.get('userStory')
        if user_story:
            html += self.format_user_story(user_story)

        # Acceptance criteria
        acceptance_criteria = beat.get('acceptanceCriteria', [])
        if acceptance_criteria:
            html += self.format_acceptance_criteria(acceptance_criteria)

        # Test information
        test_file = beat.get('testFile')
        if test_file:
            html += '<div class="detail-section">'
            html += '<div class="detail-heading">Tests</div>'
            html += f'<div class="detail-content"><code>{test_file}</code></div>'
            html += '</div>'

        html += '</div></div>'
        return html

    def generate_movement_html(self, movement: Dict[str, Any]) -> str:
        """Generate HTML for a single movement."""
        movement_number = movement.get('number', '?')
        movement_name = movement.get('name', 'Unnamed Movement')
        description = movement.get('description', '')
        beats = movement.get('beats', [])

        html = f"""
        <div class="collapsible movement">
            <div class="collapsible-header" onclick="toggleCollapsible(this)">
                <div class="collapsible-title">
                    <span class="collapsible-icon">▶</span>
                    <span class="movement-number">{movement_number}</span>
                    <span class="movement-name">{movement_name}</span>
                    <span class="movement-badge">{len(beats)} beats</span>
                </div>
            </div>
            <div class="collapsible-content">
        """

        if description:
            html += f'<div class="movement-description">{description}</div>'

        # Movement metadata
        html += '<div class="movement-meta">'
        html += f'<div class="meta-item"><span class="meta-label">ID:</span> <span class="meta-value"><code>{movement.get("id", "N/A")}</code></span></div>'
        html += f'<div class="meta-item"><span class="meta-label">Tempo:</span> <span class="meta-value">{movement.get("tempo", "Inherited")} BPM</span></div>'
        html += f'<div class="meta-item"><span class="meta-label">Error Handling:</span> <span class="meta-value"><code>{movement.get("errorHandling", "N/A")}</code></span></div>'
        html += f'<div class="meta-item"><span class="meta-label">Status:</span> <span class="meta-value"><code>{movement.get("status", "N/A")}</code></span></div>'
        html += '</div>'

        # Movement user story
        user_story = movement.get('userStory')
        if user_story:
            html += self.format_user_story(user_story)

        # Beats
        if beats:
            html += '<div class="beats-container">'
            for beat in beats:
                html += self.generate_beat_html(beat)
            html += '</div>'

        html += '</div></div>'
        return html

    def generate_html(self) -> str:
        """Generate the complete HTML presentation."""
        data = self.sequence_data

        # Extract data
        sequence_name = data.get('name', 'Unnamed Sequence')
        title = data.get('title', 'No Title')
        description = data.get('description', 'No description provided.')
        purpose = data.get('purpose', 'No purpose statement.')
        trigger = data.get('trigger', 'No trigger defined.')

        metadata = data.get('metadata', {})
        governance = data.get('governance', {})
        events = data.get('events', [])
        movements = data.get('movements', [])
        user_story = data.get('userStory', {})

        # Build HTML
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{sequence_name} - Interactive Presentation</title>
    <style>
        {self.generate_css()}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>{sequence_name}</h1>
            <div class="subtitle">{title}</div>
            <div class="description">{description}</div>
        </div>

        <!-- Metadata -->
        <div class="metadata-grid">
            <div class="metadata-card">
                <div class="metadata-label">Sequence ID</div>
                <div class="metadata-value"><code>{data.get('id', 'N/A')}</code></div>
            </div>
            <div class="metadata-card">
                <div class="metadata-label">Domain</div>
                <div class="metadata-value"><code>{data.get('domainId', 'N/A')}</code></div>
            </div>
            <div class="metadata-card">
                <div class="metadata-label">Key</div>
                <div class="metadata-value">{data.get('key', 'N/A')}</div>
            </div>
            <div class="metadata-card">
                <div class="metadata-label">Tempo</div>
                <div class="metadata-value">{data.get('tempo', 'N/A')} BPM</div>
            </div>
            <div class="metadata-card">
                <div class="metadata-label">Total Beats</div>
                <div class="metadata-value">{data.get('beats', 0)}</div>
            </div>
            <div class="metadata-card">
                <div class="metadata-label">Status</div>
                <div class="metadata-value"><code>{data.get('status', 'N/A')}</code></div>
            </div>
        </div>
"""

        # User Story
        if user_story:
            html += '<h2 style="color: var(--primary-color); margin: 2rem 0 1rem 0;">👤 User Story</h2>'
            html += self.format_user_story(user_story)

        # Purpose and Trigger
        html += f"""
        <h2 style="color: var(--primary-color); margin: 2rem 0 1rem 0;">🎯 Purpose & Context</h2>
        <div class="detail-section">
            <div class="detail-heading">Purpose</div>
            <div class="detail-content">{purpose}</div>
        </div>
        <div class="detail-section">
            <div class="detail-heading">Trigger</div>
            <div class="detail-content">{trigger}</div>
        </div>
        """

        # Governance
        if governance:
            policies = governance.get('policies', [])
            metrics = governance.get('metrics', [])

            html += '<h2 style="color: var(--primary-color); margin: 2rem 0 1rem 0;">🛡️ Governance</h2>'
            html += '<div class="governance-grid">'

            if policies:
                html += '<div class="governance-section">'
                html += '<h4>Policies</h4>'
                html += '<div class="tag-list">'
                for policy in policies:
                    html += f'<span class="tag">{policy}</span>'
                html += '</div></div>'

            if metrics:
                html += '<div class="governance-section">'
                html += '<h4>Metrics</h4>'
                html += '<div class="tag-list">'
                for metric in metrics:
                    html += f'<span class="tag">{metric}</span>'
                html += '</div></div>'

            html += '</div>'

        # Events
        if events:
            html += '<h2 style="color: var(--primary-color); margin: 2rem 0 1rem 0;">📡 Event Flow</h2>'
            html += '<div class="events-list">'
            for event in events:
                html += f'<div class="event-item">{event}</div>'
            html += '</div>'

        # Movements
        if movements:
            html += f"""
            <h2 style="color: var(--primary-color); margin: 2rem 0 1rem 0;">🎼 Movements ({len(movements)})</h2>
            <div style="margin-bottom: 1rem;">
                <button onclick="expandAll()" style="background: var(--primary-color); color: white; border: none; padding: 0.5rem 1rem; border-radius: 4px; cursor: pointer; margin-right: 0.5rem;">Expand All</button>
                <button onclick="collapseAll()" style="background: var(--card-bg); color: var(--text-primary); border: 1px solid var(--border-color); padding: 0.5rem 1rem; border-radius: 4px; cursor: pointer;">Collapse All</button>
            </div>
            """

            for movement in movements:
                html += self.generate_movement_html(movement)

        # Footer
        html += f"""
        <div class="footer">
            <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p style="margin-top: 0.5rem; font-size: 0.875rem;">Press <code>ESC</code> to collapse all sections</p>
        </div>
    </div>

    <script>
        {self.generate_javascript()}
    </script>
</body>
</html>
"""

        return html

    def save_presentation(self, content: str) -> Path:
        """
        Save the presentation to an HTML file.

        Args:
            content: HTML content to save

        Returns:
            Path to the saved presentation file
        """
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Generate output filename
        sequence_id = self.sequence_data.get('id', 'unknown')
        output_file = self.output_dir / f"{sequence_id}.presentation.html"

        # Write presentation
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)

        return output_file

    def run(self) -> Path:
        """
        Run the presentation generation process.

        Returns:
            Path to the generated presentation file
        """
        print(f"Loading sequence: {self.sequence_path}")
        self.load_sequence()

        print(f"Generating presentation for: {self.sequence_data.get('name', 'Unnamed')}")
        presentation_content = self.generate_html()

        print(f"Saving presentation...")
        output_path = self.save_presentation(presentation_content)

        print(f"Presentation generated successfully: {output_path}")
        return output_path


def main():
    """Main entry point for command-line usage."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate interactive HTML presentations from musical sequence JSON files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate presentation for a single sequence
  python scripts/generate_sequence_presentation.py sequences/hybrid-resume-generation.sequence.json

  # Generate presentations for all sequences
  python scripts/generate_sequence_presentation.py sequences/*.sequence.json

  # Specify custom output directory
  python scripts/generate_sequence_presentation.py sequences/hybrid-resume-generation.sequence.json --output-dir presentations
        """,
    )

    parser.add_argument(
        "sequence_files",
        nargs="+",
        help="Path(s) to sequence JSON file(s)",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        help="Output directory for presentations (default: presentations)",
    )

    args = parser.parse_args()

    # Process each sequence file
    output_dir = Path(args.output_dir) if args.output_dir else None

    for sequence_file in args.sequence_files:
        sequence_path = Path(sequence_file)

        if not sequence_path.exists():
            print(f"Error: File not found: {sequence_path}")
            continue

        try:
            generator = SequencePresentationGenerator(sequence_path, output_dir)
            output_path = generator.run()
            print()
        except Exception as e:
            print(f"Error processing {sequence_path}: {e}")
            import traceback
            traceback.print_exc()
            continue


if __name__ == "__main__":
    main()
