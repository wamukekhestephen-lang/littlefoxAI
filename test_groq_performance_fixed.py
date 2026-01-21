import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('GROQ_API_KEY')
MODEL = os.getenv('GROQ_MODEL', 'llama-3.3-70b-versatile')
headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

test_prompts = [
    "Say hello in one sentence",
    "What is 2+2?",
    "Write a haiku about programming",
]

print(f"Testing Groq API with model: {MODEL}\n")

total_time = 0
success_count = 0

for i, prompt in enumerate(test_prompts, 1):
    payload = {
        'model': MODEL,
        'messages': [{'role': 'user', 'content': prompt}],
        'temperature': 0.7,
        'max_tokens': 100
    }
    
    start = time.time()
    r = requests.post('https://api.groq.com/openai/v1/chat/completions', json=payload, headers=headers, timeout=10)
    elapsed = time.time() - start
    
    print(f"Test {i}: {prompt}")
    print(f"  Status: {r.status_code}")
    print(f"  Response time: {elapsed:.3f}s")
    
    if r.status_code == 200:
        data = r.json()
        content = data['choices'][0]['message']['content']
        print(f"  Response: {content[:80]}...")
        success_count += 1
        total_time += elapsed
    else:
        print(f"  Error: {r.json()['error']['message']}")
    print()

print(f"\nResults: {success_count}/{len(test_prompts)} successful")
if success_count > 0:
    print(f"Average response time: {total_time/success_count:.3f}s")
