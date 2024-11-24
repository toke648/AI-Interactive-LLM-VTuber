from main_setting import MainSetting
from openai import OpenAI
import pandas as pd
import json

class ContentGenerate:
    def __init__(self):
        # 踩坑警告： 引用外部对象时
        # 引用函数MainSetting
        # 引用变量MainSetting()
        # 因此建议只要引用就使用MainSetting这种方法

        # 形参会被重新赋值，实参不会
        self.settings = MainSetting()
        self.content_history = [{'role': 'system', 'content': f'{self.settings.system_prompt}'}]

    # Function to get response from the language model
    def generate_content(self, content: str):
        try:
            self.content_history.append({'role': 'user', 'content': content})
            pd.DataFrame(self.content_history)

            client = OpenAI(
                api_key=self.settings.api_key,
                base_url=self.settings.base_url,
            )

            # Requesting completion from the conversation history
            completion = client.chat.completions.create(
                model=self.settings.models,
                messages=self.content_history
            )

            # 返回原始数据
            back_message = completion.model_dump_json()
            # 解析输出将字符转换为字典类型  <class 'str'> ——> <class 'dict'>
            data = json.loads(back_message)
            # 解析后的文本
            result = data['choices'][0]['message']['content']

            # 将助手的回复添加到对话历史
            self.content_history.append({'role': 'assistant', 'content': result})
            return result
        except Exception as e:
            print(f'error: {e}')
            return ""







