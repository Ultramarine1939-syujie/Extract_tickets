"""应用配置。"""

import os
from dataclasses import dataclass

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8088
DEFAULT_MAX_CONTENT_LENGTH = 100 * 1024 * 1024


@dataclass(frozen=True)
class AppConfig:
    """Web 服务运行配置。"""

    host: str = DEFAULT_HOST
    port: int = DEFAULT_PORT
    max_content_length: int = DEFAULT_MAX_CONTENT_LENGTH

    @classmethod
    def from_env(cls) -> "AppConfig":
        """从环境变量读取配置，未设置时使用默认值。"""

        return cls(
            host=os.getenv("FLASK_HOST", DEFAULT_HOST),
            port=_read_positive_int("FLASK_PORT", DEFAULT_PORT),
            max_content_length=_read_positive_int(
                "MAX_CONTENT_LENGTH",
                DEFAULT_MAX_CONTENT_LENGTH,
            ),
        )


def _read_positive_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None or value == "":
        return default
    try:
        parsed = int(value)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer") from exc
    if parsed <= 0:
        raise ValueError(f"{name} must be greater than 0")
    return parsed
