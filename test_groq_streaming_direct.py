import os
from dotenv import load_dotenv

load_dotenv()

from groq_client import groq_response_streaming

print("Testing groq_response_streaming directly...")
chunks = list(groq_response_streaming("Hello, say something short"))
print(f"Total chunks: {len(chunks)}")
for i, chunk in enumerate(chunks[:5]):  # Show first 5 chunks
    print(f"  Chunk {i}: {chunk[:50]}")
