FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app/

# ENV PATH="/app/.venv/bin:$PATH"

RUN pip install --no-cache-dir poetry

COPY pyproject.toml /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY /src .
COPY .env .

ENV PYTHONPATH=/app/src/app

EXPOSE 80

CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]