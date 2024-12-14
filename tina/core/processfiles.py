"""
编写者：王出日
日期：2024，12，1
版本？
对文件进行处理包括：
1.文本类文件：docx，txt，pdf
    已经实现
2.图片类文件：jpg，png，gif
    未实现

内含：

1.docxToTxt(docx_file,isClean = False)：对docx文件进行处理，返回docx文件内容，每段内容用换行符分隔
2.pdfToTxt(pdf_file,isClean = False)：对pdf文件进行处理，返回pdf文件内容，每段内容用换行符分隔
3.txtToTxt(txt_file,isClean = False)：对txt文件进行处理，返回txt文件内容，每段内容用换行符分隔
"""

import os
import docx
import PyPDF2
import win32com.client as win32
from utils import cleaning, segment


def process_document(content: str, isClean: bool, isSegments: bool, n: int) -> list[str]:
    """处理文本内容，进行数据清洗和分段"""
    if isClean:
        content = cleaning(content)
    return segment(content, n) if isSegments else [content]


def docxToTxt(docx_file: str, isClean: bool = False, isSegments: bool = False, n: int = 100) -> list[str]:
    """对docx文件进行处理"""
    try:
        doc = docx.Document(docx_file)
        content = '\n'.join(para.text.strip() for para in doc.paragraphs if para.text.strip())
        return process_document(content, isClean, isSegments, n)
    except Exception as e:
        print(f"处理文件 {docx_file} 时出错了：{e}")
        raise


def pdfToTxt(pdf_file: str, isClean: bool = False, isSegments: bool = False, n: int = 100) -> list[str]:
    """对pdf文件进行处理"""
    try:
        with open(pdf_file, 'rb') as f:
            pdf = PyPDF2.PdfReader(f)
            content = ''.join(page.extract_text().strip() + '\n' for page in pdf.pages if page.extract_text())
            return process_document(content, isClean, isSegments, n)
    except Exception as e:
        print(f"处理文件 {pdf_file} 时出错了：{e}")
        raise


def txtToTxt(txt_file: str, isClean: bool = False, isSegments: bool = False, n: int = 100) -> list[str]:
    """对txt文件进行处理"""
    try:
        with open(txt_file, 'r', encoding='utf-8') as f:
            content = f.read().strip().split('\n')
            cleaned_content = '\n'.join(para for para in content if para.strip())
            return process_document(cleaned_content, isClean, isSegments, n)
    except Exception as e:
        print(f"处理文件 {txt_file} 时出错了：{e}")
        raise

def docToTxt(doc_file: str, isClean: bool = False, isSegments: bool = False, n: int = 100) -> list[str]:
    """对doc文件进行处理"""
    try:
        word = win32.gencache.EnsureDispatch('Word.Application')
        doc = word.Documents.Open(doc_file)
        content = '\n'.join(para.Range.Text.strip() for para in doc.Paragraphs if para.Range.Text.strip())
        doc.Close()
        word.Quit()
        return process_document(content, isClean, isSegments, n)
    except Exception as e:
        print(f"处理文件 {doc_file} 时出错了：{e}")

def fileToTxt(file_path: str, isClean: bool = False, isSegments: bool = False, n: int = 100) -> list[str]:
    """对文件夹内所有文件进行处理"""
    if os.path.isfile(file_path):
        return fileExten(file_path, isClean, isSegments, n)

    content_list = []
    file_list = os.listdir(file_path)
    for file in file_list:
        full_file_path = os.path.join(file_path, file)
        content_list.extend(fileExten(full_file_path, isClean, isSegments, n))
    return content_list


def fileExten(file_path: str, isClean: bool = False, isSegments: bool = False, n: int = 100) -> list[str]:
    """根据文件扩展名调用相应的转换函数"""
    file_suffix = os.path.splitext(file_path)[1]
    if file_suffix == '.docx':
        return docxToTxt(file_path, isClean, isSegments, n)
    elif file_suffix == '.doc':
        return docToTxt(file_path, isClean, isSegments, n)
    elif file_suffix == '.pdf':
        return pdfToTxt(file_path, isClean, isSegments, n)
    elif file_suffix == '.txt':
        return txtToTxt(file_path, isClean, isSegments, n)
    else:
        return []