import os
import json
import time
import requests
from typing import Optional, Generator, Dict
from dotenv import load_dotenv

# ---------------------------------------
# Environment
# ---------------------------------------
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_API_URL = "https://api.groq.com/openai/v1"
GROQ_MODEL = os.getenv("GROQ_MODEL", "mixtral-8x7b-32768")
GROQ_ENABLED = os.getenv("GROQ_ENABLED", "true").lower() in ("true", "1", "yes")

# ---------------------------------------
# Rate limiting (local safety guard)
# ---------------------------------------
RATE_LIMIT_REQUESTS = 30
RATE_LIMIT_WINDOW = 60
_request_times: list[float] = []

# ---------------------------------------
# Available models
# ---------------------------------------
AVAILABLE_MODELS = {
    "llama-3.3-70b-versatile": {"speed": "very_fast", "capability": "very_high"},
    "llama-3.1-8b-instant": {"speed": "ultra_fast", "capability": "medium"},
    "mixtral-8x7b-32768": {"speed": "fast", "capability": "balanced"},
}

# ---------------------------------------
# Helpers
# ---------------------------------------
def _check_rate_limit() -> bool:
    now = time.time()
    global _request_times
    _request_times = [t for t in _request_times if now - t < RATE_LIMIT_WINDOW]

    if len(_request_times) >= RATE_LIMIT_REQUESTS:
        return False

    _request_times.append(now)
    return True


def get_rate_limit_status() -> Dict:
    now = time.time()
    active = [t for t in _request_times if now - t < RATE_LIMIT_WINDOW]
    return {
        "requests_in_window": len(active),
        "limit": RATE_LIMIT_REQUESTS,
        "remaining": max(0, RATE_LIMIT_REQUESTS - len(active)),
        "status": "OK" if len(active) < RATE_LIMIT_REQUESTS else "LIMITED",
    }


def validate_model(model: str) -> bool:
    return model in AVAILABLE_MODELS


# ---------------------------------------
# Non-streaming response
# ---------------------------------------
def groq_response(
    prompt: str,
    system_prompt: Optional[str] = None,
    model: Optional[str] = None,
) -> Optional[str]:
    if not GROQ_API_KEY or not GROQ_ENABLED:
        return None

    if not _check_rate_limit():
        return None

    selected_model = model or GROQ_MODEL
    if not validate_model(selected_model):
        return None

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": selected_model,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 2048,
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        r = requests.post(
            f"{GROQ_API_URL}/chat/completions",
            json=payload,
            headers=headers,
            timeout=12,
        )
        r.raise_for_status()
        data = r.json()

        return (
            data.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
            .strip()
        )

    except Exception:
        return None


# ---------------------------------------
# STREAMING (critical path)
# ---------------------------------------
def groq_response_streaming(
    prompt: str,
    system_prompt: Optional[str] = None,
    model: Optional[str] = None,
) -> Generator[str, None, None]:
    """
    Ultra-fast streaming generator.
    Yields tokens immediately as they arrive.
    """
    if not GROQ_API_KEY or not GROQ_ENABLED:
        return

    if not _check_rate_limit():
        return

    selected_model = model or GROQ_MODEL
    if not validate_model(selected_model):
        return

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": selected_model,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 2048,
        "stream": True,
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        with requests.post(
            f"{GROQ_API_URL}/chat/completions",
            json=payload,
            headers=headers,
            timeout=12,
            stream=True,
        ) as r:
            r.raise_for_status()

            for line in r.iter_lines(decode_unicode=True):
                if not line or not line.startswith("data: "):
                    continue

                data_str = line[6:]
                if data_str == "[DONE]":
                    break

                try:
                    data = json.loads(data_str)
                    delta = data["choices"][0].get("delta", {})
                    token = delta.get("content")
                    if token:
                        yield token
                except Exception:
                    continue

    except Exception:
        return


# ---------------------------------------
# Diagnostics
# ---------------------------------------
def check_groq_api_key() -> Dict:
    if not GROQ_API_KEY:
        return {"valid": False, "message": "Missing GROQ_API_KEY"}

    try:
        r = requests.get(
            f"{GROQ_API_URL}/models",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
            timeout=8,
        )
        if r.status_code == 200:
            return {"valid": True, "message": "Groq API OK"}
        return {"valid": False, "message": f"Status {r.status_code}"}
    except Exception as e:
        return {"valid": False, "message": str(e)}


def get_groq_status() -> Dict:
    api_check = check_groq_api_key()
    return {
        "enabled": GROQ_ENABLED,
        "api_key_present": bool(GROQ_API_KEY),
        "default_model": GROQ_MODEL,
        "model_valid": validate_model(GROQ_MODEL),
        "rate_limit": get_rate_limit_status(),
        "api_status": api_check,
    }
