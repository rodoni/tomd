from .base import BaseParser
import pymupdf4llm

class PDFParser(BaseParser):
    def to_markdown(self, filepath: str) -> str:
        md_text = pymupdf4llm.to_markdown(filepath)
        return md_text
