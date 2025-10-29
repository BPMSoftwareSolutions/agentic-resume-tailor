#!/usr/bin/env python
# To guarantee the correct environment, run this script with:
#   ..\.venv\Scripts\python.exe run_encrypt_demo.py
# Or use the full path to the venv Python executable.
import subprocess
import os
import sys
import encrypt_practice

if __name__ == "__main__":
    bill_rate = "125.00"  # Example bill rate
    key = os.urandom(32)  # 256-bit key
    env = os.environ.copy()
    env["AES_KEY_HEX"] = key.hex()

    # Set working directory to project root
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    # Use correct relative path from python-practice directory
    cli_path = os.path.join("..", "ts-cli", "encrypt-billrate.ts")

    # Use the local ts-node binary directly for reliability
    ts_node_path = os.path.abspath(os.path.join("..", "ts-cli", "node_modules", ".bin", "ts-node.cmd"))
    result = subprocess.run(
        [ts_node_path, cli_path, bill_rate, key.hex()],
        capture_output=True,
        text=True,
        env=env
    )

    encrypted = result.stdout.strip()
    print("\n--- Output from TypeScript (encrypted, base64) ---")
    print(encrypted)

    # Decrypt using Python
    decrypted = encrypt_practice.decrypt_bill_rate(encrypted, key)
    print("\n--- Decrypted in Python ---")
    print(decrypted)
