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
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
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
            print('Please check your Alibaba Cloud Tongyi Qianwen API Key or Download location Ollama models')
            print('Please check the API Key and Base URL')
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
                model=self.settings.models,  # model list: https://help.aliyun.com/zh/model-studio/getting-started/models
                messages=self.content_history
            )

            ollama_message = completion.choices[-1].message.content

            return ollama_message
        except Exception as e:
            print(f'Error {e}')
            return ''
    
    def deepseek_content(self,
                         content: str
                         ) -> str:
        try:
            self.content_history.append({'role': 'user', 'content': content})
            pd.DataFrame(self.content_history)

            client = OpenAI(
                api_key=self.settings.openai_api_key,
                base_url="https://api.deepseek.com",
            )

            completion = client.chat.completions.create(
                model=self.settings.models,
                messages=self.content_history,
                stream=False # stream is False by default
            )

            deepseek_message = completion.choices[0].message.content
            self.content_history.append({'role': 'assistant', 'content': deepseek_message})

            return deepseek_message
        
        except Exception as e:
            print(f'Error {e}')
            return ''
        
    def zhipuai_content(self,
                         content: str
                         ) -> str:
        try:
            self.content_history.append({'role': 'user', 'content': content})
            pd.DataFrame(self.content_history)
            client = OpenAI(
                api_key="63f72c10e53241509645b29dfc5f06c8.x0RKmLAYwR7uJMsr",
                base_url="https://open.bigmodel.cn/api/paas/v4/",
            )
            completion = client.chat.completions.create(
                model="GLM-4-Flash",
                messages=self.content_history
            )
            zhipuai_message = completion.choices[0].message.content
            self.content_history.append({'role': 'assistant', 'content': zhipuai_message})
            return zhipuai_message
        except Exception as e:
            print(f'Error {e}')
            return ''