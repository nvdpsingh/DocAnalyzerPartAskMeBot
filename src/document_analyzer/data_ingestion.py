from ast import Pass
import os
import fitz
import uuid
from datetime import datetime
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException

log = CustomLogger().get_logger(__name__)

class DocumentHandler:
    """
    Handle PDF saving and reading operations.
    Automatically logs all actions and supports session-based operations.
    """

    def __init__(self):
        pass

    def save_pdf(self):
        """
        Save a PDF file to the database.
        """
        pass

    def read_pdf(self):
        pass

