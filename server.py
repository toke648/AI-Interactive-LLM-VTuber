from flask import Flask, jsonify, request, redirect, url_for, send_from_directory
from main_setting import MainSetting
# import playsound  # 移除阻塞本地播放
import speech_recognition as sr
from llm import Generation_LLM
from tts import Generation_Audio
from sr import audio_record
from flask_cors import CORS
import logging
import asyncio
import os
import json
import threading
import subprocess
import sys

settings = MainSetting()
speech_generator = Generation_Audio.SpeechGenerator()
content_generator = Generation_LLM.ContentGenerate()
speech_recognizer = audio_record.SpeechRecognizer(language='zh-CN')
recognizer = sr.Recognizer()

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()])

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['AUDIO_FOLDER'] = settings.audio_directory
os.makedirs(settings.audio_directory, exist_ok=True)

# 热更新：在不重启进程的情况下重新加载 main_setting.json 并更新相关实例
def reload_all_settings() -> dict:
    """Reload settings from disk and propagate to generators and app config."""
    global settings, speech_generator, content_generator
    # 重新载入配置
    new_settings = MainSetting()
    settings = new_settings
    # 更新 TTS 生成器引用的设置
    try:
        speech_generator.settings = new_settings
    except Exception:
        pass
    # 更新 LLM 生成器引用的设置与系统提示
    try:
        content_generator.settings = new_settings
        # 将历史中的 system 提示更新为新提示（保留 user/assistant 历史）
        if content_generator.content_history:
            if content_generator.content_history[0].get('role') == 'system':
                content_generator.content_history[0]['content'] = new_settings.system_prompt or ''
            else:
                content_generator.content_history.insert(0, {'role': 'system', 'content': new_settings.system_prompt or ''})
        else:
            content_generator.content_history = [{'role': 'system', 'content': new_settings.system_prompt or ''}]
    except Exception:
        pass
    # 刷新音频目录配置
    app.config['AUDIO_FOLDER'] = new_settings.audio_directory
    os.makedirs(new_settings.audio_directory, exist_ok=True)
    return {
        'audio_directory': new_settings.audio_directory,
        'audio_file': new_settings.audio_file,
        'tts_voice': new_settings.tts_voice,
        'llm_model': new_settings.models
    }

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
            for key, value in new_config.items():
                if key in ['tts', 'llm', 'path']:
                    current_config[key].update(value)
                else:
                    current_config[key] = value
            with open('main_setting.json', 'w', encoding='utf-8') as f:
                json.dump(current_config, f, indent=4, ensure_ascii=False)
            self.load_config()
            return True
        except Exception as e:
            print(f"配置更新失败: {str(e)}")
            return False

update = update_settings()

# 路由配置
# 默认路由为 static/index.html 作为首页
@app.route('/')
def index():
    return redirect(url_for('static', filename='index.html'))

# favicon.ico 路由 用于在浏览器标签中显示图标
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/x-icon')

is_recording = False
# 最近一次语音识别文本（用于前端自动填充并转文本模式发送）
last_asr_text = ""

# MCP 子进程句柄（用于启动/停止 Windows 工具 MCP 服务）
mcp_process = None

"""
mcp功能暂时不支持，可能需要一个专门的解析服务器，但有基础代码文件，后面在此基础上进行更新

- 能不能用
  - 现在“能启动/停止”本地 MCP 服务（顶部右侧 MCP 按钮）。已集成的 `mcp_tool.py` 内含多种工具，但当前前端还没直接“调用工具”的面板；需要 MCP 客户端或我再加一个调用入口。

- 怎么使用（当前）
  - 点击顶部“MCP: 未运行（点击启动）”启动；再次点击可停止。
  - 启动后，支持 MCP 协议的客户端/Agent（如支持 Model Context Protocol 的 IDE/Agent）可通过 stdio 方式调用这个子进程内的工具。
  - 想在本网页里直接用：我可立即加“工具面板”和一个后端 `/mcp/invoke` 端点，前端表单就能直接调用这些工具。

- 能实现什么操作（来自 `mcp_tool.py`）
  - 计算器：执行 Python 表达式（含 `math`/`random`）。
  - 运行软件：按预设名或绝对路径启动本地程序（支持 `.lnk`）。
  - 打开网址：用默认浏览器打开 URL。
  - 运行 CMD：执行预设/自定义命令并回显输出。
  - 创建文件并写入内容。
  - 读取剪贴板内容。
  - 酷狗歌曲搜索与播放（免费曲目下载后播放）。

- 工作原理（简述）
  - `mcp_tool.py` 使用 FastMCP 将一系列 Python 函数“声明”为 MCP 工具。
  - 我们通过 Flask 启停一个“子进程”来跑 MCP 服务（stdio 通讯）。MCP 客户端/Agent 负责和它对话，调用工具并拿结果。
  - 目前网页只负责启停；未直接把“调用工具”编排到你的对话/语音流程中。

- 如何与语音模型“交接”
  - 方案A（推荐，零侵入）：在网页增加“工具面板”（运行程序/打开网址/CMD等表单），点一下即走后端 `/mcp/invoke` 调 MCP 工具；AI 侧仍只产出文本，工具结果单独展示在侧栏。
  - 方案B（智能触发）：在文本发送前做“意图识别”（例如匹配“打开…/运行…”），命中就先调 MCP，执行成功后把结果拼进用户上下文，再送 LLM 生成回复。
  - 方案C（纯 MCP 客户端）：由外部支持 MCP 的 Agent 直接连接运行的子进程，按自己的策略调用工具；本网页只负责启停。

要不要我现在就：
- 增加后端 `/mcp/invoke`（传入 tool 名与参数），
- 在顶部加“工具面板”（运行程序/打开网址/CMD 三个快捷表单），
- 并把工具执行结果以卡片形式加入左侧历史栏？

这个mcp能用吗，怎么使用？能实现什么操作？工作原理是什么？怎么和语音模型交接的？

这个能实现最好，就不用前端的一堆按钮了，就算有也是在setting里面设置，
我觉得可以规范化输出，用一个专门的指令json栏用于指令或代码操作，然后
正常的文本就在contact的json里面正常输出这种

{
  "content": "好的，我帮你打开记事本。",
  "instruction": {
    "tool": "运行电脑端软件文件或程序",
    "args": { "program_name": "记事本" }
  }
}
"""

