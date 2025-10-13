# Auto-Verification & Token Management

**Related to GitHub Issue #24 - Phase 1: Auto-Verification & Result Analysis with Token Management**

## Overview

This feature adds intelligent result analysis and token management to the AI agent, providing:

1. **Auto-Verification**: Automatic analysis of command execution results
2. **Result Analysis**: Extraction of key information (IDs, names, counts, paths)
3. **Next-Step Suggestions**: Intelligent recommendations after operations
4. **Token Management**: Real-time token counting and memory warnings
5. **Memory Optimization**: Suggestions to prevent context overflow

## Features

### 1. Result Analyzer (`src/agent/result_analyzer.py`)

The Result Analyzer automatically:
- Parses command output for success/failure indicators
- Extracts key information (resume IDs, names, counts, file paths)
- Verifies data integrity
- Suggests next logical steps based on the operation

#### Example Output

**Before (without auto-verification):**
```
✅ Command executed successfully:
[SUCCESS] Successfully duplicated resume!
New Resume ID: abc-123-def-456
New Resume Name: Test_Resume
```

**After (with auto-verification):**
```
✅ Command executed successfully

[SUCCESS] Successfully duplicated resume!
[INFO]    New Resume ID: abc-123-def-456
[INFO]    New Resume Name: Test_Resume

✅ Successfully created resume 'Test_Resume' with ID abc-123-def-456

💡 What would you like to do next?
   1. Update specific sections (experience, skills, summary)
   2. Tailor it to a job posting
   3. List all your resumes
   4. Export to PDF or DOCX
```

### 2. Token Manager (`src/agent/token_manager.py`)

The Token Manager provides:
- Accurate token counting using `tiktoken` library
- Warning at 80% token capacity
- Critical alert at 95% token capacity
- Memory usage statistics
- Optimization suggestions

#### Token Limits by Model

| Model | Token Limit |
|-------|-------------|
| gpt-4 | 8,192 |
| gpt-4-turbo | 128,000 |
| gpt-4-32k | 32,768 |
| gpt-3.5-turbo | 4,096 |
| gpt-3.5-turbo-16k | 16,384 |

#### Warning Thresholds

- **80% Warning**: Suggests clearing memory if conversation continues
- **95% Critical**: Immediate action required to prevent failures

#### Example Warnings

**Warning (80%):**
```
⚠️  WARNING: Memory at 82.3% capacity (6584/8000 tokens).
Consider clearing memory if conversation continues.

Suggestions:
  • Clear old conversation history: Use 'clear memory' command
  • Start a new conversation session
  • Export important information before clearing
```

**Critical (95%):**
```
🚨 CRITICAL: Memory at 96.5% capacity (7720/8000 tokens).
You are very close to the limit!

IMMEDIATE ACTION REQUIRED:
  • Clear memory now: Use 'clear memory' command
  • Start a new conversation session
  • The next message may fail due to token limit
```

## API Endpoints

### GET /api/agent/memory/stats

Get token usage statistics for the agent's memory.

**Response:**
```json
{
  "success": true,
  "stats": {
    "total_tokens": 1234,
    "max_tokens": 8192,
    "percentage": 15.1,
    "warning": false,
    "critical": false,
    "message_count": 25,
    "role_counts": {
      "system": 1,
      "user": 12,
      "assistant": 12
    },
    "role_tokens": {
      "system": 450,
      "user": 384,
      "assistant": 400
    },
    "estimation_method": "accurate",
    "model": "gpt-4"
  }
}
```

## Web Interface Updates

The web interface now displays:

1. **Token Usage Bar**: Visual progress bar showing memory usage
   - Green: < 80% (healthy)
   - Yellow: 80-95% (warning)
   - Red: > 95% (critical)

2. **Token Count**: Displays current/max tokens and percentage

3. **Warning Banner**: Shows warning/critical messages when thresholds are reached

## Usage Examples

### Command-Line Agent

```bash
# Start the agent
python agent.py

# The agent will show token usage on startup:
🤖 Local AI Agent Started
==================================================
Commands:
  - Type 'run: <command>' to execute local commands
  - Type 'exit' or 'quit' to stop
  - Type anything else to chat with the AI

Settings:
  - Auto-execute: ✅ Enabled
  - Confirmation: ✅ Required
  - Memory: 1234/8192 tokens (15.1%)
==================================================
```

### Web Interface

1. Open `http://localhost:5000/agent.html`
2. Token usage is displayed in the header
3. Warning banners appear automatically when thresholds are reached
4. Click "Clear Memory" to reset when needed

## Testing

Run the comprehensive test suite:

```bash
# Run all tests
python -m pytest tests/test_result_analyzer.py tests/test_token_manager.py -v

# Run with coverage
python -m pytest tests/test_result_analyzer.py tests/test_token_manager.py --cov=src/agent --cov-report=html
```

### Test Coverage

- **Result Analyzer**: 18 tests covering:
  - Success/failure detection
  - Information extraction (IDs, names, counts, paths)
  - Status determination
  - Suggestion generation
  - Message formatting

- **Token Manager**: 25 tests covering:
  - Token counting (accurate and estimated)
  - Warning/critical thresholds
  - Statistics generation
  - Optimization suggestions
  - Model limit handling

## Installation

1. Install the required dependency:
```bash
pip install tiktoken>=0.5.0
```

2. The feature is automatically enabled in the agent

## Configuration

No configuration required. The feature works out-of-the-box with sensible defaults:

- Warning threshold: 80%
- Critical threshold: 95%
- Token limits: Automatically detected based on model

## Architecture

```
agent.py
├── ResultAnalyzer (src/agent/result_analyzer.py)
│   ├── analyze() - Main analysis method
│   ├── _determine_status() - Success/error detection
│   ├── _extract_information() - Key info extraction
│   ├── _format_message() - User-friendly formatting
│   └── _generate_suggestions() - Next-step recommendations
│
└── TokenManager (src/agent/token_manager.py)
    ├── count_tokens() - Token counting
    ├── check_limit() - Threshold checking
    ├── get_stats() - Detailed statistics
    └── suggest_optimization() - Memory optimization tips
```

## Benefits

1. **Better User Experience**: Users see structured, actionable feedback
2. **Prevent Errors**: Token warnings prevent context overflow crashes
3. **Guided Workflow**: Next-step suggestions help users navigate operations
4. **Memory Awareness**: Real-time visibility into token usage
5. **Proactive Management**: Warnings before hitting limits

## Future Enhancements

See related issues:
- #23 - Parent issue (Intelligent Agent Memory Management)
- Phase 2 - Automatic memory optimization
- Phase 3 - Memory insights dashboard

## Troubleshooting

### Token counting shows "estimated" instead of "accurate"

**Cause**: `tiktoken` library not installed or failed to load

**Solution**:
```bash
pip install tiktoken>=0.5.0
```

### Warnings not appearing in web interface

**Cause**: API server not running or CORS issues

**Solution**:
1. Ensure API server is running: `python -m flask --app src/api/app run`
2. Check browser console for errors
3. Verify API endpoint: `http://localhost:5000/api/agent/memory/stats`

### Tests failing

**Cause**: Missing dependencies or path issues

**Solution**:
```bash
# Install all dependencies
pip install -r requirements.txt

# Run tests from project root
python -m pytest tests/ -v
```

## Contributing

When adding new command types:

1. Update `ResultAnalyzer._generate_suggestions()` with command-specific suggestions
2. Add test cases in `tests/test_result_analyzer.py`
3. Update this documentation with examples

## License

Same as parent project.

