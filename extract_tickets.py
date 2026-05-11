"""兼容旧启动方式的 CLI 入口。

运行:
    python extract_tickets.py
"""

# ruff: noqa: E402

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
PACKAGE_DIR = SRC / "extract_tickets"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

# 这个文件与 src/extract_tickets 包同名。pytest 从项目根目录导入时可能先命中
# 此兼容脚本；设置 __path__ 后，它仍可继续解析 extract_tickets.cli 等子模块。
__path__ = [str(PACKAGE_DIR)]

from extract_tickets.cli import main, process_folder, save_csv  # noqa: E402

FOLDER = ROOT
OUTPUT_CSV = ROOT / "tickets.csv"

__all__ = ["FOLDER", "OUTPUT_CSV", "main", "process_folder", "save_csv"]


if __name__ == "__main__":
    raise SystemExit(main())
