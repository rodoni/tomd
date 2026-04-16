# Document to Markdown Converter (`tomd`) Tool Specification

## 1. Overview
The `tomd` tool is a Python-based command-line interface (CLI) application and library. Its purpose is to securely and efficiently translate complex or standard office documents—specifically PDF, Word (DOC/DOCX), and Excel (XLS/XLSX) files—into well-formatted, structural Markdown (`.md`).

## 2. Core Features & Requirements

### 2.1 File Ingestion
- **Formats Supported:** `.pdf`, `.docx` (and optionally legacy `.doc`), `.xlsx`, `.xls`
- **Batch Processing:** Support parsing single files or an entire directory of mixed documents.
- **Resilience:** The tool must not crash the entire process when encountering a single corrupted or encrypted file. It should log the error and proceed to the next file.

### 2.2 Conversion Standards
- **Word (DOCX) to Markdown:**
    - Parse standard document structures: headings (H1-H6), paragraphs, and inline text decorations (bold, italic, code).
    - Capture ordered (numbered) and unordered (bulleted) lists.
    - Translate simple Word tables to Markdown tables.
- **Excel (XLSX) to Markdown:**
    - Translate row/column data into Markdown tables.
    - Handle multi-sheet workbooks by creating a Markdown header for each sheet name followed by the corresponding tabular data.
    - Omit or sanitize completely empty columns/rows to avoid bloated tables.
- **PDF to Markdown:**
    - Read textual content while maintaining reading order.
    - Where feasible, infer headings or formatting based on font size or styling.
    - (Optional/Advanced) Detect and extract tabular constructs or images embedded within the PDF.

### 2.3 Command-Line Interface (CLI)
The interface should be simple and intuitive.
```bash
# Convert a single file to Markdown
tomd convert my_document.pdf

# Convert all supported documents in a folder to a specific output directory
tomd convert ./docs --output-dir ./markdown_files

# Show help
tomd --help
```

## 3. Architecture & Technical Design

### 3.1 Recommended Libraries
To ensure robust parsing without executing untrusted macros or running headless office suites, the following pure-Python (or native-binding) tools are recommended:
- **CLI Framework:** `click` or Python's built-in `argparse`.
- **Word Parsing:** `python-docx` for `.docx`. (For older `.doc` files, standardizing on a system dependency like LibreOffice headless or dropping support may be required, depending on strictness).
- **Excel Parsing:** `pandas` combined with `openpyxl` (for reading) and `tabulate` (`pandas.DataFrame.to_markdown()` utilizes `tabulate` under the hood).
- **PDF Parsing:** `PyMuPDF` (formerly `fitz`), `pdfplumber`, or the newer `pymupdf4llm` library which excels at converting PDFs directly to Markdown representations.

### 3.2 Directory Structure
```text
tomd/
├── tomd/               # Source code directory
│   ├── __init__.py
│   ├── cli.py          # Command line argument parser and entry point
│   ├── dispatcher.py   # Routes file paths to the correct parser based on extension
│   └── parsers/
│       ├── __init__.py
│       ├── pdf.py      # PDF extraction logic
│       ├── word.py     # DOCX extraction logic
│       └── excel.py    # XLSX extraction logic
├── tests/              # Unit tests
├── pyproject.toml      # Dependency management and project config
└── spec.md             # This document
```

### 3.3 Extensibility
The parsing logic should be structured around an abstract base class or a common interface (e.g., `BaseParser`), guaranteeing that every new format parser exposes a consistent `to_markdown(filepath: str) -> str` method.
