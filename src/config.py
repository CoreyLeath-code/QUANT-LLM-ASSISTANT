"""Runtime configuration with explicit, lazy validation."""

from __future__ import annotations

import os
from dataclasses import dataclass
from urllib.parse import urlparse

from dotenv import load_dotenv

load_dotenv()


def _https_url(name: str, value: str) -> str:
    parsed = urlparse(value)
    if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
        raise ValueError(f"{name} must be an HTTPS URL without embedded credentials")
    return value.rstrip("/")


@dataclass(frozen=True)
class Settings:
    openai_api_key: str | None
    data_api_key: str | None
    data_api_base_url: str
    openai_api_base: str
    request_timeout_seconds: float = 10.0

    @classmethod
    def from_env(cls, *, require_openai: bool = False, require_data: bool = False) -> Settings:
        openai_key = os.getenv("OPENAI_API_KEY")
        data_key = os.getenv("DATA_API_KEY")
        missing = []
        if require_openai and not openai_key:
            missing.append("OPENAI_API_KEY")
        if require_data and not data_key:
            missing.append("DATA_API_KEY")
        if missing:
            raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")

        timeout = float(os.getenv("REQUEST_TIMEOUT_SECONDS", "10"))
        if not 0 < timeout <= 60:
            raise ValueError("REQUEST_TIMEOUT_SECONDS must be greater than 0 and at most 60")
        return cls(
            openai_api_key=openai_key,
            data_api_key=data_key,
            data_api_base_url=_https_url(
                "DATA_API_BASE_URL",
                os.getenv("DATA_API_BASE_URL", "https://www.alphavantage.co/query"),
            ),
            openai_api_base=_https_url(
                "OPENAI_API_BASE", os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
            ),
            request_timeout_seconds=timeout,
        )


# Backward-compatible, lazily populated constants. No secrets are validated at import time.
class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DATA_API_KEY = os.getenv("DATA_API_KEY")
    DATA_API_BASE_URL = os.getenv("DATA_API_BASE_URL", "https://www.alphavantage.co/query")
    OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")

    @classmethod
    def validate(cls) -> None:
        Settings.from_env(require_openai=True, require_data=True)
