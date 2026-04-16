import pytest
from tomd.dispatcher import get_parser
from tomd.parsers import PDFParser, WordParser, ExcelParser

def test_get_parser_pdf():
    parser = get_parser("document.pdf")
    assert isinstance(parser, PDFParser)

def test_get_parser_docx():
    parser = get_parser("document.docx")
    assert isinstance(parser, WordParser)

def test_get_parser_excel():
    parser = get_parser("data.xlsx")
    assert isinstance(parser, ExcelParser)
    
    parser2 = get_parser("data.xls")
    assert isinstance(parser2, ExcelParser)

def test_get_parser_doc_unsupported():
    with pytest.raises(ValueError, match="Legacy .doc format requires conversion to .docx first"):
        get_parser("document.doc")

def test_get_parser_unsupported():
    with pytest.raises(ValueError, match="Unsupported file extension: .txt"):
        get_parser("document.txt")
