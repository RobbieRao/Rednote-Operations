from __future__ import annotations

import io
import textwrap
from pathlib import Path
from typing import List

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from PIL import Image


class MplSlide:
    """Render a single vertical slide using matplotlib."""

    def __init__(self, width: int = 1080, height: int = 1440, font_path: str | None = None):
        self.W, self.H = width / 100, height / 100
        self.font_path = font_path or self._auto_font()
        fm.fontManager.addfont(self.font_path)
        self.font_prop = fm.FontProperties(fname=self.font_path)

    def _auto_font(self) -> str:
        candidates = [
            "C:/Windows/Fonts/msyh.ttc",
            "/System/Library/Fonts/PingFang.ttc",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]
        for p in candidates:
            if Path(p).exists():
                return p
        raise FileNotFoundError("未找到可用字体，请在界面上传 .ttf/.ttc 字体")

    def draw(self, title: str, bullets: List[str]) -> Image.Image:
        plt.close("all")
        fig = plt.figure(figsize=(self.W, self.H), dpi=100)
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis("off")

        ax.text(
            0.05,
            0.9,
            title,
            fontsize=96,
            fontproperties=self.font_prop,
            fontweight="bold",
            va="top",
            ha="left",
            wrap=True,
        )

        y = 0.75
        for bp in bullets:
            wrapped = textwrap.fill(bp, 18)
            ax.text(0.07, y, "\u2022", fontsize=64, fontproperties=self.font_prop, va="top")
            ax.text(0.10, y, wrapped, fontsize=60, fontproperties=self.font_prop, va="top", wrap=True)
            y -= 0.11 * (wrapped.count("\n") + 1)

        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight")
        buf.seek(0)
        return Image.open(buf)
