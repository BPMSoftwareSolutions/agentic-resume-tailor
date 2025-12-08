"""Test sequence schemas against musical-sequence.schema.json"""

import json
import sys
from pathlib import Path

import pytest
from jsonschema import Draft7Validator, RefResolver, ValidationError

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture
def schema():
    """Load the musical sequence schema"""
    schema_path = Path(__file__).parent.parent / "schemas" / "musical-sequence.schema.json"
    with open(schema_path, 'r', encoding='utf-8') as f:
        return json.load(f)


@pytest.fixture
def validator(schema):
    """Create a JSON schema validator with proper reference resolution"""
    schema_path = Path(__file__).parent.parent / "schemas" / "musical-sequence.schema.json"
    resolver = RefResolver(
        base_uri=f"file://{schema_path.parent.resolve()}/",
        referrer=schema
    )
    return Draft7Validator(schema, resolver=resolver)


def get_sequence_files():
    """Get all sequence JSON files"""
    sequences_dir = Path(__file__).parent.parent / "sequences"
    if not sequences_dir.exists():
        return []
    return list(sequences_dir.glob("*.sequence.json"))


class TestSequenceValidation:
    """Test that all sequence files are valid against the schema"""

    @pytest.mark.parametrize("sequence_file", get_sequence_files(), ids=lambda p: p.name)
    def test_sequence_validates_against_schema(self, sequence_file, validator):
        """Test that sequence file validates against musical-sequence.schema.json"""
        with open(sequence_file, 'r', encoding='utf-8') as f:
            sequence_data = json.load(f)

        # Validate against schema
        errors = list(validator.iter_errors(sequence_data))

        if errors:
            error_messages = []
            for error in errors:
                path = " -> ".join(str(p) for p in error.path)
                error_messages.append(f"  Path: {path}\n  Error: {error.message}")

            pytest.fail(
                f"Sequence validation failed for {sequence_file.name}:\n" +
                "\n\n".join(error_messages)
            )

    @pytest.mark.parametrize("sequence_file", get_sequence_files(), ids=lambda p: p.name)
    def test_sequence_has_required_fields(self, sequence_file):
        """Test that sequence has all required top-level fields"""
        with open(sequence_file, 'r', encoding='utf-8') as f:
            sequence_data = json.load(f)

        required_fields = ["domainId", "id", "name", "movements", "userStory"]

        for field in required_fields:
            assert field in sequence_data, f"Missing required field: {field}"

    @pytest.mark.parametrize("sequence_file", get_sequence_files(), ids=lambda p: p.name)
    def test_movements_have_required_fields(self, sequence_file):
        """Test that all movements have required fields"""
        with open(sequence_file, 'r', encoding='utf-8') as f:
            sequence_data = json.load(f)

        required_movement_fields = ["name", "beats", "userStory"]

        for i, movement in enumerate(sequence_data.get("movements", [])):
            for field in required_movement_fields:
                assert field in movement, (
                    f"Movement {i} ({movement.get('name', 'unnamed')}) "
                    f"missing required field: {field}"
                )

    @pytest.mark.parametrize("sequence_file", get_sequence_files(), ids=lambda p: p.name)
    def test_beats_have_required_fields(self, sequence_file):
        """Test that all beats have required fields"""
        with open(sequence_file, 'r', encoding='utf-8') as f:
            sequence_data = json.load(f)

        required_beat_fields = ["event", "userStory", "acceptanceCriteria", "testFile"]

        for mov_i, movement in enumerate(sequence_data.get("movements", [])):
            movement_name = movement.get("name", "unnamed")
            for beat_i, beat in enumerate(movement.get("beats", [])):
                beat_name = beat.get("name", f"beat {beat_i}")
                for field in required_beat_fields:
                    assert field in beat, (
                        f"Movement '{movement_name}' -> Beat '{beat_name}' "
                        f"missing required field: {field}"
                    )

    @pytest.mark.parametrize("sequence_file", get_sequence_files(), ids=lambda p: p.name)
    def test_user_stories_have_required_fields(self, sequence_file):
        """Test that all user stories (sequence, movement, beat) have persona/goal/benefit"""
        with open(sequence_file, 'r', encoding='utf-8') as f:
            sequence_data = json.load(f)

        user_story_fields = ["persona", "goal", "benefit"]

        # Check sequence-level user story
        seq_user_story = sequence_data.get("userStory", {})
        for field in user_story_fields:
            assert field in seq_user_story, (
                f"Sequence-level userStory missing field: {field}"
            )

        # Check movement-level user stories
        for mov_i, movement in enumerate(sequence_data.get("movements", [])):
            movement_name = movement.get("name", "unnamed")
            mov_user_story = movement.get("userStory", {})
            for field in user_story_fields:
                assert field in mov_user_story, (
                    f"Movement '{movement_name}' userStory missing field: {field}"
                )

            # Check beat-level user stories
            for beat_i, beat in enumerate(movement.get("beats", [])):
                beat_name = beat.get("name", f"beat {beat_i}")
                beat_user_story = beat.get("userStory", {})
                for field in user_story_fields:
                    assert field in beat_user_story, (
                        f"Movement '{movement_name}' -> Beat '{beat_name}' "
                        f"userStory missing field: {field}"
                    )

    @pytest.mark.parametrize("sequence_file", get_sequence_files(), ids=lambda p: p.name)
    def test_acceptance_criteria_structure(self, sequence_file):
        """Test that acceptance criteria follow Given/When/Then structure"""
        with open(sequence_file, 'r', encoding='utf-8') as f:
            sequence_data = json.load(f)

        for movement in sequence_data.get("movements", []):
            movement_name = movement.get("name", "unnamed")
            for beat in movement.get("beats", []):
                beat_name = beat.get("name", "unnamed")
                acceptance_criteria = beat.get("acceptanceCriteria", [])

                assert isinstance(acceptance_criteria, list), (
                    f"Movement '{movement_name}' -> Beat '{beat_name}' "
                    f"acceptanceCriteria must be an array"
                )

                for i, criterion in enumerate(acceptance_criteria):
                    # Should have at least 'when' and 'then'
                    assert "when" in criterion or "given" in criterion, (
                        f"Movement '{movement_name}' -> Beat '{beat_name}' "
                        f"acceptanceCriteria[{i}] missing 'when' or 'given'"
                    )
                    assert "then" in criterion, (
                        f"Movement '{movement_name}' -> Beat '{beat_name}' "
                        f"acceptanceCriteria[{i}] missing 'then'"
                    )

    @pytest.mark.parametrize("sequence_file", get_sequence_files(), ids=lambda p: p.name)
    def test_handler_references_valid(self, sequence_file):
        """Test that handler references are properly structured"""
        with open(sequence_file, 'r', encoding='utf-8') as f:
            sequence_data = json.load(f)

        for movement in sequence_data.get("movements", []):
            movement_name = movement.get("name", "unnamed")
            for beat in movement.get("beats", []):
                beat_name = beat.get("name", "unnamed")
                handler = beat.get("handler")

                if handler:
                    if isinstance(handler, dict):
                        # Must have name and sourcePath
                        assert "name" in handler, (
                            f"Movement '{movement_name}' -> Beat '{beat_name}' "
                            f"handler missing 'name'"
                        )
                        assert "sourcePath" in handler, (
                            f"Movement '{movement_name}' -> Beat '{beat_name}' "
                            f"handler missing 'sourcePath'"
                        )

                        # If scope is specified, must be valid
                        if "scope" in handler:
                            valid_scopes = ["plugin", "orchestration", "system", "policy"]
                            assert handler["scope"] in valid_scopes, (
                                f"Movement '{movement_name}' -> Beat '{beat_name}' "
                                f"handler has invalid scope: {handler['scope']}"
                            )

                        # If kind is specified, must be valid
                        if "kind" in handler:
                            valid_kinds = [
                                "validation", "orchestration", "reporting",
                                "policy-enforcement", "metrics", "automation"
                            ]
                            assert handler["kind"] in valid_kinds, (
                                f"Movement '{movement_name}' -> Beat '{beat_name}' "
                                f"handler has invalid kind: {handler['kind']}"
                            )

    def test_hybrid_resume_generation_sequence_exists(self):
        """Test that hybrid-resume-generation sequence exists"""
        sequence_file = (
            Path(__file__).parent.parent /
            "sequences" /
            "hybrid-resume-generation.sequence.json"
        )
        assert sequence_file.exists(), (
            "hybrid-resume-generation.sequence.json not found"
        )

    def test_hybrid_resume_generation_has_correct_structure(self):
        """Test hybrid-resume-generation has expected movements and beats"""
        sequence_file = (
            Path(__file__).parent.parent /
            "sequences" /
            "hybrid-resume-generation.sequence.json"
        )

        with open(sequence_file, 'r', encoding='utf-8') as f:
            sequence = json.load(f)

        # Check basic metadata
        assert sequence["id"] == "hybrid-resume-generation"
        assert sequence["domainId"] == "agentic-resume-tailor"
        assert sequence["status"] == "active"

        # Check movements
        movements = sequence["movements"]
        assert len(movements) == 4, "Should have 4 movements"

        movement_names = [m["name"] for m in movements]
        expected_movements = [
            "Data Loading and Enrichment",
            "RAG-Enhanced Tailoring (Optional)",
            "HTML Generation",
            "File Export"
        ]
        assert movement_names == expected_movements

        # Check beat counts
        beat_counts = [len(m["beats"]) for m in movements]
        expected_beat_counts = [2, 3, 3, 3]  # Based on the workflow
        assert beat_counts == expected_beat_counts, (
            f"Beat counts don't match. Expected {expected_beat_counts}, "
            f"got {beat_counts}"
        )
