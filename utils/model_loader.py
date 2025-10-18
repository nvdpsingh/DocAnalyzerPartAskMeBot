import os
import dotenv 
from langchain_groq import ChatGroq
from utils.config_loader import load_config
from logger.custom_logger import CustomLogger
from langchain_community.embeddings import HuggingFaceEmbeddings
from exceptions.custom_exceptions import DocumentPortalException

log = CustomLogger().get_logger(__name__)

class ModelLoader:
    def __init__(self):
        pass
    
    def _validate_env(self):
        pass

    def load_embeddings(self):
        pass

    def load_llm(self):
        pass
        