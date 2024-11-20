# from keyring.util.platform_ import config_root
# from openai import OpenAI
# import pandas as pd
# import json
#
#
# # 全局变量 global
# # global list_content
#
# # Large-language-model
# def  large_language_model(content):
#
#
#     message = [{'role': 'system', 'content': 'Your name is neuro-sama, you are a Vtuber Anchor, And you are currently live streaming now.'},
#               {'role': 'user', 'content': f'{content}'},
#                ]
#
#     # lambda
#
#     # system_content = None
#     # user_content = None
#     #
#     # client = OpenAI(
#     #     # you need input your api_key
#     #     # api_key='your api_key',
#     #     api_key='sk-707613869ffe4b06b165e396e580f847',
#     #     base_url='https://dashscope.aliyuncs.com/compatible-mode/v1'
#     # )
#     #
#     # completion = client.chat.completions.create(
#     #     model='qwen-plus',  # Model List:https://help.aliyun.com/zh/model-studio/getting-started/models
#     #     messages=[
#     #         {'role': 'system', 'content': 'Your name is neuro-sama, you are a Vtuber Anchor, And you are currently live streaming now.'},
#     #         {'role': 'user', 'content': f'{content}'},
#     #     ]
#     # )
#     #
#     # qwen_plus = completion.model_dump_json()
#     # data = json.loads(qwen_plus)
#     #
#     # result = data['choices'][0]['message']['content']
#
#     result = "Hi, I'm neuro-sama."
#
#     conversation_history.append({'role': 'system', 'content': f'{result}'})
#     conversation_history.append({'role': 'user', 'content': f'{content}'})
#
#
#     df = pd.DataFrame(conversation_history)
#     print(df)
#     df.to_excel('output.xlsx', index=True)
#     return result
#
# # Text-to-speech
# def speech_generation_model():
#     pass
#
# # GUI
# def gui():
#     pass
#
# def main():
#     for i in range(30):
#         content = input('>>> ')
#         if content == 'exit':
#             break
#         else:
#             large_language_model(content)
#
#
# if __name__ == '__main__':
#     conversation_history = []
#
#     main()


# from keyring.util.platform_ import config_root
# from openai import OpenAI
# import pandas as pd
# import json
#
#
# # 全局变量 global
# # global list_content
#
# # Large-language-model
# def  large_language_model(content, conversation_history):
#     # lambda
#
#     system_content = None
#     user_content = None
#
#     client = OpenAI(
#         # you need input your api_key
#         # api_key='your api_key',
#         api_key='sk-707613869ffe4b06b165e396e580f847',
#         base_url='https://dashscope.aliyuncs.com/compatible-mode/v1'
#     )
#
#     completion = client.chat.completions.create(
#         model='qwen-plus',  # Model List:https://help.aliyun.com/zh/model-studio/getting-started/models
#         messages=conversation_history
#     )
#
#     qwen_plus = completion.model_dump_json()
#     data = json.loads(qwen_plus)
#
#     result = data['choices'][0]['message']['content']
#
#     conversation_history.append({'role': 'system', 'content': f'{result}'})
#     conversation_history.append({'role': 'user', 'content': f'{content}'})
#
#     df = pd.DataFrame(conversation_history)
#     print(df)
#     df.to_excel('output.xlsx', index=True)
#     return result
#
# # Text-to-speech
# def speech_generation_model():
#     pass
#
# # GUI
# def gui():
#     pass
#
# def main():
#
#
#     for i in range(30):
#         content = input('>>> ')
#         if content == 'exit':
#             break
#         else:
#             conversation_history = [
#                 {'role': 'system',
#                  'content': 'Your name is neuro-sama, you are a Vtuber Anchor, And you are currently live streaming now.'},
#                 {'role': 'user', 'content': f'{content}'},
#             ]
#             large_language_model(content, conversation_history)
#
#
# if __name__ == '__main__':
#     main()


