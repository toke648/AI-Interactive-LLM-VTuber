from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key="ollama",
    base_url="http://localhost:11434/v1/",
)
completion = client.chat.completions.create(
    model="qwen2.5:7b",  # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=[
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': '你是谁？'}],
)

ollama_message = completion.choices[-1].message.content

print(ollama_message)


