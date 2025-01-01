from main_setting import MainSetting
from openai import OpenAI
import pandas as pd
import json

class ContentGenerate:
    def __init__(self):
        # 形参会被重新赋值，实参不会
        self.settings = MainSetting()
        self.content_history = [{'role': 'system', 'content': f'{self.settings.system_prompt}'}]

    # Function to get response from the language model
    def generate_content(self,
                         content: str
                         ) -> str:
        try:
            self.content_history.append({'role': 'user', 'content': content})
            pd.DataFrame(self.content_history)

            client = OpenAI(
                api_key=self.settings.openai_api_key,
                base_url=self.settings.openai_base_url,
            )

            # Requesting completion from the conversation history
            completion = client.chat.completions.create(
                model=self.settings.models,
                messages=self.content_history
            )

            # back message
            back_message = completion.model_dump_json()
            # 'str' turn to 'dict' | <class 'str'> ——> <class 'dict'>
            data = json.loads(back_message)
            # access the result
            result = data['choices'][0]['message']['content']

            # add result to history
            self.content_history.append({'role': 'assistant', 'content': result})
            return result
        except Exception as e:
            print(f'error: {e}')
            return ""

    def ollama_content(self,
                       content: str
                       ) -> str:
        try:
            self.content_history.append({'role': 'user', 'content': content})
            pd.DataFrame(self.content_history)

            client = OpenAI(
                # if you have not configured the environment variable, please replace the following line with: api_key="sk-xxx",
                api_key="ollama",
                base_url="http://localhost:11434/v1/",
            )

            completion = client.chat.completions.create(
                model="qwen2.5:7b",  # model list: https://help.aliyun.com/zh/model-studio/getting-started/models
                messages=self.content_history
            )

            ollama_message = completion.choices[-1].message.content

            return ollama_message
        except Exception as e:
            print(f'Error {e}')
            return ''







