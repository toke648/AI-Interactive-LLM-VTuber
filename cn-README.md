# Interactive-LLM-VTuber

[![GitHub Release](https://img.shields.io/github/v/release/toke648/AI-Interactive-LLM-VTuber)](https://github.com/toke648/AI-Interactive-LLM-VTuber/releases)
[![license](https://img.shields.io/github/license/toke648/Interactive-LLM-VTuber)](https://github.com/toke648/Interactive-LLM-VTuber/main/LICENSE) 
[![](https://img.shields.io/badge/toke648%2FInteractive--LLM--VTuber-%25230db7ed.svg?logo=docker&logoColor=blue&labelColor=white&color=blue)](https://hub.docker.com/r/toke648/interactive-llm-vtuber)

[**English**](README.md) | **简体中文**

## 项目简介
这是一个虚拟主播互动模型项目。目前支持语音输入、文本生成和语音输出等基本功能。此外，项目还包括正在开发中的长期记忆、图像识别和情感分析等功能。项目的下一阶段将涉及本地部署、深度强化学习、集成、框架增强和嵌入式系统实现。

## 演示
![演示截图](Screenshot%202025-01-01%20174024-demo.png)

## 技术构成

- **Python**
- **语音识别 (ASR):** `speech_recognition(在线)`
- **大语言模型 (LLM):** `目前支持 通义千问、Deepseek(在线)、Ollama2.5:7b(本地离线)`
- **文本转语音 (TTS):** `edge-tts(在线)`

- **前后端交互：** `Flask + Html + JS + Css`

## 支持平台

- **Windows**

- **Linux** (未经测试，但应该兼容)

## 使用方法

下载并安装 **VSCode** 或 **PyCharm**，以及**Python3.11**版本编释器。

进入项目目录并运行以下命令安装依赖，建议使用虚拟环境以保持依赖项的隔离。

### 打开终端/命令提示符并进入项目目录。

### 创建虚拟环境：

```sh
python -m venv vtuber
```


### 激活虚拟环境：
- Windows系统：

    ```sh
    vtubre\Scripts\activate
    ```
- Linux/macOS系统：
    ```sh
    source vtuber/bin/activate
    ```

#### 使用requirements.txt文件安装所需依赖：
```sh
pip install -r requirements.txt
```
注意： `在mainsetting.py中更改和配置你的api接口`

### 运行server.py文件
```sh
python server.py
```
 ### 其他说明
您可以在main_setting.py文件中更改端口或其他配置。
- 确保正确设置API密钥等环境变量，特别是针对LLM集成。
- 如果您使用**阿里云通义千问API密钥**或**Ollama模型**，请确保在代码中正确配置它们。

## 使用Dockerfile

### 前提条件
- 在您的系统上安装[Docker](https://www.docker.com/)。

### 构建Docker镜像
1. 导航到包含`dockerfile`的项目目录。
2. 使用以下命令构建Docker镜像：
    ```sh
    docker build -t interactive-llm-vtuber .
    ```

### 运行Docker容器
1. 使用构建的镜像启动容器：
    ```sh
    docker run -d -p 5000:5000 --name vtuber interactive-llm-vtuber
    ```
    这将把主机的5000端口映射到容器，应用程序将在该端口访问。

2. 在浏览器中访问`http://localhost:5000`以使用应用程序。

### 停止容器
要停止容器，运行：
```sh
docker stop vtuber
```

### 删除容器
如果不再需要容器，可以使用以下命令删除：
```sh
docker rm vtuber
```
## 记忆/长期记忆（开发中）

