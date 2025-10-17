#!/usr/bin/env python3
"""List available Claude/Anthropic models for a given API key.

This script tries multiple common SDK methods to list models and prints
the names and basic metadata. Use it to confirm which models your key
can access (helps troubleshoot NotFound errors).

Usage:
  python scripts/list_claude_models.py --key <API_KEY>
"""

import argparse
import sys


def try_call(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        return e


def main():
    parser = argparse.ArgumentParser(description="List Anthropic/Claude models for an API key")
    parser.add_argument("--key", required=True, help="Anthropic/Claude API key")
    args = parser.parse_args()

    try:
        from anthropic import Anthropic
    except ImportError:
        print("The 'anthropic' package is required. Install with: pip install anthropic")
        sys.exit(2)

    client = Anthropic(api_key=args.key)

    print("Attempting to list models using several possible client methods...")

    # Try common names for listing models in SDKs
    candidates = [
        ("client.models.list()", lambda: client.models.list()),
        ("client.list_models()", lambda: client.list_models()),
        ("client.models()", lambda: client.models()),
        ("client.get_models()", lambda: client.get_models()),
        ("client.models_list()", lambda: client.models_list()),
    ]

    for desc, fn in candidates:
        res = try_call(fn)
        if isinstance(res, Exception):
            print(f"- {desc}: ERROR -> {type(res).__name__}: {res}")
        else:
            print(f"- {desc}: SUCCESS")
            try:
                # Try to extract model names
                names = []
                # Common response shapes: dict with 'data' list, or list of models
                if isinstance(res, dict) and "data" in res:
                    for item in res["data"]:
                        if isinstance(item, dict) and "id" in item:
                            names.append(item.get("id"))
                        elif isinstance(item, dict) and "name" in item:
                            names.append(item.get("name"))
                elif isinstance(res, list):
                    for item in res:
                        if isinstance(item, dict):
                            names.append(item.get("id") or item.get("name"))
                        else:
                            names.append(str(item))
                else:
                    # Fallback: stringify
                    names = [str(res)[:500]]

                print("  Models detected (sample):")
                for n in names[:50]:
                    print("   -", n)
                # Stop after first successful listing
                return
            except Exception as e:
                print("  Could not parse response:", type(e), e)
                return

    print("No listing method succeeded. The API or SDK may not support model listing with this client.\nCheck your Anthropic account dashboard or the SDK docs for available models.")


if __name__ == "__main__":
    main()
