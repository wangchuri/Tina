"""
编写者：王出日
日期：2024，12，1
版本？
使用通义大模型的词嵌入模型对中文文本进行编码
包含：
TextEmbedding类：用于对中文文本进行编码
"""
import dashscope
import json
from http import HTTPStatus
from typing import Union


dashscope.api_key= "sk-aa328698ca6f4a7c9c0dde0b9851a772"
class TextEmbedding:
    def __init__(self,model_version = "v1"):
        """
        初始化通义大模型的词嵌入模型
        :param model_version: 模型版本，默认为v1
        """
        # self.cache = getCache()
        if model_version == "v1":
            self.model = dashscope.TextEmbedding.Models.text_embedding_v1
        elif model_version == "v2":
            self.model = dashscope.TextEmbedding.Models.text_embedding_v2
        elif model_version == "v3":
            self.model = dashscope.TextEmbedding.Models.text_embedding_v3
        else:
            raise ValueError("不存在该版本")
        
    def embedding(self,text:Union[str,list],id=0,address=None,cache =False,cache_path = "cache.json"):
        """
        对中文文本进行编码
        Args:
            text: 输入的中文文本
            id: 输入文本的id，默认为0
            address:该文本所在的位置，默认为None
        Returns:
            cache.json的路径
        """
        if cache:
            data = self.strOrList(text, id, address)
            # 一次性写入更新后的数据到文件
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        else:
            return self.strOrList(text)

    def strOrList(self, text):
        if isinstance(text,list):    
            data = []
            for text in text:
                resp = self.textembedding(text)
                data.append(resp.output["embeddings"][0]['embedding'])
            return data
        else:
            resp = self.textembedding(text)
            return resp.output["embeddings"][0]['embedding']

    def strOrListInCache(self, text, id, address):
        data = []
        if isinstance(text,list):
            print(isinstance(text,list))
            for text in text:
                resp = self.textembedding(text)
                data.append({
                        "id": id,
                        "address": f"{address}",
                        "embedding": resp.output["embeddings"][0]['embedding']
                    })
        else:
            resp = self.textembedding(text)
            data.append({
                    "id": id,
                    "address": address,
                    "embedding": resp.output["embeddings"][0]['embedding']
                })
            
        return data
        
    def textembedding(self, text):
        resp = dashscope.TextEmbedding.call(
            model=self.model,
            input=text
            )
        if resp.status_code == HTTPStatus.OK:
            return resp
        else:
            print(resp)
            raise ValueError("调用API失败")
        
            
    def insertIncache(id, address, embedding):
        pass