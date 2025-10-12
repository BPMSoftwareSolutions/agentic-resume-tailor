#!/usr/bin/env python3
"""
Test script to verify emoji encoding works on Windows
"""

import sys
import os

# Fix Windows console encoding for emoji support
if sys.platform == 'win32':
    try:
        # Set console to UTF-8 mode
        os.system('chcp 65001 > nul')
        # Reconfigure stdout/stderr to use UTF-8
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        # If reconfiguration fails, continue without emoji support
        pass

# Test emoji output
print("Testing emoji output:")
print("=" * 60)
print("📋 Processing job description...")
print("🔍 Extracting keywords...")
print("📝 Tailoring resume...")
print("🎨 Generating HTML resume...")
print("✅ Command executed successfully")
print("❌ Command failed")
print("🔧 Executing command")
print("💬 User input")
print("🤖 AI response")
print("=" * 60)
print("✅ All emoji characters displayed successfully!")

