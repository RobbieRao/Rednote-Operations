from __future__ import annotations

import traceback
import gradio as gr

from .pipeline import pipeline


def ui(pdf, slides, font):
    if not pdf:
        return "❌ 未上传 PDF", "", []
    font_path = font.name if font else None
    try:
        return pipeline(pdf, int(slides), font_path)
    except Exception as e:
        return f"❌ {e}\n\n{traceback.format_exc(limit=2)}", "", []


def build_demo() -> gr.Blocks:
    with gr.Blocks(title="小红书论文摘要生成 · matplotlib") as demo:
        gr.Markdown("**确保：浏览器已登录 ChatGPT，并启用 Tampermonkey 用户脚本**")
        with gr.Row():
            pdf_in = gr.File(label="论文 PDF", type="filepath", file_types=[".pdf"])
            font_in = gr.File(label="中文字体(可选)", type="filepath", file_types=[".ttf", ".ttc"])
        slides_in = gr.Slider(4, 8, step=1, value=6, label="幻灯片张数")
        btn = gr.Button("生成")
        title_out = gr.Textbox(label="标题 / 报错")
        copy_out = gr.Textbox(label="文案", lines=6)
        gallery = gr.Gallery(label="幻灯片预览", columns=1, height="auto")
        btn.click(ui, inputs=[pdf_in, slides_in, font_in], outputs=[title_out, copy_out, gallery])
    return demo


def launch():
    demo = build_demo()
    demo.launch()
