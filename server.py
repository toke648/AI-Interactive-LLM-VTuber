from flask import Flask, jsonify, request, redirect, url_for, send_from_directory
from llm import Tongyi_Qianwen_LLM
from tts import generate_audio
from main_setting import MainSetting
from flask_cors import CORS
import asyncio
import os

# Main Program Interface
settings = MainSetting()
speech_generator = generate_audio.SpeechGenerator()
content_generator = Tongyi_Qianwen_LLM.ContentGenerate()
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
    content = content_generator.ollama_content(text)
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

