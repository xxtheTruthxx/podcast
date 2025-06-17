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

docker compose up
```

If you're want to using dedicated server for the PostgreSQL instead of local (Docker Image).

```bash
bash scripts/run.sh backend mkdocs
# or
docker compose up backend mkdocs
```

## **Docs**

    # Swagger UI:
    - http://localhost:8000/docs
    
    # ReDoc UI:
    - http://localhost:8000/redoc
    
    # Project docs (MkDocs): 
    - http://localhost:8005