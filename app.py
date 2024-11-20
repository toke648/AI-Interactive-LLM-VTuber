from  language_generate import large_language_model
from flask import Flask, request, jsonify, url_for
from flask import send_from_directory
from flask_cors import CORS
import edge_tts
import os

app = Flask(__name__)
CORS(app)

@app.route('/dealAudio', methods=['GET'])
async def deal_audio():
    content = request.args.get('text')
    conversation_history.append({'role': 'user', 'content': content})
    response = large_language_model(content, conversation_history)
    conversation_history.append({'role': 'assistant', 'content': response})
    print(response)

    voice = request.args.get('voice', '')
    file_name = request.args.get('file_name', 'audio/output.mp3')

    if not response:
        return jsonify({"error": "Missing text"}), 400

    try:
        communicate = edge_tts.Communicate(response, voice)
        print(f"Saving audio to {file_name}")  # 调试输出
        await communicate.save(file_name)
        print(f"Audio saved successfully: {file_name}")  # 成功信息
        return jsonify({"audio_file": f"http://127.0.0.1:5000/audio/{file_name}"})
    except Exception as e:
        print(f"Error occurred: {str(e)}")  # 错误信息
        return jsonify({"error": str(e)}), 500

@app.route('/audio/<path:filename>', methods=['GET'])
def get_audio(filename):
    return send_from_directory(os.getcwd(), filename)

if __name__ == '__main__':
    # You can set Initial Setting of AI
    setting = open('ai_setting.txt', 'r').read()

    # You can use dictionary to show it
    conversation_history = [
        {'role': 'system', 'content': f'{setting}'},
    ]

    app.run(host='127.0.0.1', port=5000)


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