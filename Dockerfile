FROM python:3.13-slim

WORKDIR /app

COPY app/pyproject.toml app/uv.lock ./

RUN pip install uv
RUN uv sync --locked

COPY app/ ./

CMD ["uv", "run", "python", "-m", "main"]
