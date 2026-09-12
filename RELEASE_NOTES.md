# QUANT-LLM-ASSISTANT v1.0.0

First stable release of the trust-bounded quantitative research assistant following the latest engineering, security, reproducibility, and quantitative-research audit.

## Highlights

- Validated external market-data boundary with fail-closed provider handling
- Research-only OpenAI-compatible LLM boundary
- Deterministic single-instrument backtesting engine
- Return and maximum-drawdown statistics
- Strict input, data-contract, configuration, and signal validation
- MCP host allowlisting and declared-parameter enforcement
- Deterministic 1,000-row latency regression benchmark
- Mathematical foundations and complexity documentation
- Academic evidence audit and documented research limitations
- CI quality, security, coverage, performance, and container gates
- Docker build and CLI smoke-test workflow
- Production-readiness, rollout, rollback, and incident-response guidance

## Verification

The repository CI gates cover:

- Ruff
- Strict MyPy
- Pytest with a 90% minimum coverage requirement
- Bandit
- pip-audit
- Deterministic latency regression testing
- Docker build and CLI smoke testing

## Scope

This release is for research and educational use. It does not execute trades, connect to brokerage accounts, manage portfolios, or provide personalized investment advice.

Backtests intentionally omit real-market effects including fees, spread, slippage, liquidity, borrow costs, taxes, corporate actions, and execution delay.

## Reproducibility

The latency benchmark records commit-bound evidence and runner metadata. Benchmark timings are regression evidence rather than trading-performance, capacity, or production-SLO claims.

## Security

External credentials are intended to remain outside source control. The project documents trust boundaries for CLI input, environment configuration, market-data providers, MCP configuration, LLM output, backtesting, and CI/supply-chain controls.

