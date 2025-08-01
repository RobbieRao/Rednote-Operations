from __future__ import annotations

"""Program entry point for Rednote Operations.

This script ensures the browser userscript is reachable before
starting the Gradio interface. When the local connector isn't
running, the previous implementation would simply raise a generic
``SystemExit`` which makes it hard to understand the fix.  We now
provide a clearer message so users know to enable the Tampermonkey
script before launching the app.
"""

from rednote.connector import exec_js
from rednote.ui import launch
import sys

if __name__ == "__main__":
    try:
        exec_js("1")
    except Exception as e:  # pragma: no cover - network dependent
        print("⚠️  无法连接浏览器脚本：", e)
        print(
            "👉 请确认已在浏览器中安装并启用了 Tampermonkey 脚本 gptconnector.js, "
            "并且已打开受支持的 AI 页面(例如 chatgpt.com)。"
        )
        sys.exit(1)
    launch()
