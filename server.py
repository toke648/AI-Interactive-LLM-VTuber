from flask import Flask, jsonify, request, redirect, url_for, send_from_directory
from main_setting import MainSetting 
from llm import Generation_LLM
from tts import Generation_Audio
from sr import audio_record
from flask_cors import CORS
import asyncio
import os
import json

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

update = update_settings()
settings = MainSetting()
speech_generator = Generation_Audio.SpeechGenerator()
content_generator = Generation_LLM.ContentGenerate()
speech_recognizer = audio_record.SpeechRecognizer()
print(speech_generator.settings.audio_directory)
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# home page route
@app.route('/')
def index():
    return redirect(url_for('static', filename='index.html'))

# favicon route
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/x-icon')

@app.route('/dealAudio', methods=['POST'])
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
