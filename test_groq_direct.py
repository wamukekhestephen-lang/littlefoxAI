import os
from dotenv import load_dotenv

load_dotenv()

from groq_client import groq_response

print("Testing groq_response directly...")
result = groq_response("Hello, how are you?")
print(f"Result: {result}")
print(f"Type: {type(result)}")
