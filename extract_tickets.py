"""兼容旧启动方式的 CLI 入口。

运行:
    python extract_tickets.py
"""

# ruff: noqa: E402

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from extract_tickets.cli import main, process_folder, save_csv  # noqa: E402

FOLDER = ROOT
OUTPUT_CSV = ROOT / "tickets.csv"

__all__ = ["FOLDER", "OUTPUT_CSV", "main", "process_folder", "save_csv"]


if __name__ == "__main__":
    raise SystemExit(main())
