# Interactive-LLM-VTuber

[![GitHub Release](https://img.shields.io/github/v/release/toke648/AI-Interactive-LLM-VTuber)](https://github.com/toke648/AI-Interactive-LLM-VTuber/releases)
[![license](https://img.shields.io/github/license/toke648/Interactive-LLM-VTuber)](https://github.com/toke648/Interactive-LLM-VTuber/main/LICENSE) 
[![](https://img.shields.io/badge/toke648%2FInteractive--LLM--VTuber-%25230db7ed.svg?logo=docker&logoColor=blue&labelColor=white&color=blue)](https://hub.docker.com/r/toke648/interactive-llm-vtuber) 

[![](https://dcbadge.limes.pink/api/server/u5BsCFWEvW)](https://discord.gg/u5BsCFWEvW)

**English** | [**简体中文**](cn-README.md)

## What is this project
This project is a virtual VTuber interactive model. Currently, it supports basic functionalities like speech input, text generation, and voice output. Additionally, it includes features such as long-term memory, image recognition, and emotion analysis, which are under active development. The next phase of the project involves local deployment, deep reinforcement learning, integration, framework enhancement, and embedded system implementation.

## Demo (In Progress)
![Demo Screenshot](Screenshot%202025-01-01%20174024-demo.png)

## Constructed by

- **Python**
- **Speech Recognition (ASR):** `speech_recognition`
- **Large Language Model (LLM):** Tongyi Qianwen
- **Text-to-Speech (TTS):** `edge-tts`

## Target Platforms

- **Windows**
- **Linux** (Not tested, but should be compatible)

## How to work it

Download and install either **VSCode** or **PyCharm**.
Navigate to the project directory and run the following command to install dependencies:

It's recommended to use a virtual environment to keep the dependencies isolated.

### Open a terminal/command prompt and navigate to the project directory.

### Create a virtual environment by running the following command:

   ```sh
   python -m venv vtuber
   ```

### Activate the virtual environment:
   - On Windows:

      ```sh
      vtubre\Scripts\activate
      ```
   - On Linux/macOS:
      ```sh
      source vtuber/bin/activate
      ```

#### Use the requirements. txt file to install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```
### Run the server.py file
   ```sh
   python server.py
   ```
 ### Additional Notes
You can change the port or other configurations in the main_setting.py file.
- Ensure that any environment variables like API keys are set correctly, especially for LLM integration.
- If you're using  **Alibaba Cloud Tongyi Qianwen API Key** or **Ollama models**, make sure to properly configure them in code.

## Using the Dockerfile

### Prerequisites
- Install [Docker](https://www.docker.com/) on your system.

### Building the Docker Image
1. Navigate to the project directory containing the `dockerfile`.
2. Build the Docker image with the following command:
   ```sh
   docker build -t interactive-llm-vtuber .
   ```

### Running the Docker Container
1. Start a container using the built image:
   ```sh
   docker run -d -p 5000:5000 --name vtuber interactive-llm-vtuber
   ```
   This maps port 5000 on your host machine to the container, where the application will be accessible.

2. Access the application by visiting `http://localhost:5000` in your browser.

### Stopping the Container
To stop the container, run:
```sh
docker stop vtuber
```

### Removing the Container
If you no longer need the container, you can remove it with:
```sh
docker rm vtuber
```
## Mem0/Long Memory (In Development)