# import json
# import pandas as pd
# from hvplot import output
# from openai import OpenAI
# from playsound import playsound
# import edge_tts
# import asyncio
#
# from pygame.examples.music_drop_fade import volume
#
# # 定义全局对话历史
# conversation_history = [
#     {'role': 'system',
#      'content': 'You are a helpful assistant.'}
# ]
#
#
# async def large_language_model(content):
#     global conversation_history  # 引用全局变量
#
#     client = OpenAI(
#         api_key='sk-707613869ffe4b06b165e396e580f847',  # 使用安全方法处理API密钥
#         base_url='https://dashscope.aliyuncs.com/compatible-mode/v1'
#     )
#
#     try:
#         completion = client.chat.completions.create(
#             model='qwen-plus',
#             messages=conversation_history + [{'role': 'user', 'content': content}]
#         )
#
#         qwen_plus = completion.model_dump_json()
#         data = json.loads(qwen_plus)
#         result = data['choices'][0]['message']['content']
#
#         # 更新对话历史
#         conversation_history.append({'role': 'user', 'content': content})
#         conversation_history.append({'role': 'system', 'content': result})
#
#         # 保存到Excel
#         df = pd.DataFrame(conversation_history)
#         df.to_excel('output.xlsx', index=True)
#
#         return result
#     except Exception as e:
#         print(f"发生错误: {e}")
#         return "抱歉，处理您的请求时出现错误。"
#
# # Text-to-speech
# async def speech_generation_model(text, output):
#     # 以下是可选的声音：选择一个即可
#     # voice = 'zh-CN-XiaoxiaoNeural'
#     # voice = 'zh-CN-XiaoyiNeural'
#     voice = 'en-US-AvaNeural'
#     # voice = 'zh-CN-YunjianNeural'
#     # voice = 'zh-CN-YunxiNeural'
#     # voice = 'zh-CN-YunxiaNeural'
#     # voice = 'zh-CN-YunyangNeural'
#
#     rate = '-15%'
#     volume = '+50%'
#
#     tts = edge_tts.Communicate(text=text, voice=voice, rate=rate, volume=volume)
#     await tts.save(output)
#
# def gui():
#     pass
#
# async def main():
#     text = ''
#     output = 'C:\\Users\\16673\\Desktop\\output.mp3'
#
#     while True:
#         # 大语言模型openai+通义千问
#         content = input('\n>>> ')
#         if content.lower() == 'exit':
#             break
#         else:
#             response = large_language_model(content)
#             print(response)
#             text = response
#
#     # 语音生成模型edge-tts
#     await speech_generation_model(text, output)
#
#     playsound(output)
#
# if __name__ == '__main__':
#     main()



# from playsound import playsound
# from openai import OpenAI
# import pandas as pd
# import edge_tts
# import asyncio
# import json
#
# # 定义全局对话历史
# conversation_history = [
#     {'role': 'system', 'content': 'You are a helpful assistant.'}
# ]
#
# async def large_language_model(content):
#     global conversation_history  # 引用全局变量
#
#     client = OpenAI(
#         api_key='sk-707613869ffe4b06b165e396e580f847',  # 使用安全方法处理API密钥
#         base_url='https://dashscope.aliyuncs.com/compatible-mode/v1'
#     )
#
#     try:
#         completion = client.chat.completions.create(
#             model='qwen-plus',
#             messages=conversation_history + [{'role': 'user', 'content': content}]
#         )
#
#         qwen_plus = completion.model_dump_json()
#         data = json.loads(qwen_plus)
#         result = data['choices'][0]['message']['content']
#
#         # 更新对话历史
#         conversation_history.append({'role': 'user', 'content': content})
#         conversation_history.append({'role': 'system', 'content': result})
#
#         # 保存到Excel
#         df = pd.DataFrame(conversation_history)
#         df.to_excel('output.xlsx', index=True)
#
#         return result
#     except Exception as e:
#         print(f"发生错误: {e}")
#         return "抱歉，处理您的请求时出现错误。"
#
# # Text-to-speech
# async def speech_generation_model(text, output):
#     voice = 'en-US-AvaNeural'
#     rate = '-15%'
#     volume = '+50%'
#
#     try:
#         tts = edge_tts.Communicate(text=text,
#                                    voice=voice,
#                                    rate=rate,
#                                    volume=volume,
#                                    proxy='http://127.0.0.1:7897')
#         await tts.save(output)
#     except Exception as e:
#         print(f"语音生成发生错误: {e}")
#
# async def main():
#     output = 'sound.mp3'
#
#     while True:
#         content = input('\n>>> ')
#         if content.lower() == 'exit':
#             break
#         else:
#             response = await large_language_model(content)
#             print(type(response))
#             print(response)
#             #
#             # # 语音生成模型edge-tts
#             # await speech_generation_model(response, output)
#             # playsound(output)
#
# if __name__ == '__main__':
#     asyncio.run(main())

