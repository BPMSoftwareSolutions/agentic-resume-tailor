# Local AI Agent Documentation

**Related to GitHub Issue #8**

## Overview

The Local AI Agent is a Python-based interactive command-line tool that provides natural language automation using OpenAI's API. It enables conversational interaction with AI models, local command execution, and persistent memory across sessions.

## Features

- 🤖 **Natural Language Interaction**: Chat with OpenAI models directly from your terminal
- 🔧 **Local Command Execution**: Execute system commands using the `run:` prefix
- 💾 **Persistent Memory**: Conversation history is saved and restored across sessions
- 🔒 **Secure**: API keys are managed via environment variables
- 🎯 **Simple Interface**: Easy-to-use command-line interface

## Installation

### Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Setup

1. **Install dependencies:**

```bash
pip install -r requirements.txt
```

2. **Configure environment variables:**

Create a `.env` file in the project root (or set environment variables):

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=your-actual-api-key-here
OPENAI_MODEL=gpt-4
```

Alternatively, export the environment variable:

```bash
# Linux/Mac
export OPENAI_API_KEY='your-api-key-here'

# Windows (PowerShell)
$env:OPENAI_API_KEY='your-api-key-here'

# Windows (CMD)
set OPENAI_API_KEY=your-api-key-here
```

## Usage

### Starting the Agent

Run the agent from the project root:

```bash
python agent.py
```

You should see:

```
🤖 Local AI Agent Started
==================================================
Commands:
  - Type 'run: <command>' to execute local commands
  - Type 'exit' or 'quit' to stop
  - Type anything else to chat with the AI
==================================================

💬 >
```

### Basic Interaction

**Chat with the AI:**

```
💬 > What's the weather like today?
🤖 I don't have access to real-time weather data, but I can help you find it...
```

**Execute local commands:**

```
💬 > run: ls -la
🔧 Executing command: ls -la
✅ Command executed successfully:
total 48
drwxr-xr-x  12 user  staff   384 Oct 12 10:30 .
drwxr-xr-x   5 user  staff   160 Oct 11 15:20 ..
-rw-r--r--   1 user  staff  1234 Oct 12 10:30 agent.py
...
```

**Check Git status:**

```
💬 > run: git status
🔧 Executing command: git status
✅ Command executed successfully:
On branch main
nothing to commit, working tree clean
```

**Exit the agent:**

```
💬 > exit
👋 Goodbye!
💾 Memory saved
```

## Examples

### Example 1: Getting Help with Code

```
💬 > How do I read a JSON file in Python?

🤖 Here's how to read a JSON file in Python:

```python
import json

with open('file.json', 'r') as f:
    data = json.load(f)
```

This opens the file, parses the JSON, and stores it in the `data` variable.
```

### Example 2: Combining AI and Commands

```
💬 > What files are in the current directory?

🤖 I can help you check that. Try running: run: ls

💬 > run: ls
🔧 Executing command: ls
✅ Command executed successfully:
agent.py
memory.json
requirements.txt
...
```

### Example 3: Multi-turn Conversation

```
💬 > I need to create a new Python file

🤖 I can help with that! What would you like to name the file and what should it contain?

💬 > Create a file called hello.py with a simple hello world

🤖 You can create it with this command: run: echo "print('Hello, World!')" > hello.py

💬 > run: echo "print('Hello, World!')" > hello.py
🔧 Executing command: echo "print('Hello, World!')" > hello.py
✅ Command executed successfully:
```

## Memory Persistence

The agent automatically saves conversation history to `memory.json` in the current directory. This file includes:

- All user messages
- All assistant responses
- Command execution results

The memory is:
- **Loaded** automatically when the agent starts
- **Saved** after each interaction
- **Preserved** across sessions

To start fresh, simply delete `memory.json`:

```bash
rm memory.json
```

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | None | Yes |
| `OPENAI_MODEL` | Model to use | `gpt-4` | No |

### Supported Models

- `gpt-4` (recommended)
- `gpt-4-turbo-preview`
- `gpt-3.5-turbo`
- Any other OpenAI chat model

## Security Considerations

⚠️ **Important Security Notes:**

1. **Never commit your `.env` file** - It contains your API key
2. **Command execution** - The agent can execute any command you type with `run:`
3. **API costs** - Each interaction uses your OpenAI API quota
4. **Memory file** - Contains conversation history in plain text

### Best Practices

- Keep your API key secure
- Review commands before executing them
- Monitor your OpenAI API usage
- Don't share your `memory.json` if it contains sensitive information

## Troubleshooting

### "OPENAI_API_KEY environment variable is required"

**Solution:** Set your API key in the environment or `.env` file.

```bash
export OPENAI_API_KEY='your-key-here'
```

### "Command timed out after 30 seconds"

**Solution:** The command took too long to execute. Try a simpler command or increase the timeout in `agent.py`.

### "Error communicating with OpenAI"

**Possible causes:**
- Invalid API key
- Network connectivity issues
- OpenAI API is down
- Rate limit exceeded

**Solution:** Check your API key, internet connection, and OpenAI status page.

### Memory file is corrupted

**Solution:** Delete `memory.json` and start fresh:

```bash
rm memory.json
python agent.py
```

## Architecture

### Components

1. **Agent** - Main orchestrator class
   - Manages OpenAI client
   - Coordinates memory and command execution
   - Handles user interaction loop

2. **MemoryManager** - Handles conversation persistence
   - Loads/saves `memory.json`
   - Manages message history
   - Provides messages to OpenAI API

3. **CommandExecutor** - Executes local commands
   - Detects `run:` prefix
   - Executes commands via subprocess
   - Captures output and errors

### Data Flow

```
User Input
    ↓
Agent.process_message()
    ↓
Is it a command? (starts with "run:")
    ↓                           ↓
   Yes                         No
    ↓                           ↓
CommandExecutor.execute()   OpenAI API
    ↓                           ↓
Capture output            Get AI response
    ↓                           ↓
    └─────→ MemoryManager ←─────┘
                ↓
           Save to memory.json
                ↓
           Return response
```

## Testing

Run the test suite:

```bash
# Run all agent tests
python -m pytest tests/test_agent.py -v

# Run with coverage
python -m pytest tests/test_agent.py --cov=agent --cov-report=html

# Run specific test
python -m pytest tests/test_agent.py::TestAgent::test_agent_init -v
```

## Future Enhancements

Potential improvements for Phase 2:

- 🔌 **Plugin Architecture** - Extensible tool system
- 📁 **File Operations** - Read/write files with AI assistance
- 🔀 **Git Integration** - Automated Git workflows
- 🌐 **API Connectors** - Integrate with external services
- 🎨 **Rich Terminal UI** - Better formatting and colors
- 📊 **Usage Analytics** - Track API usage and costs
- 🔄 **Streaming Responses** - Real-time AI responses
- 🧠 **Context Management** - Smart memory pruning

## Contributing

When contributing to the agent:

1. Follow TDD principles - write tests first
2. Update documentation for new features
3. Link commits to GitHub issues
4. Ensure all tests pass before committing

## License

This project is part of the Agentic Resume Tailor system.

## Support

For issues or questions:
- Create a GitHub issue
- Reference issue #8 for agent-related topics
- Check the troubleshooting section above

