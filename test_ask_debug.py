import requests
import json

try:
    response = requests.post('http://127.0.0.1:5000/ask', 
        json={'user_input': 'hello'},
        timeout=30
    )
    print(f"Status: {response.status_code}")
    print(f"Headers: {response.headers}")
    print(f"Content-Length: {len(response.text)}")
    print(f"Response text: '{response.text}'")
    if response.text:
        try:
            print(f"JSON: {json.dumps(response.json(), indent=2)}")
        except:
            print("Not JSON")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
