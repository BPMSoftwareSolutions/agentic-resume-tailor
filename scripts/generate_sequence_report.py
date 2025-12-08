"""
Generate Markdown Reports for Musical Sequences

This script generates comprehensive markdown documentation from musical sequence JSON files.
It includes detailed information about movements, beats, user stories, acceptance criteria,
governance policies, and metrics.

Usage:
    python scripts/generate_sequence_report.py sequences/hybrid-resume-generation.sequence.json
    python scripts/generate_sequence_report.py sequences/*.sequence.json --output-dir docs/sequences
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime


class SequenceReportGenerator:
    """Generate markdown reports from musical sequence definitions."""

    def __init__(self, sequence_path: Path, output_dir: Optional[Path] = None):
        """
        Initialize the report generator.

        Args:
            sequence_path: Path to the sequence JSON file
            output_dir: Optional output directory for the report
        """
        self.sequence_path = sequence_path
        self.output_dir = output_dir or sequence_path.parent.parent / "docs" / "sequences"
        self.sequence_data: Dict[str, Any] = {}

    def load_sequence(self) -> None:
        """Load the sequence JSON file."""
        with open(self.sequence_path, "r", encoding="utf-8") as f:
            self.sequence_data = json.load(f)

    def generate_header(self) -> str:
        """Generate the report header section."""
        data = self.sequence_data
        lines = [
            f"# {data.get('name', 'Unnamed Sequence')}",
            "",
            f"**{data.get('title', 'No Title')}**",
            "",
            data.get('description', 'No description provided.'),
            "",
            "---",
            "",
        ]
        return "\n".join(lines)

    def generate_metadata_section(self) -> str:
        """Generate the metadata section."""
        data = self.sequence_data
        metadata = data.get("metadata", {})

        lines = [
            "## 📋 Sequence Metadata",
            "",
            "| Field | Value |",
            "|-------|-------|",
            f"| **Sequence ID** | `{data.get('id', 'N/A')}` |",
            f"| **Domain** | `{data.get('domainId', 'N/A')}` |",
            f"| **Package** | `{data.get('packageName', 'N/A')}` |",
            f"| **Kind** | `{data.get('kind', 'N/A')}` |",
            f"| **Status** | `{data.get('status', 'N/A')}` |",
            f"| **Category** | `{data.get('category', 'N/A')}` |",
            f"| **Total Beats** | {data.get('beats', 0)} |",
            f"| **Version** | {metadata.get('version', 'N/A')} |",
            f"| **Author** | {metadata.get('author', 'N/A')} |",
            f"| **Created** | {metadata.get('created', 'N/A')} |",
            "",
        ]

        # Add tags if present
        tags = metadata.get("tags", [])
        if tags:
            lines.append(f"**Tags:** {', '.join(f'`{tag}`' for tag in tags)}")
            lines.append("")

        return "\n".join(lines)

    def generate_musical_properties(self) -> str:
        """Generate musical properties section."""
        data = self.sequence_data

        lines = [
            "## 🎵 Musical Properties",
            "",
            "| Property | Value |",
            "|----------|-------|",
            f"| **Key** | {data.get('key', 'N/A')} |",
            f"| **Tempo** | {data.get('tempo', 'N/A')} BPM |",
            f"| **Time Signature** | {data.get('timeSignature', 'N/A')} |",
            "",
        ]
        return "\n".join(lines)

    def generate_purpose_section(self) -> str:
        """Generate purpose and trigger section."""
        data = self.sequence_data

        lines = [
            "## 🎯 Purpose & Context",
            "",
            "### Purpose",
            data.get('purpose', 'No purpose statement provided.'),
            "",
            "### Trigger",
            f"**Event:** {data.get('trigger', 'No trigger defined.')}",
            "",
        ]

        # Add business value if present
        business_value = data.get('businessValue')
        if business_value:
            lines.extend([
                "### Business Value",
                business_value,
                "",
            ])

        return "\n".join(lines)

    def generate_user_story_section(self) -> str:
        """Generate top-level user story section."""
        data = self.sequence_data
        user_story = data.get('userStory', {})

        if not user_story:
            return ""

        lines = [
            "## 👤 User Story",
            "",
            f"**As a** {user_story.get('persona', 'User')}  ",
            f"**I want to** {user_story.get('goal', 'achieve a goal')}  ",
            f"**So that** {user_story.get('benefit', 'I receive value')}",
            "",
        ]
        return "\n".join(lines)

    def generate_governance_section(self) -> str:
        """Generate governance policies and metrics section."""
        data = self.sequence_data
        governance = data.get('governance', {})

        if not governance:
            return ""

        lines = [
            "## 🛡️ Governance",
            "",
        ]

        # Policies
        policies = governance.get('policies', [])
        if policies:
            lines.extend([
                "### Policies",
                "",
            ])
            for policy in policies:
                lines.append(f"- `{policy}`")
            lines.append("")

        # Metrics
        metrics = governance.get('metrics', [])
        if metrics:
            lines.extend([
                "### Metrics",
                "",
            ])
            for metric in metrics:
                lines.append(f"- `{metric}`")
            lines.append("")

        return "\n".join(lines)

    def generate_events_section(self) -> str:
        """Generate events section."""
        data = self.sequence_data
        events = data.get('events', [])

        if not events:
            return ""

        lines = [
            "## 📡 Events",
            "",
            "This sequence emits the following events in order:",
            "",
        ]

        for idx, event in enumerate(events, 1):
            lines.append(f"{idx}. `{event}`")

        lines.append("")
        return "\n".join(lines)

    def format_user_story_compact(self, user_story: Dict[str, str]) -> str:
        """Format a user story in compact form."""
        if not user_story:
            return "_No user story defined_"

        return (
            f"**As a** {user_story.get('persona', 'User')}, "
            f"**I want to** {user_story.get('goal', 'achieve a goal')}, "
            f"**so that** {user_story.get('benefit', 'I receive value')}"
        )

    def format_acceptance_criteria(self, criteria: List[Dict[str, Any]], indent: int = 0) -> List[str]:
        """
        Format acceptance criteria in Given/When/Then format.

        Args:
            criteria: List of acceptance criteria dictionaries
            indent: Number of spaces to indent

        Returns:
            List of formatted lines
        """
        if not criteria:
            return ["_No acceptance criteria defined_"]

        lines = []
        indent_str = " " * indent

        for idx, scenario in enumerate(criteria, 1):
            if len(criteria) > 1:
                lines.append(f"{indent_str}**Scenario {idx}:**")
                lines.append("")

            # Given
            given = scenario.get('given', [])
            if given:
                lines.append(f"{indent_str}**Given:**")
                for item in given:
                    lines.append(f"{indent_str}- {item}")
                lines.append("")

            # When
            when = scenario.get('when', [])
            if when:
                lines.append(f"{indent_str}**When:**")
                for item in when:
                    lines.append(f"{indent_str}- {item}")
                lines.append("")

            # Then
            then = scenario.get('then', [])
            if then:
                lines.append(f"{indent_str}**Then:**")
                for item in then:
                    lines.append(f"{indent_str}- {item}")
                lines.append("")

            # And (optional)
            and_clause = scenario.get('and', [])
            if and_clause:
                lines.append(f"{indent_str}**And:**")
                for item in and_clause:
                    lines.append(f"{indent_str}- {item}")
                lines.append("")

        return lines

    def generate_movements_section(self) -> str:
        """Generate detailed movements section."""
        data = self.sequence_data
        movements = data.get('movements', [])

        if not movements:
            return ""

        lines = [
            "## 🎼 Movements",
            "",
            f"This sequence consists of {len(movements)} movements:",
            "",
        ]

        # Movement summary table
        lines.extend([
            "| # | Movement | Beats | Error Handling | Status |",
            "|---|----------|-------|----------------|--------|",
        ])

        for movement in movements:
            num = movement.get('number', '?')
            name = movement.get('name', 'Unnamed')
            beats_count = len(movement.get('beats', []))
            error_handling = movement.get('errorHandling', 'N/A')
            status = movement.get('status', 'N/A')
            lines.append(f"| {num} | {name} | {beats_count} | `{error_handling}` | `{status}` |")

        lines.append("")
        lines.append("---")
        lines.append("")

        # Detailed movement sections
        for movement in movements:
            lines.extend(self.generate_movement_detail(movement))

        return "\n".join(lines)

    def generate_movement_detail(self, movement: Dict[str, Any]) -> List[str]:
        """Generate detailed section for a single movement."""
        lines = [
            f"### Movement {movement.get('number', '?')}: {movement.get('name', 'Unnamed')}",
            "",
        ]

        # Movement description
        description = movement.get('description')
        if description:
            lines.append(description)
            lines.append("")

        # Movement metadata
        lines.extend([
            "**Movement Properties:**",
            "",
            f"- **ID:** `{movement.get('id', 'N/A')}`",
            f"- **Tempo:** {movement.get('tempo', 'Inherited')} BPM",
            f"- **Error Handling:** `{movement.get('errorHandling', 'N/A')}`",
            f"- **Status:** `{movement.get('status', 'N/A')}`",
            "",
        ])

        # Movement user story
        user_story = movement.get('userStory')
        if user_story:
            lines.extend([
                "**User Story:**",
                "",
                self.format_user_story_compact(user_story),
                "",
            ])

        # Beats
        beats = movement.get('beats', [])
        if beats:
            lines.extend([
                f"**Beats ({len(beats)}):**",
                "",
            ])

            for beat in beats:
                lines.extend(self.generate_beat_detail(beat))

        lines.append("---")
        lines.append("")

        return lines

    def generate_beat_detail(self, beat: Dict[str, Any]) -> List[str]:
        """Generate detailed section for a single beat."""
        lines = [
            f"#### Beat {beat.get('beat', '?')}: {beat.get('name', 'Unnamed')}",
            "",
        ]

        # Beat title and description
        title = beat.get('title')
        if title:
            lines.append(f"**{title}**")
            lines.append("")

        description = beat.get('description')
        if description:
            lines.append(description)
            lines.append("")

        # Beat metadata table
        lines.extend([
            "| Property | Value |",
            "|----------|-------|",
            f"| **Event** | `{beat.get('event', 'N/A')}` |",
            f"| **Dynamics** | `{beat.get('dynamics', 'N/A')}` |",
            f"| **Timing** | `{beat.get('timing', 'N/A')}` |",
            f"| **Error Handling** | `{beat.get('errorHandling', 'N/A')}` |",
        ])

        # Dependencies
        dependencies = beat.get('dependencies', [])
        if dependencies:
            deps_str = ", ".join(f"`{dep}`" for dep in dependencies)
            lines.append(f"| **Dependencies** | {deps_str} |")

        lines.append("")

        # Handler information
        handler = beat.get('handler')
        if handler:
            if isinstance(handler, str):
                handler_name = handler
                source_path = "N/A"
                capabilities = []
            else:
                handler_name = handler.get('name', 'N/A')
                source_path = handler.get('sourcePath', 'N/A')
                capabilities = handler.get('handlerCapabilities', [])

            lines.extend([
                "**Handler:**",
                "",
                f"- **Name:** `{handler_name}`",
                f"- **Source:** `{source_path}`",
            ])

            if capabilities:
                caps_str = ", ".join(f"`{cap}`" for cap in capabilities)
                lines.append(f"- **Capabilities:** {caps_str}")

            lines.append("")

        # User story
        user_story = beat.get('userStory')
        if user_story:
            lines.extend([
                "**User Story:**",
                "",
                self.format_user_story_compact(user_story),
                "",
            ])

        # Acceptance criteria
        acceptance_criteria = beat.get('acceptanceCriteria', [])
        if acceptance_criteria:
            lines.extend([
                "**Acceptance Criteria:**",
                "",
            ])
            lines.extend(self.format_acceptance_criteria(acceptance_criteria))

        # Test information
        test_file = beat.get('testFile')
        test_case = beat.get('testCase')
        if test_file or test_case:
            lines.extend([
                "**Tests:**",
                "",
            ])
            if test_file:
                lines.append(f"- **Test File:** `{test_file}`")
            if test_case:
                lines.append(f"- **Test Case:** `{test_case}`")
            lines.append("")

        lines.append("")
        return lines

    def generate_footer(self) -> str:
        """Generate report footer."""
        lines = [
            "---",
            "",
            f"*Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
            "",
        ]
        return "\n".join(lines)

    def generate_report(self) -> str:
        """Generate the complete markdown report."""
        sections = [
            self.generate_header(),
            self.generate_metadata_section(),
            self.generate_musical_properties(),
            self.generate_purpose_section(),
            self.generate_user_story_section(),
            self.generate_governance_section(),
            self.generate_events_section(),
            self.generate_movements_section(),
            self.generate_footer(),
        ]

        return "\n".join(section for section in sections if section)

    def save_report(self, content: str) -> Path:
        """
        Save the report to a markdown file.

        Args:
            content: Markdown content to save

        Returns:
            Path to the saved report file
        """
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Generate output filename
        sequence_id = self.sequence_data.get('id', 'unknown')
        output_file = self.output_dir / f"{sequence_id}.md"

        # Write report
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)

        return output_file

    def run(self) -> Path:
        """
        Run the report generation process.

        Returns:
            Path to the generated report file
        """
        print(f"Loading sequence: {self.sequence_path}")
        self.load_sequence()

        print(f"Generating report for: {self.sequence_data.get('name', 'Unnamed')}")
        report_content = self.generate_report()

        print(f"Saving report...")
        output_path = self.save_report(report_content)

        print(f"Report generated successfully: {output_path}")
        return output_path


def main():
    """Main entry point for command-line usage."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate markdown documentation from musical sequence JSON files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate report for a single sequence
  python scripts/generate_sequence_report.py sequences/hybrid-resume-generation.sequence.json

  # Generate reports for all sequences
  python scripts/generate_sequence_report.py sequences/*.sequence.json

  # Specify custom output directory
  python scripts/generate_sequence_report.py sequences/hybrid-resume-generation.sequence.json --output-dir docs/sequences
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
        help="Output directory for reports (default: docs/sequences)",
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
            generator = SequenceReportGenerator(sequence_path, output_dir)
            output_path = generator.run()
            print()
        except Exception as e:
            print(f"Error processing {sequence_path}: {e}")
            import traceback
            traceback.print_exc()
            continue


if __name__ == "__main__":
    main()
