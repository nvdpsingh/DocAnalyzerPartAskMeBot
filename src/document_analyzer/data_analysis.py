import os
from utils.model_loader import ModelLoader
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from model.models import *
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser

class DocumentAnalyzer:
    """
    Analyzes documents and extracts relevant information.
    automatically logs all actions and supports session-based operations.
    """
    def __init__(self,session_id:str=None):
        pass

    
    def analyze_document(self):
        pass