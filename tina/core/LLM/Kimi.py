"""
编写者：王出日
日期：2024，12，1
版本？

将Kimi的API封装成类，方便调用。
包含：
Kimi：类，包含初始化、生成函数。
    init：静态方法，用于初始化API、模型名称。
    generate：静态方法，用于生成回复。
"""
from openai import OpenAI


class Kimi():

    @staticmethod
    def init(api):
        Kimi.api = api

    @staticmethod
    def generate(input_text,temperature=0.3,prompt="做好你的工作！你是最棒的",format="text",tools = []):
        client = OpenAI(
            api_key=Kimi.api, 
            base_url="https://api.moonshot.cn/v1",
        )
        if input_text == "":
            raise ValueError("输入不能为空")
        completion = client.chat.completions.create(
            model="moonshot-v1-auto",
            messages=[
                {"role": "system", "content": "你是一个好的助手"},
                {"role": "system", "content": prompt},
                {"role": "user", "content": input_text}
            ],
            temperature=temperature,
            tools=tools,
            response_format={"type": format}
        )
        return completion.choices[0].message.content
    
if __name__ == '__main__':
    Kimi.init(api="sk-T0I373lAL5y9eQZyuygXr4zWlzdX785BJQlf0H1OKYeBQCx5")
    print(Kimi.generate())