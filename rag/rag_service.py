from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document

from rag.vector_store import VectorStoreService
from utils.prompt_loader import load_rag_prompt
from model.factory import chat_model


'''
question, search message, summarize question and message to model.
'''
class RagSummarize(object):
    def __init__(self):
        self.vector_store = VectorStoreService()
        self.retriever = self.vector_store.get_retriver()
        self.prompt_text = load_rag_prompt()
        self.prompt_template = PromptTemplate.from_template(self.prompt_text)

        self.model = chat_model
        self.chain = self.init_chain()
    
    def init_chain(self):
        chain = self.prompt_template | self.model | StrOutputParser()
        return chain
    
    def retriever_docs(self, qury: str)->list[Document]:
        return self.retriever.invoke(qury)
    
    def rag_summarize(self, qury: str)->str:
        docs = self.retriever_docs(qury)
        context = ""
        cnt = 0
        for doc in docs:
            cnt += 1
            context += f"[refrence message]content:{doc.page_content} | metadata:{doc.metadata}\n"
        return self.chain.invoke({
            "input":qury,
            "context":context,
        })
    
if __name__ == "__main__":
    rag = RagSummarize()
    print(rag.rag_summarize("small house fit what type robot"))
