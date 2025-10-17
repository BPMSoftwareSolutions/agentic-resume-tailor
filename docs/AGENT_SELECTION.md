# Agent Selection in Web UI

## Overview

The web UI now allows users to select which AI agent (provider and model) they want to chat with. This feature enables switching between OpenAI (GPT-4, GPT-3.5, etc.) and Claude (Sonnet, Haiku, Opus) models directly from the chat interface.

## Features

✅ **Provider Selection** - Choose between OpenAI and Claude  
✅ **Model Selection** - Select specific models for each provider  
✅ **Model Information** - Display context window and description for each model  
✅ **Persistent Selection** - Selected agent is used for all subsequent messages  
✅ **Dynamic Loading** - Available agents are loaded from the API on page load  

## Implementation Details

### Backend Changes

#### 1. New API Endpoint: `/api/agents` (GET)

Returns all available AI providers and their models with metadata.

**Response:**
```json
{
  "success": true,
  "agents": {
    "openai": {
      "name": "Openai",
      "models": {
        "gpt-4": {
          "name": "GPT-4",
          "description": "Most capable GPT-4 model for complex tasks",
          "context_window": 8192,
          "max_output_tokens": 4096,
          "cost_per_1k_input": 0.03,
          "cost_per_1k_output": 0.06
        },
        ...
      }
    },
    "claude": {
      "name": "Claude",
      "models": {
        "claude-3-5-sonnet-20241022": {
          "name": "Claude 3.5 Sonnet",
          "description": "Claude 3.5 Sonnet (deprecated)",
          "context_window": 200000,
          "max_output_tokens": 8192,
          "cost_per_1k_input": 0.003,
          "cost_per_1k_output": 0.015
        },
        ...
      }
    }
  }
}
```

#### 2. Updated `/api/agent/chat` Endpoint (POST)

Now accepts optional `provider` and `model` parameters.

**Request Body:**
```json
{
  "message": "Your message here",
  "provider": "openai",  // optional, defaults to "openai"
  "model": "gpt-4"       // optional, uses default for provider if not specified
}
```

#### 3. Updated `get_agent_instance()` Function

Modified to accept `provider` and `model` parameters:
```python
def get_agent_instance(provider=None, model=None):
    """
    Get or create the agent instance.
    
    Args:
        provider: Optional provider name ('openai' or 'claude')
        model: Optional model name
    
    Returns:
        Agent instance or None if initialization fails
    """
```

### Frontend Changes

#### 1. Updated `agent.html`

Added agent selection UI in the card header:
- Provider dropdown selector
- Model dropdown selector (dynamically populated based on provider)
- Model information display (context window, description)

#### 2. Updated `agent.js`

Added the following functionality:

**Global State:**
```javascript
let availableAgents = {};
let selectedProvider = 'openai';
let selectedModel = 'gpt-4';
```

**New Functions:**
- `loadAvailableAgents()` - Fetches available agents from API
- `populateProviderDropdown()` - Populates provider selector
- `populateModelDropdown()` - Populates model selector based on provider
- `onProviderChange()` - Handles provider selection change
- `onModelChange()` - Handles model selection change

**Updated Functions:**
- `sendMessage()` - Now passes `provider` and `model` to API
- `autoExecuteCommand()` - Now passes `provider` and `model` to API

### Files Modified

1. **src/api/app.py**
   - Added import: `from src.agent.model_registry import get_all_models, get_providers, get_model_info, format_model_info`
   - Added new endpoint: `@app.route("/api/agents", methods=["GET"])`
   - Updated `get_agent_instance()` to accept provider and model parameters
   - Updated `agent_chat()` endpoint to accept and use provider/model from request
   - Added static file serving for web UI: `@app.route("/src/web/<path:filename>")`

2. **src/web/agent.html**
   - Added agent provider selector dropdown
   - Added agent model selector dropdown
   - Reorganized card header layout to accommodate selectors

3. **src/web/agent.js**
   - Added global state for agent selection
   - Added `loadAvailableAgents()` function
   - Added `populateProviderDropdown()` function
   - Added `populateModelDropdown()` function
   - Added `onProviderChange()` event handler
   - Added `onModelChange()` event handler
   - Updated `sendMessage()` to pass provider and model
   - Updated `autoExecuteCommand()` to pass provider and model

### Files Created

1. **tests/test_agent_selection.py**
   - Test for `/api/agents` endpoint
   - Test for agent chat with provider selection
   - Test for agent chat without provider (default behavior)

## Usage

### For Users

1. Open the AI Agent Chat interface
2. In the top-right corner, you'll see two dropdowns:
   - **Agent Provider**: Select "Openai" or "Claude"
   - **Model**: Select the specific model for the chosen provider
3. The selected agent will be used for all subsequent messages
4. Switch agents at any time by selecting a different provider/model

### For Developers

To use the agent selection API:

```javascript
// Send message with specific agent
const response = await fetch('/api/agents/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        message: 'Your message',
        provider: 'claude',
        model: 'claude-3-5-sonnet-20241022'
    })
});
```

## Testing

Run the test suite:
```bash
python tests/test_agent_selection.py
```

Expected output:
```
============================================================
Agent Selection Tests
============================================================
Testing /api/agents endpoint...
✅ /api/agents endpoint test passed!
   - Found 2 providers
   - OpenAI: 6 models
   - Claude: 8 models

Testing /api/agent/chat with provider selection...
✅ Agent chat with OpenAI provider test passed!

Testing /api/agent/chat without provider (default)...
✅ Agent chat without provider test passed!

============================================================
Results: 3/3 tests passed
============================================================
```

## Future Enhancements

- [ ] Save user's preferred agent selection to localStorage
- [ ] Display model pricing information
- [ ] Show token usage per model
- [ ] Add model comparison view
- [ ] Support for custom model configurations
- [ ] Model performance metrics and benchmarks

## Related Issues

- GitHub Issue #31 - Agent Selection in Web UI

