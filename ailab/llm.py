import requests

OLLAMA_URL = "http://localhost:11434"
DEFAULT_MODEL = "qwen2.5:3b"


class LLMError(RuntimeError):
    pass


def generate(prompt, model=DEFAULT_MODEL, system=None, json_mode=False,
             temperature=0.0, timeout=300):
    payload = {"model": model, "prompt": prompt, "stream": False,
               "options": {"temperature": temperature}}
    if system:
        payload["system"] = system
    if json_mode:
        payload["format"] = "json"
    try:
        r = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=timeout)
        r.raise_for_status()
        return r.json()["response"]
    except (requests.RequestException, KeyError) as e:
        raise LLMError(str(e)) from e
