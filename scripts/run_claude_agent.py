#!/usr/bin/env python3
"""Run the local agent with Anthropic Claude.

This small helper sets the CLAUDE_API_KEY environment variable for the
subprocess that launches `agent.py` and then runs the agent with the
`--provider claude` flag. It supports an optional `--persist` flag to
store the key in the current user's environment using Windows `setx`.

Usage:
  python scripts/run_claude_agent.py --key <YOUR_KEY> [--persist] [--model MODEL]

Security:
  Avoid committing API keys. Prefer passing the key at runtime or use a
  secure secret manager. If you use `--persist` it will save the key to
  your Windows user environment variables (visible to processes run as your user).
"""

import argparse
import os
import shlex
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description="Run agent.py with Anthropic Claude")
    parser.add_argument("--key", required=True, help="Anthropic/Claude API key")
    parser.add_argument("--persist", action="store_true", help="Persist key with setx for current user (Windows)")
    parser.add_argument("--model", default="claude-3-5-sonnet-20241022", help="Claude model to use")
    parser.add_argument("--no-auto-execute", action="store_true", help="Pass --no-auto-execute to agent.py")

    args = parser.parse_args()

    # Optionally persist the key in user environment (Windows setx)
    if args.persist:
        if sys.platform.startswith("win"):
            print("Persisting CLAUDE_API_KEY to user environment via setx (Windows)")
            # setx does not take piped input; use subprocess
            subprocess.run(["setx", "CLAUDE_API_KEY", args.key], check=True)
            print("Persisted. Start a new shell or log out/in to see the variable in new sessions.")
        else:
            print("--persist currently supports only Windows (setx). Skipping persist.")

    # Prepare environment for the subprocess
    env = os.environ.copy()
    env["CLAUDE_API_KEY"] = args.key
    # Ensure PYTHONPATH includes repo root so agent.py can import src
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    env["PYTHONPATH"] = env.get("PYTHONPATH", repo_root)

    # Build command
    cmd = [sys.executable, os.path.join(repo_root, "agent.py"), "--provider", "claude", "--model", args.model]
    if args.no_auto_execute:
        cmd.append("--no-auto-execute")

    print("Running:", shlex.join(cmd))

    # Launch the agent interactively, forwarding console IO
    subprocess.run(cmd, env=env)


if __name__ == "__main__":
    main()
