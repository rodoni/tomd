import click
import os
import logging
from pathlib import Path
from .dispatcher import convert_file

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

@click.group()
def cli():
    """tomd - Document to Markdown Converter"""
    pass

@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--output-dir', type=click.Path(file_okay=False, writable=True), default=None,
              help='Output directory to save markdown files. If not provided, files are saved in the input directory.')
def convert(path, output_dir):
    """Convert a file or directory of documents to Markdown."""
    input_path = Path(path)
    
    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    
    if input_path.is_file():
        success = _process_single_file(input_path, output_dir)
        if not success:
            exit(1)
    elif input_path.is_dir():
        # Batch processing
        supported_exts = {'.pdf', '.doc', '.docx', '.xls', '.xlsx'}
        success_count = 0
        error_count = 0
        
        for item in input_path.iterdir():
            if item.is_file() and item.suffix.lower() in supported_exts:
                if _process_single_file(item, output_dir):
                    success_count += 1
                else:
                    error_count += 1
                    
        logger.info(f"Batch conversion complete: {success_count} succeeded, {error_count} failed.")
    else:
        logger.error("Invalid path.")
        exit(1)

def _process_single_file(filepath: Path, output_dir: Path) -> bool:
    logger.info(f"Converting: {filepath.name} ...")
    try:
        md_text = convert_file(str(filepath))
        
        if output_dir:
            out_file = output_dir / f"{filepath.stem}.md"
        else:
            out_file = filepath.parent / f"{filepath.stem}.md"
            
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(md_text)
            
        logger.info(f"Saved: {out_file}")
        return True
    except Exception as e:
        logger.error(f"Failed to convert {filepath.name}: {e}")
        return False

if __name__ == '__main__':
    cli()
