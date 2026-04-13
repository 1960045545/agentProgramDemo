from abc import ABC
from typing import Optional
from langchain.embeddings import Embeddings
from langchain.chat_models import BaseChatModel
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings
from utils.config_handler import rag_conf

class BaseModelFactory(ABC):
    def generator(self)->Optional[Embeddings | BaseChatModel]:
        pass

class ChatModelFactory(BaseModelFactory):
    def generator(self):
        return ChatTongyi(model=rag_conf["chat_model_name"])

class EmbeddingModelFactory(BaseModelFactory):
    def generator(self):
        return DashScopeEmbeddings(model=rag_conf["embedding_model_name"])

chat_model = ChatModelFactory().generator()
embedding_model = EmbeddingModelFactory().generator()
