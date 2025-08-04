# Rednote Operations

将学术论文 PDF 一键转换成小红书竖版幻灯片。

## 主要特性
- 本地解析 PDF 并提取文本
- 基于本地 Ollama 模型生成信息充实的标题与文案
- Matplotlib 绘制 1080×1440 竖屏幻灯片，动态排版提升可读性，支持自定义字体
- Gradio Web 界面即时预览

## 环境要求
- 已安装并启动 [Ollama](https://github.com/ollama/ollama)，默认使用本地 `llama3` 模型
- Python 3.10+，依赖见 `requirements.txt`
- 可选：用于中文显示的 `.ttf`/`.ttc` 字体文件

## 安装
```bash
pip install -r requirements.txt
```

## 运行
在命令行执行：
```bash
python main.py
```
按照界面提示上传 PDF 和字体，设置幻灯片数量后点击“生成”。

## 项目结构
```
rednote/
    connector.py   # 本地 Ollama 通信
    slide.py       # Matplotlib 幻灯片渲染
    prompts.py     # Prompt 模板与 JSON 解析
    pipeline.py    # 主流程调度
    ui.py          # Gradio 界面
main.py            # 程序入口
```

## 联系
Robbie Fenggui Rao
robbie.rao@connect.polyu.hk
