FROM python:3.12-slim AS builder

WORKDIR /app

RUN pip install --no-cache-dir poetry poetry-plugin-export

COPY pyproject.toml poetry.lock /app/

RUN poetry export -f requirements.txt --without-hashes --output requirements.txt

FROM python:3.12-slim AS runtime

WORKDIR /app

COPY --from=builder /app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src /app/src

EXPOSE 8000

CMD ["uvicorn", "src.insightnet.api:app", "--host", "0.0.0.0", "--port", "8000"]
