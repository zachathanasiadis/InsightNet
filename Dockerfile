FROM python:3.12-slim AS builder

WORKDIR /app

RUN pip install --no-cache-dir poetry

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1

COPY pyproject.toml poetry.lock ./

RUN poetry install --without dev --no-root

FROM python:3.12-slim

RUN useradd -m nonroot

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH"

COPY --chown=nonroot:nonroot ./src /app/src

USER nonroot

EXPOSE 8000

CMD ["uvicorn", "src.insightnet.api:app", "--host", "0.0.0.0", "--port", "8000"]