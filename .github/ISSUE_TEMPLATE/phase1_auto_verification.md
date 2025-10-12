# Phase 1: Auto-Verification & Result Analysis with Token Management

**Parent Issue**: #23 - Intelligent Agent Memory Management  
**Priority**: 🔴 Critical  
**Estimated Effort**: 10-14 hours

## User Value Delivered

Users will be able to:
1. ✅ **See the agent automatically verify command results** - Agent analyzes success/failure and extracts key information
2. ✅ **Get intelligent follow-up suggestions** - Agent suggests next logical steps after operations
3. ✅ **Avoid context overflow errors** - Token management prevents crashes from long conversations
4. ✅ **See memory usage warnings** - Agent warns when approaching token limits

## Problem Statement

Currently:
- ❌ Agent executes commands but doesn't analyze results intelligently
- ❌ Agent doesn't extract key information (IDs, names, counts) from outputs
- ❌ Agent doesn't suggest next steps after successful operations
- ❌ Memory grows indefinitely until hitting OpenAI context limits
- ❌ No visibility into token usage or warnings

## Solution Overview

Combine **auto-verification** with **token management** to deliver immediate user value:

### Part A: Auto-Verification & Result Analysis
Agent automatically:
1. Parses command output for success/failure indicators
2. Extracts key information (IDs, names, counts, paths)
3. Verifies data integrity
4. Suggests next logical steps

### Part B: Token Management & Warnings
System automatically:
1. Counts tokens before each API call
2. Warns user when approaching limits (80% threshold)
3. Provides memory optimization options
4. Prevents context overflow errors

## Technical Implementation

### 1. Add Dependencies

**File**: `requirements.txt`
```
tiktoken>=0.5.0
```

### 2. Create Result Analyzer Module

**File**: `src/agent/result_analyzer.py`
```python
import re
from typing import Dict, List, Optional

class ResultAnalyzer:
    """Analyzes command execution results and extracts key information."""
    
    def analyze_result(self, command: str, output: str, success: bool) -> Dict:
        """
        Analyze command result and extract key information.
        
        Returns:
            {
                "success": bool,
                "key_info": Dict,  # Extracted IDs, names, counts, etc.
                "verification": str,  # Human-readable verification
                "next_steps": List[str]  # Suggested next actions
            }
        """
        analysis = {
            "success": success,
            "key_info": {},
            "verification": "",
            "next_steps": []
        }
        
        if not success:
            analysis["verification"] = self._analyze_error(output)
            analysis["next_steps"] = self._suggest_error_fixes(command, output)
            return analysis
        
        # Extract key information based on command type
        if "duplicate_resume.py" in command:
            analysis["key_info"] = self._extract_resume_info(output)
            analysis["verification"] = self._verify_resume_creation(analysis["key_info"])
            analysis["next_steps"] = self._suggest_resume_next_steps()
        
        elif "update_resume_experience.py" in command:
            analysis["key_info"] = self._extract_update_info(output)
            analysis["verification"] = self._verify_update(analysis["key_info"])
            analysis["next_steps"] = self._suggest_update_next_steps()
        
        elif "tailor.py" in command:
            analysis["key_info"] = self._extract_tailor_info(output)
            analysis["verification"] = self._verify_tailor(analysis["key_info"])
            analysis["next_steps"] = self._suggest_tailor_next_steps()
        
        return analysis
    
    def _extract_resume_info(self, output: str) -> Dict:
        """Extract resume ID, name from duplicate_resume.py output."""
        info = {}
        
        # Extract ID: "New Resume ID: abc-123"
        id_match = re.search(r'New Resume ID:\s*([a-f0-9-]+)', output, re.IGNORECASE)
        if id_match:
            info["id"] = id_match.group(1)
        
        # Extract name: "New Resume Name: Sidney_Jones_..."
        name_match = re.search(r'New Resume Name:\s*(.+?)(?:\n|$)', output, re.IGNORECASE)
        if name_match:
            info["name"] = name_match.group(1).strip()
        
        return info
    
    def _verify_resume_creation(self, info: Dict) -> str:
        """Generate verification message for resume creation."""
        if "id" in info and "name" in info:
            return f"✅ Successfully created resume '{info['name']}' with ID {info['id']}"
        return "✅ Resume created successfully"
    
    def _suggest_resume_next_steps(self) -> List[str]:
        """Suggest next steps after resume creation."""
        return [
            "Update specific sections (experience, skills, summary)",
            "Tailor it to a job posting",
            "List all your resumes",
            "Export to PDF or DOCX"
        ]
```

