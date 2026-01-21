#!/usr/bin/env python3
"""Test Groq response times to verify performance improvement"""

import time
import os
import logging

# Suppress Flask logs
logging.getLogger('flask').setLevel(logging.ERROR)
logging.getLogger('werkzeug').setLevel(logging.ERROR)

from groq_client import groq_response

def test_groq_performance():
    print('=' * 70)
    print('GROQ RESPONSE TIME TEST')
    print('=' * 70)
    
    tests = [
        {
            'name': 'Simple Greeting',
            'query': 'Say hello in one sentence',
            'system_prompt': 'Be brief and friendly.'
        },
        {
            'name': 'Math Problem',
            'query': 'What is 15 * 3?',
            'system_prompt': 'Answer with just the number.'
        },
        {
            'name': 'Code Generation',
            'query': 'Write a Python function to add two numbers in one line',
            'system_prompt': 'Provide only the code, no explanation.'
        },
        {
            'name': 'Definition',
            'query': 'What is artificial intelligence?',
            'system_prompt': 'Give a concise definition in 1-2 sentences.'
        },
        {
            'name': 'Story Generation',
            'query': 'Write a short 2-sentence story about a robot',
            'system_prompt': 'Keep it brief and creative.'
        }
    ]
    
    times = []
    
    for i, test in enumerate(tests, 1):
        print(f'\nTest {i}: {test["name"]}')
        print(f'Query: {test["query"][:50]}...')
        
        try:
            start = time.time()
            response = groq_response(test['query'], system_prompt=test['system_prompt'])
            elapsed = time.time() - start
            times.append(elapsed)
            
            response_preview = response[:70] + '...' if len(response) > 70 else response
            print(f'✓ Time: {elapsed:.2f}s')
            print(f'  Response: {response_preview}')
        except Exception as e:
            print(f'✗ Error: {e}')
            times.append(None)
    
    # Summary
    print('\n' + '=' * 70)
    print('SUMMARY')
    print('=' * 70)
    
    valid_times = [t for t in times if t is not None]
    if valid_times:
        avg_time = sum(valid_times) / len(valid_times)
        min_time = min(valid_times)
        max_time = max(valid_times)
        
        print(f'\nSuccessful requests: {len(valid_times)}/{len(tests)}')
        print(f'Average response time: {avg_time:.2f} seconds')
        print(f'Fastest response: {min_time:.2f} seconds')
        print(f'Slowest response: {max_time:.2f} seconds')
        
        if avg_time < 1:
            print('\n✓ EXCELLENT - Groq is VERY FAST (< 1 second average)')
            print('✓ This is 5-10x faster than local Ollama')
            print('✓ Cloud inference provides instant responses')
        elif avg_time < 2:
            print('\n✓ GOOD - Groq is fast (1-2 seconds average)')
            print('✓ Still much faster than local Ollama')
        elif avg_time < 5:
            print('\n⚠ MODERATE - Response time is acceptable (2-5 seconds)')
            print('  Consider checking internet connection or API quotas')
        else:
            print('\n✗ SLOW - Responses are taking too long (> 5 seconds)')
            print('  Check Groq API status or rate limiting')
    else:
        print('✗ All requests failed. Check GROQ_API_KEY configuration.')

if __name__ == '__main__':
    test_groq_performance()
