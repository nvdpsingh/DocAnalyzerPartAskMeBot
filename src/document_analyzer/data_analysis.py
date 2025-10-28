import os
import sys
from utils.model_loader import ModelLoader
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from model.models import *
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser
from prompt.prompt_library import prompt

class DocumentAnalyzer:
    """
    Analyzes documents and extracts relevant information.
    automatically logs all actions and supports session-based operations.
    """
    def __init__(self,session_id:str=None):
        self.log = CustomLogger().get_logger(__name__)
        try:
            self.loader=ModelLoader()
            self.llm=self.loader.load_llm()
            
            # Prepare parsers
            self.parser = JsonOutputParser(pydantic_object=Metadata)
            self.fixing_parser = OutputFixingParser.from_llm(parser=self.parser, llm=self.llm)
            
            self.prompt = prompt
            
            self.log.info("DocumentAnalyzer initialized successfully")
            
            
        except Exception as e:
            self.log.error(f"Error initializing DocumentAnalyzer: {e}")
            raise DocumentPortalException("Error in DocumentAnalyzer initialization", sys)

    
    def analyze_document(self,document_text:str)->dict:
        """Analyze a document's text and rxtract structured mertadata and summary"""

        try:
            chain = self.prompt | self.llm | self.fixing_parser

            self.log.info("Meta data analyssis chain initialized")

            response = chain.invoke({
                "format_instructions": self.parser.get_format_instructions(),
                "document_text": document_text
            })

            self.log.info("Meta data analysis completed successfully")

            return response
        
        except Exception as e:
            self.log.error(f"Error analyzing document: {e}")
            raise DocumentPortalException("Error in document analysis", sys)