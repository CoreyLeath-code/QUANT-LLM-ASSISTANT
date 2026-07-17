"""Allowlisted HTTP tool client for repository-owned configuration."""

from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse

import requests
import yaml


class MCPClient:
    ALLOWED_HOSTS = {"query1.finance.yahoo.com"}

    def __init__(self, config_path: str = "mcp_config.yaml", timeout: float = 10.0) -> None:
        self.timeout = timeout
        with Path(config_path).open(encoding="utf-8") as handle:
            self.config = yaml.safe_load(handle) or {}

    def get_tool(self, tool_name: str) -> dict[str, object]:
        tool = next(
            (item for item in self.config.get("tools", []) if item.get("name") == tool_name),
            None,
        )
        if not tool:
            raise ValueError(f"tool {tool_name!r} is not configured")
        endpoint = str(tool.get("endpoint", ""))
        parsed = urlparse(endpoint)
        if parsed.scheme != "https" or parsed.hostname not in self.ALLOWED_HOSTS:
            raise ValueError("tool endpoint is not allowlisted")
        return tool

    def call_tool(self, tool_name: str, **kwargs: str) -> dict[str, object]:
        tool = self.get_tool(tool_name)
        allowed = set(tool.get("params", []))
        if set(kwargs) - allowed:
            raise ValueError("unsupported tool parameters")
        response = requests.get(str(tool["endpoint"]), params=kwargs, timeout=self.timeout)
        response.raise_for_status()
        payload = response.json()
        if not isinstance(payload, dict):
            raise ValueError("tool returned an invalid response")
        return payload
