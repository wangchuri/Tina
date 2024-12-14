"""
编写者：王出日
日期：2024，12，1
版本？
描述：
使用QwenEmbeddings库将文本转换为向量，并使用Faiss建立索引。
包含：
QwenDocvec(file_path)：将文本文件转换为向量，并建立Faiss索引。
"""

import faiss
from ..core.Embeddings.embeddings import Embeddings
import numpy as np
from tina.core.processfiles import fileToTxt

def docVec(file_path):
    """
    """
    data = fileToTxt(file_path)
    emd = Embeddings()
    vectors=emd.embedding(data)
    index = faiss.IndexFlatIP(1536)
    vectors_np = np.array([d["embedding"] for d in vectors])
    index.add(vectors_np)
    #保存索引
    faiss.write_index(index, "index.faiss")