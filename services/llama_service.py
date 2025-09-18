import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

OLLAMA_API = "http://localhost:11434/api/generate"

def generate_counterargument(text, stance="for"):
    """
    Generate a counterargument using LLaMA via Ollama API.
    """
    prompt = f"""
    The user argued: "{text}".
    Their stance is {stance}.
    Please generate a structured counterargument with reasoning.
    """
    payload = {
        "model": "llama2",
        "prompt": prompt,
        "stream": False
    }

    logging.info("Sending counterargument request to Ollama...")
    try:
        response = requests.post(OLLAMA_API, json=payload, timeout=180)  # 3 minutes timeout
        response.raise_for_status()
        result = response.json()
        counter = result.get("response", "No counterargument generated.")
        logging.info("Counterargument received successfully.")
        return counter
    except requests.exceptions.Timeout:
        logging.error("Timeout: Ollama did not respond in 3 minutes.")
        return "Error: Ollama request timed out."
    except requests.exceptions.RequestException as e:
        logging.error("Request error: %s", e)
        return f"Error generating counterargument: {e}"
    except Exception as e:
        logging.error("Unexpected error: %s", e)
        return f"Error generating counterargument: {e}"

def summarize_debate(arguments):
    """
    Summarize the debate arguments into a short neutral summary.
    """
    prompt = f"Summarize this debate neutrally:\n\n{arguments}"
    payload = {
        "model": "llama2",
        "prompt": prompt,
        "stream": False
    }

    logging.info("Sending summary request to Ollama...")
    try:
        response = requests.post(OLLAMA_API, json=payload, timeout=180)  # 3 minutes timeout
        response.raise_for_status()
        result = response.json()
        summary = result.get("response", "No summary generated.")
        logging.info("Summary received successfully.")
        return summary
    except requests.exceptions.Timeout:
        logging.error("Timeout: Ollama did not respond in 3 minutes.")
        return "Error: Ollama request timed out."
    except requests.exceptions.RequestException as e:
        logging.error("Request error: %s", e)
        return f"Error summarizing debate: {e}"
    except Exception as e:
        logging.error("Unexpected error: %s", e)
        return f"Error summarizing debate: {e}"
