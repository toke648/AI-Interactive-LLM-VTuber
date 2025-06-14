from mcp.server.fastmcp import FastMCP
import logging
import subprocess
import webbrowser
import math
import random
#import ctypes
import sys
import os
#import requests
#from bs4 import BeautifulSoup

# mcp_tool.py

# -------------------------------------------------------------------------------------------------
# 配置编码和日志
# 确保输出和日志使用正确的编码，避免中文字符显示问题
if sys.stderr.reconfigure(encoding='utf-8'):
    sys.stderr.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('Windows_MCP_Tools')
# -------------------------------------------------------------------------------------------------

# 创建MCP服务器实例
mcp = FastMCP("WindowsToos")

# -------------------------------------------------------------------------------------------------
# 获取当前脚本所在的目录
# 这样可以确保我们能够正确找到预设文件，而无需手动指定绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))

# 构建预设文件的完整路径
# 假设预设文件位于当前目录下的"预设"子文件夹中
programs_file_path = os.path.join(current_dir, "预设", "程序预设.txt")
commands_file_path = os.path.join(current_dir, "预设", "命令预设.txt")

# -------------------------------------------------------------------------------------------------

# 读取预设文件
def load_presets(file_path: str) -> dict:
    """
    从指定的文本文档中加载预设信息。
    参数： file_path: 文本文档的路径
    """
    try:
        presets = {}
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line:
                    # 分割键值对，格式为 "键=值"
                    key, value = line.split('=', 1)
                    presets[key] = value
        return presets
    except FileNotFoundError:
        logger.error(f"预设文件 {file_path} 未找到")
        return {}
    except Exception as e:
        logger.error(f"读取预设文件 {file_path} 时出错: {str(e)}")
        return {}

# 加载预设
preset_programs = load_presets(programs_file_path)
preset_commands = load_presets(commands_file_path)

