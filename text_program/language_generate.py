from openai import OpenAI
import json
import time

# Function to get response from the language model
def large_language_model(content,conversation_history, retries=3):
    conversation_history.append({'role': 'user', 'content': content})

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
            # Add assistant's response to conversation history
            conversation_history.append({'role': 'assistant', 'content': result})
            return result
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(2)  # wait retry
            else:
                raise  # If all retries fail, throw an exception
