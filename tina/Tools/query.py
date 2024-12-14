"""
编写者：王出日
日期：2024，12，13
版本？
tina提供的查询文档工具，可以根据输入的文本进行向量检索，并返回最相似的文档。
"""
import pickle
import numpy as np
import faiss
from ..core.Embedding.QwenEmbeddings import TextEmbedding
from ..core.manage import TinaFolderManager

def query(query_text, n=10):
    try:
        segments_path = TinaFolderManager.getSegment()
        faiss_index_path = TinaFolderManager.getFaissIndexFile()
        
        # 实例化 embedding 对象
        em = TextEmbedding()
        query_vec = em.embedding(query_text)
        
        # 检查 embedding 结果
        if query_vec is None or len(query_vec) == 0:
            raise ValueError("embedding出现错误")
        
        # 重塑查询向量
        query_vec = np.array(query_vec).reshape(1, -1)

        # 加载 FAISS 索引
        faiss_index = faiss.read_index(faiss_index_path)
        
        # 执行搜索
        D, I = faiss_index.search(query_vec, n)
        I = I.flatten().tolist()  # 使用 flatten() 简化为一维
        
        # 加载片段
        with open(segments_path, 'rb') as f:
            segments = pickle.load(f)

        # 根据索引获取结果
        result = [segments[i] for i in I if i < len(segments)]  # 加入安全检查
        
        return result

    except Exception as e:
        print(f"查询过程中发生错误: {e}")
        raise e