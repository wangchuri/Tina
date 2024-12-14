class prompt:
    def __init__(self, prompt_str):
        self.prompt_str = prompt_str
        self.prompt={
            "agent":r"""
            你好！你是一个智能体，我们为你提供很多个工具，你可以调用他们来完成你的任务！
            当然，不一定需要调用工具，调用工具应该满足以下条件：
            1.当用户输入的信息量较少时，如果有搜索工具的话，可以调用它；
            2.用户需要你做出一些对环境做出改变行为的操作时；
            3.可能需要调用多个工具的时候，请一个个调用
            我会将过去的信息作为消息提供在system角色中，你通过该消息体可以知道过去自己做过什么行为。
            下面时关于消息体内部的标签：
            <system><\system> 这是系统消息，包括了你对工具调用后结果的返回
            <user><\user>这是用户输入的消息
            <assistant><\assistant>这是你回复的消息
            """
        }

    def __str__(self):
        return self.prompt_str
    def generate_prompt(self,text:str,LLM:type) ->str:
        """
        使用大模型来输出prompt
            Args:
                text: 输入的文本
                LLM: 模型实例
            Returns:
                prompt: 输出的prompt
        """
        prompt_text ="""
        请分析用户的需要后，为用户生成合适的prompt用在对话系统中。
        """
        prompt=LLM.predict(text)
        return prompt
        