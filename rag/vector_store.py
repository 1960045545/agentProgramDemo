from langchain_chroma.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import Runnable
from langchain_core.documents import Document

from model.factory import embedding_model

from utils.path_tool import get_abs_path
from utils.config_handler import chroma_conf
from utils.log_handler import logger
from utils.file_handler import txt_loader, pdf_loader, listdir_with_allowed_type, get_file_md5_hex

import os
from hashlib import md5

class VectorStoreService:
    def __init__(self):
        self.vector_store = Chroma(
            collection_name=chroma_conf["collection_name"],
            embedding_function=embedding_model,
            persist_directory=chroma_conf["persist_directory"],
        )

        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=chroma_conf["chunk_size"],
            chunk_overlap=chroma_conf["chunk_overlap"],
            separators=chroma_conf["seperators"],
            length_function = len
        )
    
    def get_retriver(self)->Runnable:
        return self.vector_store.as_retriever(search_kwargs={
            "k":chroma_conf["k"]
        })
    
    def load_Document(self)->None:
        '''
        from data folder read files transform to vector into database
        calculate MD5 no duplicate
        return Nono
        '''
        def check_hex(md5_for_check:str)->bool:
            store_md5_path = chroma_conf["md5_hex_store"]
            abs_md5_path = get_abs_path(store_md5_path)
            if not os.path.exists(abs_md5_path):
                open(abs_md5_path, "w", encoding="utf-8").close()
                return False
            
            with open(abs_md5_path, "r", encoding="utf-8") as f:
                for line in f.readlines():
                    line = line.strip()
                    if md5_for_check == line:
                        return True
            return False
        
        def save_md5_hex(md5_for_check: str)->None:
            store_md5_path = chroma_conf["md5_hex_store"]
            abs_md5_path = get_abs_path(store_md5_path)
            with open(abs_md5_path, "a", encoding="utf-8") as f:
                f.write(md5_for_check+"\n")
        
        def get_file_documents(read_file_path:str)->list[Document]:
            if read_file_path.endswith("txt"):
                return txt_loader(read_file_path)
            
            if read_file_path.endswith("pdf"):
                return pdf_loader(read_file_path)
            
            return []
        allow_file_path = listdir_with_allowed_type(
            chroma_conf["data_path"], 
            tuple(chroma_conf["adlow_knowledge_file_type"])
            )
        
        for file_path in allow_file_path:
            md5_hex = get_file_md5_hex(file_path)
            if check_hex(md5_hex):
               logger.info("[check md5] this file {file_path} in database")
               continue
            try:
                docs: list[Document] = get_file_documents(file_path) 
                if not docs:
                    logger.warning(f"[load knowledge database] not context pass")
                    continue
                split_document:list[Document] = self.spliter.split_documents(docs)
                if not split_document:
                    logger.warning(f"[load knowledge] this document spliter no context")
                    continue
                self.vector_store.add_documents(split_document)
                print(type(md5_hex))
                save_md5_hex(md5_hex)
                logger.info(f"[load knowledge]{file_path} loading success")
            except Exception as e:
                logger.error(f"[load knowledge database]{file_path} error{str(e)}", exc_info=True)
                raise e

if __name__ == "__main__":
    vs = VectorStoreService()
    vs.load_Document()
    retriver = vs.get_retriver()
    res = retriver.invoke("miss")
    for r in res:
        print(r)
        print("="*20)