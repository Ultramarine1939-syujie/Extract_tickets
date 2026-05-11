"""国铁电子客票 PDF 解析模块。"""

from __future__ import annotations

import io
import os
import re
from dataclasses import dataclass
from pathlib import Path

import pdfplumber

from .constants import (
    FIELDNAMES,
    STATUS_EMPTY_TEXT,
    STATUS_ERROR,
    STATUS_OK,
    STATUS_UNRECOGNIZED,
)


@dataclass(frozen=True)
class ParseResult:
    """结构化解析结果，record 保持旧版接口兼容。"""

    status: str
    record: dict[str, str]
    message: str = ""


def empty_record(filename: str) -> dict[str, str]:
    """创建包含全部标准字段的空记录。"""

    rec = {field: "" for field in FIELDNAMES}
    rec["文件名"] = filename
    return rec


def extract_text_from_bytes(pdf_bytes: bytes) -> str:
    """用 pdfplumber 从 PDF 字节流提取全文。"""

    texts = []
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                texts.append(text)
    return "\n".join(texts)


def extract_text_from_file(pdf_path: str | os.PathLike[str]) -> str:
    """用 pdfplumber 从 PDF 文件路径提取全文。"""

    texts = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                texts.append(text)
    return "\n".join(texts)


def parse_guotie(text: str, filename: str) -> dict[str, str]:
    """从国铁电子客票文本中解析各字段，返回兼容旧接口的字典。"""

    rec = empty_record(filename)

    if match := re.search(r"发票号码[：:]\s*(\d+)", text):
        rec["发票号码"] = match.group(1)

    if match := re.search(r"开票日期[：:]\s*(\d{4}年\d{1,2}月\d{1,2}日)", text):
        rec["开票日期"] = match.group(1)

    match = re.search(
        r"^([^\n]+?)\s+([A-Za-z]\d{3,5})\s+([^\n]+?)$",
        text,
        re.MULTILINE,
    )
    if match:
        rec["出发站"] = match.group(1).replace(" ", "").strip()
        rec["车次"] = match.group(2).upper().strip()
        rec["到达站"] = match.group(3).replace(" ", "").strip()

    match = re.search(
        r"(\d{4}年\d{1,2}月\d{1,2}日)\s+(\d{2}:\d{2})开\s+"
        r"(\d+)车(\w+?)号(\S+铺)?\s*([\S]*[座铺卧])",
        text,
    )
    if match:
        rec["乘车日期"] = match.group(1)
        rec["开车时间"] = match.group(2)
        rec["车厢号"] = match.group(3)
        rec["座位号"] = match.group(4) + (match.group(5) or "")
        rec["席别"] = match.group(6).strip()

    if match := re.search(r"[¥￥]([\d]+\.?\d*)", text):
        rec["票价(元)"] = match.group(1)

    if match := re.search(r"(\d{6}\*{4}\d{4,6})\s+([\u4e00-\u9fa5]{2,6})", text):
        rec["证件号(脱敏)"] = match.group(1)
        rec["乘车人"] = match.group(2)

    if match := re.search(r"电子客票号[：:]\s*(\d+)", text):
        rec["电子客票号"] = match.group(1)

    notes = []
    if "始发改签" in text:
        notes.append("始发改签")
    if re.search(r"学生", text):
        notes.append("学生票")
    rec["备注"] = "；".join(notes)

    return rec


def parse_text(text: str, filename: str) -> ParseResult:
    """解析已提取的文本并返回结构化状态。"""

    if not text.strip():
        rec = empty_record(filename)
        rec["备注"] = "图片型PDF，需OCR，暂跳过"
        return ParseResult(STATUS_EMPTY_TEXT, rec, rec["备注"])

    if any(keyword in text for keyword in ["电子客票", "中国铁路", "发票号码"]):
        rec = parse_guotie(text, filename)
        return ParseResult(STATUS_OK, rec)

    rec = empty_record(filename)
    rec["备注"] = "未识别的发票格式"
    return ParseResult(STATUS_UNRECOGNIZED, rec, rec["备注"])


def process_pdf_bytes_result(pdf_bytes: bytes, filename: str) -> ParseResult:
    """从 PDF 字节流解析，返回结构化结果。"""

    try:
        return parse_text(extract_text_from_bytes(pdf_bytes), filename)
    except Exception as exc:
        rec = empty_record(filename)
        rec["备注"] = f"解析错误: {exc}"
        return ParseResult(STATUS_ERROR, rec, rec["备注"])


def process_pdf_bytes(pdf_bytes: bytes, filename: str) -> dict[str, str]:
    """从 PDF 字节流解析，返回旧版兼容记录。"""

    return process_pdf_bytes_result(pdf_bytes, filename).record


def process_pdf_file_result(
    pdf_path: str | os.PathLike[str],
    filename: str | None = None,
) -> ParseResult:
    """从 PDF 文件路径解析，返回结构化结果。"""

    display_name = filename or Path(pdf_path).name
    try:
        return parse_text(extract_text_from_file(pdf_path), display_name)
    except Exception as exc:
        rec = empty_record(display_name)
        rec["备注"] = f"解析错误: {exc}"
        return ParseResult(STATUS_ERROR, rec, rec["备注"])


def process_pdf_file(
    pdf_path: str | os.PathLike[str],
    filename: str | None = None,
) -> dict[str, str]:
    """从 PDF 文件路径解析，返回旧版兼容记录。"""

    return process_pdf_file_result(pdf_path, filename).record
