"""国铁电子客票解析工具。"""

from .constants import FIELDNAMES, FIELDNAMES_EXT
from .parser import parse_guotie, process_pdf_bytes, process_pdf_file
from .web import create_app

__all__ = [
    "FIELDNAMES",
    "FIELDNAMES_EXT",
    "create_app",
    "parse_guotie",
    "process_pdf_bytes",
    "process_pdf_file",
]
