import requests
import json

# First, get a guest token
print("1. Getting guest token...")
guest_response = requests.post('http://127.0.0.1:5000/auth/guest')
print(f"   Status: {guest_response.status_code}")
guest_data = guest_response.json()
print(f"   Response: {json.dumps(guest_data, indent=2)}")

if guest_response.status_code != 200:
    print("Failed to get guest token!")
    exit(1)

# Extract token
token = guest_data.get('token')
print(f"   Token: {token[:20]}..." if token else "   No token!")

# Now ask a question with the token
print("\n2. Asking a question...")
headers = {'Authorization': f'Bearer {token}'}
ask_response = requests.post(
    'http://127.0.0.1:5000/ask', 
    json={'message': 'Generate a simple Python script that prints a greeting'},
    headers=headers,
    timeout=30,
    stream=True
)

print(f"   Status: {ask_response.status_code}")
print(f"\n   Response stream:")

# Read streaming response
for line in ask_response.iter_lines(decode_unicode=True):
    if line:
        print(f"     {line[:100]}")
