# Interactive-LLM-VTuber

[![GitHub Release](https://img.shields.io/github/v/release/toke648/AI-Interactive-LLM-VTuber)](https://github.com/toke648/AI-Interactive-LLM-VTuber/releases)
[![license](https://img.shields.io/github/license/toke648/Interactive-LLM-VTuber)](https://github.com/toke648/Interactive-LLM-VTuber/main/LICENSE)
[![](https://img.shields.io/badge/toke648%2FInteractive--LLM--VTuber-%25230db7ed.svg?logo=docker&logoColor=blue&labelColor=white&color=blue)](https://hub.docker.com/r/toke648/interactive-llm-vtuber)

**English** | [**简体中文**](./README_zh.md)

## Project Overview

**Interactive-LLM-VTuber** is an innovative platform for interactive virtual streamers, leveraging advanced AI technologies to deliver an immersive user experience. The project supports voice input, text generation, and voice output, with high scalability. Currently in development are features like long-term memory, image recognition, and sentiment analysis. Future plans include local deployment, deep reinforcement learning, system integration, framework optimization, and embedded device support to build an intelligent VTuber ecosystem.

## Feature Highlights

- **Real-time Voice Interaction**: Enables natural language input via automatic speech recognition (ASR).
- **Intelligent Conversation**: Supports multiple large language models (LLMs), including Tongyi Qianwen, Deepseek (online), and Ollama2.5:7b (local offline).
- **Speech Synthesis**: Utilizes Edge-TTS for smooth text-to-speech output.
- **Dynamic Front-end**: Built with Flask, HTML, JavaScript, and CSS for an intuitive user interface.
- **Modular Design**: Facilitates feature expansion and third-party integration.

## Demo

![Demo screenshot](Screenshot%202025-01-01%20174024-demo.png)

*Showcasing real-time interaction with the VTuber model.*

## Technology Stack

- **Programming Language**: Python
- **Speech Recognition (ASR)**: `speech_recognition` (online)
- **Large Language Models (LLMs)**:
  - Tongyi Qianwen (online)
  - Deepseek (online)
  - Ollama2.5:7b (local offline)
- **Text-to-Speech (TTS)**: `edge-tts` (online)
- **Front-end and Back-end Interaction**: Flask + HTML + JavaScript + CSS

*Note*: Some models may require specific configurations for compatibility.

## Supported Platforms

- **Windows**: Fully tested and stable.
- **Linux**: Theoretically compatible (testing recommended).

## Installation and Use

### Prerequisites

- Install **VSCode** or **PyCharm**.
- Install **Python 3.11** interpreter.
- (Optional) Use a virtual environment to isolate dependencies.

### Steps

1. **Clone the project and enter the directory**:

   ```sh
   git clone https://github.com/toke648/AI-Interactive-LLM-VTuber.git
   cd AI-Interactive-LLM-VTuber
   ```

2. **Create and activate a virtual environment**:

   - Windows:

     ```sh
     python -m venv vtuber
     vtuber\Scripts\activate
     ```

   - Conda Environment:
     ```sh
     conda create -n vtuber python=3.11
     conda activate vtuber
     ```

   - Linux/macOS:

     ```sh
     python -m venv vtuber
     source vtuber/bin/activate
     ```

3. **Install dependencies**:

   ```sh
   pip install -r requirements.txt
   ```

4. **Configure API**:

   - Edit `mainsetting.py` to configure API keys (e.g., for Tongyi Qianwen or Ollama) and other settings.

5. **Start the project**:

   ```sh
   python server.py
   ```

   Or use the one-click startup script (Windows):

   ```sh
   setup.bat
   ```

### Other Configurations

- **Port Modification**: Adjust the port or other settings in `mainsetting.py`.
- **Model Switching**: Modify the `cubism4Model` variable in `static/js/appserver.js` to switch VTuber models (not yet integrated into the UI).
- **System Settings**: Access the configuration page via the “Settings” button in the UI. Restart the project to apply changes.

## Update Log (Version 0.4.0)

1. **One-click Startup**: Added `setup.bat` script to simplify the startup process for Windows users.
2. **Model Switching**: Supports manual VTuber model switching by modifying the path in `static/js/appserver.js`.
3. **System Configuration Page**: Added a settings interface, accessible via the “Settings” button. Restart the project to apply changes.

## Notes

- Ensure API keys and environment variables are correctly configured for LLM and TTS functionality.
- Linux users may need to verify compatibility. Feedback is welcome via GitHub Issues.
- The project is actively updated. Follow the GitHub repository for the latest updates.

## License

This project is licensed under the MIT License. Contributions and suggestions are warmly welcomed!