# from playsound import playsound
# from openai import OpenAI
# import pandas as pd
# import edge_tts
# import asyncio
# import json
#
# # 定义全局对话历史
# conversation_history = [
#     {'role': 'system', 'content': 'You are a helpful assistant.'}
# ]
#
# async def large_language_model(content):
#     global conversation_history  # 引用全局变量
#
#     client = OpenAI(
#         api_key='sk-707613869ffe4b06b165e396e580f847',  # 使用安全方法处理API密钥
#         base_url='https://dashscope.aliyuncs.com/compatible-mode/v1'
#     )
#
#     try:
#         completion = client.chat.completions.create(
#             model='qwen-plus',
#             messages=conversation_history + [{'role': 'user', 'content': content}]
#         )
#
#         qwen_plus = completion.model_dump_json()
#         data = json.loads(qwen_plus)
#         result = data['choices'][0]['message']['content']
#
#         # 更新对话历史
#         conversation_history.append({'role': 'user', 'content': content})
#         conversation_history.append({'role': 'system', 'content': result})
#
#         # 保存到Excel
#         df = pd.DataFrame(conversation_history)
#         df.to_excel('output.xlsx', index=True)
#
#         return result
#     except Exception as e:
#         print(f"发生错误: {e}")
#         return "抱歉，处理您的请求时出现错误。"
#
# # Text-to-speech
# async def speech_generation_model(text, output):
#     voice = 'en-US-AvaNeural'
#     rate = '-15%'
#     volume = '+50%'
#
#     try:
#         tts = edge_tts.Communicate(text=text,
#                                    voice=voice,
#                                    rate=rate,
#                                    volume=volume,
#                                    proxy='http://127.0.0.1:7897')
#         await tts.save(output)
#     except Exception as e:
#         print(f"语音生成发生错误: {e}")
#
# async def main():
#     output = 'sound.mp3'
#
#     while True:
#         content = input('\n>>> ')
#         if content.lower() == 'exit':
#             break
#         else:
#             response = await large_language_model(content)
#             print(type(response))
#             print(response)
#             #
#             # # 语音生成模型edge-tts
#             # await speech_generation_model(response, output)
#             # playsound(output)
#
# if __name__ == '__main__':
#     asyncio.run(main())
from playsound import playsound
from openai import OpenAI
import pandas as pd
import edge_tts
import asyncio
import time
import json


# Function to get response from the language model
def large_language_model(content, retries=3):
    client = OpenAI(
        api_key="sk-707613869ffe4b06b165e396e580f847",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    # Requesting completion from the conversation history
    for attempt in range(retries):
        try:
            completion = client.chat.completions.create(
                model="qwen-plus",
                messages=conversation_history
            )
            qwen_plus = completion.model_dump_json()
            data = json.loads(qwen_plus)
            result = data['choices'][0]['message']['content']
            return result
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(2)  # 等待重试
            else:
                raise  # 如果所有重试都失败，抛出异常

# Asynchronous function for speech generation
async def speech_generation_model(response):
    text = response
    voice = 'en-US-AvaNeural'  # Change voice as needed
    output = r'C:\Users\16673\Desktop\yuyin4.mp3'
    rate = '-10%'
    volume = '+50%'

    try:
        tts = edge_tts.Communicate(text=text,
                                   voice=voice,
                                   rate=rate,
                                   volume=volume,
                                   proxy='http://127.0.0.1:7897')
        await tts.save(output)
    except Exception as e:
        print(f'Error during speech generation: {e}')


# GUI
def gui():
    pass


# Main execution part
if __name__ == '__main__':
    conversation_history = [
        {'role': 'system', 'content': 'You are a helpful assistant.'},
    ]

    while True:
        content = input('\n>>> ')
        if content.lower() == 'exit':
            break
        else:
            # Add user input to conversation history
            conversation_history.append({'role': 'user', 'content': content})
            try:
                # Get the model's response
                response = large_language_model(content)
                print(response)

                # Add assistant's response to conversation history
                conversation_history.append({'role': 'assistant', 'content': response})

                # Generate speech
                asyncio.run(speech_generation_model(response))

                # Play audio file
                audio_file_path = "C:/Users/16673/Desktop/audio.mp3"
                playsound(audio_file_path)
                print(conversation_history)
            except Exception as e:
                print(f'Error playing audio: {e}')