#!/usr/bin/env python3
"""
Resume Editor Startup Script

Starts both the Flask API server and opens the web interface in the default browser.
Related to GitHub Issue #2
"""

import sys
import time
import webbrowser
import subprocess
from pathlib import Path
import threading

def start_api_server():
    """Start the Flask API server."""
    print("🚀 Starting Flask API server...")
    api_path = Path(__file__).parent / "src" / "api" / "app.py"
    
    try:
        subprocess.run([sys.executable, str(api_path)], check=True)
    except KeyboardInterrupt:
        print("\n✋ API server stopped")
    except Exception as e:
        print(f"❌ Error starting API server: {e}")

def open_web_interface():
    """Open the web interface in the default browser."""
    time.sleep(2)  # Wait for API server to start
    
    web_path = Path(__file__).parent / "src" / "web" / "index.html"
    web_url = f"file://{web_path.absolute()}"
    
    print(f"🌐 Opening web interface: {web_url}")
    webbrowser.open(web_url)

def main():
    """Main entry point."""
    print("=" * 80)
    print("Resume Editor - Web Interface")
    print("=" * 80)
    print()
    print("📋 This will start:")
    print("   1. Flask API server on http://localhost:5000")
    print("   2. Web interface in your default browser")
    print()
    print("💡 Press Ctrl+C to stop the server")
    print()
    
    # Start web interface in a separate thread
    web_thread = threading.Thread(target=open_web_interface, daemon=True)
    web_thread.start()
    
    # Start API server (blocking)
    start_api_server()

if __name__ == "__main__":
    main()