### 3. Create Token Manager Module

**File**: `src/agent/token_manager.py`
```python
import tiktoken
from typing import List, Dict, Optional

class TokenManager:
    """Manages token counting and memory optimization."""
    
    def __init__(self, model: str = "gpt-4", max_tokens: int = 8000):
        self.model = model
        self.max_tokens = max_tokens
        self.encoding = tiktoken.encoding_for_model(model)
        self.warning_threshold = 0.8  # Warn at 80%
    
    def count_tokens(self, messages: List[Dict]) -> int:
        """Count total tokens in message list."""
        total = 0
        for message in messages:
            # Count tokens for role and content
            total += len(self.encoding.encode(message.get("role", "")))
            total += len(self.encoding.encode(message.get("content", "")))
            total += 4  # Every message has overhead
        total += 2  # Conversation overhead
        return total
    
    def check_limit(self, messages: List[Dict]) -> Dict:
        """
        Check if messages are approaching token limit.
        
        Returns:
            {
                "current_tokens": int,
                "max_tokens": int,
                "percentage": float,
                "warning": bool,
                "critical": bool,
                "message": str
            }
        """
        current = self.count_tokens(messages)
        percentage = current / self.max_tokens
        
        result = {
            "current_tokens": current,
            "max_tokens": self.max_tokens,
            "percentage": percentage,
            "warning": percentage >= self.warning_threshold,
            "critical": percentage >= 0.95,
            "message": ""
        }
        
        if result["critical"]:
            result["message"] = (
                f"⚠️ CRITICAL: Memory at {percentage*100:.1f}% capacity "
                f"({current}/{self.max_tokens} tokens). "
                f"Please clear or optimize memory soon."
            )
        elif result["warning"]:
            result["message"] = (
                f"⚠️ WARNING: Memory at {percentage*100:.1f}% capacity "
                f"({current}/{self.max_tokens} tokens). "
                f"Consider clearing memory if conversation continues."
            )
        
        return result
    
    def get_optimization_suggestions(self, current_tokens: int) -> List[str]:
        """Get suggestions for optimizing memory."""
        suggestions = []
        
        if current_tokens > self.max_tokens * 0.8:
            suggestions.append("Clear old conversation history: Use 'clear memory' command")
            suggestions.append("Start a new conversation session")
            suggestions.append("Export important information before clearing")
        
        return suggestions
```

### 4. Integrate into Agent

**File**: `agent.py`

Add imports:
```python
from src.agent.result_analyzer import ResultAnalyzer
from src.agent.token_manager import TokenManager
```

Update `Agent.__init__()`:
```python
def __init__(self, memory_file: str = "memory.json", model: str = "gpt-4",
             auto_execute: bool = True, confirm_execution: bool = True):
    # ... existing code ...
    
    # Add new components
    self.result_analyzer = ResultAnalyzer()
    self.token_manager = TokenManager(model=model)
```

Update `process_message()` to add verification:
```python
if should_execute:
    print(f"🔧 Executing command: {command}")
    result = self.command_executor.execute(command)
    
    # NEW: Analyze result
    analysis = self.result_analyzer.analyze_result(
        command=command,
        output=result["output"],
        success=result["success"]
    )
    
    # Format result with analysis
    execution_result = self._format_execution_result_with_analysis(result, analysis)
    
    # Add execution result to memory
    self.memory_manager.add_message("user", f"run: {command}")
    self.memory_manager.add_message("assistant", execution_result)
    self.memory_manager.save()
    
    # Append execution result to response
    assistant_message += f"\n\n{execution_result}"
```

Add token checking before API calls:
```python
def process_message(self, user_input: str) -> str:
    # ... existing code ...
    
    # NEW: Check token limit before API call
    token_status = self.token_manager.check_limit(
        self.memory_manager.get_messages()
    )
    
    if token_status["warning"]:
        print(f"\n{token_status['message']}\n")
        
        if token_status["critical"]:
            suggestions = self.token_manager.get_optimization_suggestions(
                token_status["current_tokens"]
            )
            print("Suggestions:")
            for suggestion in suggestions:
                print(f"  • {suggestion}")
            print()
    
    # Continue with API call...
```

