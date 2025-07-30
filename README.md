ZoteroGPT‑XHS Slide Generator

把一篇学术论文一键变成 6–8 张「小红书风」竖版幻灯片，并支持定时自动发布到小红书将 Zotero、ChatGPT、matplotlib、Gradio 串联在一起，助力科研传播 ✨

✨ 主要特性

功能

说明

PDF→JSON 摘要

调用 ZoteroGPT 插件 + OpenAI API，抽取题目、亮点、方法、结论等结构化信息

自动排版幻灯片

使用 matplotlib 生成 1080 × 1440 px 竖屏幻灯片；自动字体回退，支持拖入自定义 .ttf

一键批量渲染

Gradio UI 支持多 PDF 上传、进度条、实时画廊预览

小红书一键发展（可选）

通过 Cookie + Selenium 或 RedBookSDK，将生成的图片与文案直接发布

定时/队列发展

内置 schedule 模块，支持每天/每周固定时间自动发送

CLI & API 双模式

既可命令行批量处理，也能 import 在其他 Python 项目中调用

...

🗓️ Roadmap / TODO
幻灯片美化‑ 引入 CSS‑like 主题系统‑ 支持背景渐变、icon 风格包
小红书 OAuth 登录（摆脱 Cookie）
定时队列管理‑ Web 控制面板‑ 发布失败自动重试
批量参数网格搜索（prompt & 版式）
多平台同步（微博 / Bilibili / 抖音）
支持 PPTX 导出（python‑pptx）
CI 单元测试 + GitHub Actions
...

📌 联系方式

作者：Robbie Fenggui Rao

邮箱：robbie.rao@connect.polyu.hk

项目还在快速迭代中，欢迎 ⭐️ Star 与建议！

