# Interactive-LLM-VTuber

[![GitHub Release](https://img.shields.io/github/v/release/toke648/AI-Interactive-LLM-VTuber)](https://github.com/toke648/AI-Interactive-LLM-VTuber/releases)
[![license](https://img.shields.io/github/license/toke648/Interactive-LLM-VTuber)](https://github.com/toke648/Interactive-LLM-VTuber/main/LICENSE) 
[![](https://img.shields.io/badge/toke648%2FInteractive--LLM--VTuber-%25230db7ed.svg?logo=docker&logoColor=blue&labelColor=white&color=blue)](https://hub.docker.com/r/toke648/interactive-llm-vtuber) 


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

## Project Structure

```
2025/01/02  00:19    <DIR>          .
2025/01/02  00:10    <DIR>          ..
2025/01/02  00:11    <DIR>          .idea
2025/01/02  00:11    <DIR>          audio
2025/01/01  20:23               761 config.yaml
2025/01/02  00:11    <DIR>          data
2025/01/02  00:06             1,781 dockerfile
2025/01/01  16:05             1,064 LICENSE
2025/01/02  00:11    <DIR>          llm
2025/01/02  00:15             2,078 main_setting.py
2025/01/02  00:21             1,037 README.md
2025/01/02  00:18               174 requirements.txt
2025/01/01  17:40           191,857 Screenshot 2025-01-01 174024-demo.png
2025/01/01  20:19             1,532 server.py
2025/01/02  00:11    <DIR>          static
2025/01/02  00:11    <DIR>          stt
2025/01/02  00:11    <DIR>          templates
2025/01/02  00:11    <DIR>          text_program
2025/01/02  00:11    <DIR>          translate
2025/01/02  00:11    <DIR>          tts
2025/01/02  00:11    <DIR>          __pycache__
```
