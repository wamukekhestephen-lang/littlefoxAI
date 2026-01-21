import requests

response = requests.post('http://127.0.0.1:5000/ask', json={
    'user_input': 'Generate a simple Python script that prints a greeting'
})

print(f"Status: {response.status_code}")
print(f"Response: {response.text}")
