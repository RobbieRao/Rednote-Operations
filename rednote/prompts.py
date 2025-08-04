from __future__ import annotations

import json
import re

PROMPT_TITLE = (
    "你是一名科研助手。请根据以下论文内容生成一条信息充实且不过度夸张的小红书标题（≤20字，突出论文核心贡献）与配套文案"
    "（120-150字，需交代关键发现与意义，文案结尾固定：#HCI #设计 #人机交互 +3 个签）。\n"
    "论文内容如下：\n{paper}\n"
    '请用 JSON 返回：{"title":…, "copy":…}'
)
PROMPT_SLIDES = (
    "以下是论文内容：\n{paper}\n"
    "请把论文内容深入浅出地总结成 6-8 张幻灯片，信息密度要高。每张 JSON："
    '{"title":…, "bullets":[…]}。标题≤15字，Bullet 3-5 条，每条≤40字，需包含具体信息或结论，避免空洞表述。'
    "仅返回 JSON 数组。"
)


def extract_json(txt: str):
    match = re.search(r'(\{.*\}|\[.*\])', txt, re.S)
    if not match:
        raise ValueError("模型未返回 JSON")
    return json.loads(match.group())
