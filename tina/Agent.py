"""
编写者：王出日
日期：2024，12，1
版本？
Agent类，创建智能体的基类
"""
from typing import Type
from tina.Tools.tools import Tools
from tina.core.LLM.tina import tina
import importlib
import json

class Agent:
    def __init__(self,
                 LLM:Type,
                 tools:Type,
                 prompt:Type
                 ):
        """
        创建智能体，需要指定LLM（语言模型）,tools（LLM需要用到的工具）和propmt（引导词）

        Args:
            LLM (Type): LLM类
            tools (Type): _description_
        """
        self.LLM = LLM
        self.tools = tools
        self.prompt = prompt
        self.messages =''
        
        
        
    def executor(self,text:str)->str:
        """
        执行智能体的逻辑，输入文本，输出文本

        Args:            
            text (str): 输入文本

        Returns:
            str: 输出文本
        """
        self.messages += '<user>'+text+'<\\user>\n'
        value = LLM.predict(
            input_text=self.messages,
            prompt=self.prompt,
            tools=self.tools.tools,
            stream=False,
            temperature=0.5,
        )
        self.decision(value)
        
        
        
    def decision(self,value:dict)->str:
        """
        根据LLM的输出做出决策

        Args:
            value (str): LLM的输出

        Returns:
            str: 输出文本
        """
        role = value['role']
        content = value['content'].strip()
        if role == 'assistant' and (content[0:11]+content[-12:] == "<tool_call></tool_call>"):
            self.messages += "<assistant>" + value + "<\\assistant>\n"
            #提取关键内容
            main_content = content[12:-13]
            main_content_json = json.loads(main_content)
            self.funExecutor(main_content_json)
        else:
            print(role+":"+content)
        
    def funExecutor(self,info:json)->str:
        """
        执行智能体的操作

        Args:            
            text (str): 输入文本

        Returns:
            str: 输出文本
        """
        #获取工具名称
        tool_name = info['name']
        tool_parameters = info['arguments']
        #查询工具是否注册
        if self.tools.checkTools(tool_name):
            raise Exception("不存在该工具")
        #获取工具参数并检测参数类型,构建参数字符串
        parameters_str = ""
        for key,value in tool_parameters.items():
            if self.tools.queryParameterType(tool_name,key) == "int" or self.tools.queryParameterType(tool_name,key) == "float" or self.tools.queryParameterType(tool_name,key) == "bool":
                parameters_str += key + "=" + str(value) + ","
            elif self.tools.queryParameterType(tool_name,key) == "str":
                parameters_str += key + "='" + str(value) + "',"
        
        #执行工具
        try:
            importlib.import_module(tool_name)
        except:
            raise Exception("工具不存在")
        #构建工具调用语句
        tool_call = tool_name + "." + tool_name + "(" + parameters_str + ")"
        #执行工具并获取结果
        result = eval(tool_call)
        #输出到信息列表
        self.messages += "<system>执行工具" + tool_name + "结果为：" + str(result) + "<\\system>\n"
        
        
        
    def run(self):
        """
        运行智能体
        """
        while True:
            if input("输入exit退出智能体") == "exit":
                break
            self.executor(input("输入文本"))
            
    
if __name__ == '__main__':
    LLM = tina(
        path=r"D:\wangchuri\development\project\tina\tina-sauce----tcgai\model\GGUF\qwen2.5-7b-instruct-q4_k_m.gguf",
        device="gpu",
        context_length=2048
    )
    tools = Tools()
    tools.register(
        name = "word_embedding",
        description="对文本进行词嵌入",
        required_parameters=["word"],
        parameters=[{
            "word": {
                "type": "str",
                "description": "词"
            }
            }]
        
    )
    tools.tools
    prompt = "你好，我是智能体。"
    Agent(LLM,tools,prompt)
