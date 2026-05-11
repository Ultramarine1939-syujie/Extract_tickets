import pytest

from extract_tickets.config import (
    DEFAULT_HOST,
    DEFAULT_MAX_CONTENT_LENGTH,
    DEFAULT_PORT,
    AppConfig,
)
from extract_tickets.web import create_app


def test_app_config_uses_defaults(monkeypatch):
    monkeypatch.delenv("FLASK_HOST", raising=False)
    monkeypatch.delenv("FLASK_PORT", raising=False)
    monkeypatch.delenv("MAX_CONTENT_LENGTH", raising=False)

    config = AppConfig.from_env()

    assert config.host == DEFAULT_HOST
    assert config.port == DEFAULT_PORT
    assert config.max_content_length == DEFAULT_MAX_CONTENT_LENGTH


def test_app_config_reads_environment(monkeypatch):
    monkeypatch.setenv("FLASK_HOST", "0.0.0.0")
    monkeypatch.setenv("FLASK_PORT", "9000")
    monkeypatch.setenv("MAX_CONTENT_LENGTH", "209715200")

    config = AppConfig.from_env()

    assert config.host == "0.0.0.0"
    assert config.port == 9000
    assert config.max_content_length == 209715200


def test_app_config_rejects_invalid_port(monkeypatch):
    monkeypatch.setenv("FLASK_PORT", "not-a-number")

    with pytest.raises(ValueError, match="FLASK_PORT must be an integer"):
        AppConfig.from_env()


def test_create_app_uses_environment_max_content_length(monkeypatch):
    monkeypatch.setenv("MAX_CONTENT_LENGTH", "12345")

    app = create_app()

    assert app.config["MAX_CONTENT_LENGTH"] == 12345
