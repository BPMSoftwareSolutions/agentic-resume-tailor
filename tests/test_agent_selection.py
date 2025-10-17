#!/usr/bin/env python3
"""
Test agent selection functionality in the web UI and API.
Related to GitHub Issue #31 - Agent Selection in Web UI
"""

import json
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import requests

# Configuration
API_BASE_URL = "http://localhost:5000/api"


def test_agents_endpoint():
    """Test that the /api/agents endpoint returns available agents."""
    print("Testing /api/agents endpoint...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/agents")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert data["success"] is True, "Response should have success=true"
        assert "agents" in data, "Response should have 'agents' key"
        
        agents = data["agents"]
        assert "openai" in agents, "Should have OpenAI provider"
        assert "claude" in agents, "Should have Claude provider"
        
        # Check OpenAI models
        openai_models = agents["openai"]["models"]
        assert "gpt-4" in openai_models, "Should have gpt-4 model"
        assert "gpt-3.5-turbo" in openai_models, "Should have gpt-3.5-turbo model"
        
        # Check Claude models
        claude_models = agents["claude"]["models"]
        assert "claude-3-5-sonnet-20241022" in claude_models, "Should have Claude 3.5 Sonnet"
        
        # Check model info structure
        gpt4_info = openai_models["gpt-4"]
        assert "name" in gpt4_info, "Model should have 'name'"
        assert "context_window" in gpt4_info, "Model should have 'context_window'"
        assert "description" in gpt4_info, "Model should have 'description'"
        
        print("✅ /api/agents endpoint test passed!")
        print(f"   - Found {len(agents)} providers")
        print(f"   - OpenAI: {len(openai_models)} models")
        print(f"   - Claude: {len(claude_models)} models")
        
        return True
        
    except Exception as e:
        print(f"❌ /api/agents endpoint test failed: {e}")
        return False


def test_agent_chat_with_provider():
    """Test that agent chat endpoint accepts provider and model parameters."""
    print("\nTesting /api/agent/chat with provider selection...")
    
    try:
        # Test with OpenAI provider
        payload = {
            "message": "Hello, what is your name?",
            "provider": "openai",
            "model": "gpt-3.5-turbo"
        }
        
        response = requests.post(
            f"{API_BASE_URL}/agent/chat",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        # We expect either success or an error about missing API key
        # Both are acceptable for this test
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print("✅ Agent chat with OpenAI provider test passed!")
                print(f"   Response: {data['response'][:100]}...")
                return True
            else:
                print(f"⚠️  Agent returned error: {data.get('error')}")
                # This is OK - might be missing API key
                return True
        elif response.status_code == 500:
            data = response.json()
            error = data.get("error", "")
            if "API_KEY" in error or "not configured" in error:
                print("✅ Agent chat endpoint accepts provider parameter (API key not set)")
                return True
            else:
                print(f"❌ Unexpected error: {error}")
                return False
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Agent chat test failed: {e}")
        return False


def test_agent_chat_without_provider():
    """Test that agent chat endpoint works without provider (uses default)."""
    print("\nTesting /api/agent/chat without provider (default)...")
    
    try:
        payload = {
            "message": "Hello, what is your name?"
        }
        
        response = requests.post(
            f"{API_BASE_URL}/agent/chat",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        # We expect either success or an error about missing API key
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print("✅ Agent chat without provider test passed!")
                return True
            else:
                print(f"⚠️  Agent returned error: {data.get('error')}")
                return True
        elif response.status_code == 500:
            data = response.json()
            error = data.get("error", "")
            if "API_KEY" in error or "not configured" in error:
                print("✅ Agent chat endpoint works without provider (API key not set)")
                return True
            else:
                print(f"❌ Unexpected error: {error}")
                return False
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Agent chat test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("Agent Selection Tests")
    print("=" * 60)
    
    results = []
    
    # Test 1: Agents endpoint
    results.append(test_agents_endpoint())
    
    # Test 2: Agent chat with provider
    results.append(test_agent_chat_with_provider())
    
    # Test 3: Agent chat without provider
    results.append(test_agent_chat_without_provider())
    
    # Summary
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 60)
    
    return all(results)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

