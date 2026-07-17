"""Deterministic core-engine benchmark with a generous CI regression budget."""

from __future__ import annotations

import argparse
import time

import pandas as pd

from src.backtest import BacktestEngine


def run(iterations: int = 100, rows: int = 1_000) -> float:
    frame = pd.DataFrame(
        {"close": [100.0 + (index % 20) for index in range(rows)]},
        index=pd.date_range("2020-01-01", periods=rows, freq="min"),
    )
    started = time.perf_counter()
    for _ in range(iterations):
        BacktestEngine(frame, lambda data: pd.Series(1, index=data.index)).run()
    return (time.perf_counter() - started) / iterations


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-seconds", type=float, default=0.25)
    args = parser.parse_args()
    latency = run()
    print(f"mean_backtest_latency_seconds={latency:.6f}")
    if latency > args.max_seconds:
        raise SystemExit(f"latency regression: {latency:.6f}s > {args.max_seconds:.6f}s")


if __name__ == "__main__":
    main()
