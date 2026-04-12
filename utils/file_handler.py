from hashlib import md5
from path_tool import get_abs_path
import os
from log_handler import logger
from langchain_community.document_loaders import PyPDFLoader, TextLoader 
from langchain_core.documents import Document

def get_file_md5_hex(filename:str)->str: # 获取文件md5的十六进制字符串
    file_abs_path = get_abs_path("data/"+filename)
    if not os.path.exists(file_abs_path):
        logger.error(f"[md5 calculate] file:{filename} not exist")
    if not os.path.isfile(file_abs_path):
        logger.error(f"[md5 calculate] file:{filename} not file")

    md5_obj = md5()
    chunk_size = 4096 # 流式读入文件防止爆内存
    try:
        with open(file_abs_path, "rb") as f:
            while chunk := f.read(chunk_size):
                md5_obj.update(chunk)
        return md5_obj.hexdigest
    except:
        logger.error(f"[read file] file:{filename} can't read")

def listdir_with_allowed_type(file_dir: str, allow_type:tuple[str]=(".txt", ".pdf")): # 返回允许的文件后缀的文件夹里的文件，以列表返回
    files = []
    file_dir = get_abs_path(file_dir)
    if not os.path.isdir(file_dir):
        logger.error(f"[listdir_with_allowed_type] dir path:{file_dir} is not dir")
    
    for f in os.listdir(file_dir):
        if f.endswith(allow_type):
            files.append(os.path.join(file_dir, f))
    return tuple(files)

def pdf_loader(pdf_file:str, pwd:str=None): # 加载pdf
    return PyPDFLoader(pdf_file, pwd)

def txt_loader(text_file:str): # 加载txt
    return TextLoader(text_file)


if __name__ == "__main__":
    print(get_file_md5_hex(""))