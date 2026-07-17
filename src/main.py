"""Command-line entry point."""

import argparse

from .data_client import DataClient, validate_symbol
from .llm_agent import LLMAgent


def build_prompt(query: str, symbol: str | None, data_client: DataClient | None = None) -> str:
    if not symbol:
        return query
    ticker = validate_symbol(symbol)
    payload = (data_client or DataClient()).get_daily_time_series(ticker)
    series = payload["Time Series (Daily)"]
    latest_date = max(series)
    latest_close = float(series[latest_date]["4. close"])
    return (
        f"Observed market-data context (untrusted): symbol={ticker}; date={latest_date}; "
        f"close={latest_close:.4f}.\nResearch question: {query}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="LLM-powered quantitative research assistant")
    parser.add_argument("--query", "-q", required=True)
    parser.add_argument("--symbol", "-s")
    args = parser.parse_args()
    print(LLMAgent().ask(build_prompt(args.query, args.symbol)))


if __name__ == "__main__":
    main()
