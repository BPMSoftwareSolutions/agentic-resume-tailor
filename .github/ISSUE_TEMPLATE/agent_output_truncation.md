---
name: Agent Output Truncation Issue
about: Command output is truncated in agent responses
title: 'Agent truncates command output to 500 characters'
labels: bug, agent, enhancement
assignees: ''
---

## 🐛 Bug Description

The AI agent truncates command output to 500 characters in the result analyzer, causing incomplete display of command results. This is particularly problematic for commands that return large amounts of data, such as listing experience entries.

## 📍 Location

**File**: `src/agent/result_analyzer.py`  
**Lines**: 176, 185, 188, 194  
**Function**: `_format_message()`

## 🔍 Root Cause

The result analyzer hardcodes a 500-character limit on command output:

```python
# Line 176
clean_output = output.strip()[:500]

# Line 185
clean_error = error.strip()[:500]

# Line 188
clean_output = output.strip()[:500]

# Line 194
message += output.strip()[:500]
```

## 📊 Impact

### Commands Affected
- `python src/crud/experience.py --resume "Ford" --list` - Shows only first 2-3 experience entries
- `python src/utils/list_resumes.py` - May truncate resume list
- `python src/utils/list_job_listings.py` - May truncate job listings
- Any command with verbose output

### User Experience
Users see truncated output like:
```
Experience (20 entries):

  [0] **Edward Jones — Senior Application Architect / Platform Team Delivery Lead
      2021–2024
      Bullets: 6
        [0] Led modernization of Edward Jones' enterprise *Online Access* platform, **transi...
        [1] Directed **cross-functional teams (web, mobile, API, mainframe)** across multipl...
        [2] Esta
```

Instead of seeing all 20 experience entries with full details.

## 🎯 Expected Behavior

The agent should display complete command output, or provide intelligent truncation with:
1. A configurable limit (not hardcoded)
2. A "show more" option
3. Smart truncation that preserves structure
4. Clear indication when output is truncated

## 💡 Proposed Solutions

### Option 1: Increase Limit (Quick Fix)
```python
# Increase from 500 to 5000 characters
clean_output = output.strip()[:5000]
```

**Pros**: Simple, immediate fix  
**Cons**: Still arbitrary limit, doesn't solve root issue

### Option 2: Configurable Limit (Better)
```python
class ResultAnalyzer:
    def __init__(self, max_output_length: int = 5000):
        self.max_output_length = max_output_length
    
    def _format_message(self, ...):
        clean_output = output.strip()[:self.max_output_length]
```

**Pros**: Flexible, can be adjusted per use case  
**Cons**: Still truncates, just more configurable

### Option 3: Smart Truncation (Best)
```python
def _format_message(self, status, output, error, extracted_info):
    MAX_LENGTH = 5000
    
    if status == 'success':
        message = "✅ Command executed successfully\n\n"
        
        if extracted_info:
            message += self._format_extracted_info(extracted_info)
        
        if output:
            clean_output = output.strip()
            
            # Smart truncation
            if len(clean_output) > MAX_LENGTH:
                truncated = clean_output[:MAX_LENGTH]
                # Find last complete line
                last_newline = truncated.rfind('\n')
                if last_newline > 0:
                    truncated = truncated[:last_newline]
                
                lines_total = clean_output.count('\n') + 1
                lines_shown = truncated.count('\n') + 1
                
                message += f"\n{truncated}\n\n"
                message += f"... (showing {lines_shown} of {lines_total} lines)\n"
                message += f"💡 Tip: Output truncated. Use --format simple for shorter output."
            else:
                message += f"\n{clean_output}"
    
    return message
```

**Pros**: 
- Preserves complete lines
- Shows truncation indicator
- Provides helpful tips
- Better UX

**Cons**: More complex implementation

### Option 4: Command-Specific Handling (Most Flexible)
```python
# Detect list commands and handle differently
UNLIMITED_OUTPUT_COMMANDS = [
    'list_resumes.py',
    'list_job_listings.py',
    'experience.py --list',
]

def _should_truncate(self, command: str) -> bool:
    """Check if command output should be truncated."""
    for pattern in self.UNLIMITED_OUTPUT_COMMANDS:
        if pattern in command:
            return False
    return True

def _format_message(self, status, output, error, extracted_info, command=""):
    # ... existing code ...
    
    if output:
        clean_output = output.strip()
        
        if self._should_truncate(command):
            clean_output = clean_output[:5000]
        
        message += f"\n{clean_output}"
```

**Pros**: 
- Flexible per-command behavior
- No truncation for list commands
- Maintains safety for other commands

**Cons**: Requires passing command to format method

## 🧪 Test Cases

### Test 1: List All Experiences
```bash
python agent.py
> List all experiences in the Ford resume
# Expected: All 20 experience entries displayed
# Actual: Only first 2-3 entries shown
```

### Test 2: List Resumes
```bash
python agent.py
> List all resumes
# Expected: All 18 resumes in formatted table
# Actual: May be truncated if output > 500 chars
```

### Test 3: Long Command Output
```bash
python agent.py
> run: python src/crud/experience.py --resume "Ford" --list --verbose
# Expected: Full verbose output
# Actual: Truncated at 500 characters
```

## 📝 Acceptance Criteria

- [ ] Command output is not arbitrarily truncated at 500 characters
- [ ] List commands show complete output
- [ ] If truncation is necessary, it's done intelligently (complete lines)
- [ ] Users are informed when output is truncated
- [ ] Truncation limit is configurable
- [ ] Tests pass for all affected commands

## 🔗 Related Issues

- Issue #27: Intelligent CRUD Orchestration (this affects list operations)
- Issue #24: Auto-Verification & Token Management (result analyzer)

## 🏷️ Labels

- `bug` - Incorrect behavior
- `agent` - Affects AI agent functionality
- `enhancement` - Improvement to existing feature
- `good first issue` - Well-defined problem with clear solution

## 📅 Priority

**Medium-High** - Affects user experience for common operations (listing data)

## 💬 Additional Context

This issue was discovered when implementing the `--verbose` flag for experience listing. Even with `--verbose`, users couldn't see full output because the result analyzer was truncating at 500 characters.

The 500-character limit was likely added to:
1. Prevent overwhelming the OpenAI API with large context
2. Keep agent responses concise
3. Avoid token limit issues

However, for list/display commands, users need to see complete output. A smarter approach would be command-specific handling or intelligent truncation with clear indicators.

