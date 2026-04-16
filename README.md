# tomd - Document to Markdown Converter

`tomd` is a Python-based command-line interface (CLI) application and library. Its purpose is to securely and efficiently translate complex or standard office documents—specifically PDF, Word (DOCX), and Excel (XLSX) files—into well-formatted, structural Markdown (`.md`).

## Features

- **Multi-Format Support:** Converts `.pdf`, `.docx`, and `.xlsx` files into Markdown.
- **Batch Processing:** Support parsing single files or an entire directory of mixed documents.
- **Resilient Parsing:** Continues processing even if an individual file is corrupted or encrypted by logging the error and proceeding to the next file.
- **Structured Output:** 
  - Extracts Word headings, lists, inline decorations, and basic tables.
  - Converts Excel data into properly formatted Markdown tables for each sheet.
  - Retains reading order and parses text from PDF documents using `pymupdf4llm`.

## Installation

You can get the environment set up and all required packages installed by running the provided setup and install scripts:

1. Setting up the environment (this will create a virtual environment and install the package in editable mode):
   ```bash
   ./setup.sh
   # Or directly install dependencies if you have your own environment active
   ./install.sh
   ```

2. Make sure your virtual environment is active:
   ```bash
   source venv/bin/activate
   ```

## Usage

Once installed, the `tomd` command will be available in your terminal. You can also run it using the convenient wrapper script `tomd.sh`.

### Convert a Single File
```bash
tomd convert my_document.pdf
# Or using the shell wrapper:
./tomd.sh convert my_document.pdf
```

### Batch Conversion
Convert all supported documents in a folder and place the results in a specific output directory:
```bash
tomd convert ./docs --output-dir ./markdown_files
```

### Help Option
View all available commands and arguments:
```bash
tomd --help
```

## Architecture

`tomd` relies on the following robust, pure-Python libraries:
- **CLI Framework:** `click`
- **PDF Parsing:** `pymupdf4llm`
- **Word Parsing:** `python-docx`
- **Excel Parsing:** `pandas`, `openpyxl`, and `tabulate`

The project uses an extensible object-oriented pattern where parsing strategies correspond to different file types, ensuring you can easily plug in new parsers in the future.