Add new formatting method:
```python
def _format_execution_result_with_analysis(self, result: Dict, analysis: Dict) -> str:
    """Format execution result with analysis."""
    output = []
    
    if result["success"]:
        output.append("✅ Command executed successfully")
        output.append(f"\n{result['output']}")
        
        # Add verification
        if analysis["verification"]:
            output.append(f"\n{analysis['verification']}")
        
        # Add next steps
        if analysis["next_steps"]:
            output.append("\n\n💡 What would you like to do next?")
            for i, step in enumerate(analysis["next_steps"], 1):
                output.append(f"   {i}. {step}")
    else:
        output.append("❌ Command failed")
        output.append(f"\n{result['error']}")
        
        # Add error analysis
        if analysis["verification"]:
            output.append(f"\n{analysis['verification']}")
        
        # Add fix suggestions
        if analysis["next_steps"]:
            output.append("\n\n💡 Suggestions to fix:")
            for i, step in enumerate(analysis["next_steps"], 1):
                output.append(f"   {i}. {step}")
    
    return "\n".join(output)
```

### 5. Add API Endpoint for Token Status

**File**: `src/api/app.py`

```python
@app.route('/api/agent/memory/stats', methods=['GET'])
def get_memory_stats():
    """
    Get memory usage statistics including token count.
    
    Returns:
        JSON response with memory statistics
    """
    try:
        agent = get_agent_instance()
        if not agent:
            return jsonify({"error": "Agent not initialized"}), 500
        
        messages = agent.memory_manager.get_messages()
        token_status = agent.token_manager.check_limit(messages)
        
        return jsonify({
            "success": True,
            "stats": {
                "message_count": len(messages),
                "current_tokens": token_status["current_tokens"],
                "max_tokens": token_status["max_tokens"],
                "percentage": token_status["percentage"],
                "warning": token_status["warning"],
                "critical": token_status["critical"],
                "message": token_status["message"]
            }
        })
    
    except Exception as e:
        return jsonify({"error": f"Failed to get stats: {str(e)}"}), 500
```

### 6. Update Web Interface

**File**: `src/web/agent.html`

Add memory stats display:
```html
<div class="memory-stats" id="memoryStats">
    <span id="tokenCount">0 tokens</span>
    <span id="tokenPercentage" class="badge">0%</span>
</div>
```

**File**: `src/web/agent.js`

Add function to load stats:
```javascript
async function loadMemoryStats() {
    try {
        const response = await fetch(`${API_BASE_URL}/agent/memory/stats`);
        const data = await response.json();
        
        if (response.ok && data.success) {
            const stats = data.stats;
            document.getElementById('tokenCount').textContent = 
                `${stats.current_tokens} / ${stats.max_tokens} tokens`;
            
            const badge = document.getElementById('tokenPercentage');
            badge.textContent = `${(stats.percentage * 100).toFixed(1)}%`;
            
            // Update badge color based on usage
            badge.className = 'badge';
            if (stats.critical) {
                badge.classList.add('badge-danger');
            } else if (stats.warning) {
                badge.classList.add('badge-warning');
            } else {
                badge.classList.add('badge-success');
            }
            
            // Show warning message if needed
            if (stats.message) {
                showAlert(stats.message, stats.critical ? 'danger' : 'warning');
            }
        }
    } catch (error) {
        console.error('Failed to load memory stats:', error);
    }
}

// Call after each message
async function sendMessage(message) {
    // ... existing code ...
    await loadMemoryStats();  // Add this
}
```

## Testing & Verification

### Unit Tests

**File**: `tests/test_result_analyzer.py`
```python
def test_analyze_duplicate_resume_success():
    """Test analyzing successful resume duplication."""
    analyzer = ResultAnalyzer()
    
    output = """
    [SUCCESS] Successfully duplicated resume!
    [INFO]    New Resume ID: abc-123-def-456
    [INFO]    New Resume Name: Sidney_Jones_Engineer_Ford
    """
    
    analysis = analyzer.analyze_result(
        command="python src/duplicate_resume.py --resume Master --new-name Test",
        output=output,
        success=True
    )
    
    assert analysis["success"] == True
    assert "abc-123-def-456" in analysis["key_info"]["id"]
    assert "Sidney_Jones_Engineer_Ford" in analysis["key_info"]["name"]
    assert len(analysis["next_steps"]) > 0
```

