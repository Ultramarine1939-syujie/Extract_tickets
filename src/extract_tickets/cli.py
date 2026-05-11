"""命令行入口。"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from .constants import FIELDNAMES
from .parser import process_pdf_file


def process_folder(folder: str | Path) -> list[dict[str, str]]:
    """遍历文件夹，解析所有 PDF 文件，返回记录列表。"""

    folder_path = Path(folder)
    records = []
    pdf_files = sorted(path for path in folder_path.iterdir() if path.suffix.lower() == ".pdf")

    for path in pdf_files:
        print(f"处理: {path.name}")
        record = process_pdf_file(path, path.name)
        _print_record_status(path.name, record)
        records.append(record)

    return records


def save_csv(records: list[dict[str, str]], output_path: str | Path) -> None:
    """将记录列表保存为 CSV 文件。"""

    output = Path(output_path)
    with output.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(records)
    print(f"\n已保存 {len(records)} 条记录 -> {output}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="批量解析国铁电子客票 PDF")
    parser.add_argument(
        "folder",
        nargs="?",
        default=Path.cwd(),
        help="PDF 所在目录，默认当前目录",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="输出 CSV 路径，默认写入目标目录下的 tickets.csv",
    )
    args = parser.parse_args(argv)

    folder = Path(args.folder).resolve()
    output = Path(args.output).resolve() if args.output else folder / "tickets.csv"
    records = process_folder(folder)
    save_csv(records, output)
    return 0


def _print_record_status(filename: str, record: dict[str, str]) -> None:
    remark = record.get("备注", "")
    if remark.startswith("图片型PDF"):
        print(f"  [!] 无文字层，跳过: {filename}")
    elif remark.startswith("未识别"):
        print(f"  [?] 未识别格式: {filename}")
    elif remark.startswith("解析错误"):
        print(f"  [ERR] 错误: {remark}")
    else:
        print(
            f"  [OK] {record['出发站']} -> {record['到达站']}  "
            f"{record['车次']}  {record['乘车日期']} {record['开车时间']}  "
            f"{record['乘车人']}"
        )


if __name__ == "__main__":
    raise SystemExit(main())
