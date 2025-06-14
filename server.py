from flask import Flask, jsonify, request, redirect, url_for, send_from_directory
from main_setting import MainSetting 
import playsound
import speech_recognition as sr
from llm import Generation_LLM
from tts import Generation_Audio
from sr import audio_record
from flask_cors import CORS
import logging
import asyncio
import os
import json

# -*- coding: utf-8 -*-
# server.py

"""
主要功能模块：
"""
settings = MainSetting()
speech_generator = Generation_Audio.SpeechGenerator()
content_generator = Generation_LLM.ContentGenerate()
speech_recognizer = audio_record.SpeechRecognizer()
print(speech_generator.settings.audio_directory)
recognizer = sr.Recognizer()

# 设置日志记录
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()])

# 构建基础Flask应用
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}) # 允许跨域请求


# 设置静态文件目录
app.config['STATIC_FOLDER'] = 'static' # 静态文件目录（默认html、css、js等文件读取目录）
app.config['AUDIO_FOLDER'] = settings.audio_directory  # 音频文件目录
os.makedirs(settings.audio_directory, exist_ok=True)


# Main Program Interface
class update_settings:
    def __init__(self):
        self.load_config()
    
    def load_config(self):
        with open('main_setting.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
            self.__dict__.update(config['path'])
            self.__dict__.update(config['tts'])
            self.__dict__.update(config['llm'])    
    def update_config(self, new_config):
        try:
            with open('main_setting.json', 'r', encoding='utf-8') as f:
                current_config = json.load(f)
            
            # 更新配置
            for key, value in new_config.items():
                if key in ['tts', 'llm','path']:
                    current_config[key].update(value)
                else:
                    current_config[key] = value
            
            # 保存更新后的配置
            with open('main_setting.json', 'w', encoding='utf-8') as f:
                json.dump(current_config, f, indent=4, ensure_ascii=False)
            
            # 重新加载配置
            self.load_config()
            return True
        except Exception as e:
            print(f"配置更新失败: {str(e)}")
            return False

# 监听语音识别是否有文本输出
def wake_word_detected():
    while is_recording:
        text = speech_recognizer.record(recognizer=recognizer, language='en-US')  # 假设record函数封装好了麦克风输入识别
        if not is_recording:
            break
        if text:
            print("语音识别成功:", text)
            return text
        else:
            print("没有检测到语音，继续监听...")
    return None

def record_thread():
    global is_recording
    print("录音线程启动")
    while is_recording:
        text = wake_word_detected()
        if not text:
            continue

        print("生成回答中:", text)
        content = content_generator.zhipuai_content(text)
        print("回答内容:", content)

        try:
            if content.strip():
                asyncio.run(speech_generator.generate_audio(content))
                print("音频生成成功")
            else:
                print("内容为空，跳过生成")
        except Exception as e:
            print("音频生成出错：", e)

        if not is_recording:
            break


"""
# 初始化配置更新类
"""
update = update_settings()


# home page route
@app.route('/')
def index():
    return redirect(url_for('static', filename='index.html'))

# favicon route
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/x-icon')


import threading # 引入线程模块

is_recording = False  # 全局变量，控制录音状态
last_audio_url = None


@app.route('/start_record', methods=['POST'])
def start_record():
    global is_recording
    if not is_recording:
        is_recording = True
        threading.Thread(target=record_thread).start()
    return jsonify({'status': 'recording'})

@app.route('/stop_record', methods=['POST'])
def stop_record():
    global is_recording
    is_recording = False
    audio_path = os.path.join(settings.audio_directory, settings.audio_file)
    if os.path.exists(audio_path):
        return jsonify({
            'status': 'stopped',
            'audio_file': f"http://127.0.0.1:5000/{settings.audio_directory}/{settings.audio_file}"
        })
    return jsonify({'status': 'stopped'})


@app.route('/latest_audio', methods=['GET'])
def latest_audio():
    audio_path = os.path.join(settings.audio_directory, settings.audio_file)
    playsound(audio_path) #  播放音频
    if os.path.exists(audio_path):
        return jsonify({
            'audio_file': f"http://127.0.0.1:5000/{settings.audio_directory}/{settings.audio_file}"
        })
    return jsonify({'error': 'not ready'}), 404


# 本文模式路由
@app.route('/text', methods=['POST'])
def deal_audio():
    text = request.json.get('text', '')
        
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    print("Thinking...")
    content = content_generator.zhipuai_content(text)
    print(content)

    try:
        asyncio.run(speech_generator.generate_audio(content))
        audio_url = f"http://127.0.0.1:5000/{settings.audio_directory}/{settings.audio_file}"
        print(f"Audio file generated: {audio_url}")
        return jsonify({'audio_file': audio_url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# provide audio files
@app.route('/audio/<path:filename>', methods=['GET'])
def get_audio(filename):
    return send_from_directory('audio', filename)

@app.route('/settings', methods=['GET'])
def get_settings():
    try:
        with open('main_setting.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        return jsonify(config)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/settings', methods=['POST'])
def update_settings():
    try:
        new_config = request.json
        if update.update_config(new_config):
            return jsonify({'message': '配置更新成功'})
        return jsonify({'error': '配置更新失败'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

