# Quant LLM Assistant

A guardrailed command-line assistant for quantitative research. It combines validated market-data
context with an LLM summary and includes a deterministic research backtester. It does not execute
orders and its output is not investment advice.

## Quick start

Requires Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
cp .env.example .env
python -m src.main --symbol AAPL --query "Summarize the observed close and limitations"
```

`OPENAI_API_KEY` is required for every query. `DATA_API_KEY` is required only when `--symbol` is
used. Configuration is validated at the point of use, so importing the package does not require
credentials.

## Trust boundaries

- Tickers, intervals, output sizes, prompt sizes, URLs, timeouts, and strategy signals are validated.
- Market-provider responses must contain the expected time-series contract; provider error and
  throttling payloads fail closed.
- Retrieved data is labeled untrusted before it reaches the model. A system policy requires facts,
  estimates, dates, limitations, and a research-only disclaimer to remain distinct.
- API failures omit secrets and raw response bodies. No order-execution capability exists.
- Backtests reject missing/non-positive prices, unordered data, invalid positions, and misaligned
  signals. Results exclude fees, slippage, liquidity, taxes, and survivorship effects.

## Verification

```bash
ruff check src tests
mypy src/config.py src/data_client.py src/llm_agent.py
pytest
bandit -r src -q
python -m benchmarks.latency_benchmark --max-seconds 0.25
docker build -t quant-llm-assistant .
docker run --rm quant-llm-assistant --help
```

CI enforces these gates, 90% coverage across critical modules, dependency auditing, and a container
smoke test. It never contacts live market or LLM services.

## Operations

The CLI writes results to standard output and errors to the process error path. Monitor exit rate,
provider latency/error rate, throttling responses, token consumption, and benchmark latency. Keep
API keys in a secret manager, rotate them on exposure, and restrict outbound traffic to configured
providers. See [docs/production-readiness.md](docs/production-readiness.md).
