from __future__ import annotations

from rednote.connector import exec_js
from rednote.ui import launch

if __name__ == "__main__":
    try:
        exec_js("1")
    except Exception as e:
        print("⚠️  无法连接浏览器脚本：", e)
        raise SystemExit(1)
    launch()
