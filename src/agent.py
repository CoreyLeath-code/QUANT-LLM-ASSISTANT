"""Deterministic market lookup agent."""

from __future__ import annotations

from .data_client import validate_symbol
from .mcp_client import MCPClient


class QuantLLMAgent:
    def __init__(self, client: MCPClient | None = None) -> None:
        self.client = client or MCPClient()

    def analyze_stock(self, symbol: str) -> dict[str, object]:
        ticker = validate_symbol(symbol)
        raw_data = self.client.call_tool("get_stock_data", symbols=ticker)
        results = raw_data.get("quoteResponse", {}).get("result", [])
        if not results:
            raise ValueError(f"no quote returned for {ticker}")
        quote = results[0]
        return {"symbol": ticker, "name": quote.get("shortName", ticker),
                "price": quote.get("regularMarketPrice"), "currency": quote.get("currency")}

    def run(self, query: str) -> dict[str, object]:
        return self.analyze_stock(query)
