from __future__ import annotations

import json
import re

PROMPT_STEP1 = "请阅读我刚刚上传的论文 PDF，并等待后续提问，只回答“OK”。"
PROMPT_TITLE = (
    "请生成小红书标题（格式：每日HCI·<亮点>，≤20字）与配套文案（120‑150字），文案结尾固定："
    "#HCI #设计 #人机交互 +3 个签。用 JSON 返回：{\"title\":…, \"copy\":…}"
)
PROMPT_SLIDES = (
    "请把论文内容深入浅出地总结成 6‑8 张幻灯片，每张 JSON："
    "{\"title\":…, \"bullets\":[…]}。Bullet ≤30字。仅返回 JSON 数组。"
)


def extract_json(txt: str):
    match = re.search(r'(\{.*\}|\[.*\])', txt, re.S)
    if not match:
        raise ValueError("GPT 未返回 JSON")
    return json.loads(match.group())
