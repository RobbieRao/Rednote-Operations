import base64
import json
import time
from pathlib import Path
from typing import Any, Generator

import requests

# Local HTTP endpoint exposed by the browser userscript
CONNECTOR_URL = "http://127.0.0.1:5123/connector"


def exec_js(code: str) -> Any:
    """Execute JavaScript in the browser via the local connector."""
    r = requests.post(CONNECTOR_URL, json={"code": code}, timeout=15)
    r.raise_for_status()
    return r.json()["result"]


def wait_done(timeout: int = 300) -> dict:
    """Wait for the last task to report ``type=='done'``."""
    t0 = time.time()
    while time.time() - t0 < timeout:
        task = exec_js("window.Meet?.Connector?.tasks.slice(-1)[0]||{}")
        if task.get("type") == "done":
            return task
        time.sleep(1)
    raise RuntimeError("浏览器端超时（>5min）")


def upload_pdf(path: str) -> None:
    """Upload a PDF file via the connector."""
    b64 = base64.b64encode(Path(path).read_bytes()).decode()
    name = Path(path).name
    exec_js(
        f"""window.Meet.Connector.tasks.push({{
        type:\"pending\",file:{{base64String:{json.dumps(b64)},name:{json.dumps(name)}}}
    }});"""
    )
    wait_done(180)


def stream_gpt_ask(prompt: str, timeout: int = 600) -> Generator[str, None, None]:
    """Send a prompt and yield streamed response text pieces."""
    exec_js(
        f"""window.Meet.Connector.tasks.push({{
        type:\"pending\",requestText:{json.dumps(prompt)}
    }});"""
    )
    t0 = time.time()
    last = ""
    while time.time() - t0 < timeout:
        task = exec_js("window.Meet?.Connector?.tasks.slice(-1)[0]||{}")
        text = task.get("responseText", "") or ""
        if text.startswith(last):
            chunk = text[len(last):]
        else:
            chunk = text
        if chunk:
            yield chunk
            last = text
        if task.get("type") == "done":
            break
        time.sleep(1)
    else:
        raise RuntimeError("浏览器端超时（>5min）")


def gpt_ask(prompt: str, timeout: int = 600) -> str:
    """Send a prompt and return the model response text."""
    return "".join(stream_gpt_ask(prompt, timeout)).strip()

