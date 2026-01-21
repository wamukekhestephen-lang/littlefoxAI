import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('GROQ_API_KEY')
headers = {'Authorization': f'Bearer {API_KEY}'}

print('Fetching available models from Groq...')
r = requests.get('https://api.groq.com/openai/v1/models', headers=headers, timeout=10)
if r.status_code == 200:
    models = r.json()
    print('Available models:')
    for model in models['data']:
        print(f'  - {model["id"]}')
else:
    print(f'Error: {r.status_code}')
    print(r.text)
