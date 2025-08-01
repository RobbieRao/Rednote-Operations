# Rednote Operations

将学术论文 PDF 一键转换成小红书竖版幻灯片。

## 主要特性
- 通过浏览器用户脚本上传并解析 PDF
- LLM 生成信息充实的标题与文案
- Matplotlib 绘制 1080×1440 竖屏幻灯片，动态排版提升可读性，支持自定义字体
- Gradio Web 界面即时预览

## 环境要求
- 已安装 Tampermonkey 并加载仓库中的 `gptconnector.js`
- Python 3.10+，依赖见 `requirements.txt`
- 可选：用于中文显示的 `.ttf`/`.ttc` 字体文件

## 安装
```bash
pip install -r requirements.txt
```

## 运行
启动前请确保：
- 浏览器已登录支持的 AI 网站（如 [chatgpt.com](https://chatgpt.com)）。
- Tampermonkey 中启用了本仓库提供的 `gptconnector.js` 脚本。
- 首次启用脚本时，Tampermonkey 会提示是否允许访问 `http://127.0.0.1:5123`，请点击允许。

然后在命令行执行：
```bash
python main.py
```
若出现“无法连接浏览器脚本”的提示，通常是由于用户脚本未启用或页面未打开。
如已确认上述步骤仍报错，请检查防火墙是否允许访问 `http://127.0.0.1:5123/connector`。
按照界面提示上传 PDF 和字体，设置幻灯片数量后点击“生成”。

## 项目结构
```
rednote/
    connector.py   # 浏览器通信封装
    slide.py       # Matplotlib 幻灯片渲染
    prompts.py     # Prompt 模板与 JSON 解析
    pipeline.py    # 主流程调度
    ui.py          # Gradio 界面
main.py            # 程序入口
gptconnector.js    # Tampermonkey 用户脚本
```

## 联系
Robbie Fenggui Rao  
robbie.rao@connect.polyu.hk
