#!/usr/bin/env python3
"""
Quick test to verify Ollama is working with your app
"""

import requests
from ollama_client import ollama_response

def test_ollama():
    print("🧪 Testing Ollama Connection...")
    print("=" * 50)
    
    try:
        # Test 1: Simple response
        print("\n✅ Test 1: Simple Response")
        response = ollama_response("Hello! How are you?")
        print(f"Response: {response[:200]}...")
        
        # Test 2: Check Ollama API
        print("\n✅ Test 2: Checking Ollama API")
        api_response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if api_response.status_code == 200:
            models = api_response.json().get("models", [])
            print(f"Available models: {[m['name'] for m in models]}")
        else:
            print("❌ Ollama API not responding")
            return False
        
        # Test 3: Longer response
        print("\n✅ Test 3: Multi-turn Conversation")
        response = ollama_response("What is Python used for?")
        print(f"Response: {response[:300]}...")
        
        print("\n" + "=" * 50)
        print("✅ ALL TESTS PASSED! Ollama is working!")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to Ollama at localhost:11434")
        print("   Make sure Ollama is running: ollama serve")
        return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    success = test_ollama()
    exit(0 if success else 1)
