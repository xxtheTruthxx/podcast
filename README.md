# **PodGen**

**PodGen** is a podcast episodes generator service. Users can create podcast episodes, fetch a list of episodes, auto-generate alternative titles or descriptions via LLM.

# **Features**

- High-performace Python web framework for building APIs. 
- Fully asynchronous using `async def` path operation, enabling non-blocking oprations.
- Fast and Robust data validation using SQLModel (which is based on Pydantic) and Pydantic library.
- Integrated with PostgreSQL using Docker image and SQLModel library.
- Seamless containerzation using Docker / Docker compose.
- Environment configuration.

# FAQ

### - Why I use asynchronous instead of synchronous paradigm?
Using the asynchronous programming paradigm significantly improves the performance and responsiveness of an application. <br>
Benefits:
 - Improved Performance: FastAPI can handle a higher volume of requests with minimal resource consumption.
 - Enhanced Responsiveness: Users experience faster response time.
 - Better suited with databases: Significantly improves database interaction.  

### - Why I use the PostgreSQL?
Honestly, I had never used SQL databases before, so I challenged myself to learn by using PostgreSQL for this project. </br>
I set up PostgreSQL in a Docker container, because it simplifies, isolation and portability across environments. 

### - Why I use Groq for the Level 2?
Because, It offers a free tier with good speed and perfomance, making it good choice for development or even producation. </br>
For the `GroqClient`, I use LangChain framework. [LangChain](https://www.langchain.com/) is a framework that makes it easy to build application with LLMs. </br>
Combined with `Groq API` to achieve fast inference speed and maintain simplicity.


https://npr.github.io/content-distribution-service/faq/table-of-aggregations.html

### - How to check environment configuration (variables)?
In the `.env.example` file.

# **Installation**

Follow this guide step-by-step.

## **Requirements**

- [Python >=3.9](https://www.python.org/downloads/)
- [Docker](https://docs.docker.com/get-started/get-docker/)

## Configure

You must update configs in the `.env` file. 

> Make sure your `DB_PASSWORD` in the `.env` file matches the one defined in Docker `compose.yaml`. 

## How to use

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

# **Code Snippets**

```

.



```



<!--  -->
<!-- `exec` not working ad9 -->
<!-- -third party labries -->
<!-- - add entry -->