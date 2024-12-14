"""
编写者：王出日
日期：2024，12，1
版本？
用于嵌入文档，将文档转换为向量，存储在cache中，以便后续使用。
"""
from llama_cpp import Llama
class Embeddings:
    def __init__(self, model_path):
        self.model = Llama(model_path)
        
    def embedding(self, text):
        pass