# 读取token
def load_token(file_path: str) -> str:
    """
    从指定的文本文档中加载token。
    参数： file_path: 文本文档的路径
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            token = file.read().strip()
            return token
    except FileNotFoundError:
        logger.error(f"token文件 {file_path} 未找到")
        return ""
    except Exception as e:
        logger.error(f"读取token文件 {file_path} 时出错: {str(e)}")
        return ""

# -------------------------------------------------------------------------------------------------


# 添加一个计算器工具
@mcp.tool()
def 计算器(python_expression: str) -> dict:
    """
    用于数学计算时，请始终使用此工具来计算 Python 表达式的结果。
    可以使用 `math` 和 `random` 模块。
    """
    result = eval(python_expression)
    logger.info(f"计算公式：{python_expression}，结果：{result}")
    return {"是否成功": True, "结果": result}

# -------------------------------------------------------------------------------------------------

# 定义工具函数：运行电脑端程序
@mcp.tool()
def 运行电脑端软件文件或程序(program_name: str) -> dict:
    """
    运行预设程序或指定路径的程序
    参数： program_name: 程序名称或路径，例如 "记事本" 或 "C:\\Windows\\System32\\notepad.exe"
    """
    try:
        # 如果是预设程序名称，则获取对应的路径
        program_path = preset_programs.get(program_name, program_name)
        if program_path.endswith('.lnk'):
            # 如果是.lnk文件，使用os.startfile打开
            os.startfile(program_path)
        else:
            # 否则直接运行程序
            subprocess.Popen(program_path)
        logger.info(f"\n\n运行程序：{program_path}\n")
        return {"是否成功": True, "结果": f"程序已启动：{program_path}"}
    except Exception as e:
        logger.error(f"\n\n错误！程序: {program_name} 运行失败！: {str(e)}\n")
        return {"是否成功": False, "错误请检查路径": str(e)}

# -------------------------------------------------------------------------------------------------
# 定义工具函数：在电脑上打开URL网址
@mcp.tool()
def 在电脑上打开URL网址(url: str) -> dict:
    """
    打开指定URL的网页。在电脑的浏览器上
    参数： url: 网页URL，例如 "https://www.baidu.com"
    """
    try:
        webbrowser.open(url)
        logger.info(f"\n\n执行打开URL网页: {url}\n")
        return {"是否成功": True, "结果": f"网页已打开：{url}"}
    except Exception as e:
        logger.error(f"错误！网页 {url} 打开失败！: {str(e)}\n")
        return {"是否成功": False, "错误": str(e)}

# -------------------------------------------------------------------------------------------------


# 定义工具函数：在电脑上运行CMD指令
@mcp.tool()
def 在电脑上运行CMD命令(command_name: str) -> dict:
    """
    运行预设CMD指令或指定的CMD指令。控制查看操作电脑信息/状态/锁定电脑等
    参数： command_name: CMD指令名称或命令，例如 "锁定电脑" 或 "ipconfig"
    """
    try:
        # 如果是预设指令名称，则获取对应的命令
        command = preset_commands.get(command_name, command_name)
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        logger.info(f"\n\n执行 CMD 命令: {command}\n执行结果: {output}\n")

        return {"是否成功": True, "结果": f"命令执行成功：\n{output}"}
    except Exception as e:
        logger.error(f"错误！运行 CMD 命令：{command_name} 失败！: {str(e)}\n")
        return {"是否成功": False, "错误": str(e)}

# -------------------------------------------------------------------------------------------------
   
# 定义工具函数：创建文件写入内容
@mcp.tool()
def 在电脑上创建文件与写入内容(file_path: str, content: str) -> dict:
    """
    在指定路径创建文件并写入内容
    参数： file_path: 文件路径，例如 "C:\\小智创建的文件.txt"
    参数： content: 要写入的内容
    """
    try:
        # 确保文件路径的目录存在
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        # 打开文件并写入内容
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        logger.info(f"\n\n文件创建并写入成功：{file_path}\n内容：{content}\n")
        return {"是否成功": True, "结果": f"文件已创建并写入成功：{file_path}"}
    except Exception as e:
        logger.error(f"创建文件并写入内容失败：{str(e)}")
        return {"是否成功": False, "错误": str(e)}

# -------------------------------------------------------------------------------------------------


# 定义工具函数：读取复制内容
@mcp.tool()
def 读取复制内容() -> dict:
    """
    读取计算机中复制的内容，比如复制题目，复制文字文本等
    """
    try:
        # 导入tkinter模块来处理剪贴板
        import tkinter as tk
        
        # 创建一个Tkinter根窗口
        root = tk.Tk()
        root.withdraw()  # 隐藏窗口
        
        # 从剪贴板读取内容
        clipboard_content = root.clipboard_get()
        
        # 销毁窗口
        root.destroy()
        
        logger.info(f"\n\n从剪贴板读取到内容: {clipboard_content[:50]}...\n")
        
        return {"是否成功": True, "结果": clipboard_content}
    except Exception as e:
        logger.error(f"读取剪贴板内容失败: {str(e)}")
        return {"是否成功": False, "错误": str(e)}

# -------------------------------------------------------------------------------------------------



from pydub import AudioSegment
from pydub.playback import play
import requests
# -------------------------------------------------------------------------------------------------
# 定义工具函数：在电脑上打开URL网址
@mcp.tool()
def 播放酷狗歌曲API_输入音乐名字(song_name: str) -> dict:
    """
    搜索歌曲并返回基础信息与播放链接。提供歌曲名即可。
    适用于获取歌曲播放链接、歌手、专辑等元信息。
    """
    try:
        response = requests.get(
            f"http://mobilecdn.kugou.com/api/v3/search/song?format=json&keyword={song_name}&page=1")
        data = response.json()
        song = data['data']['info'][0]
        
        songname = song['songname']
        singername = song['singername']
        album_id = song['album_id']
        audio_id = song['audio_id']
        hash = song['hash']
        duration = song['duration']
        pay_type = song['pay_type']

        hash_url = f"http://m.kugou.com/app/i/getSongInfo.php?cmd=playInfo&hash={hash}"
        song_info = requests.get(hash_url).json()
        mp3_url = song_info.get('url')
        backup_url = song_info.get('backup_url')[0]

        os.makedirs("music", exist_ok=True)  # 确保目录存在,如果不存在则创建

        if pay_type == 0: 
            pay_type="免费"

            # 下载音乐并播放
            response = requests.get(backup_url)
            if response.status_code == 200:
                with open(f"./music/{songname}.mp3", "wb") as f:
                    f.write(response.content)
                
                    play(AudioSegment.from_mp3(f"./music/{songname}.mp3"))
                logger.info(f"歌曲 {songname} 下载并播放成功")
                return f"success {songname}，类型:{pay_type} 搜索成功，开始播放..."

            else:
                logger.error(f"无法下载歌曲，状态码：{response.status_code}")

        # 判断播放类型       
        elif pay_type == 3: 
            pay_type == "付费"
            return f"success {songname}，类型:{pay_type} 付费歌曲暂时不支持播放..."


        # return {
        #     "success": True,
        #     "songname": songname,
        #     "singer": singername,
        #     "album_id": album_id,
        #     "audio_id": audio_id,
        #     "duration": duration,
        #     "pay_type": pay_type,
        #     "url": mp3_url,
        #     "backup_url": backup_url
        # }

    except Exception as e:
        logger.error(f"Error searching song: {e}")
        return f"failure error {e}"
# -------------------------------------------------------------------------------------------------


# 主程序入口
if __name__ == "__main__":
    logger.info("\n\n\tMCP_Windows服务已启动！等待调用！\n\n当前支持：\n1.运行电脑端程序 预设软件 或 具体路径\n2.在电脑上打开URL网址 网页名 或 具体URL网址\n3.在电脑上运行CMD指令 预设指令 或 具体指令\n4.官方的计算器示例\n5.创建文件写入内容\n6.读取复制内容\n\n快尝试让小智控制你的PC吧！\n\n\t\b版本：v6.2.6 (2025-06-03 更新)\n\t\tBy[粽子同学]\n\n")

    mcp.run(transport="stdio")
# -------------------------------------------------------------------------------------------------