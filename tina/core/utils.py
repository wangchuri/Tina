"""
编写者：王出日
日期：2024，12，1
版本？
实用工具：
1. cleaning(text)：清理文本，去除乱码、空格、换行符、制表符等
2. segment(text,n=100)：将文本分段，每段不超过n个字符
"""
import os
import re

import re

def cleaning(text: str) -> str:
    """
    清理文本，去除乱码、空格、换行符、制表符等，同时保留常用标点符号
    Args:
        text: 待清理文本
    Returns:
        str: 清理后的文本
    """
    # 定义需要保留的常用标点符号
    punctuation = r'，。！？；：“”‘’（）、.?!\'\";:'

    # 更新正则表达式以保留标点符号
    pattern = re.compile(r'[^、\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a\u0020-\u007E\u00A0-\u00FF' + punctuation + r']+')
    text = pattern.sub('', text)
    text = text.replace('\n', '').replace('\t', '').replace('\r', '')
    
    return text

def segment(text:str,n=100) -> list:
    """
    将文本分段，每段不超过n个字符
    Args:
        text: 待分段文本
        n: 每段字符数
    Returns:
        list: 分段后的文本列表
    """
    if len(text) <= n:
        return [text]
    else:
        return [text[i:i+n] for i in range(0,len(text),n)]

def sliding(text:str,n=100,step=10) -> list:
    """
    将文本滑动窗口分段，每段不超过n个字符
    Args:
        text: 待滑动窗口分段文本
        n: 每段字符数
        step: 滑动窗口步长
    Returns:
        list: 滑动窗口分段后的文本列表
    """
    if len(text) <= n:
        return [text]
    else:
        return [text[i:i+n] for i in range(0,len(text)-n+1,step)]