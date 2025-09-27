""" utf-8 encoding Generation_LLM.py """
from main_setting import MainSetting
from openai import OpenAI
import pandas as pd
import json

class ContentGenerate:
    """内容生成类"""
    def __init__(self):
        """初始化内容生成类"""
        self.settings = MainSetting()
        self.content_history = [
            {'role': 'system', 'content': f'{self.settings.system_prompt}'}
        ]

    def _client(self) -> OpenAI:
        """初始化OpenAI客户端"""
        return OpenAI(
            api_key=self.settings.openai_api_key,
            base_url=(self.settings.openai_base_url or None)
        )

    
    def _chat(self, content: str, model: str) -> str:
        try:
            self.content_history.append({'role': 'user', 'content': content})
            pd.DataFrame(self.content_history)
            client = self._client()
            completion = client.chat.completions.create(
                model=model or self.settings.models,
                messages=self.content_history
            )
            message = completion.choices[0].message.content
            self.content_history.append({'role': 'assistant', 'content': message})
            return message
        except Exception as e:
            print(f'LLM error: {e}')
            return ''

    def generate_content(self, content: str) -> str:
        return self._chat(content, self.settings.models)

    def ollama_content(self, content: str) -> str:
        return self._chat(content, self.settings.models)

    def deepseek_content(self, content: str) -> str:
        return self._chat(content, self.settings.models)

    def zhipuai_content(self, content: str) -> str:
        return self._chat(content, self.settings.models)
