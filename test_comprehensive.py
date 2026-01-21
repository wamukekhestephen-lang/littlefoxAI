import os
import sys
sys.path.insert(0, '/Users/k/Desktop/my_ai_assistant')
os.chdir('c:/Users/k/Desktop/my_ai_assistant')

from dotenv import load_dotenv
load_dotenv()

from main import comprehensive_response

print("Testing comprehensive_response...")
result_text, quality_report = comprehensive_response("Generate a simple Python script that prints a greeting", mode="online")
print(f"\nResult: {result_text[:100]}")
print(f"Quality Report: {quality_report}")
