# **Installation**

Follow this guide step-by-step.

## **Requirements**

- [Python >=3.9](https://www.python.org/downloads/)
- [Docker](https://docs.docker.com/get-started/get-docker/)

## **Configure**

You must update configs in the `.env` file. 

> If you're using Docker container with a PostgreSQL database, ensure that the `DB_PASSWORD` in your `.env` file matches the one defined in your `compose.yaml`. 

## **Usage**

If you have installed `bash shell`.

```bash
bash scripts/build.sh

bash scripts/run.sh 
```

Alternative way:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install poetry

poetry install --no-root

docker compose up # -d
```

If you want to use dedicated PostgreSQL server instead of running it locally in a Docker container, simply execute the following command.

```bash
bash scripts/run.sh backend mkdocs # -d
# or
docker compose up backend mkdocs # -d
```

If you want to run the Telegram bot, simply execute the following command in the project root:

```bash
python bot/bot.py
```

## **Docs**

    # Project docs (MkDocs): 
    - http://localhost:8005

    # Swagger UI:
    - http://localhost:8000/docs
    
    # ReDoc UI:
    - http://localhost:8000/redoc
    