**File**: `tests/test_token_manager.py`
```python
def test_token_counting():
    """Test token counting accuracy."""
    manager = TokenManager(model="gpt-4", max_tokens=8000)
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"},
        {"role": "assistant", "content": "Hi there!"}
    ]
    
    count = manager.count_tokens(messages)
    assert count > 0
    assert count < 100  # Should be small for short messages

def test_warning_threshold():
    """Test warning triggers at 80% capacity."""
    manager = TokenManager(model="gpt-4", max_tokens=100)
    
    # Create messages that exceed 80 tokens
    messages = [
        {"role": "user", "content": "word " * 50}  # ~100 tokens
    ]
    
    status = manager.check_limit(messages)
    assert status["warning"] == True
```

### Manual Testing Scenarios

#### Scenario 1: Auto-Verification of Resume Duplication

**Steps**:
1. Start agent: `python agent.py`
2. Send message: "Duplicate the Master resume and call it Test_Resume"
3. Observe agent response

**Expected Output**:
```
🤖 I'll duplicate the Master resume for you.

run: python src/duplicate_resume.py --resume "Master" --new-name "Test_Resume"

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

#### Scenario 2: Token Warning

**Steps**:
1. Start agent with small token limit for testing
2. Have a long conversation (10+ exchanges)
3. Observe warning messages

**Expected Output**:
```
⚠️ WARNING: Memory at 82.3% capacity (6584/8000 tokens).
Consider clearing memory if conversation continues.

Suggestions:
  • Clear old conversation history: Use 'clear memory' command
  • Start a new conversation session
  • Export important information before clearing
```

#### Scenario 3: Error Analysis

**Steps**:
1. Send message: "Duplicate a resume that doesn't exist"
2. Observe error analysis

**Expected Output**:
```
❌ Command failed

[ERROR] No resume found matching 'NonExistent'

❌ Resume 'NonExistent' not found

💡 Suggestions to fix:
   1. List all available resumes: python src/crud/list_resumes.py
   2. Check the resume name spelling
   3. Use the resume UUID instead of name
```

### Integration Tests

**File**: `tests/test_agent_integration.py`
```python
def test_end_to_end_verification():
    """Test complete flow with verification."""
    # 1. Create test resume
    # 2. Send agent message to duplicate it
    # 3. Verify agent extracts ID and name
    # 4. Verify agent suggests next steps
    # 5. Clean up test data
```

## Success Criteria

- [ ] Agent automatically analyzes all command results
- [ ] Agent extracts key information (IDs, names, counts) from outputs
- [ ] Agent suggests 3-5 relevant next steps after successful operations
- [ ] Agent provides helpful error analysis and fix suggestions
- [ ] Token counting works accurately for all models
- [ ] Warning appears at 80% token capacity
- [ ] Critical warning appears at 95% token capacity
- [ ] Web interface shows token usage in real-time
- [ ] All unit tests pass (15+ tests)
- [ ] Manual testing scenarios work as expected
- [ ] No regressions in existing functionality

## Documentation Updates

- [ ] Update `README.md` with auto-verification examples
- [ ] Update `docs/LOCAL_AI_AGENT.md` with token management section
- [ ] Create `docs/AUTO_VERIFICATION.md` with detailed guide
- [ ] Update `agent_knowledge_base.json` with verification patterns

## Estimated Effort Breakdown

- Result Analyzer implementation: 3-4 hours
- Token Manager implementation: 2-3 hours
- Agent integration: 2-3 hours
- API endpoint: 1 hour
- Web interface updates: 1-2 hours
- Unit tests: 2-3 hours
- Integration tests: 1-2 hours
- Documentation: 1-2 hours
- **Total: 10-14 hours**

## Dependencies

- `tiktoken>=0.5.0` (for token counting)
- No breaking changes to existing code
- Backward compatible with current memory format

## Related Issues

- #23 - Parent issue (Intelligent Agent Memory Management)
- #19 - Resume Duplication (benefits from auto-verification)
- #17 - CRUD Scripts (all benefit from auto-verification)

