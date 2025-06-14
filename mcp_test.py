# 假设这段代码和你写的mcp_tool.py在同一目录

import mcp_tool
from mcp_tool import *

from pydub import AudioSegment
from pydub.playback import play

if __name__ == "__main__":
    expr = "math.sin(math.pi / 2) + random.randint(1, 10)"
    result = 计算器(expr)
    print("计算结果:", result)

    path = r"audio\output.mp3"
    play(AudioSegment.from_mp3(path)) #  播放音频

    # music = mcp_tool.播放酷狗歌曲API_输入音乐名字("Moon Halo")
    # print("音乐播放结果:", music)

    # 列出所有可用的工具(mcp_tool.py种的可用函数)
    
