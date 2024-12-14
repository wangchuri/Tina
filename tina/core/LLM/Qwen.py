"""
编写者：王出日
日期：2024，12，1
版本？

将Qwen（通义千问）的API封装成类，方便调用。
包含：
Qwen：类，包含初始化、生成函数。
    init：静态方法，用于初始化API、模型名称。
    generate：静态方法，用于生成回复。
"""
from openai import OpenAI

class Qwen:

    @staticmethod
    def init(api, model_name:str):
        Qwen.model_providers = {
            # 目前只支持Qwen（通义千问）
            "Qwen": "https://dashscope.aliyuncs.com/compatible-mode/v1"
        }
        Qwen.model_names = {
            "Qwen": "qwen-plus"
        }
        Qwen.model_provider = Qwen.model_providers[model_name]
        Qwen.model_name = Qwen.model_names[model_name]
        Qwen.api = api

    @staticmethod
    def generate(input_text:str,prompt:str="做好你的工作！",temperature:float=0.3) -> str:
        client = OpenAI(
            api_key=Qwen.api, 
            base_url=Qwen.model_provider,
        )
        completion = client.chat.completions.create(
            model=Qwen.model_name,
            messages=[
                {"role": "system", "content":   "你是一个好的助手"},
                {"role": "system", "content": prompt},
                {"role": "user", "content": input_text}
            ],
            temperature=temperature,
            # response_format={"type": format}
        )
        return completion.choices[0].message.content
    @staticmethod
    def stream(input_text:str,prompt:str="做好你的工作！",temperature:float=0.3) -> str:
        client = OpenAI(
            api_key=Qwen.api, 
            base_url=Qwen.model_provider,
        )
        completion = client.chat.completions.create(
            model=Qwen.model_name,
            messages=[
                {"role": "system", "content":   "你是一个好的助手"},
                {"role": "system", "content": prompt},
                {"role": "user", "content": input_text}
            ],
            temperature=temperature,
            stream=True,
            # response_format={"type": format}
        )
        message = ""
        for chunk in completion:
            message += chunk.choices[0].delta.content
            print(chunk.choices[0].delta.content)
        return message
        
# Example usage:
# Qwen.init(api="YOUR_API_KEY", model_name="Qwen")
# print(Qwen.generate("你好，请问有什么可以帮助您的？"))
if __name__ == '__main__':
    Qwen.init(api="sk-aa328698ca6f4a7c9c0dde0b9851a772", model_name="Qwen")
    print(Qwen.stream(input_text="你好，请问有什么可以帮助您的？"))

