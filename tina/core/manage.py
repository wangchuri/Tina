"""
编写者：王出日
日期：2024，12，1
版本？
管理tina的文件夹模块
"""

import os

file_dir = os.path.join(os.path.dirname(__file__), "TinaSauce")

class TinaFolderManager:
    """
    管理tina文件夹
    """
    @staticmethod
    def init(file_dir: str = file_dir):
        """
        初始化tina文件夹
        """
        TinaFolderManager.file_dir = file_dir
        try:
            os.makedirs(file_dir, exist_ok=True)
            os.makedirs(os.path.join(file_dir, "memory"), exist_ok=True)
            os.makedirs(os.path.join(file_dir, "faiss_index"), exist_ok=True)

            # 创建索引文件、缓存文件和分段文件（不是分词文件）
            for filename in ["faiss.index", "cache.json", "segment.pkl"]:
                path = os.path.join(file_dir, "faiss_index" if filename == "faiss.index" else "", filename)
                if not os.path.exists(path):
                    with open(path, "w") as f: 
                        pass

        except OSError as e:
            print(f"初始化失败: {e}")

    @staticmethod
    def getCache() -> str:
        """
        获取缓存文件路径
        """
        return os.path.join(TinaFolderManager.file_dir, "cache.json")

    @staticmethod
    def getMemory() -> str:
        """
        获取记忆文件夹路径
        """
        return os.path.join(TinaFolderManager.file_dir, "memory")

    @staticmethod
    def getMemoryFile(filename: str) -> str:
        """
        获取记忆文件路径
        """
        return os.path.join(TinaFolderManager.getMemory(), filename)

    @staticmethod
    def getFaissIndex() -> str:
        """
        获取faiss索引文件夹路径
        """
        return os.path.join(TinaFolderManager.file_dir, "faiss_index")

    @staticmethod
    def getFaissIndexFile() -> str:
        """
        获取faiss索引文件
        """
        return os.path.join(TinaFolderManager.getFaissIndex(), "faiss.index")
    
    @staticmethod
    def getSegment() -> str:
        """
        获取分词文件路径
        """
        return os.path.join(TinaFolderManager.file_dir, "segment.pkl")

