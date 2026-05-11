from extract_tickets.constants import STATUS_EMPTY_TEXT, STATUS_OK
from extract_tickets.parser import parse_guotie, parse_text, process_pdf_file_result

SAMPLE_TEXT = """
中国铁路电子客票
发票号码：26379118647000002974
开票日期：2026年2月1日
威海南海 G6989 青岛北
2025年10月18日 10:47开 08车10F号 二等座
￥110.00
370101****0812 张三
电子客票号：1864780086101690009372025
始发改签 学生
"""


def test_parse_guotie_extracts_core_fields():
    record = parse_guotie(SAMPLE_TEXT, "001.pdf")

    assert record["文件名"] == "001.pdf"
    assert record["发票号码"] == "26379118647000002974"
    assert record["开票日期"] == "2026年2月1日"
    assert record["出发站"] == "威海南海"
    assert record["到达站"] == "青岛北"
    assert record["车次"] == "G6989"
    assert record["乘车日期"] == "2025年10月18日"
    assert record["开车时间"] == "10:47"
    assert record["车厢号"] == "08"
    assert record["座位号"] == "10F"
    assert record["席别"] == "二等座"
    assert record["票价(元)"] == "110.00"
    assert record["乘车人"] == "张三"
    assert record["证件号(脱敏)"] == "370101****0812"
    assert record["电子客票号"] == "1864780086101690009372025"
    assert record["备注"] == "始发改签；学生票"


def test_parse_text_reports_empty_pdf_text():
    result = parse_text("", "scan.pdf")

    assert result.status == STATUS_EMPTY_TEXT
    assert result.record["文件名"] == "scan.pdf"
    assert result.record["备注"].startswith("图片型PDF")


def test_process_pdf_file_default_filename_uses_path_name(monkeypatch, tmp_path):
    pdf_path = tmp_path / "ticket.pdf"
    pdf_path.write_bytes(b"not a real pdf; extractor is monkeypatched")

    monkeypatch.setattr("extract_tickets.parser.extract_text_from_file", lambda _: SAMPLE_TEXT)

    result = process_pdf_file_result(pdf_path)

    assert result.status == STATUS_OK
    assert result.record["文件名"] == "ticket.pdf"
