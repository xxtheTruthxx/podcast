FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app/

RUN pip install --no-cache-dir poetry

COPY ./pyproject.toml /app/

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root
    
COPY ./backend/app/ /app/    

ENV PYTHONPATH=.

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]