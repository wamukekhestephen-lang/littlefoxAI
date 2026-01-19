#!/usr/bin/env python3
"""Test script to verify real-time streaming and web search"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:5000"

def test_streaming():
    """Test real-time streaming response"""
    print("\n" + "="*60)
    print("TESTING: Real-Time Streaming Response with Web Search")
    print("="*60 + "\n")
    
    response = requests.post(
        f"{BASE_URL}/ask",
        json={"message": "What is the current date?", "chat_id": "test-123"},
        stream=True
    )
    
    print("Response Status:", response.status_code)
    print("Content-Type:", response.headers.get("Content-Type"))
    print("\nStreaming response:\n")
    
    full_response = ""
    event_count = 0
    
    for line in response.iter_lines():
        if line:
            line = line.decode("utf-8") if isinstance(line, bytes) else line
            
            if line.startswith("data: "):
                try:
                    data = json.loads(line[6:])
                    event_count += 1
                    
                    if data.get("type") == "text":
                        print(data.get("text", ""), end="", flush=True)
                        full_response += data.get("text", "")
                    elif data.get("type") == "status":
                        print(f"\n[{data.get('text')}]", flush=True)
                    elif data.get("type") == "done":
                        print("\n\n✓ Stream complete!", flush=True)
                except json.JSONDecodeError:
                    pass
    
    print(f"\nTotal events received: {event_count}")
    print(f"Full response length: {len(full_response)} characters")
    print("="*60 + "\n")

if __name__ == "__main__":
    # Give server time to fully start
    time.sleep(2)
    test_streaming()
