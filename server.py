from flask import Flask, jsonify, request, redirect, url_for, send_from_directory
from llm import generate_content
from tts import generate_audio
from main_setting import MainSetting
from flask_cors import CORS
import asyncio
import os

# 主要接口程序
settings = MainSetting()
speech_generator = generate_audio.SpeechGenerator()
content_generator = generate_content.ContentGenerate()
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# 首页路由
@app.route('/')
def index():
    return redirect(url_for('static', filename='index.html'))

# favicon 路由
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/x-icon')

@app.route('/dealAudio', methods=['POST'])
def deal_audio():
    text = request.json.get('text', '')
    # voice = request.json.get("text", '')
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    print("Thinking...")
    content = content_generator.generate_content(text)
    print(content)

    try:
        asyncio.run(speech_generator.generate_audio(content))
        audio_url = f"http://127.0.0.1:5000/{settings.audio_directory}/{settings.audio_file}"
        return jsonify({'audio_file': audio_url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 提供音频文件
@app.route('/audio/<path:filename>', methods=['GET'])
def get_audio(filename):
    return send_from_directory('audio', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


# from flask import Flask, request, jsonify, url_for, redirect, send_from_directory
# from language_generate import large_language_model
# from generate_audio import SeepchGenerate
# from flask_cors import CORS
# import asyncio
# import os
#
#
# app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "*"}})
#
# # 首页路由
# @app.route('/')
# def index():
#     return redirect(url_for('static', filename='index.html'))
#
# # favicon 路由
# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/x-icon')
#
# # 从前端获取文本信息，生成语言并返回音频文件
# @app.route('/dealAudio', methods=['GET', 'POST'])
# def deal_audio():
#     # 主要设置
#     setting = open('ai_setting_VTuber-Neuro sama.txt', 'r').read()
#     conversation_history = [{'role': 'system', 'content': f'{setting}'}]
#
#     # voice = 'en-US-AvaNeural'
#     # voice = 'ja-JP-NanamiNeural'
#     voice = 'zh-CN-XiaoxiaoNeural'
#     audio_address = os.path.join('audio', 'output.mp3')
#
#     # 从前端接口获取输入文本，同样可以设置 语言 音频 地址 注意确保前后端的通信地址一致
#     if request.method == 'POST':
#         content = request.json.get('text', '')
#     else:
#         content = request.args.get('text', '')
#
#     print('Thinking...')
#     response = large_language_model(content, conversation_history)
#     print(response)
#
#     if not response:
#         return jsonify({'error': "Missing text"}), 400
#
#     # 生成音频
#     try:
#         asyncio.run(SeepchGenerate.speech_generate_model(response))
#         return jsonify({"audio_file": f"http://127.0.0.1:5000/{audio_address}"})
#     except Exception as e:
#         print(f"Error occurred: {str(e)}")
#         return jsonify({"error": str(e)}), 500
#
# # 提供音频文件
# @app.route('/audio/<path:filename>', methods=['GET'])
# def get_audio(filename):
#     return send_from_directory('audio', filename)
#
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)



# from language_generate import large_language_model
# from flask import Flask, request, jsonify, url_for, redirect
# from flask import send_from_directory
# from flask_cors import CORS
# import edge_tts
# import os
#
# app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "*"}})  # 允许所有域名访问
#
# @app.route('/')
# def index():
#     return redirect(url_for('static', filename='index.html'))
#
# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
#
# @app.route('/dealAudio', methods=['GET', 'POST'])
# async def deal_audio():
#     if request.method == 'POST':
#         content = request.json.get('text', '')
#         voice = request.json.get('voice', 'en-US-AvaNeural')
#         file_name = request.json.get('file_name', 'audio/output.mp3')
#     else:
#         content = request.args.get('text', '')
#         voice = request.args.get('voice', 'en-US-AvaNeural')
#         file_name = request.args.get('file_name', 'audio/output.mp3')
#
#     conversation_history.append({'role': 'user', 'content': content})
#     print('Thinking...')
#     response = large_language_model(content, conversation_history)
#     conversation_history.append({'role': 'assistant', 'content': response})
#     print(response)
#
#     if not response:
#         return jsonify({"error": "Missing text"}), 400
#
#     try:
#         communicate = edge_tts.Communicate(response, voice)
#         print(f"Saving audio to {file_name}")
#         await communicate.save(file_name)
#         print(f"Audio saved successfully: {file_name}")
#         return jsonify({"audio_file": f"http://127.0.0.1:5000/audio/{file_name}"})
#     except Exception as e:
#         print(f"Error occurred: {str(e)}")
#         return jsonify({"error": str(e)}), 500
#
# @app.route('/audio/<path:filename>', methods=['GET'])
# def get_audio(filename):
#     return send_from_directory(os.getcwd(), filename)
#
# if __name__ == '__main__':
#     setting = open('ai_setting_VTuber-Neuro sama.txt', 'r').read()
#     conversation_history = [{'role': 'system', 'content': f'{setting}'}]
#     app.run(host='0.0.0.0', port=5000)


# from language_generate import large_language_model
# from flask import Flask, request, jsonify, url_for, redirect
# from flask import send_from_directory
# from flask_cors import CORS
# import edge_tts
# import os
#
# app = Flask(__name__)
# CORS(app)
#
# @app.route('/dealAudio', methods=['GET'])
# async def deal_audio():
#     content = request.args.get('text')
#     conversation_history.append({'role': 'user', 'content': content})
#     print('Thinking...')
#     response = large_language_model(content, conversation_history)
#     conversation_history.append({'role': 'assistant', 'content': response})
#     print(response)
#     voice = request.args.get('voice', '')
#     file_name = request.args.get('file_name', 'audio/output.mp3')
#
#     if not response:
#         return jsonify({"error": "Missing text"}), 400
#
#     try:
#         communicate = edge_tts.Communicate(response, voice)
#         print(f"Saving audio to {file_name}")  # 调试输出
#         await communicate.save(file_name)
#         print(f"Audio saved successfully: {file_name}")  # 成功信息
#         return jsonify({"audio_file": f"http://127.0.0.1:5000/audio/{file_name}"})
#     except Exception as e:
#         print(f"Error occurred: {str(e)}")  # 错误信息
#         return jsonify({"error": str(e)}), 500
#
#
# @app.route('/audio/<path:filename>', methods=['GET'])
# def get_audio(filename):
#     return send_from_directory(os.getcwd(), filename)
#
#
# if __name__ == '__main__':
#     # You can set Initial Setting of AI
#     setting = open('ai_setting_VTuber-Neuro sama.txt', 'r').read()
#
#     # You can use dictionary to show it
#     conversation_history = [
#         {'role': 'system', 'content': f'{setting}'},
#     ]
#
#     app.run(host='127.0.0.1', port=5000)




# from language_generate import large_language_model
# from flask import Flask, request, jsonify, url_for, redirect
# from flask import send_from_directory
# from flask_cors import CORS
# import edge_tts
# import os
#
# app = Flask(__name__)
# CORS(app)
#
# @app.route('/')
# def index():
#     return redirect(url_for('static', filename='index.html'))
#
# @app.route('/dealAudio', methods=['POST'])
# def content_llm():
#     content = request.args.get('text')
#     conversation_history.append({'role': 'user', 'content': content})
#     print('Thinking...')
#     response = large_language_model(content, conversation_history)
#     conversation_history.append({'role': 'assistant', 'content': response})
#     print(response)
#     return response
#
# @app.route('/audio/output.mp3', methods=['POST'])
# async def text_to_speech():
#     response = content_llm()
#     voice = request.args.get('voice', '')
#     file_name = request.args.get('file_name', 'output.mp3')
#
#     if not response:
#         return jsonify({"error": "Missing text"}), 400
#
#     try:
#         communicate = edge_tts.Communicate(response, voice)
#         print(f"Saving audio to {file_name}")  # 调试输出
#         await communicate.save(file_name)
#         print(f"Audio saved successfully: {file_name}")  # 成功信息
#         return jsonify({"audio_file": f"http://127.0.0.1:5000/audio/{file_name}"})
#     except Exception as e:
#         print(f"Error occurred: {str(e)}")  # 错误信息
#         return jsonify({"error": str(e)}), 500
#
#
# @app.route('/audio/<path:filename>', methods=['GET'])
# def get_audio(filename):
#     return send_from_directory(os.getcwd(), filename)
#
# if __name__ == '__main__':
#     # You can set Initial Setting of AI
#     setting = open('ai_setting_VTuber-Neuro sama.txt', 'r').read()
#
#     # You can use dictionary to show it
#     conversation_history = [
#         {'role': 'system', 'content': f'{setting}'},
#     ]
#
#     app.run(host='0.0.0.0', port=5000)


# from flask import Flask, request, jsonify, send_from_directory
# from flask_cors import CORS
# import edge_tts
# import os
#
# app = Flask(__name__)
# CORS(app)
#
# @app.route('/dealAudio', methods=['GET'])
# async def deal_audio():
#     text = request.args.get('text')
#     voice = request.args.get('voice', 'zh-CN-XiaoxiaoNeural')
#     file_name = request.args.get('file_name', 'test.mp3')
#
#     if not text:
#         return jsonify({"error": "Missing text"}), 400
#
#     try:
#         communicate = edge_tts.Communicate(text, voice, proxy='127.0.0.1:7897')
#         await communicate.save(file_name)
#         return jsonify({"audio_file": f"http://127.0.0.1:2020/audio/{file_name}"})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
#
# @app.route('/audio/<path:filename>', methods=['GET'])
# def get_audio(filename):
#     return send_from_directory(os.getcwd(), filename)
#
# if __name__ == '__main__':
#     app.run(host='127.0.0.1', port=2020)