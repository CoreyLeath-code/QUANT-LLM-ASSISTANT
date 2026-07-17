"""Hardened Alpha Vantage market-data client."""

from __future__ import annotations

import re
from typing import Any

import requests

from .config import Settings

_SYMBOL = re.compile(r"^[A-Z][A-Z0-9.-]{0,9}$")
_INTERVALS = {"1min", "5min", "15min", "30min", "60min"}
_OUTPUT_SIZES = {"compact", "full"}


class MarketDataError(RuntimeError):
    """Raised when a provider response cannot be trusted as market data."""


def validate_symbol(symbol: str) -> str:
    normalized = symbol.strip().upper()
    if not _SYMBOL.fullmatch(normalized):
        raise ValueError("symbol must be 1-10 ticker characters (letters, digits, '.', or '-')")
    return normalized


class DataClient:
    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        *,
        timeout: float | None = None,
        session: requests.Session | None = None,
    ) -> None:
        settings = Settings.from_env(require_data=api_key is None)
        self.base_url = base_url or settings.data_api_base_url
        self.api_key = api_key or settings.data_api_key
        self.timeout = timeout or settings.request_timeout_seconds
        self.session = session or requests.Session()

    def _request(self, params: dict[str, str], expected_key: str) -> dict[str, Any]:
        try:
            response = self.session.get(self.base_url, params=params, timeout=self.timeout)
            response.raise_for_status()
            payload = response.json()
        except (requests.RequestException, ValueError) as exc:
            raise MarketDataError("market-data provider request failed") from exc
        if not isinstance(payload, dict):
            raise MarketDataError("market-data provider returned a non-object response")
        provider_error = (
            payload.get("Error Message") or payload.get("Information") or payload.get("Note")
        )
        if provider_error:
            raise MarketDataError(f"market-data provider rejected the request: {provider_error}")
        if expected_key not in payload or not isinstance(payload[expected_key], dict):
            raise MarketDataError(f"market-data response is missing {expected_key!r}")
        return payload

    def get_daily_time_series(self, symbol: str, outputsize: str = "compact") -> dict[str, Any]:
        if outputsize not in _OUTPUT_SIZES:
            raise ValueError("outputsize must be 'compact' or 'full'")
        params = {
            "function": "TIME_SERIES_DAILY_ADJUSTED",
            "symbol": validate_symbol(symbol),
            "apikey": str(self.api_key),
            "outputsize": outputsize,
        }
        return self._request(params, "Time Series (Daily)")

    def get_intraday(
        self, symbol: str, interval: str = "60min", outputsize: str = "compact"
    ) -> dict[str, Any]:
        if interval not in _INTERVALS:
            raise ValueError(f"interval must be one of {sorted(_INTERVALS)}")
        if outputsize not in _OUTPUT_SIZES:
            raise ValueError("outputsize must be 'compact' or 'full'")
        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": validate_symbol(symbol),
            "interval": interval,
            "apikey": str(self.api_key),
            "outputsize": outputsize,
        }
        return self._request(params, f"Time Series ({interval})")
