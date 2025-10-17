# Claude Configuration

## Overview

The system has been updated to use **Claude Sonnet 4.5** (`claude-sonnet-4-5-20250929`) as the default Claude model, with support for the `CLAUDE_API_KEY` environment variable.

## Configuration Details

### Default Model

- **Provider**: Claude (Anthropic)
- **Model**: `claude-sonnet-4-5-20250929`
- **Name**: Claude Sonnet 4.5
- **Context Window**: 200,000 tokens
- **Description**: Claude 4.5 Sonnet - balanced capability

### Environment Variables

The system supports two environment variables for Claude API authentication:

1. **CLAUDE_API_KEY** (Recommended)
   - Primary environment variable for Claude API key
   - Used by the agent system

2. **ANTHROPIC_API_KEY** (Fallback)
   - Alternative environment variable
   - Used if CLAUDE_API_KEY is not set
   - Provides backward compatibility

### Files Updated

1. **src/agent/model_registry.py**
   - Updated `get_default_model()` to return `claude-sonnet-4-5-20250929` for Claude provider

2. **src/agent/llm_provider.py**
   - Updated `ClaudeProvider.__init__()` default model parameter

3. **agent.py**
   - Updated fallback default model for Claude

4. **src/api/app.py**
   - Updated `get_agent_instance()` to use new Claude default

5. **scripts/test_claude_api.py**
   - Updated test script to use new Claude model

## Usage

### Setting Up Claude

1. **Set the API Key**
   ```bash
   # On Windows (PowerShell)
   $env:CLAUDE_API_KEY = "your-api-key-here"
   
   # On Linux/Mac
   export CLAUDE_API_KEY="your-api-key-here"
   ```

2. **Using with Agent CLI**
   ```bash
   python agent.py --provider claude
   # Uses claude-sonnet-4-5-20250929 by default
   
   # Or specify a different Claude model
   python agent.py --provider claude --model claude-3-5-sonnet-20241022
   ```

3. **Using with Web UI**
   - Open http://localhost:5000/src/web/agent.html
   - Select "Claude" from the Agent Provider dropdown
   - Select "Claude Sonnet 4.5" from the Model dropdown
   - Start chatting!

4. **Using with API**
   ```bash
   curl -X POST http://localhost:5000/api/agent/chat \
     -H "Content-Type: application/json" \
     -d '{
       "message": "Hello, Claude!",
       "provider": "claude",
       "model": "claude-sonnet-4-5-20250929"
     }'
   ```

### Available Claude Models

The system supports the following Claude models:

**Claude 4.x (Recommended)**
- `claude-sonnet-4-5-20250929` - Claude Sonnet 4.5 (Default)
- `claude-haiku-4-5-20251001` - Claude Haiku 4.5
- `claude-opus-4-1-20250805` - Claude Opus 4.1

**Claude 3.x (Deprecated)**
- `claude-3-5-sonnet-20241022` - Claude 3.5 Sonnet
- `claude-3-5-haiku-20241022` - Claude 3.5 Haiku
- `claude-3-opus-20240229` - Claude 3 Opus
- `claude-3-sonnet-20240229` - Claude 3 Sonnet
- `claude-3-haiku-20240307` - Claude 3 Haiku

## Testing

### Verify Configuration

```bash
python -c "from src.agent.model_registry import get_default_model; print(get_default_model('claude'))"
# Output: claude-sonnet-4-5-20250929
```

### Test Claude API

```bash
python scripts/test_claude_api.py \
  --key "your-api-key" \
  --prompt "Say hello" \
  --model claude-sonnet-4-5-20250929
```

### Test with Agent

```bash
export CLAUDE_API_KEY="your-api-key"
python agent.py --provider claude
```

## Pricing

Claude Sonnet 4.5 pricing:
- **Input**: $0.004 per 1K tokens
- **Output**: $0.016 per 1K tokens

## Model Capabilities

Claude Sonnet 4.5 is optimized for:
- Balanced performance and cost
- Complex reasoning tasks
- Long context understanding (200K tokens)
- Code generation and analysis
- Resume tailoring and optimization

## Troubleshooting

### "CLAUDE_API_KEY not set" Error

**Solution**: Set the environment variable before running the agent
```bash
export CLAUDE_API_KEY="your-api-key"
python agent.py --provider claude
```

### "Model not found" Error

**Solution**: Use a model from the available list above. The system will fall back to the default if an unknown model is specified.

### API Rate Limiting

If you encounter rate limiting:
- Wait a few seconds before retrying
- Consider using a different model (Haiku is faster)
- Check your Anthropic account usage

## Related Documentation

- [Agent Selection in Web UI](./AGENT_SELECTION.md)
- [Model Registry](../src/agent/model_registry.py)
- [LLM Provider](../src/agent/llm_provider.py)

## Support

For issues with Claude API:
- Check [Anthropic Documentation](https://docs.anthropic.com)
- Verify your API key is valid
- Ensure you have sufficient credits

