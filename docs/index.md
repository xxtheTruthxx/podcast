# Home

**PodGen** is a podcast episodes generator service. Users can create podcast episodes, fetch a list of episodes, auto-generate alternative titles or descriptions via LLM, integrate external episodes via RSS, and get updates via Telegram.

# Features

- High-performace Python web framework for building APIs. 
- Fully asynchronous using `async def` path operation, enabling non-blocking oprations.
- Fast and Robust data validation using SQLModel (which is based on Pydantic) and Pydantic library.
- Integrated with PostgreSQL using Docker image and SQLModel library.
- Seamless containerzation using Docker / Docker compose.
- Environment configuration.
- Project documentation with MkDocs material

# FAQ

#### **- Why I use asynchronous instead of synchronous paradigm?**
Using the asynchronous programming paradigm significantly improves the performance and responsiveness of an application.

- **Improved Performance**: FastAPI can handle a higher volume of requests with minimal resource consumption.
- **Enhanced Responsiveness**: Users experience faster response time.
- **Better suited with databases**: Significantly improves database interaction.  

#### **- Why I use the PostgreSQL?**
I had never used SQL databases before, so I challenged myself to learn by using PostgreSQL for this project. </br>
PostgreSQL setup options:

- Local setup: Recommend to use Docker container for development stages due to simplicity, isolation and portability across environments.
- Producation setup: Use PostgreSQL hosting platforms for a managed experience and easier deployment. (e.g., [Supabase](https://supabase.com/))

*If you want to use Supabase, you must connect via the `session pooler`.*

#### **- Why I use Groq as the LLM API?**
Because, It offers a free tier with good speed and perfomance, making it good choice for development or even producation. </br>
For the `GroqClient`, I use LangChain framework. [LangChain](https://www.langchain.com/) is a framework that makes it easy to build application with LLMs. </br>
Combined with `Groq API` to achieve fast inference speed and maintain simplicity.

#### **- Why I use aiogram for my Telegram bot?**
`aiogram` is built on Python`s asyncio, which makes it highly efficient and scalable. It also comes with a rich set of features, including:

- **Type Hints**: Comprehensive type hinting support for better code assistance in IDEs.
- **Middleware**: Flexible middleware system for request processing.
- **Routers**: Advanced routing system for organizing commands and message handlers.
- **FSM**: Built-in Finite State Machine for complex conversation flows.
- **Filters**: Extensible filters system for handling specific messages and callbacks.

#### **- What did I use for parse RSS feeds?**
I used the `Beatiful Soap 4` and `lxml` libraries. `Beatiful Soap 4` is a Python library that makes it easy to parse information from HTML and XML documents. The `lxml` is the most feature-rich, easy-to-use and fastest library for processing XML and HTML in the Python language. Together, they allow efficient parsing of RSS feeds, which are XML-based.

#### **- How to check environment configuration (variables)?**
In the `.env` file.

#### **- Why I'm having trouble with tests (using `pytest`)?**
FastAPI has asynchronous features make it one of the best web frameworks. However, because of its use of asynchronous code, testing a FastAPI API can be more complex than a standard synchronous API.</br>
I've attemted to write tests for FastAPI endpoints multiples times, but often run into obstacles like:

- Confusion around how to mock dependencies.
- Difficulty in integrating `pytest` with async functions.
- Getting a lot of errors related to the implementation of `conftest.py`.
- Switching to a test database.

If you want to experiment with pytests and run your test suite, simply execute the following command in the project root:

    pytest