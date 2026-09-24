# Quant LLM Assistant

[![CI](https://github.com/CoreyLeath-code/QUANT-LLM-ASSISTANT/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/CoreyLeath-code/QUANT-LLM-ASSISTANT/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A Python-based quantitative research assistant that combines validated market-data retrieval, a guarded OpenAI-compatible LLM boundary, and a deterministic single-instrument backtesting engine.

> **Research and education only.** This project does not execute trades, connect to a brokerage for order placement, or provide personalized investment advice.

## What it does

Quant LLM Assistant is designed around explicit trust boundaries between external data, probabilistic model output, and quantitative calculations.

- Retrieves daily and intraday market data through an Alpha Vantage-compatible API.
- Validates ticker symbols, response structure, provider errors, request timeouts, and supported query parameters.
- Labels retrieved market observations as untrusted context before they reach the LLM.
- Uses an OpenAI-compatible chat interface with a research-focused system policy.
- Runs a deterministic long/flat/short backtest over supplied close prices.
- Reports total return and maximum drawdown for the backtest.
- Provides CLI, Docker, test, static-analysis, security-audit, and package-release workflows.

## Architecture

~~~mermaid
flowchart LR
    A[Researcher] --> B[CLI]
    B --> C[Input validation]
    C --> D[Market-data client]
    D --> E[External market-data API]
    E --> F[Response validation]
    F --> G[Untrusted dated context]
    G --> H[LLM boundary]
    H --> I[Research output]

    C --> J[BacktestEngine]
    J --> K[Equity curve]
    K --> L[Return / drawdown]
~~~

The two main paths are deliberately separated:

1. **Research path:** validated external observations are passed to the LLM as context, not instructions.
2. **Quantitative path:** the backtesting engine operates on caller-supplied price data and strategy signals without making external trades.

## Core components

| Component | Purpose |
| --- | --- |
| `src/main.py` | CLI entry point and research-context assembly |
| `src/config.py` | Environment-backed configuration and validation |
| `src/data_client.py` | Market-data requests and response validation |
| `src/llm_agent.py` | OpenAI-compatible LLM boundary and research policy |
| `src/backtest.py` | Deterministic strategy simulation and risk statistics |
| `src/mcp_client.py` | Configuration-driven external tool boundary |
| `src/plotting.py` | Quantitative visualization helpers |
| `src/report.py` | Research report generation |
| `benchmarks/` | Deterministic latency regression workload |
| `tests/` | Unit and failure-path coverage |
| `.github/workflows/ci.yml` | Quality, security, benchmark, and container checks |
| `.github/workflows/release.yml` | Version validation and package release pipeline |

## Backtesting model

`BacktestEngine` accepts:

- an ordered `pandas.DataFrame` containing a positive, finite `close` series;
- a strategy function returning a signal aligned exactly to the price index;
- positive starting cash.

Positions are constrained to:

- `1` — long
- `0` — flat
- `-1` — short

The engine produces an equity curve containing cash, position, holdings, and total equity. `stats()` reports:

- **Total return**
- **Maximum drawdown**

The implementation is intentionally simple and deterministic. It does **not** model:

- commissions or fees;
- bid/ask spread;
- slippage;
- liquidity;
- borrow costs;
- margin requirements;
- taxes;
- corporate actions;
- execution latency;
- portfolio-level allocation;
- survivorship or market-selection effects.

Consequently, backtest output should be treated as illustrative research accounting rather than evidence of live trading performance.

## LLM safety boundary

The LLM integration is intentionally constrained.

The system prompt instructs the model to:

- treat market data and user text as untrusted data;
- distinguish observed facts from estimates;
- avoid claims of certainty;
- avoid personalized investment advice;
- avoid trade execution;
- state material data dates and limitations;
- identify the response as research-only.

The application also validates prompt length, temperature, maximum output tokens, and empty model responses.

These controls reduce common failure modes but **do not make generated analysis authoritative**. Model output can still be incomplete, incorrect, or inappropriate for a particular research question.

## Market-data boundary

The market-data client validates the boundary before data is used.

It checks:

- ticker-symbol format;
- supported intraday intervals;
- supported output sizes;
- HTTPS/provider configuration through the settings layer;
- request timeouts;
- HTTP failures;
- JSON decoding;
- provider error/throttling messages;
- expected time-series fields.

Provider failures are surfaced as controlled `MarketDataError` exceptions rather than silently treated as valid observations.

## Requirements

- Python **3.11+**
- An OpenAI API key for LLM queries
- An Alpha Vantage API key when retrieving market data
- Docker for the container workflow

Runtime dependencies are declared in `pyproject.toml`. Development tooling includes pytest, coverage, Ruff, MyPy, Bandit, and pip-audit.

## Installation

### From source

~~~bash
git clone https://github.com/CoreyLeath-code/QUANT-LLM-ASSISTANT.git
cd QUANT-LLM-ASSISTANT

python -m venv .venv
~~~

Activate the environment:

~~~powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
~~~

~~~bash
# macOS / Linux
source .venv/bin/activate
~~~

Install the project with development dependencies:

~~~bash
python -m pip install --upgrade pip "setuptools>=83"
python -m pip install -e ".[dev]"
~~~

### PyPI

The project metadata defines the distribution as `quant-llm-assistant` at version `1.0.0`.

After the first successful PyPI publication, the package can be installed with:

~~~bash
python -m pip install quant-llm-assistant
~~~

## Configuration

Create a local `.env` file from `.env.example` and provide only the credentials required for the command you are running.

~~~dotenv
OPENAI_API_KEY=
DATA_API_KEY=
DATA_API_BASE_URL=https://www.alphavantage.co/query
OPENAI_API_BASE=https://api.openai.com/v1
REQUEST_TIMEOUT_SECONDS=10
~~~

| Variable | Purpose |
| --- | --- |
| `OPENAI_API_KEY` | Authentication for the configured OpenAI-compatible LLM endpoint |
| `DATA_API_KEY` | Authentication for market-data requests |
| `DATA_API_BASE_URL` | Market-data API endpoint |
| `OPENAI_API_BASE` | OpenAI-compatible API base URL |
| `REQUEST_TIMEOUT_SECONDS` | Bounded network timeout |

Do not commit API keys or other credentials to the repository.

## CLI usage

Ask a research question without market-data retrieval:

~~~bash
python -m src.main --query "Explain the limitations of a simple momentum backtest"
~~~

Include a validated daily market observation:

~~~bash
python -m src.main --symbol AAPL --query "Summarize the latest observed close and explain what cannot be inferred from it"
~~~

Display command-line help:

~~~bash
python -m src.main --help
~~~

## Backtest example

~~~python
import pandas as pd

from src.backtest import BacktestEngine

prices = pd.DataFrame(
    {"close": [100.0, 103.0, 101.0]},
    index=pd.date_range("2026-01-01", periods=3),
)


def always_long(frame: pd.DataFrame) -> pd.Series:
    return pd.Series(1, index=frame.index)


engine = BacktestEngine(
    prices,
    always_long,
    initial_cash=10_000,
)

equity = engine.run()
metrics = engine.stats()

print(metrics)
~~~

This example demonstrates the accounting engine only. It is not a trading recommendation or a prediction of future returns.

## Reproducible latency benchmark

The repository includes a deterministic benchmark for the backtesting workload:

~~~bash
python -m benchmarks.latency_benchmark --max-seconds 0.25 --output artifacts/latency-benchmark.json
~~~

CI runs the benchmark against a fixed synthetic workload and stores the resulting JSON as a workflow artifact. The benchmark is intended as a **regression check**, not as a claim about trading performance, production throughput, or a universal latency guarantee.

The evidence record includes the commit, workload definition, timing samples, summary statistics, runner information, and applied threshold.

## Quality gates

The CI workflow runs separate quality, security, and container jobs.

### Quality

~~~bash
ruff check src tests benchmarks
mypy src/config.py src/data_client.py src/llm_agent.py
python -m pytest
~~~

The pytest configuration enforces a **90% minimum coverage threshold** over the configured core modules.

### Security

~~~bash
bandit -r src -q
pip-audit
~~~

### Container

~~~bash
docker build -t quant-llm-assistant:local .
docker run --rm quant-llm-assistant:local --help
~~~

The container check verifies that the image builds and that the CLI help command can execute successfully.

## Release process

Package metadata is maintained in `pyproject.toml`.

The release workflow:

1. Runs when a `v*` Git tag is pushed.
2. Verifies that the tag version matches the package version.
3. Builds source and wheel distributions.
4. Validates the distributions with Twine.
5. Stores the distributions as a workflow artifact.
6. Creates a GitHub Release from the tag.
7. Publishes the distributions to PyPI through GitHub Actions OIDC / PyPI Trusted Publishing.

For a release such as `1.0.0`, the corresponding Git tag is:

~~~text
v1.0.0
~~~

The PyPI publisher must be configured to trust this repository and the release workflow before the OIDC publication step can succeed.

## Trust boundaries

| Boundary | Risk | Repository control |
| --- | --- | --- |
| User/CLI input | Invalid or oversized input | Input validation and bounded parameters |
| Environment | Missing or exposed credentials | Lazy configuration and secret-free error handling |
| Market-data provider | Malformed, throttled, or unexpected responses | HTTP, schema, and provider-error validation |
| LLM | Prompt injection or unsupported certainty | Untrusted-context labeling and system policy |
| Backtest | Invalid prices or misaligned signals | Ordered index, positive finite prices, exact signal alignment |
| CI supply chain | Dependency and code regressions | Static analysis, dependency audit, tests, and container checks |

## Limitations

This repository is intentionally a research-oriented foundation rather than a production trading platform.

Current limitations include:

- limited provider integration;
- no brokerage order execution;
- no portfolio-management layer;
- no live-trading controls;
- simplified single-instrument backtesting;
- no transaction-cost or market-impact model;
- no hosted authentication or multi-tenant authorization;
- no guarantee that LLM-generated analysis is correct;
- environment-specific deployment assets require validation before operational use.

## Roadmap

Potential future work includes:

1. Add typed provider adapters and recorded response fixtures.
2. Add transaction-cost, spread, slippage, borrow-cost, and portfolio models.
3. Expand benchmark coverage across representative workloads.
4. Add structured, redacted telemetry for latency and cost analysis.
5. Add stronger package provenance and software-supply-chain evidence.
6. Introduce an HTTP API only after authentication, authorization, quota, and abuse controls are defined.

Roadmap items are planned areas of exploration, not delivery commitments.

## Repository documentation

Additional technical documentation is available in:

- [`docs/ACADEMIC_AUDIT.md`](docs/ACADEMIC_AUDIT.md)
- [`docs/COMPLEXITY_ANALYSIS.md`](docs/COMPLEXITY_ANALYSIS.md)
- [`docs/MATHEMATICAL_FOUNDATIONS.md`](docs/MATHEMATICAL_FOUNDATIONS.md)
- [`docs/production-readiness.md`](docs/production-readiness.md)
- [`CONTRIBUTING.md`](CONTRIBUTING.md)
- [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md)
- [`CHANGELOG.md`](CHANGELOG.md)

## Contributing

Contributions should preserve the repository's trust boundaries and include tests for new behavior and failure modes.

Before opening a pull request, run the applicable quality and security checks locally:

~~~bash
ruff check src tests benchmarks
mypy src/config.py src/data_client.py src/llm_agent.py
python -m pytest
bandit -r src -q
pip-audit
~~~

Keep changes focused and document security, operational, or behavioral consequences in the pull request.

## License

This project is licensed under the MIT License. See [`LICENSE`](LICENSE).

## Disclaimer

Quant LLM Assistant is provided for research and educational purposes. It is not investment, legal, accounting, or tax advice. Historical or simulated results do not guarantee future performance. Independently validate data, assumptions, and model output before making financial decisions.
