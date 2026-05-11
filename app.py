"""兼容旧启动方式的 Web 入口。

运行:
    python app.py
"""

# ruff: noqa: E402

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from extract_tickets.config import AppConfig  # noqa: E402
from extract_tickets.web import create_app  # noqa: E402

config = AppConfig.from_env()
app = create_app(config)


if __name__ == "__main__":
    app.run(debug=False, port=config.port, host=config.host)
