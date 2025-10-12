# Agent Web Integration Documentation

**Related to:** [GitHub Issue #12](https://github.com/BPMSoftwareSolutions/agentic-resume-tailor/issues/12)

## Overview

The Local AI Agent has been successfully integrated into the Resume Editor Web UI, allowing users to interact with the AI agent directly from their browser. This integration provides a seamless experience for resume tailoring, command execution, and AI-powered assistance.

## Features

✅ **Browser-Based Chat Interface** - Interact with the AI agent through a modern web UI  
✅ **Command Execution** - Execute whitelisted commands directly from the browser  
✅ **Persistent Memory** - Conversation history is maintained across sessions  
✅ **Security Controls** - Command whitelisting and dangerous pattern blocking  
✅ **Real-time Responses** - Instant feedback from the AI agent  
✅ **Memory Management** - View, clear, and manage conversation history  
✅ **Quick Actions** - Pre-configured shortcuts for common tasks  

## Architecture

### Backend Components

#### API Endpoints (`src/api/app.py`)

**Agent Chat Endpoint:**
- `POST /api/agent/chat` - Send messages to the AI agent
  - Request: `{"message": "User message or command"}`
  - Response: `{"success": true, "response": "Agent response"}`

**Memory Management Endpoints:**
- `GET /api/agent/memory` - Retrieve conversation history
  - Response: `{"success": true, "messages": [...]}`
- `POST /api/agent/memory/clear` - Clear conversation history
  - Response: `{"success": true, "message": "Memory cleared"}`

**Security Endpoint:**
- `POST /api/agent/validate-command` - Validate command security
  - Request: `{"command": "Command to validate"}`
  - Response: `{"valid": true/false, "error": "..."}`

#### Security Implementation

**Command Whitelist:**
```python
ALLOWED_COMMAND_PREFIXES = [
    'python src/tailor.py',
    'python src/update_resume_experience.py',
    # CRUD scripts (Issue #17)
    'python src/crud/basic_info.py',
    'python src/crud/summary.py',
    'python src/crud/technical_skills.py',
    'python src/crud/expertise.py',
    'python src/crud/achievements.py',
    'python src/crud/education.py',
    'python src/crud/certifications.py',
    'python src/crud/experience.py',
    # Testing and utilities
    'python -m pytest',
    'python -m json.tool',
    # Git commands
    'git status',
    'git log',
    'git diff',
    # File system commands
    'ls',
    'dir',
    'pwd',
    'echo',
    'cat',
    'type'
]
```

**Blocked Patterns:**
```python
BLOCKED_COMMAND_PATTERNS = [
    'rm -rf',
    'del /f /s /q',
    'format',
    'dd if=',
    'mkfs',
    '> /dev/',
    'chmod 777',
    'sudo',
    'su ',
]
```

### Frontend Components

#### Agent Interface (`src/web/agent.html`)

The agent interface provides:
- Chat message display with role-based styling
- Input field for user messages
- Quick action buttons for common tasks
- Memory management controls
- Conversation history viewer

#### Agent JavaScript (`src/web/agent.js`)

Key functions:
- `sendMessage()` - Send user message to agent
- `loadMemory()` - Load conversation history
- `clearMemory()` - Clear conversation history
- `viewMemory()` - Display full conversation history
- `addMessageToChat()` - Add message to chat display

## Usage Guide

### Accessing the Agent Interface

1. **From Dashboard:**
   - Navigate to `http://localhost:8080/dashboard.html`
   - Click the "AI Agent" button in the navigation bar

2. **From Resume Editor:**
   - Navigate to `http://localhost:8080/index.html`
   - Click the "AI Agent" button in the navigation bar

3. **Direct Access:**
   - Navigate to `http://localhost:8080/agent.html`

### Chatting with the Agent

**Basic Chat:**
```
User: How can I tailor my resume for a software engineering role?
Agent: I can help you tailor your resume! To get started, I'll need...
```

**Executing Commands:**
```
User: run: python src/tailor.py --help
Agent: ✅ Command executed successfully:
usage: tailor.py [-h] --resume RESUME --jd JD --out OUT...
```

**CRUD Operations (Natural Language):**
```
User: Add Python to my technical skills
Agent: I'll add Python to your technical skills.
run: python src/crud/technical_skills.py --resume "Master Resume" --append-to-category "languages" "Python"
✅ Successfully added Python to languages category

User: Update my title to Principal Architect
Agent: I'll update your title.
run: python src/crud/basic_info.py --resume "Master Resume" --update-title "Principal Architect"
✅ Successfully updated title

User: List my certifications
Agent: I'll list your certifications.
run: python src/crud/certifications.py --resume "Master Resume" --list
✅ Certifications (7 entries):
  [0] SAFe 5 Certified DevOps Practitioner
  ...
```

### Quick Actions

The interface provides pre-configured quick actions:
- **Tailor Resume** - Start resume tailoring conversation
- **View Jobs** - Ask about available job listings
- **Git Status** - Check repository status
- **Run Tests** - Execute test suite

### Memory Management

**View History:**
1. Click "View History" button
2. Modal displays all conversation messages
3. Messages are numbered and color-coded by role

**Clear Memory:**
1. Click "Clear Memory" button
2. Confirm the action
3. Conversation history is cleared
4. Fresh conversation starts

## Security Considerations

### Command Execution Security

1. **Whitelist Enforcement:**
   - Only commands starting with allowed prefixes are executed
   - All other commands are blocked with error message

2. **Dangerous Pattern Blocking:**
   - Commands containing dangerous patterns are blocked
   - Prevents destructive operations (rm -rf, format, etc.)

3. **Timeout Protection:**
   - Commands timeout after 30 seconds
   - Prevents hanging processes

4. **Error Handling:**
   - All errors are caught and displayed safely
   - No sensitive information leaked in error messages

### API Security

1. **CORS Configuration:**
   - CORS enabled for local development
   - Should be restricted in production

2. **Input Validation:**
   - All inputs validated before processing
   - Empty messages rejected

3. **Environment Variables:**
   - OpenAI API key stored in environment
   - Never exposed to client

## Testing

### Unit Tests

**Agent API Tests** (`tests/test_api.py`):
- `TestAgentChatEndpoint` - Chat functionality tests
- `TestAgentMemoryEndpoint` - Memory retrieval tests
- `TestAgentMemoryClearEndpoint` - Memory clearing tests
- `TestAgentCommandValidation` - Security validation tests

**Agent Core Tests** (`tests/test_agent.py`):
- `TestMemoryManager` - Memory persistence tests
- `TestCommandExecutor` - Command execution tests
- `TestAgent` - Agent integration tests

### Running Tests

```bash
# Run all agent-related tests
python -m pytest tests/test_api.py::TestAgentChatEndpoint -v
python -m pytest tests/test_api.py::TestAgentMemoryEndpoint -v
python -m pytest tests/test_agent.py -v

# Run all tests
python -m pytest tests/ -v
```

## Configuration

### Environment Variables

```bash
# Required for agent functionality
export OPENAI_API_KEY='your-api-key-here'

# Optional: Specify OpenAI model
export OPENAI_MODEL='gpt-4'
```

### API Configuration

In `src/web/agent.js`:
```javascript
const API_BASE_URL = 'http://localhost:5000/api';
```

## Troubleshooting

### Agent Not Responding

**Issue:** Agent returns error about missing API key

**Solution:**
```bash
export OPENAI_API_KEY='your-api-key-here'
# Restart the API server
python src/api/app.py
```

### Command Blocked

**Issue:** Command is blocked by security

**Solution:**
- Check if command is in whitelist
- Verify command doesn't contain blocked patterns
- Use allowed command prefixes

### Memory Not Persisting

**Issue:** Conversation history not saved

**Solution:**
- Check file permissions for `memory.json`
- Verify API server has write access
- Check browser console for errors

## Future Enhancements

Potential improvements for future releases:

1. **Enhanced Security:**
   - Role-based access control
   - Command approval workflow
   - Audit logging

2. **UI Improvements:**
   - Markdown rendering in messages
   - Code syntax highlighting
   - File upload support

3. **Agent Capabilities:**
   - Resume analysis and scoring
   - Job description parsing
   - Automated resume tailoring

4. **Integration:**
   - Direct resume editing from chat
   - Job listing management
   - Document generation

## Related Documentation

- [Local AI Agent Documentation](LOCAL_AI_AGENT.md)
- [Resume Editor Web Interface](RESUME_EDITOR_WEB_INTERFACE.md)
- [Multi-Resume Support](MULTI_RESUME_SUPPORT.md)

## Support

For issues or questions:
1. Check existing GitHub issues
2. Review troubleshooting section
3. Create new issue with detailed description

