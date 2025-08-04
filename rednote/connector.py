from __future__ import annotations

"""Utilities for interacting with a local Ollama instance."""

from typing import Any

import requests

# Default local Ollama endpoint
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
DEFAULT_MODEL = "llama3"


def gpt_ask(prompt: str, timeout: int = 600, model: str = DEFAULT_MODEL) -> str:
    """Send a prompt to Ollama and return the generated text."""
    r = requests.post(
        OLLAMA_URL,
        json={"model": model, "prompt": prompt, "stream": False},
        timeout=timeout,
    )
    r.raise_for_status()
    data: Any = r.json()
    return data.get("response", "").strip()
