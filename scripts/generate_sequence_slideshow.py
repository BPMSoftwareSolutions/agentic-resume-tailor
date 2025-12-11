"""
Generate HTML Slideshow Presentations for Musical Sequences

This script generates beautiful, reveal.js-style HTML slideshows from musical sequence JSON files.
Each slideshow walks through the sequence with dedicated slides for overview, user stories,
movements, beats, acceptance criteria, and handlers.

Usage:
    python scripts/generate_sequence_slideshow.py sequences/hybrid-resume-generation.sequence.json
    python scripts/generate_sequence_slideshow.py sequences/*.sequence.json --output-dir slideshows
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime
import html


class SequenceSlideshowGenerator:
    """Generate HTML slideshow presentations from musical sequence definitions."""

    def __init__(self, sequence_path: Path, output_dir: Optional[Path] = None):
        """
        Initialize the slideshow generator.

        Args:
            sequence_path: Path to the sequence JSON file
            output_dir: Optional output directory for the slideshow
        """
        self.sequence_path = sequence_path
        self.output_dir = output_dir or sequence_path.parent.parent / "slideshows"
        self.sequence_data: Dict[str, Any] = {}

    def load_sequence(self) -> None:
        """Load the sequence JSON file."""
        with open(self.sequence_path, "r", encoding="utf-8") as f:
            self.sequence_data = json.load(f)

    def escape_html(self, text: str) -> str:
        """Escape HTML in text while preserving line breaks."""
        return html.escape(text).replace('\n', '<br>')

    def generate_css(self) -> str:
        """Generate custom CSS styles for the slideshow."""
        return """
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

        :root {
            /* GitHub-inspired colors */
            --gh-primary: #2f81f7;
            --gh-success: #3fb950;
            --gh-warning: #d29922;
            --gh-danger: #f85149;
            --gh-purple: #a371f7;
            --gh-pink: #f778ba;

            /* GitHub dark theme */
            --gh-canvas-default: #0d1117;
            --gh-canvas-subtle: #161b22;
            --gh-canvas-inset: #010409;
            --gh-border-default: #30363d;
            --gh-border-muted: #21262d;

            /* Text colors */
            --gh-fg-default: #e6edf3;
            --gh-fg-muted: #7d8590;
            --gh-fg-subtle: #6e7681;

            /* Semantic colors */
            --primary: var(--gh-primary);
            --secondary: var(--gh-purple);
            --accent: var(--gh-warning);
            --success: var(--gh-success);
            --danger: var(--gh-danger);
            --dark: var(--gh-canvas-default);
            --dark-alt: var(--gh-canvas-subtle);
            --light: #f6f8fa;
            --text: var(--gh-fg-default);
            --text-dim: var(--gh-fg-muted);
            --border: var(--gh-border-default);
        }

        .reveal {
            font-family: 'Inter', sans-serif;
            font-size: 32px;
            font-weight: 400;
            color: var(--text);
        }

        .reveal .slides {
            text-align: left;
        }

        .reveal h1, .reveal h2, .reveal h3, .reveal h4 {
            font-weight: 700;
            text-transform: none;
            margin-bottom: 0.5em;
        }

        .reveal h1 {
            font-size: 2.5em;
            font-weight: 900;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.3em;
        }

        .reveal h2 {
            font-size: 2em;
            color: var(--primary);
            border-bottom: 3px solid var(--primary);
            padding-bottom: 0.2em;
        }

        .reveal h3 {
            font-size: 1.5em;
            color: var(--secondary);
        }

        .reveal h4 {
            font-size: 1.2em;
            color: var(--accent);
        }

        /* Custom slide backgrounds */
        .reveal .slide-background {
            background: var(--dark);
        }

        .reveal .title-slide {
            text-align: center;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100%;
        }

        .reveal .title-slide h1 {
            font-size: 3.5em;
            margin-bottom: 0.2em;
        }

        .reveal .subtitle {
            font-size: 1.3em;
            color: var(--text-dim);
            margin-bottom: 1em;
        }

        /* Metadata grid */
        .metadata-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1.5rem;
            margin: 2rem 0;
        }

        .metadata-card {
            background: var(--gh-canvas-subtle);
            padding: 1.5rem;
            border-radius: 6px;
            border: 1px solid var(--gh-border-default);
            text-align: center;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
        }

        .metadata-label {
            font-size: 0.7em;
            color: var(--text-dim);
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 0.5rem;
        }

        .metadata-value {
            font-size: 1.1em;
            font-weight: 700;
            color: var(--text);
        }

        /* Content sections - GitHub card style */
        .content-box {
            background: var(--gh-canvas-subtle);
            padding: 1.5rem;
            border-radius: 6px;
            margin: 1.5rem 0;
            border: 1px solid var(--gh-border-default);
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
        }

        .content-box.accent {
            border-left: 3px solid var(--gh-warning);
        }

        .content-box.success {
            border-left: 3px solid var(--gh-success);
        }

        .content-box.secondary {
            border-left: 3px solid var(--gh-purple);
        }

        .content-box.primary {
            border-left: 3px solid var(--gh-primary);
        }

        /* User story */
        .user-story {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.15), rgba(139, 92, 246, 0.15));
            padding: 2rem;
            border-radius: 12px;
            border-left: 4px solid var(--primary);
            font-size: 0.9em;
        }

        .user-story-line {
            margin: 1rem 0;
            line-height: 1.6;
        }

        .user-story-label {
            font-weight: 700;
            color: var(--primary);
            font-size: 1.1em;
        }

        /* Lists */
        .reveal ul, .reveal ol {
            margin: 1.5rem 0;
            line-height: 1.8;
        }

        .reveal ul li, .reveal ol li {
            margin: 0.8rem 0;
        }

        .reveal ul.fancy li {
            list-style: none;
            position: relative;
            padding-left: 2rem;
        }

        .reveal ul.fancy li::before {
            content: "→";
            position: absolute;
            left: 0;
            color: var(--primary);
            font-weight: bold;
            font-size: 1.2em;
        }

        /* Movement list */
        .movement-list {
            display: grid;
            gap: 1rem;
            margin: 2rem 0;
        }

        .movement-item {
            background: var(--gh-canvas-subtle);
            padding: 1.5rem;
            border-radius: 6px;
            border: 1px solid var(--gh-border-default);
            border-left: 3px solid var(--gh-primary);
            display: grid;
            grid-template-columns: 80px 1fr auto;
            align-items: center;
            gap: 1.5rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
            transition: all 0.2s ease;
        }

        .movement-item:hover {
            border-left-width: 4px;
            box-shadow: 0 2px 8px rgba(47, 129, 247, 0.2);
        }

        .movement-number {
            font-size: 2.5em;
            font-weight: 900;
            color: var(--primary);
            text-align: center;
        }

        .movement-info h4 {
            margin: 0 0 0.3rem 0;
            color: var(--text);
        }

        .movement-desc {
            font-size: 0.7em;
            color: var(--text-dim);
        }

        .movement-badge {
            background: var(--primary);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.7em;
            font-weight: 600;
            white-space: nowrap;
        }

        /* Beat list */
        .beat-list {
            display: grid;
            gap: 1rem;
            margin: 2rem 0;
        }

        .beat-item {
            background: var(--gh-canvas-subtle);
            padding: 1.2rem;
            border-radius: 6px;
            border: 1px solid var(--gh-border-default);
            border-left: 3px solid var(--gh-warning);
            display: grid;
            grid-template-columns: 60px 1fr;
            align-items: center;
            gap: 1rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
            transition: all 0.2s ease;
        }

        .beat-item:hover {
            border-left-width: 4px;
            box-shadow: 0 2px 8px rgba(210, 153, 34, 0.2);
        }

        .beat-number {
            font-size: 1.8em;
            font-weight: 900;
            color: var(--accent);
            text-align: center;
        }

        .beat-info h4 {
            margin: 0 0 0.3rem 0;
            color: var(--text);
            font-size: 1em;
        }

        .beat-event {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.6em;
            color: var(--accent);
            background: rgba(245, 158, 11, 0.15);
            padding: 0.3rem 0.6rem;
            border-radius: 4px;
            display: inline-block;
            margin-top: 0.3rem;
        }

        /* Code and inline code - GitHub style */
        .reveal code {
            font-family: 'JetBrains Mono', 'Consolas', 'Monaco', monospace;
            background: var(--gh-canvas-inset);
            padding: 0.2em 0.4em;
            border-radius: 6px;
            color: var(--gh-fg-default);
            font-size: 0.85em;
            border: 1px solid var(--gh-border-default);
            font-weight: 500;
        }

        .reveal pre {
            margin: 1.5rem 0;
            box-shadow: none;
        }

        .reveal pre code {
            background: var(--gh-canvas-inset);
            padding: 1rem;
            border-radius: 6px;
            display: block;
            border: 1px solid var(--gh-border-default);
            font-size: 0.75em;
            line-height: 1.6;
            overflow-x: auto;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
        }

        /* Syntax highlighting for code */
        .reveal code .keyword { color: #ff7b72; }
        .reveal code .string { color: #a5d6ff; }
        .reveal code .comment { color: #8b949e; font-style: italic; }
        .reveal code .function { color: #d2a8ff; }
        .reveal code .number { color: #79c0ff; }

        /* Acceptance criteria - GitHub style */
        .criteria-section {
            background: var(--gh-canvas-subtle);
            padding: 0;
            border-radius: 6px;
            border: 1px solid var(--gh-border-default);
            margin: 1.5rem 0;
            overflow: hidden;
        }

        .criteria-label {
            background: var(--gh-canvas-inset);
            padding: 0.75rem 1.25rem;
            margin: 0;
            font-weight: 600;
            color: var(--gh-success);
            font-size: 0.75em;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            border-bottom: 1px solid var(--gh-border-default);
        }

        .criteria-list {
            list-style: none;
            padding: 0;
            margin: 0;
        }

        .criteria-list li {
            padding: 0.75rem 1.25rem 0.75rem 3rem;
            position: relative;
            font-size: 0.75em;
            color: var(--gh-fg-default);
            border-bottom: 1px solid var(--gh-border-muted);
            line-height: 1.6;
        }

        .criteria-list li:last-child {
            border-bottom: none;
        }

        .criteria-list li::before {
            content: "✓";
            position: absolute;
            left: 1.25rem;
            color: var(--gh-success);
            font-weight: bold;
            font-size: 1.3em;
        }

        /* Scenario headers */
        .criteria-scenario {
            background: var(--gh-canvas-inset);
            padding: 0.75rem 1.25rem;
            margin: 0;
            font-weight: 600;
            color: var(--gh-fg-default);
            font-size: 0.8em;
            border-top: 2px solid var(--gh-border-default);
            border-bottom: 1px solid var(--gh-border-default);
        }

        /* Handler info */
        .handler-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1.5rem;
            margin: 2rem 0;
        }

        .handler-card {
            background: var(--gh-canvas-subtle);
            padding: 1.5rem;
            border-radius: 6px;
            border: 1px solid var(--gh-border-default);
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
        }

        .handler-card h4 {
            margin-top: 0;
            font-size: 0.8em;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--text-dim);
            margin-bottom: 1rem;
        }

        .handler-card .value {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.7em;
            color: var(--text);
            word-break: break-all;
        }

        /* Tags - GitHub badge style */
        .tag-list {
            display: flex;
            flex-wrap: wrap;
            gap: 0.8rem;
            margin: 1.5rem 0;
        }

        .tag {
            background: var(--gh-canvas-inset);
            color: var(--gh-fg-default);
            padding: 0.3rem 0.8rem;
            border-radius: 2em;
            font-size: 0.7em;
            border: 1px solid var(--gh-border-default);
            font-weight: 500;
            font-family: 'JetBrains Mono', monospace;
        }

        .tag.policy {
            border-color: var(--gh-primary);
            color: var(--gh-primary);
        }

        .tag.metric {
            border-color: var(--gh-success);
            color: var(--gh-success);
        }

        /* GitHub-style alerts/callouts */
        .gh-alert {
            padding: 1rem 1rem 1rem 3rem;
            margin: 1.5rem 0;
            border-left: 4px solid;
            border-radius: 6px;
            position: relative;
            font-size: 0.85em;
        }

        .gh-alert::before {
            position: absolute;
            left: 1rem;
            font-weight: bold;
            font-size: 1.2em;
        }

        .gh-alert.note {
            background: rgba(47, 129, 247, 0.1);
            border-color: var(--gh-primary);
            color: var(--gh-fg-default);
        }

        .gh-alert.note::before {
            content: "ℹ️";
        }

        .gh-alert.tip {
            background: rgba(63, 185, 80, 0.1);
            border-color: var(--gh-success);
        }

        .gh-alert.tip::before {
            content: "💡";
        }

        .gh-alert.warning {
            background: rgba(210, 153, 34, 0.1);
            border-color: var(--gh-warning);
        }

        .gh-alert.warning::before {
            content: "⚠️";
        }

        /* Emphasis boxes */
        .emphasis-box {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(139, 92, 246, 0.2));
            padding: 2rem;
            border-radius: 12px;
            border: 2px solid var(--primary);
            margin: 2rem 0;
            text-align: center;
        }

        .emphasis-box h3 {
            margin: 0;
            color: var(--text);
        }

        /* Progress indicator */
        .slide-number {
            font-family: 'JetBrains Mono', monospace;
        }

        /* Two-column layout */
        .two-column {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
            margin: 2rem 0;
        }

        /* Section divider */
        .section-divider {
            text-align: center;
            padding: 4rem 2rem;
        }

        .section-divider h2 {
            font-size: 3em;
            border: none;
            margin-bottom: 1rem;
        }

        .section-divider .subtitle {
            font-size: 1.2em;
            color: var(--text-dim);
        }

        /* Fragment animations */
        .reveal .fragment.highlight-current-blue.current-fragment {
            color: var(--primary);
        }
        """

    def generate_title_slide(self) -> str:
        """Generate the title slide."""
        data = self.sequence_data
        name = data.get('name', 'Unnamed Sequence')
        title = data.get('title', '')
        description = data.get('description', '')

        metadata = data.get('metadata', {})
        version = metadata.get('version', 'N/A')
        author = metadata.get('author', 'Unknown')

        return f"""
        <section class="title-slide">
            <h1>{name}</h1>
            <p class="subtitle">{title}</p>
            <p style="font-size: 0.8em; color: var(--text-dim); max-width: 800px;">
                {description}
            </p>
            <div style="margin-top: 2rem; font-size: 0.6em; color: var(--text-dim);">
                <p>Version {version} • {author}</p>
            </div>
        </section>
        """

    def generate_overview_slide(self) -> str:
        """Generate overview slide with purpose and trigger."""
        data = self.sequence_data
        purpose = data.get('purpose', 'No purpose defined')
        trigger = data.get('trigger', 'No trigger defined')

        # Metadata
        sequence_id = data.get('id', 'N/A')
        domain = data.get('domainId', 'N/A')
        key = data.get('key', 'N/A')
        tempo = data.get('tempo', 'N/A')
        total_beats = data.get('beats', 0)
        status = data.get('status', 'N/A')

        return f"""
        <section>
            <h2>📋 Overview</h2>

            <div class="metadata-grid">
                <div class="metadata-card">
                    <div class="metadata-label">Musical Key</div>
                    <div class="metadata-value">{key}</div>
                </div>
                <div class="metadata-card">
                    <div class="metadata-label">Tempo</div>
                    <div class="metadata-value">{tempo} BPM</div>
                </div>
                <div class="metadata-card">
                    <div class="metadata-label">Total Beats</div>
                    <div class="metadata-value">{total_beats}</div>
                </div>
            </div>

            <div class="content-box">
                <h3>🎯 Purpose</h3>
                <p>{purpose}</p>
            </div>

            <div class="content-box accent">
                <h3>⚡ Trigger</h3>
                <p>{trigger}</p>
            </div>
        </section>
        """

    def generate_user_story_slide(self) -> str:
        """Generate user story slide."""
        data = self.sequence_data
        user_story = data.get('userStory', {})

        if not user_story:
            return ""

        persona = user_story.get('persona', 'User')
        goal = user_story.get('goal', 'achieve a goal')
        benefit = user_story.get('benefit', 'receive value')

        business_value = data.get('businessValue', '')

        business_section = ""
        if business_value:
            business_section = f"""
            <div class="content-box success" style="margin-top: 2rem;">
                <h3>💼 Business Value</h3>
                <p>{business_value}</p>
            </div>
            """

        return f"""
        <section>
            <h2>👤 User Story</h2>

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

            {business_section}
        </section>
        """

    def generate_governance_slide(self) -> str:
        """Generate governance slide."""
        data = self.sequence_data
        governance = data.get('governance', {})

        if not governance:
            return ""

        policies = governance.get('policies', [])
        metrics = governance.get('metrics', [])

        policies_html = ""
        if policies:
            tags_html = ''.join(f'<span class="tag policy">{p}</span>' for p in policies)
            policies_html = f"""
            <div class="content-box primary">
                <h3>🛡️ Policies</h3>
                <div class="tag-list">
                    {tags_html}
                </div>
            </div>
            """

        metrics_html = ""
        if metrics:
            tags_html = ''.join(f'<span class="tag metric">{m}</span>' for m in metrics)
            metrics_html = f"""
            <div class="content-box success">
                <h3>📊 Metrics</h3>
                <div class="tag-list">
                    {tags_html}
                </div>
            </div>
            """

        if not policies_html and not metrics_html:
            return ""

        return f"""
        <section>
            <h2>🛡️ Governance</h2>
            {policies_html}
            {metrics_html}
        </section>
        """

    def generate_movements_summary_slide(self) -> str:
        """Generate movements summary slide."""
        data = self.sequence_data
        movements = data.get('movements', [])

        if not movements:
            return ""

        movement_items = []
        for movement in movements:
            num = movement.get('number', '?')
            name = movement.get('name', 'Unnamed')
            description = movement.get('description', '')
            beats_count = len(movement.get('beats', []))

            desc_html = ""
            if description:
                desc_html = f'<div class="movement-desc">{description}</div>'

            movement_items.append(f"""
            <div class="movement-item">
                <div class="movement-number">{num}</div>
                <div class="movement-info">
                    <h4>{name}</h4>
                    {desc_html}
                </div>
                <div class="movement-badge">{beats_count} beats</div>
            </div>
            """)

        return f"""
        <section>
            <h2>🎼 Movements ({len(movements)})</h2>
            <div class="movement-list">
                {''.join(movement_items)}
            </div>
        </section>
        """

    def generate_movement_divider_slide(self, movement: Dict[str, Any]) -> str:
        """Generate a divider slide for a movement."""
        num = movement.get('number', '?')
        name = movement.get('name', 'Unnamed')
        description = movement.get('description', '')

        return f"""
        <section class="section-divider">
            <h2>Movement {num}</h2>
            <h3>{name}</h3>
            <p class="subtitle">{description}</p>
        </section>
        """

    def generate_movement_beats_slide(self, movement: Dict[str, Any]) -> str:
        """Generate beats summary slide for a movement."""
        beats = movement.get('beats', [])
        movement_name = movement.get('name', 'Unnamed')

        if not beats:
            return ""

        beat_items = []
        for beat in beats:
            beat_num = beat.get('beat', '?')
            beat_name = beat.get('name', 'Unnamed')
            event = beat.get('event', 'N/A')

            beat_items.append(f"""
            <div class="beat-item">
                <div class="beat-number">{beat_num}</div>
                <div class="beat-info">
                    <h4>{beat_name}</h4>
                    <span class="beat-event">{event}</span>
                </div>
            </div>
            """)

        return f"""
        <section>
            <h2>Beats in {movement_name}</h2>
            <div class="beat-list">
                {''.join(beat_items)}
            </div>
        </section>
        """

    def generate_beat_user_story_slide(self, beat: Dict[str, Any], movement: Dict[str, Any]) -> str:
        """Generate user story slide for a beat."""
        beat_num = beat.get('beat', '?')
        beat_name = beat.get('name', 'Unnamed')
        description = beat.get('description', '')
        user_story = beat.get('userStory', {})

        if not user_story:
            return ""

        persona = user_story.get('persona', 'User')
        goal = user_story.get('goal', 'achieve a goal')
        benefit = user_story.get('benefit', 'receive value')

        desc_html = ""
        if description:
            desc_html = f"""
            <div class="content-box" style="margin-bottom: 2rem;">
                <p>{description}</p>
            </div>
            """

        return f"""
        <section>
            <h2>Beat {beat_num}: {beat_name}</h2>
            <h3 style="color: var(--text-dim); font-size: 1em; margin-top: -1rem;">User Story</h3>

            {desc_html}

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
        </section>
        """

    def generate_beat_acceptance_criteria_slide(self, beat: Dict[str, Any]) -> str:
        """Generate acceptance criteria slide(s) for a beat, splitting if needed."""
        beat_num = beat.get('beat', '?')
        beat_name = beat.get('name', 'Unnamed')
        criteria = beat.get('acceptanceCriteria', [])

        if not criteria:
            return ""

        # Build all scenarios first
        all_scenarios = []
        for idx, scenario in enumerate(criteria, 1):
            # Scenario title as a header (only if multiple scenarios)
            scenario_header = ""
            if len(criteria) > 1:
                scenario_header = f'<div class="criteria-scenario">Scenario {idx}</div>'

            # Build sections (given, when, then, and)
            sections_html = []
            for section in ['given', 'when', 'then', 'and']:
                items = scenario.get(section, [])
                if items:
                    items_html = ''.join(f'<li>{item}</li>' for item in items)
                    sections_html.append(f"""
                        <div class="criteria-label">{section.title()}</div>
                        <ul class="criteria-list">
                            {items_html}
                        </ul>
                    """)

            # Calculate item count for this scenario
            total_items = sum(len(scenario.get(section, [])) for section in ['given', 'when', 'then', 'and'])

            all_scenarios.append({
                'html': f"""
                <div class="criteria-section">
                    {scenario_header}
                    {''.join(sections_html)}
                </div>
                """,
                'item_count': total_items,
                'scenario_num': idx
            })

        # Split scenarios into slides (max ~8-10 items per slide)
        MAX_ITEMS_PER_SLIDE = 8
        slides = []
        current_slide_scenarios = []
        current_item_count = 0

        for scenario in all_scenarios:
            # If adding this scenario would exceed the limit, start a new slide
            if current_item_count > 0 and (current_item_count + scenario['item_count']) > MAX_ITEMS_PER_SLIDE:
                slides.append(current_slide_scenarios)
                current_slide_scenarios = []
                current_item_count = 0

            current_slide_scenarios.append(scenario)
            current_item_count += scenario['item_count']

        # Add the last slide
        if current_slide_scenarios:
            slides.append(current_slide_scenarios)

        # Generate HTML for each slide
        slide_html = []
        for page_num, slide_scenarios in enumerate(slides, 1):
            page_indicator = f" ({page_num}/{len(slides)})" if len(slides) > 1 else ""
            scenarios_html = ''.join(s['html'] for s in slide_scenarios)

            slide_html.append(f"""
        <section>
            <h2>Beat {beat_num}: {beat_name}</h2>
            <h3 style="color: var(--text-dim); font-size: 1em; margin-top: -1rem;">Acceptance Criteria{page_indicator}</h3>

            {scenarios_html}
        </section>
            """)

        return '\n'.join(slide_html)

    def generate_beat_handler_slide(self, beat: Dict[str, Any]) -> str:
        """Generate handler summary slide for a beat."""
        beat_num = beat.get('beat', '?')
        beat_name = beat.get('name', 'Unnamed')
        handler = beat.get('handler')
        event = beat.get('event', 'N/A')
        test_file = beat.get('testFile', 'N/A')

        # Parse handler info
        handler_name = 'N/A'
        source_path = 'N/A'
        capabilities = []

        if handler:
            if isinstance(handler, str):
                handler_name = handler
            else:
                handler_name = handler.get('name', 'N/A')
                source_path = handler.get('sourcePath', 'N/A')
                capabilities = handler.get('handlerCapabilities', [])

        caps_html = ""
        if capabilities:
            tags_html = ''.join(f'<span class="tag">{cap}</span>' for cap in capabilities)
            caps_html = f"""
            <div style="margin-top: 1rem;">
                <div style="font-size: 0.7em; color: var(--text-dim); margin-bottom: 0.5rem;">CAPABILITIES</div>
                <div class="tag-list">
                    {tags_html}
                </div>
            </div>
            """

        return f"""
        <section>
            <h2>Beat {beat_num}: {beat_name}</h2>
            <h3 style="color: var(--text-dim); font-size: 1em; margin-top: -1rem;">Handler Summary</h3>

            <div class="handler-grid">
                <div class="handler-card">
                    <h4>Handler</h4>
                    <div class="value"><code>{handler_name}</code></div>
                </div>
                <div class="handler-card">
                    <h4>Event</h4>
                    <div class="value"><code>{event}</code></div>
                </div>
                <div class="handler-card">
                    <h4>Source Path</h4>
                    <div class="value"><code>{source_path}</code></div>
                </div>
                <div class="handler-card">
                    <h4>Test File</h4>
                    <div class="value"><code>{test_file}</code></div>
                </div>
            </div>

            {caps_html}
        </section>
        """

    def generate_end_slide(self) -> str:
        """Generate the end slide."""
        data = self.sequence_data
        name = data.get('name', 'Unnamed Sequence')

        return f"""
        <section class="title-slide">
            <h1>Thank You!</h1>
            <p class="subtitle">{name}</p>
            <p style="font-size: 0.8em; color: var(--text-dim); margin-top: 2rem;">
                Press <code style="background: var(--dark-alt); padding: 0.3rem 0.6rem; border-radius: 4px;">ESC</code> for overview •
                Use arrow keys to navigate
            </p>
        </section>
        """

    def generate_html(self) -> str:
        """Generate the complete HTML slideshow."""
        data = self.sequence_data
        name = data.get('name', 'Unnamed Sequence')
        movements = data.get('movements', [])

        # Build all slides
        slides = []

        # 1. Title slide
        slides.append(self.generate_title_slide())

        # 2. Overview slide
        slides.append(self.generate_overview_slide())

        # 3. User story slide
        user_story_slide = self.generate_user_story_slide()
        if user_story_slide:
            slides.append(user_story_slide)

        # 4. Governance slide (if exists)
        governance_slide = self.generate_governance_slide()
        if governance_slide:
            slides.append(governance_slide)

        # 5. Movements summary
        slides.append(self.generate_movements_summary_slide())

        # 6. Per-movement slides
        for movement in movements:
            # Movement divider
            slides.append(self.generate_movement_divider_slide(movement))

            # Movement beats summary
            slides.append(self.generate_movement_beats_slide(movement))

            # Per-beat slides (3 slides per beat)
            beats = movement.get('beats', [])
            for beat in beats:
                # Beat user story
                user_story_slide = self.generate_beat_user_story_slide(beat, movement)
                if user_story_slide:
                    slides.append(user_story_slide)

                # Beat acceptance criteria
                criteria_slide = self.generate_beat_acceptance_criteria_slide(beat)
                if criteria_slide:
                    slides.append(criteria_slide)

                # Beat handler summary
                slides.append(self.generate_beat_handler_slide(beat))

        # 7. End slide
        slides.append(self.generate_end_slide())

        # Combine all slides
        slides_html = '\n'.join(slides)

        # Generate full HTML
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} - Slideshow</title>

    <!-- Reveal.js CSS -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/dist/reset.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/dist/reveal.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/dist/theme/black.css">

    <!-- Highlight.js for syntax highlighting - GitHub Dark theme -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">

    <style>
        {self.generate_css()}
    </style>
</head>
<body>
    <div class="reveal">
        <div class="slides">
            {slides_html}
        </div>
    </div>

    <!-- Reveal.js JavaScript -->
    <script src="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/dist/reveal.js"></script>

    <!-- Highlight.js for syntax highlighting -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/python.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/javascript.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/typescript.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/json.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/yaml.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/bash.min.js"></script>

    <script>
        // Initialize Highlight.js
        hljs.highlightAll();

        // Initialize Reveal.js
        Reveal.initialize({{
            hash: true,
            slideNumber: 'c/t',
            showSlideNumber: 'all',
            transition: 'slide',
            backgroundTransition: 'fade',
            center: false,
            width: 1280,
            height: 720,
            margin: 0.1,
            minScale: 0.2,
            maxScale: 2.0,
            controls: true,
            progress: true,
            history: true,
            keyboard: true,
            overview: true,
            touch: true,
            loop: false,
            rtl: false,
            navigationMode: 'default',
            shuffle: false,
            fragments: true,
            fragmentInURL: true,
            embedded: false,
            help: true,
            pause: true,
            showNotes: false,
            autoPlayMedia: null,
            preloadIframes: null,
            autoAnimate: true,
            autoAnimateMatcher: null,
            autoAnimateEasing: 'ease',
            autoAnimateDuration: 1.0,
            autoAnimateUnmatched: true,
            autoSlide: 0,
            mouseWheel: false,
            previewLinks: false,
            postMessage: true,
            postMessageEvents: false,
            focusBodyOnPageVisibilityChange: true,
            hideInactiveCursor: true,
            hideCursorTime: 5000
        }});
    </script>
</body>
</html>
"""
        return html

    def save_slideshow(self, content: str) -> Path:
        """
        Save the slideshow to an HTML file.

        Args:
            content: HTML content to save

        Returns:
            Path to the saved slideshow file
        """
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Generate output filename
        sequence_id = self.sequence_data.get('id', 'unknown')
        output_file = self.output_dir / f"{sequence_id}.slideshow.html"

        # Write slideshow
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)

        return output_file

    def run(self) -> Path:
        """
        Run the slideshow generation process.

        Returns:
            Path to the generated slideshow file
        """
        print(f"Loading sequence: {self.sequence_path}")
        self.load_sequence()

        print(f"Generating slideshow for: {self.sequence_data.get('name', 'Unnamed')}")
        slideshow_content = self.generate_html()

        print(f"Saving slideshow...")
        output_path = self.save_slideshow(slideshow_content)

        print(f"Slideshow generated successfully: {output_path}")
        return output_path


def main():
    """Main entry point for command-line usage."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate HTML slideshows from musical sequence JSON files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate slideshow for a single sequence
  python scripts/generate_sequence_slideshow.py sequences/hybrid-resume-generation.sequence.json

  # Generate slideshows for all sequences
  python scripts/generate_sequence_slideshow.py sequences/*.sequence.json

  # Specify custom output directory
  python scripts/generate_sequence_slideshow.py sequences/hybrid-resume-generation.sequence.json --output-dir slideshows
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
        help="Output directory for slideshows (default: slideshows)",
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
            generator = SequenceSlideshowGenerator(sequence_path, output_dir)
            output_path = generator.run()
            print()
        except Exception as e:
            print(f"Error processing {sequence_path}: {e}")
            import traceback
            traceback.print_exc()
            continue


if __name__ == "__main__":
    main()
