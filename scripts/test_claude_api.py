#!/usr/bin/env python3
"""Simple smoke test for Anthropic Claude messages API.

Usage:
  python scripts/test_claude_api.py --key <API_KEY> --prompt "Say hello" [--model MODEL]

This will call the Claude messages.create endpoint and print the assistant reply.
"""

import argparse
import os
import sys


def main():
    parser = argparse.ArgumentParser(description="Smoke test Anthropic Claude messages API")
    parser.add_argument("--key", required=True, help="Anthropic/Claude API key")
    parser.add_argument("--prompt", required=True, help="Prompt to send to Claude")
    parser.add_argument("--model", default="claude-sonnet-4-5-20250929", help="Claude model name")
    parser.add_argument("--max-tokens", type=int, default=3000, help="max_tokens to request")
    args = parser.parse_args()

    try:
        from anthropic import Anthropic, NotFoundError
    except ImportError:
        print("The 'anthropic' package is required. Install with: pip install anthropic")
        sys.exit(2)

    # Validate model name against local registry and provide suggestions
    try:
        from src.agent.model_registry import get_all_models
        available = list(get_all_models('claude').keys())
    except Exception:
        available = []

    if available and args.model not in available:
        print(f"Warning: requested model '{args.model}' not found in local registry.\nAvailable Claude models: {', '.join(available)}")

    client = Anthropic(api_key=args.key)

    # Build the messages shape expected by src.agent.llm_provider
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": args.prompt}
    ]

    # Prepare request parameters similar to ClaudeProvider.chat_completion
    claude_messages = [m for m in messages if m.get("role") != "system"]
    system_message = next((m.get("content") for m in messages if m.get("role") == "system"), None)

    request_params = {
        "model": args.model,
        "messages": claude_messages,
        "max_tokens": args.max_tokens,
    }
    if system_message:
        request_params["system"] = system_message

    try:
        response = client.messages.create(**request_params)
        # Attempt to print the assistant text
        try:
            text = response.content[0].text
        except Exception:
            # Fallback if response shaped differently
            text = str(response)

        print("=== Claude response ===")
        print(text)
    except NotFoundError as e:
        print("Anthropic returned NotFoundError (likely invalid or deprecated model):", e)
        if available:
            print("Available Claude models in registry:")
            for m in available:
                print(" -", m)
        sys.exit(2)
    except Exception as e:
        print("Error calling Anthropic API:", type(e), e)
        # If the exception wraps HTTP details, print repr
        try:
            print(repr(e))
        except Exception:
            pass


if __name__ == "__main__":
    main()
