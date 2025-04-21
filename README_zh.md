# Interactive-LLM-VTuber

[![GitHub Release](https://img.shields.io/github/v/release/toke648/AI-Interactive-LLM-VTuber)](https://github.com/toke648/AI-Interactive-LLM-VTuber/releases)
[![license](https://img.shields.io/github/license/toke648/Interactive-LLM-VTuber)](https://github.com/toke648/Interactive-LLM-VTuber/main/LICENSE) 
[![](https://img.shields.io/badge/toke648%2FInteractive--LLM--VTuber-%25230db7ed.svg?logo=docker&logoColor=blue&labelColor=white&color=blue)](https://hub.docker.com/r/toke648/interactive-llm-vtuber)

[**English**](README.md) | **简体中文**

## 项目概述

**Interactive-LLM-VTuber** 是一个创新的虚拟主播互动平台，融合了前沿的人工智能技术，为用户提供沉浸式的交互体验。该项目支持语音输入、文本生成和语音输出，具备高度可扩展性。当前开发中的功能包括长期记忆、图像识别和情感分析，未来计划实现本地部署、深度强化学习、系统集成、框架优化以及嵌入式设备支持，致力于打造智能化的虚拟主播生态。

## 功能亮点

- **实时语音交互**：通过语音识别（ASR）实现自然语言输入。
- **智能对话**：支持多种大语言模型（LLM），包括通义千问、Deepseek（在线）和Ollama2.5:7b（本地离线）。
- **语音合成**：采用Edge-TTS技术，提供流畅的文本转语音输出。
- **动态前端**：基于Flask框架，结合HTML、JavaScript和CSS打造直观的用户界面。
- **模块化设计**：便于功能扩展与第三方集成。

## 演示
![演示截图](Screenshot%202025-01-01%20174024-demo.png)

## 技术栈（目前支持的）

- **编程语言**：Python
- **语音识别（ASR）**：`speech_recognition`（在线）
- **大语言模型（LLM）**：
  - 通义千问（在线）
  - Deepseek（在线）
  - Ollama2.5:7b（本地离线）

  注：解析器问题，部分模型可能不支持
- **文本转语音（TTS）**：`edge-tts`（在线）
- **前后端交互**：Flask + HTML + JavaScript + CSS

## 支持平台

- **Windows**：全面测试，稳定运行
- **Linux**：理论兼容（建议测试验证）

## 安装与使用

### 前置条件

- 安装 **VSCode** 或 **PyCharm**。
- 安装 **Python 3.11** 解释器 或 配置**Conda环境**。
- （可选）使用虚拟环境以隔离依赖。

### 步骤

1. **克隆项目并进入目录**：

   ```sh
   git clone https://github.com/toke648/AI-Interactive-LLM-VTuber.git
   cd AI-Interactive-LLM-VTuber
   ```

2. **创建并激活虚拟环境**：

   - Windows：

     ```sh
     python -m venv vtuber
     vtuber\Scripts\activate
     ```
   
   - Conda 环境：
     ```sh
     conda create -n vtuber python=3.11
     conda activate vtuber
     ```

   - Linux/macOS：

     ```sh
     python -m venv vtuber
     source vtuber/bin/activate
     ```

3. **安装依赖**：

   ```sh
   pip install -r requirements.txt
   ```

4. **配置API**：

   - 编辑 `mainsetting.py`，填入您的API密钥（如阿里云通义千问或Ollama模型）及其他配置。

5. **启动项目**：

   ```sh
   python server.py
   ```

   或使用一键启动脚本（Windows）：

   ```sh
   setup.bat
   ```

### 其他配置

- **端口修改**：在 `main_setting.py` 中调整端口号或其他参数。
- **模型切换**：修改 `static/js/appserver.js` 中的 `cubism4Model` 变量以切换VTuber模型（暂未集成至UI）。
- **系统设置**：通过UI中的“Settings”按钮进入配置页面，调整后需重启项目以应用更改。

## 更新日志（Version 0.4.0）

1. **一键启动**：新增 `setup.bat` 脚本，简化Windows用户的启动流程。
2. **模型切换**：支持手动切换VTuber模型，需修改 `static/js/appserver.js` 中的路径。
3. **系统配置页面**：新增可视化设置界面，点击“Settings”按钮进入，配置保存后需重启项目。

## 注意事项

- 确保API密钥和环境变量正确配置，以保证LLM和TTS功能正常运行。
- Linux用户可能需要额外验证兼容性，欢迎反馈问题至GitHub Issues。
- 项目持续更新，建议关注 GitHub 仓库 获取最新动态。

## 许可证

本项目遵循 MIT 许可证，欢迎贡献代码或提出建议！