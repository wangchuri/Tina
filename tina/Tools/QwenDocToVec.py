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
import numpy as np
import pickle
from ..core.Embedding.QwenEmbeddings import TextEmbedding
from core.processfiles import fileToTxt
from core.manage import TinaFolderManager

def QwenDocToVec(file_path,dimesion=1536,n=500,isAdd = False):
    """
    将文本文件转换为向量，并建立Faiss索引。
    Args:
    file_path: 文本文件路径
    dimesion: 向量维度(qwen编码模型默认1536，如果是选择v3模型，维度是不固定的)
    n: 返回的段落数量
    isAdd: 新增索引
    """
    try:
        em = TextEmbedding()
        faiss_index_file = TinaFolderManager.getFaissIndexFile()
        segment_dir = TinaFolderManager.getSegment()

        # 读取文本并清理
        text = fileToTxt(file_path=file_path, isClean=True, isSegments=True, n=n)

        # 序列化文本

        # 获取文本的向量表示
        embedding = np.array(em.embedding(text))

        # 创建和保存Faiss索引
        faiss_index = faiss.IndexFlatIP(dimesion)
        faiss_index.add(embedding)
        faiss.write_index(faiss_index, faiss_index_file)
        with open(segment_dir, 'wb') as f:
            pickle.dump(text, f)

    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")
