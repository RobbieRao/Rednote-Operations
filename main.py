#!/usr/bin/env python
# xhs_zoterogpt_mpl.py  —— 论文 PDF ➜ 小红书图文 · Matplotlib 渲染版

from __future__ import annotations
import base64, io, json, os, re, textwrap, time, traceback
from pathlib import Path
from typing import List, Tuple

import requests, gradio as gr, matplotlib.pyplot as plt, matplotlib.font_manager as fm
from pdfminer.high_level import extract_text
from PIL import Image
from tqdm import tqdm

ZPORT = "http://127.0.0.1:23119/zoterogpt"          # ZoteroGPT 端口

# ──────────────────── 1. 浏览器通信 ──────────────────────
def exec_js(code: str):
    r = requests.post(ZPORT, json={"code": code}, timeout=15)
    r.raise_for_status()
    return r.json()["result"]

def wait_done(timeout=300):
    t0 = time.time()
    while time.time() - t0 < timeout:
        task = exec_js("window.Meet?.Connector?.tasks.slice(-1)[0]||{}")
        if task.get("type") == "done":
            return task
        time.sleep(1)
    raise RuntimeError("浏览器端超时（>5min）")

def upload_pdf(path: str):
    b64 = base64.b64encode(Path(path).read_bytes()).decode()
    name = Path(path).name
    exec_js(f"""window.Meet.Connector.tasks.push({{
        type:"pending",file:{{base64String:{json.dumps(b64)},name:{json.dumps(name)}}}
    }});""")
    wait_done(180)

def gpt_ask(prompt: str, timeout=600) -> str:
    exec_js(f"""window.Meet.Connector.tasks.push({{
        type:"pending",requestText:{json.dumps(prompt)}
    }});""")
    return wait_done(timeout).get("responseText","").strip()

# ──────────────────── 2. matplotlib SlidePainter ─────────────────
class MplSlide:
    def __init__(self, width=1080, height=1440, font_path: str | None = None):
        self.W, self.H = width/100, height/100        # inches, dpi=100
        self.font_path = font_path or self._auto_font()

        fm.fontManager.addfont(self.font_path)
        self.fname = fm.FontProperties(fname=self.font_path).get_name()

    def _auto_font(self):
        cand = [
            "C:/Windows/Fonts/msyh.ttc",                          # Win
            "/System/Library/Fonts/PingFang.ttc",                 # mac
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"     # Linux
        ]
        for p in cand:
            if Path(p).exists():
                return p
        raise FileNotFoundError("未找到可用字体，请在界面上传 .ttf/.ttc 字体")

    def draw(self, title:str, bullets:List[str])->Image.Image:
        plt.close("all")
        fig = plt.figure(figsize=(self.W,self.H), dpi=100)
        ax = fig.add_axes([0,0,1,1]); ax.axis("off")

        # 标题——自动缩放
        t_size = 96
        ax.text(0.05, 0.9, title, fontsize=t_size, font=self.fname, fontweight="bold",
                va="top", ha="left", wrap=True)
        # bullets
        y = 0.75
        for bp in bullets:
            wrapped = textwrap.fill(bp, 18)
            ax.text(0.07, y, u"\u2022", fontsize=64, font=self.fname, va="top")
            ax.text(0.10, y, wrapped, fontsize=60,
                    font=self.fname, va="top", wrap=True)
            # 粗估高度：行数×行高
            y -= 0.11 * (wrapped.count("\n")+1)

        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight")
        buf.seek(0)
        return Image.open(buf)

# ──────────────────── 3. Prompt 模板 ───────────────────────
PROMPT_STEP1 = "请阅读我刚刚上传的论文 PDF，并等待后续提问，只回答“OK”。"
PROMPT_TITLE = (
    "请生成小红书标题（格式：每日HCI·<亮点>，≤20字）与配套文案（120‑150字），文案结尾固定："
    "#HCI #设计 #人机交互 +3 个标签。用 JSON 返回：{\"title\":…, \"copy\":…}"
)
PROMPT_SLIDES = (
    "请把论文内容深入浅出地总结成 6‑8 张幻灯片，每张 JSON："
    "{\"title\":…, \"bullets\":[…]}。Bullet ≤30字。仅返回 JSON 数组。"
)

def extract_json(txt:str):
    m=re.search(r'(\{.*\}|\[.*\])',txt,re.S)
    if not m: raise ValueError("GPT 未返回 JSON")
    return json.loads(m.group())

# ──────────────────── 4. 主流程 ─────────────────────────────
def pipeline(pdf_path:str, n_slides:int, font_file:str|None):
    upload_pdf(pdf_path)
    gpt_ask(PROMPT_STEP1, 120)      # 等 “OK”

    # ── Step 2 标题+文案
    meta = extract_json(gpt_ask(PROMPT_TITLE, 300))
    title, copy = meta["title"], meta["copy"]

    # ── Step 3 Slides
    specs = extract_json(gpt_ask(PROMPT_SLIDES, 600))[:n_slides]

    painter = MplSlide(font_path=font_file)
    gallery=[]
    for s in tqdm(specs, desc="绘制幻灯片"):
        img=painter.draw(s["title"], s["bullets"])
        gallery.append((img, s["title"]))
    return title, copy, gallery

# ──────────────────── 5. Gradio UI ──────────────────────────
def ui(pdf, slides, font):
    if not pdf: return "❌ 未上传 PDF", "", []
    font_path = font.name if font else None
    try:
        return pipeline(pdf, int(slides), font_path)
    except Exception as e:
        return f"❌ {e}\n\n{traceback.format_exc(limit=2)}", "", []

with gr.Blocks(title="小红书论文摘要生成 · matplotlib") as demo:
    gr.Markdown("**确保：浏览器已登录 ChatGPT，Tampermonkey ZoteroGPT 插件运行**")
    with gr.Row():
        pdf_in = gr.File(label="论文 PDF", type="filepath", file_types=[".pdf"])
        font_in= gr.File(label="中文字体(可选)", type="filepath", file_types=[".ttf", ".ttc"])
    slides_in= gr.Slider(4,8,step=1,value=6,label="幻灯片张数")
    btn = gr.Button("生成")
    title_out = gr.Textbox(label="标题 / 报错")
    copy_out  = gr.Textbox(label="文案", lines=6)
    gallery   = gr.Gallery(label="幻灯片预览", columns=1, height="auto")
    btn.click(ui, inputs=[pdf_in, slides_in, font_in], outputs=[title_out, copy_out, gallery])

if __name__=="__main__":
    try: exec_js("1")
    except Exception as e:
        print("⚠️  无法连接 ZoteroGPT：", e); exit(1)
    demo.launch()
