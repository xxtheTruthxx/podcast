## Інформація про здобувача освіти
- ПІБ: Панасюк Владислав Васильович
- Група: ІПЗ-22

## Опис проєкту
- Назва застосунку: PodGen
- Тема/Галузь: PodGen is an RESTful API that offers generate podcast episodes. Users can create podcast episodes, fetch a list of episodes, auto-generate alternative titles or descriptions via LLM, and get updates via Telegram.
- Посилання на Render:

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

#### **- How to check environment configuration (variables)?**
In the `.env` file.

## Функціональні можливості

- **[GET]** /api/v1/podcast/ - Головна сторінка (Привітання) 
- **[GET]** /api/v1/podcast/episodes/all - Получити всі наявні епізоди подкасту 
- **[POST]** /api/v1/podcast/episodes/create - Створити епізод з динамічними полями (title / description / host).
- **[POST (PUT)]** /api/v1/podcast/episodes/{episode_id}/generate_alternative - Перегенерувати title або description використовуючи мовну модель Groq.
- **[DELETE]** /api/v1/podcast/episodes/{episode_id}/delete - Видалити певний епізод використовуючи його id. 

## Технології та інструменти
- Backend: FastAPI, Groq (LLM), Docker (Dockerfile, Docker compose)
- Frontend: Jinja2
- База даних: PostgreSQL (Supabase or **Docker compose**)
- Додаткові бібліотеки: uvicorn, sqlmodel, asyncpg, mkdocs-material, langchain-groq

## Архітектура проєкту

```
  .               
  ├── backend                     # Основний бекенд проекту
  │   └── app  
  │       ├── api                 # API-шари
  │       │   ├── api.py          # Точка входу для API
  │       │   ├── dependencies.py # Визначення залежностей для роутів
  │       │   ├── __init__.py
  │       │   └── routes          # Конкретні маршрути API
  │       │       ├── __init__.py
  │       │       ├── podcast.py  # Роут для подкастів
  │       │       └── webhook.py  # Роут для вебхуків
  │       ├── core                # Основні налаштування та ядро проекту
  │       │   ├── config.py       # Конфігурації проєкту
  │       │   ├── db              # Робота з базою даних
  │       │   │   ├── database.py # Підключення до БД
  │       │   │   └── __init__.py
  │       │   ├── __init__.py
  │       │   ├── logger.py       # Налаштування логування
  │       │   ├── models          # ORM моделі
  │       │   │   └── podcast.py  # Модель подкасту
  │       │   └── services        # Сервіси / бізнес-логіка
  │       │       ├── groq.py     # Сервіс для роботи з Groq (можливо запити до CMS)
  │       │       └── __init__.py
  │       ├── crud                 # CRUD-операції для моделей
  │       │   ├── base_crud.py     # Базові CRUD-функції
  │       │   ├── __init__.py
  │       │   └── podcast_crud.py  # CRUD для подкастів
  │       ├── __init__.py
  │       ├── main.py             # Основний файл запуску FastAPI
  │       ├── static              # Статичні файли
  │       │   ├── assets          # Зображення, іконки
  │       │   │   └── bg.jpg      
  │       │   └── css             # CSS стилі
  │       │       └── styles.css
  │       └── templates           # HTML-шаблони (Jinja2)
  │           ├── base.html       # Базовий шаблон
  │           ├── components      # Компоненти UI
  │           │   ├── footer.html
  │           │   ├── header.html
  │           │   ├── notFound.html
  │           │   └── podcast
  │           │       ├── create_alternative_episode.html
  │           │       ├── create_episode.html
  │           │       └── list_episodes.html
  │           └── home.html       # Головна сторінка
  ├── bot                        # Telegram або інший бот
  │   ├── bot.py                 # Основний файл бота
  │   └── helper                  # Допоміжні утиліти
  │       ├── __init__.py
  │       └── utils.py           # Функції для повторного використання
  ├── compose.yaml               # Docker Compose конфігурація
  ├── Dockerfile                 # Dockerfile для бекенду
  ├── docs                        # Документація проєкту
  │   ├── index.md
  │   ├── installation.md
  │   └── report.md
  ├── LICENSE                    # Ліцензія
  ├── mkdocs.yml                 # Конфіг для документації MkDocs
  ├── poetry.lock                # Заблоковані версії залежностей
  ├── pyproject.toml             # Налаштування проєкту та залежностей Poetry
  ├── README.md                  # Опис проєкту
  └── scripts                    # Скрипти для розробки та деплою
      ├── build.sh               # Скрипт для збірки
      └── run.sh                 # Скрипт для запуску
```

## API документація

| Метод | URL | Опис | Параметри |
|-------|-----|------|-----------|
| GET | /api/v1/podcast/ | Main (Greeting) page | Absence |
| GET | /api/v1/podcast/episodes/all | Get all episodes. | offset: int, limit: int |
| POST | /api/v1/podcast/episodes/create | Create an episode. | title, description, host (author) |
| POST (PUT) | /api/v1/podcast/episodes/{episode_id}/generate_alternative | Generate an alternative version of the episode. | episode_id: int |
| DELETE | /api/v1/podcast/episodes/{episode_id}/delete | Deletes episode by id | episode_id: int |
| POST | /api/v1/webhook/event | /api/v1/webhook/event | Absence |

## Схема бази даних

PostgreSQL setup options:

- Local setup: Recommend to use Docker container for development stages due to simplicity, isolation and portability across environments.
- Producation setup: Use PostgreSQL hosting platforms for a managed experience and easier deployment. (e.g., [Supabase](https://supabase.com/))

*If you want to use Supabase, you must connect via the `session pooler`.*

```
  user <==> clinet (PodGen) <==> PostgreSQL 
```

## Висновки

Під час виконання лабораторної роботи я, як студент, застосував усі наявні знання та навички, прагнучи зробити проєкт більш масштабним. Для реалізації було обрано нестандартний підхід щодо кожного пункту завдання. Важливо зазначити, що я не використовував ШІ як основний засіб розв’язання.
Окремої уваги заслуговує набір інструментів, який я підібрав: FastAPI, Docker (Compose) із можливістю локального розгортання PostgreSQL, Groq (LLM), aiogram та інші.
Попри те, що я вже маю певний досвід у сфері бекенд-розробки, ця лабораторна робота дала мені нове вміння — гнучко створювати та організовувати path operations.

## Самооцінка
Очікувана оцінка: 12 балів
Обґрунтування: Під час виконання роботи, я реалізував не стандартний підхід щодо створення бекенду. Також важливо зазначит те, що я використував Git (GitHub), Mkdocs-material (яку розгорнув на Docker локально) та весь проєкт був реалізований на операційній системі Arch Linux. 