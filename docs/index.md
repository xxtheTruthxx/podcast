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

- Improved Performance: FastAPI can handle a higher volume of requests with minimal resource consumption.
- Enhanced Responsiveness: Users experience faster response time.
- Better suited with databases: Significantly improves database interaction.  

#### **- Why I use the PostgreSQL?**
I had never used SQL databases before, so I challenged myself to learn by using PostgreSQL for this project. </br>
PostgreSQL setup options:

- Local setup: Recommend to use Docker container for development stages due to simplicity, isolation and portability across environments.
- Producation setup: Use PostgreSQL hosting platforms for a managed experience and easier deployment. (e.g., [Supabase](https://supabase.com/))

#### **- Why I use Groq for the Level 2?**
Because, It offers a free tier with good speed and perfomance, making it good choice for development or even producation. </br>
For the `GroqClient`, I use LangChain framework. [LangChain](https://www.langchain.com/) is a framework that makes it easy to build application with LLMs. </br>
Combined with `Groq API` to achieve fast inference speed and maintain simplicity.

#### **- How to check environment configuration (variables)?**
In the `.env.example` file.

#### **- What did I use for parse RSS feeds?**
I used the `Beatiful Soap 4` and `lxml` libraries. `Beatiful Soap 4` is a Python library that makes it easy to parse information from HTML and XML documents. The `lxml` is the most feature-rich, easy-to-use and fastest library for processing XML and HTML in the Python language. Together, they allow efficient parsing of RSS feeds, which are XML-based.

#### **- How to test endpoints?**
