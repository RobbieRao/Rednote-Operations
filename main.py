from __future__ import annotations

"""Program entry point for Rednote Operations.

Launches the Gradio interface that generates slides from PDF papers using
an Ollama language model running locally."""

from rednote.ui import launch

if __name__ == "__main__":
    launch()
