"""兼容旧导入路径的解析模块。

新代码位于 ``src/extract_tickets/parser.py``。
"""

# ruff: noqa: E402

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from extract_tickets.constants import FIELDNAMES  # noqa: E402
from extract_tickets.parser import (
    ParseResult,
    empty_record,
    extract_text_from_bytes,
    extract_text_from_file,
    parse_guotie,
    parse_text,
    process_pdf_bytes,
    process_pdf_bytes_result,
    process_pdf_file,
    process_pdf_file_result,
)  # noqa: E402

__all__ = [
    "FIELDNAMES",
    "ParseResult",
    "empty_record",
    "extract_text_from_bytes",
    "extract_text_from_file",
    "parse_guotie",
    "parse_text",
    "process_pdf_bytes",
    "process_pdf_bytes_result",
    "process_pdf_file",
    "process_pdf_file_result",
]
