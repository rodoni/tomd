from .base import BaseParser
import pandas as pd

class ExcelParser(BaseParser):
    def to_markdown(self, filepath: str) -> str:
        # Read all sheets; returns a dict mapping sheet name to DataFrame
        # openpyxl engine is standard for xlsx
        sheets = pd.read_excel(filepath, sheet_name=None, engine='openpyxl')
        
        md_parts = []
        for sheet_name, df in sheets.items():
            # Drop empty columns and rows
            df_cleaned = df.dropna(how='all', axis=0).dropna(how='all', axis=1)
            
            md_parts.append(f"## {sheet_name}\n")
            if not df_cleaned.empty:
                # Convert the cleaned dataframe to markdown
                md_parts.append(df_cleaned.to_markdown(index=False))
            else:
                md_parts.append("*Sheet is empty.*\n")
            
            md_parts.append("") # padding
            
        return "\n".join(md_parts)
