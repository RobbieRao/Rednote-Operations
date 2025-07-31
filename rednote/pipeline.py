from __future__ import annotations

from typing import List, Tuple

from tqdm import tqdm

from .connector import gpt_ask, upload_pdf
from .prompts import PROMPT_STEP1, PROMPT_TITLE, PROMPT_SLIDES, extract_json
from .slide import MplSlide


def pipeline(pdf_path: str, n_slides: int, font_file: str | None):
    """Run the end-to-end pipeline and return title, copy and slide gallery."""
    upload_pdf(pdf_path)
    gpt_ask(PROMPT_STEP1, 120)

    meta = extract_json(gpt_ask(PROMPT_TITLE, 300))
    title, copy = meta["title"], meta["copy"]

    specs = extract_json(gpt_ask(PROMPT_SLIDES, 600))[:n_slides]

    painter = MplSlide(font_path=font_file)
    gallery = []
    for s in tqdm(specs, desc="绘制幻灯片"):
        img = painter.draw(s["title"], s["bullets"])
        gallery.append((img, s["title"]))
    return title, copy, gallery