def wake_word_detected():
    """语音识别函数，在录音线程中调用"""
    while is_recording:
        text = speech_recognizer.record(recognizer=recognizer, language='zh-CN')
        if not is_recording:
            break
        if text:
            print("ASR ok:", text)
            return text
        else:
            print("未检测到语音，继续监听...")
    return None


def record_thread():
    """
    录音线程：只负责ASR识别，将结果写入 last_asr_text，
    不再直接在服务端生成回复与音频，交由前端拿到文本后走 /text 流程。
    """
    global is_recording, last_asr_text
    print("录音线程启动")
    while is_recording:
        text = wake_word_detected()
        if not text:
            continue
        print("ASR 捕获:", text)
        # 覆盖最近一次识别文本（前端读取一次后清空）
        last_asr_text = text
        # 若需要单句即停，可在此处自动停止录音
        # is_recording = False
        if not is_recording:
            break

    print("录音线程结束")

# 健康检查路由
@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200

# 开始录音路由
@app.route('/start_record', methods=['POST'])
def start_record():
    global is_recording
    if not is_recording:
        is_recording = True
        threading.Thread(target=record_thread, daemon=True).start()
    return jsonify({'status': 'recording'})

# 停止录音路由
@app.route('/stop_record', methods=['POST'])
def stop_record():
    global is_recording
    is_recording = False
    # 改为仅返回状态，音频将由前端基于 /text 生成
    return jsonify({'status': 'stopped'})

# 获取最新音频路由
@app.route('/latest_audio', methods=['GET'])
def latest_audio():
    audio_path = os.path.join(settings.audio_directory, settings.audio_file)
    if os.path.exists(audio_path):
        absolute_url = request.host_url.rstrip('/') + f"/audio/{settings.audio_file}"
        return jsonify({'audio_file': absolute_url})
    return jsonify({'error': 'not ready'}), 404

@app.route('/latest_asr', methods=['GET'])
def latest_asr():
    """返回最近一次ASR文本，并在读取后清空，避免重复消费"""
    global last_asr_text
    if last_asr_text:
        text = last_asr_text
        last_asr_text = ""
        return jsonify({'text': text})
    return jsonify({'error': 'no asr'}), 404

# ============================= MCP 控制 =============================
@app.route('/mcp/status', methods=['GET'])
def mcp_status():
    global mcp_process
    alive = bool(mcp_process and (mcp_process.poll() is None))
    return jsonify({'running': alive})

@app.route('/mcp/start', methods=['POST'])
def mcp_start():
    """启动 mcp_tool.py 作为子进程（仅在未运行时启动）"""
    global mcp_process
    if mcp_process and (mcp_process.poll() is None):
        return jsonify({'running': True, 'message': 'MCP 已在运行'}), 200
    try:
        mcp_process = subprocess.Popen([sys.executable, 'mcp_tool.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return jsonify({'running': True, 'message': 'MCP 已启动'}), 200
    except Exception as e:
        return jsonify({'running': False, 'error': str(e)}), 500

@app.route('/mcp/stop', methods=['POST'])
def mcp_stop():
    """停止 mcp_tool.py 子进程"""
    global mcp_process
    try:
        if mcp_process and (mcp_process.poll() is None):
            mcp_process.terminate()
            mcp_process = None
            return jsonify({'running': False, 'message': 'MCP 已停止'})
        return jsonify({'running': False, 'message': 'MCP 未运行'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 处理文本路由
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
        audio_path = os.path.join(settings.audio_directory, settings.audio_file)
        if not os.path.exists(audio_path):
            return jsonify({'error': 'Audio not generated'}), 500
        audio_url = request.host_url.rstrip('/') + f"/audio/{settings.audio_file}"
        return jsonify({'audio_file': audio_url, 'text': content})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 获取音频路由
@app.route('/audio/<path:filename>', methods=['GET'])
def get_audio(filename):
    return send_from_directory(settings.audio_directory, filename)

# 获取设置路由
@app.route('/settings', methods=['GET'])
def get_settings():
    try:
        with open('main_setting.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        return jsonify(config)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 更新设置路由
@app.route('/settings', methods=['POST'])
def update_settings_route():
    try:
        new_config = request.json
        if update.update_config(new_config):
            info = reload_all_settings()
            return jsonify({'message': '配置更新成功', 'applied': info})
        return jsonify({'error': '配置更新失败'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/reload_settings', methods=['POST'])
def reload_settings_route():
    """手动触发热更新，无需修改文件内容即可让内存中的设置与磁盘同步。"""
    try:
        info = reload_all_settings()
        return jsonify({'message': '重载完成', 'applied': info})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
