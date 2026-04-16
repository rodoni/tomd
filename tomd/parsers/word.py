from .base import BaseParser
import docx
from docx.document import Document
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import Table
from docx.text.paragraph import Paragraph

class WordParser(BaseParser):
    def to_markdown(self, filepath: str) -> str:
        doc = docx.Document(filepath)
        md_parts = []
        
        def iter_block_items(parent):
            """
            Yield each paragraph and table child within *parent*, in document order.
            Each returned value is an instance of either Table or Paragraph.
            """
            if isinstance(parent, Document):
                parent_elm = parent.element.body
            elif hasattr(parent, '_p'):
                parent_elm = parent._p
            elif hasattr(parent, '_element'):
                parent_elm = parent._element
            else:
                parent_elm = parent

            for child in parent_elm.iterchildren():
                if isinstance(child, CT_P):
                    yield Paragraph(child, parent)
                elif isinstance(child, CT_Tbl):
                    yield Table(child, parent)

        for block in iter_block_items(doc):
            if isinstance(block, Paragraph):
                res = self._process_paragraph(block)
                if res.strip():
                    md_parts.append(res)
            elif isinstance(block, Table):
                md_parts.append(self._process_table(block))
                md_parts.append("")

        return "\n".join(filter(None, md_parts))
        
    def _process_paragraph(self, p) -> str:
        text = ""
        for run in p.runs:
            t = run.text
            if not t:
                continue
            
            leading_space = " " if t.startswith(" ") else ""
            trailing_space = " " if t.endswith(" ") else ""
            t_stripped = t.strip()
            
            if not t_stripped:
                text += t
                continue
                
            # If basic styles:
            if run.bold and run.italic:
                t_formatted = f"***{t_stripped}***"
            elif run.bold:
                t_formatted = f"**{t_stripped}**"
            elif run.italic:
                t_formatted = f"*{t_stripped}*"
            elif run.font.name and run.font.name.lower() in ["courier", "courier new", "consolas"]:
                t_formatted = f"`{t_stripped}`"
            else:
                t_formatted = t_stripped
                
            text += f"{leading_space}{t_formatted}{trailing_space}"

        if not text.strip():
            return ""
            
        style = p.style.name.lower() if p.style and p.style.name else ""
        if style.startswith("heading"):
            try:
                level = int(style.replace("heading", "").strip())
                return f"{'#' * level} {text}\n"
            except ValueError:
                pass
        
        if style == "title":
            return f"# {text}\n"
                
        if "list bullet" in style or "bullet" in style:
            return f"- {text}"
        elif "list number" in style or "number" in style:
            # Simplistic support for ordered list (just use 1.)
            return f"1. {text}"
            
        return f"{text}\n"

    def _process_table(self, table) -> str:
        md = []
        for i, row in enumerate(table.rows):
            row_data = []
            for cell in row.cells:
                # Replace newlines within cell with space to not break md table
                row_data.append(cell.text.replace('\n', ' ').strip())
            
            md.append("| " + " | ".join(row_data) + " |")
            
            # Headers separator
            if i == 0:
                header_sep = ["---"] * len(row.cells)
                md.append("| " + " | ".join(header_sep) + " |")
                
        return "\n".join(md)
