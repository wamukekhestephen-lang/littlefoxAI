"""Test the new web-search-first architecture"""
import requests
import json

# Step 1: Get guest token
print("1. Getting guest token...")
guest_response = requests.post('http://127.0.0.1:5000/auth/guest')
if guest_response.status_code != 200:
    print(f"   Failed: {guest_response.text}")
    exit(1)

token = guest_response.json()['token']
print(f"   ✓ Token obtained")

# Step 2: Ask a question using the new pipeline
print("\n2. Testing new web-search-first pipeline...")
headers = {'Authorization': f'Bearer {token}'}
test_query = "What is the current weather in New York?"

print(f"   Query: {test_query}")
print("\n   Response stream:")

response = requests.post(
    'http://127.0.0.1:5000/ask', 
    json={'message': test_query},
    headers=headers,
    timeout=60,
    stream=True
)

print(f"   Status: {response.status_code}\n")

buffer = ""
for line in response.iter_lines(decode_unicode=True):
    if line and line.startswith('data: '):
        data_str = line[6:]
        try:
            data = json.loads(data_str)
            
            if data.get('type') == 'status':
                print(f"   [STATUS] {data.get('text')}")
            elif data.get('type') == 'text':
                text = data.get('text', '')
                buffer += text
                print(text, end='', flush=True)
            elif data.get('type') == 'done':
                print(f"\n\n   [DONE]")
        except json.JSONDecodeError:
            pass

print("\n3. Full response received successfully!")
print(f"\n   Total length: {len(buffer)} characters")
