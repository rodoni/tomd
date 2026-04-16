import os
import logging
from pathlib import Path

from .parsers import PDFParser, WordParser, ExcelParser

logger = logging.getLogger(__name__)

def get_parser(filepath: str):
    ext = Path(filepath).suffix.lower()
    if ext == '.pdf':
        return PDFParser()
    elif ext in ['.docx']:
        # Note: .doc requires additional handling (e.g. libreoffice headless or antiword), standard python-docx only supports docx.
        # Can fallback or error for now.
        return WordParser()
    elif ext in ['.doc']:
        raise ValueError(f"Legacy .doc format requires conversion to .docx first. Not supported by default python-docx.")
    elif ext in ['.xlsx', '.xls']:
        return ExcelParser()
    else:
        raise ValueError(f"Unsupported file extension: {ext}")

def convert_file(filepath: str) -> str:
    """
    Dispatcher to convert a single file. Returns markdown string.
    Raises exception if parsing fails or extension unsupported.
    """
    parser = get_parser(filepath)
    return parser.to_markdown(filepath)
