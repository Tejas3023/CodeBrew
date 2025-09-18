import requests
import json

OLLAMA_API = "http://localhost:11434/api/generate"

payload = {
    "model": "llama2",
    "prompt": "Write a short counterargument to: 'AI will dominate humans.'",
    "stream": False
}

try:
    response = requests.post(OLLAMA_API, json=payload, timeout=120)
    print("Status code:", response.status_code)
    print("Response JSON:", json.dumps(response.json(), indent=2))
except Exception as e:
    print("Error calling Ollama:", e)
