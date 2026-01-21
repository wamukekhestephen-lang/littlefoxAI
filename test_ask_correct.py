import requests
import json

try:
    response = requests.post('http://127.0.0.1:5000/ask', 
        json={'message': 'hello'},
        timeout=30
    )
    print(f"Status: {response.status_code}")
    print(f"Content-Type: {response.headers.get('Content-Type')}")
    
    # For streaming responses, read line by line
    print("\nStreaming response:")
    for line in response.iter_lines(decode_unicode=True):
        if line:
            print(f"  {line}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
