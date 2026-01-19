import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "phi"

def ollama_response(prompt):
    """Try Ollama first, fallback to placeholder if not enough RAM"""
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    try:
        r = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response = r.json().get("response", "No response from Ollama")
        if response:
            return response
    except requests.exceptions.ConnectionError:
        pass
    except Exception as e:
        if "requires more system memory" in str(e):
            return "⚠️ Ollama needs more RAM. Please close unnecessary applications and restart, or upgrade your system RAM to 8GB+."
    
    # Fallback placeholder response
    return f"[Ollama not available] Your question: {prompt[:100]}... (Waiting for Ollama to load. Please restart if it's been more than 2 minutes.)"
