# Use the Python runtime required by pyproject.toml (>=3.11).
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/app \
    HOME=/home/appuser

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt

RUN useradd --uid 10001 --create-home --shell /usr/sbin/nologin appuser
COPY --chown=appuser:appuser src/ ./src/
USER 10001:10001

ENTRYPOINT ["python", "-m", "src.main"]
