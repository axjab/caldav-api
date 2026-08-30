FROM python:3.13-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv

COPY app/pyproject.toml app/uv.lock ./

RUN uv sync --locked --no-install-project

COPY app/ ./

RUN uv sync --locked

CMD ["uv", "run", "python", "-m", "main"]
