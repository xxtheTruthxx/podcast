# Лабораторна робота №5: Розробка RESTful API

## Інформація про проєкт
- **Назва проєкту:** PodGen
- **Автори:** Панасюк Владислав Васильович, Пінкевич Артем Романович; ІПЗ-22

## Опис проєкту
PodGen - це RESTful API для генерації епізодів подкастів. Додаток дозволяє користувачам створювати епізоди подкастів, отримувати список епізодів, автоматично генерувати альтернативні назви або описи за допомогою LLM (Groq), та отримувати оновлення через Telegram. API також підтримує роботу з RSS-фідами для отримання інформації про подкасти.

## Технології
- Python 3.9+
- FastAPI
- PostgreSQL (через asyncpg)
- SQLModel
- Groq (LLM API)
- LangChain-Groq
- BeautifulSoup4
- Jinja2 (шаблонізатор для frontend)
- Uvicorn (ASGI сервер)
- Docker & Docker Compose
- MkDocs Material (документація)

## Встановлення та запуск

### Вимоги
- Python >=3.9
- Docker та Docker Compose

### Налаштування
1. Створіть файл `.env` в корені проєкту з наступними змінними:
```env
NAME=PodGen
DESCRIPTION=Podcast episodes aggregator and generator service
VERSION=0.1.0
API_V1_STR=/api/v1
BACKEND_CORS_ORIGINS=["*"]

DB_USERNAME=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
DB_NAME=podgen

GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL_TEMPLATE=You are a helpful assistant that generates creative podcast content.
GROQ_MODEL=llama-3.1-70b-versatile

RSS_URL=https://example.com/rss/feed.xml

ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin
```

2. Запустіть проєкт через Docker Compose:
```bash
docker compose up -d
```

Або використовуйте скрипти:
```bash
bash scripts/build.sh
bash scripts/run.sh
```

### Доступ до сервісів
- **Головна сторінка:** http://localhost:80
- **API документація (Swagger):** http://localhost:80/docs
- **API документація (ReDoc):** http://localhost:80/redoc
- **MkDocs документація:** http://localhost:8005

## Endpoints API

### Головні сторінки

#### 1. Головна сторінка
- **URL:** `/`
- **Метод:** `GET`
- **Опис:** Повертає головну HTML сторінку з привітанням та навігацією
- **Приклад запиту:**
```
GET /
```
- **Приклад відповіді:**
```html
HTTP 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
  <head>
    <title>PodGen</title>
  </head>
  <body>
    <!-- HTML сторінка з навігацією -->
  </body>
</html>
```
- **Скріншот з Postman (або Swagger):**
![Головна сторінка](docs/images/screenshots/apihome.png)

#### 2. Сторінка "Про проєкт"
- **URL:** `/about`
- **Метод:** `GET`
- **Опис:** Повертає HTML сторінку з інформацією про проєкт
- **Приклад запиту:**
```
GET /about
```
- **Приклад відповіді:**
```html
HTTP 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
  <head>
    <title>Про проєкт - PodGen</title>
  </head>
  <body>
    <!-- HTML сторінка з інформацією про проєкт -->
  </body>
</html>
```

- **Скріншот з Postman (або Swagger):**
![Опис](docs/images/screenshots/apiabout.png)

### Podcast Endpoints (HTML)

#### 3. Отримати всі епізоди
- **URL:** `/podcast/episodes/all`
- **Метод:** `GET`
- **Опис:** Отримує список всіх доступних епізодів подкасту з підтримкою пагінації
- **Параметри запиту:**
  - `offset` (int, опціонально): Зміщення для пагінації (за замовчуванням: 0)
  - `limit` (int, опціонально): Максимальна кількість епізодів для повернення
- **Приклад запиту:**
```
GET /podcast/episodes/all?offset=0&limit=10
```
- **Приклад відповіді:**
```html
HTTP 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
  <!-- HTML сторінка зі списком епізодів -->
</html>
```
- **Скріншот з Postman (або Swagger):**
![Список епізодів](docs/images/screenshots/apiepall.png)

#### 4. Форма створення епізоду
- **URL:** `/podcast/episodes/create`
- **Метод:** `GET`
- **Опис:** Повертає HTML форму для створення нового епізоду
- **Приклад запиту:**
```
GET /podcast/episodes/create
```
- **Приклад відповіді:**
```html
HTTP 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
  <!-- HTML форма з полями: title, description, host -->
</html>
```
- **Скріншот з Postman (або Swagger):**
![Форма створення епізоду](docs/images/screenshots/apiepcreate.png)

#### 5. Створити епізод
- **URL:** `/podcast/episodes/create`
- **Метод:** `POST`
- **Опис:** Створює новий епізод подкасту з вказаними полями
- **Формат:** `application/x-www-form-urlencoded`
- **Параметри:**
  - `title` (string): Назва епізоду
  - `description` (string): Опис епізоду
  - `host` (string): Ім'я хоста
- **Приклад запиту:**
```
POST /podcast/episodes/create
Content-Type: application/x-www-form-urlencoded

title=Назва епізоду&description=Опис епізоду&host=Ім'я хоста
```
- **Приклад відповіді:**
```
HTTP 303 See Other
Location: /podcast/episodes/all
```
- **Скріншот з Postman (або Swagger):**
![Створення епізоду](docs/images/screenshots/apiepcreate2.png)

#### 6. Форма генерації альтернативного контенту
- **URL:** `/podcast/episodes/{episode_id}/generate_alternative`
- **Метод:** `GET`
- **Опис:** Повертає HTML форму для генерації альтернативної назви або опису епізоду за допомогою LLM
- **Параметри шляху:**
  - `episode_id` (int): ID епізоду
- **Приклад запиту:**
```
GET /podcast/episodes/1/generate_alternative
```
- **Приклад відповіді:**
```html
HTTP 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
  <!-- HTML форма з полями: target (title/description), prompt -->
</html>
```
- **Скріншот з Postman (або Swagger):**
![Форма генерації альтернативного контенту](docs/images/screenshots/apigenalt.png)

#### 7. Генерувати альтернативний контент
- **URL:** `/podcast/episodes/{episode_id}/generate_alternative`
- **Метод:** `POST`
- **Опис:** Генерує альтернативну назву або опис епізоду за допомогою Groq LLM на основі підказки користувача
- **Параметри шляху:**
  - `episode_id` (int): ID епізоду для оновлення
- **Формат:** `application/x-www-form-urlencoded`
- **Параметри:**
  - `target` (string): "title" або "description"
  - `prompt` (string): Підказка для генерації
- **Приклад запиту:**
```
POST /podcast/episodes/1/generate_alternative
Content-Type: application/x-www-form-urlencoded

target=title&prompt=Зроби назву більш захоплюючою
```
- **Приклад відповіді:**
```
HTTP 303 See Other
Location: /podcast/episodes/all
```
- **Скріншот з Postman (або Swagger):**
![Генерація альтернативного контенту](docs/images/screenshots/apigenalt2.png)

### Podcast API Endpoints (JSON)

#### 8. Отримати всі епізоди (API)
- **URL:** `/api/v1/podcast/episodes/all`
- **Метод:** `GET`
- **Опис:** Отримує список всіх епізодів у форматі JSON
- **Параметри запиту:**
  - `offset` (int, опціонально): Зміщення для пагінації (за замовчуванням: 0)
  - `limit` (int, опціонально): Максимальна кількість епізодів
- **Приклад запиту:**
```
GET /api/v1/podcast/episodes/all?offset=0&limit=10
```
- **Приклад відповіді:**
```json
[
  {
    "id": 1,
    "title": "Назва епізоду",
    "description": "Опис епізоду",
    "host": "Ім'я хоста"
  },
  {
    "id": 2,
    "title": "Інший епізод",
    "description": "Опис іншого епізоду",
    "host": "Інший хост"
  }
]
```
- **Скріншот з Postman (або Swagger):**
![Отримати всі епізоди API](docs/images/screenshots/apipodall.png)

#### 9. Створити епізод (API)
- **URL:** `/api/v1/podcast/episodes/create`
- **Метод:** `POST`
- **Опис:** Створює новий епізод подкасту
- **Формат:** `application/x-www-form-urlencoded`
- **Параметри:**
  - `title` (string): Назва епізоду
  - `description` (string): Опис епізоду
  - `host` (string): Ім'я хоста
- **Приклад запиту:**
```
POST /api/v1/podcast/episodes/create
Content-Type: application/x-www-form-urlencoded

title=Новий епізод&description=Опис нового епізоду&host=Ведучий
```
- **Приклад відповіді:**
```json
{
  "message": "Episode has been created successfully."
}
```
- **Скріншот з Postman (або Swagger):**
![Створити епізод API](docs/images/screenshots/apipodcreate.png)

#### 10. Отримати епізод за ID (API)
- **URL:** `/api/v1/podcast/episodes/{episode_id}`
- **Метод:** `GET`
- **Опис:** Отримує інформацію про конкретний епізод
- **Параметри шляху:**
  - `episode_id` (int): ID епізоду
- **Приклад запиту:**
```
GET /api/v1/podcast/episodes/1
```
- **Приклад відповіді:**
```json
{
  "id": 1,
  "title": "Назва епізоду",
  "description": "Опис епізоду",
  "host": "Ім'я хоста"
}
```

- **Скріншот з Postman (або Swagger):**
![Отримати епізод API](docs/images/screenshots/apipodget.png)

#### 11. Перевірити існування епізоду (API)
- **URL:** `/api/v1/podcast/episodes/{episode_id}`
- **Метод:** `HEAD`
- **Опис:** Перевіряє чи існує епізод з вказаним ID
- **Параметри шляху:**
  - `episode_id` (int): ID епізоду
- **Приклад запиту:**
```
HEAD /api/v1/podcast/episodes/1
```
- **Приклад відповіді:**
```
HTTP 200 OK
```
- **Скріншот з Postman (або Swagger):**
![Отримати епізод API](docs/images/screenshots/apipodhead.png)

#### 12. Повне оновлення епізоду (API)
- **URL:** `/api/v1/podcast/episodes/{episode_id}`
- **Метод:** `PUT`
- **Опис:** Повністю оновлює епізод (всі поля обов'язкові)
- **Параметри шляху:**
  - `episode_id` (int): ID епізоду
- **Формат:** `application/json`
- **Приклад запиту:**
```json
PUT /api/v1/podcast/episodes/1
Content-Type: application/json

{
  "title": "Нова назва",
  "description": "Новий опис",
  "host": "Новий хост"
}
```
- **Приклад відповіді:**
```json
{
  "id": 1,
  "title": "Нова назва",
  "description": "Новий опис",
  "host": "Новий хост"
}
```
- **Скріншот з Postman (або Swagger):**
![Оновити епізод API](docs/images/screenshots/apipodupd.png)

#### 13. Часткове оновлення епізоду (API)
- **URL:** `/api/v1/podcast/episodes/{episode_id}`
- **Метод:** `PATCH`
- **Опис:** Частково оновлює епізод (тільки вказані поля)
- **Параметри шляху:**
  - `episode_id` (int): ID епізоду
- **Формат:** `application/json`
- **Приклад запиту:**
```json
PATCH /api/v1/podcast/episodes/1
Content-Type: application/json

{
  "title": "Оновлена назва"
}
```
- **Приклад відповіді:**
```json
{
  "id": 1,
  "title": "Оновлена назва",
  "description": "Оригінальний опис",
  "host": "Оригінальний хост"
}
```
- **Скріншот з Postman (або Swagger):**
![Частково оновити епізод API](docs/images/screenshots/apipodupd2.png)

#### 14. Видалити епізод (API)
- **URL:** `/api/v1/podcast/episodes/{episode_id}/delete`
- **Метод:** `DELETE`
- **Опис:** Видаляє епізод за його ID
- **Параметри шляху:**
  - `episode_id` (int): ID епізоду для видалення
- **Приклад запиту:**
```
DELETE /api/v1/podcast/episodes/1/delete
```
- **Приклад відповіді:**
```json
{
  "message": "Episode has been removed successfully."
}
```
- **Скріншот з Postman (або Swagger):**
![Видалити епізод](docs/images/screenshots/apidel.png)

### RSS Feed Endpoints (HTML)

#### 15. Отримати RSS фіди
- **URL:** `/rss/feeds`
- **Метод:** `GET`
- **Опис:** Отримує та парсить RSS фіди з вказаної URL та повертає список доступних епізодів
- **Параметри запиту:**
  - `offset` (int, опціонально): Зміщення для пагінації (за замовчуванням: 0)
  - `limit` (int, опціонально): Максимальна кількість фідів для повернення
- **Приклад запиту:**
```
GET /rss/feeds?offset=0&limit=10
```
- **Приклад відповіді:**
```html
HTTP 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
  <!-- HTML сторінка зі списком RSS фідів -->
</html>
```
- **Скріншот з Postman (або Swagger):**
![RSS фіди](docs/images/screenshots/apirss.png)

#### 16. Переглянути RSS фід
- **URL:** `/rss/feed/{uuid}`
- **Метод:** `GET`
- **Опис:** Отримує детальну інформацію про конкретний RSS фід
- **Параметри шляху:**
  - `uuid` (string): UUID фіду
- **Приклад запиту:**
```
GET /rss/feed/550e8400-e29b-41d4-a716-446655440000
```
- **Приклад відповіді:**
```html
HTTP 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
  <!-- HTML сторінка з детальною інформацією про RSS фід -->
</html>
```
- **Скріншот з Postman (або Swagger):**
![RSS фід](docs/images/screenshots/apiuuid.png)

#### 17. Додати RSS фід як епізод
- **URL:** `/rss/feed/{uuid}/add`
- **Метод:** `GET`
- **Опис:** Додає RSS фід як епізод подкасту
- **Параметри шляху:**
  - `uuid` (string): UUID фіду
- **Приклад запиту:**
```
GET /rss/feed/550e8400-e29b-41d4-a716-446655440000/add
```
- **Приклад відповіді:**
```html
HTTP 201 Created
Content-Type: text/html

<!DOCTYPE html>
<html>
  <!-- HTML сторінка з повідомленням про успішне додавання -->
</html>
```

- **Скріншот з Postman (або Swagger):**
![RSS додавання](docs/images/screenshots/apiuuidadd.png)

### RSS Feed API Endpoints (JSON)

#### 18. Отримати RSS фіди (API)
- **URL:** `/api/v1/rss/feeds`
- **Метод:** `GET`
- **Опис:** Отримує список RSS фідів у форматі JSON
- **Параметри запиту:**
  - `offset` (int, опціонально): Зміщення для пагінації (за замовчуванням: 0)
  - `limit` (int, опціонально): Максимальна кількість фідів
- **Приклад запиту:**
```
GET /api/v1/rss/feeds?offset=0&limit=10
```
- **Приклад відповіді:**
```json
[
  {
    "uuid": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Назва RSS фіду",
    "description": "Опис RSS фіду",
    "author": "Автор",
    "link": "https://example.com/feed",
    "pub_date": "2024-01-01T00:00:00",
    "image": "https://example.com/image.jpg"
  }
]
```
- **Скріншот з Postman (або Swagger):**
![RSS фіди API](docs/images/screenshots/apirssget.png)

#### 19. Отримати RSS фід за UUID (API)
- **URL:** `/api/v1/rss/feed/{uuid}`
- **Метод:** `GET`
- **Опис:** Отримує детальну інформацію про конкретний RSS фід
- **Параметри шляху:**
  - `uuid` (string): UUID фіду
- **Приклад запиту:**
```
GET /api/v1/rss/feed/550e8400-e29b-41d4-a716-446655440000
```
- **Приклад відповіді:**
```json
{
  "uuid": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Назва RSS фіду",
  "description": "Опис RSS фіду",
  "author": "Автор",
  "link": "https://example.com/feed",
  "pub_date": "2024-01-01T00:00:00",
  "image": "https://example.com/image.jpg"
}
```

- **Скріншот з Postman (або Swagger):**
![RSS фіди API](docs/images/screenshots/apirssuuid.png)

#### 20. Додати RSS фід як епізод (API)
- **URL:** `/api/v1/rss/feed/{uuid}/add`
- **Метод:** `POST`
- **Опис:** Додає RSS фід як епізод подкасту
- **Параметри шляху:**
  - `uuid` (string): UUID фіду
- **Приклад запиту:**
```
POST /api/v1/rss/feed/550e8400-e29b-41d4-a716-446655440000/add
```
- **Приклад відповіді:**
```json
{
  "detail": "Feed has been added successfully."
}
```
- **Скріншот з Postman (або Swagger):**
![Додати RSS фід API](docs/images/screenshots/apiuuidrssadd.png)

### Admin Endpoints

#### 21. Сторінка входу адміністратора
- **URL:** `/admin/login`
- **Метод:** `GET`
- **Опис:** Повертає HTML форму для входу адміністратора
- **Приклад запиту:**
```
GET /admin/login
```
- **Приклад відповіді:**
```html
HTTP 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
  <!-- HTML форма входу з полями: username, password -->
</html>
```

- **Скріншот з Postman (або Swagger):**
![Адмін](docs/images/screenshots/adminlogin.png)

#### 22. Вхід адміністратора
- **URL:** `/admin/login`
- **Метод:** `POST`
- **Опис:** Автентифікує адміністратора
- **Формат:** `application/x-www-form-urlencoded`
- **Параметри:**
  - `username` (string): Ім'я користувача
  - `password` (string): Пароль
- **Приклад запиту:**
```
POST /admin/login
Content-Type: application/x-www-form-urlencoded

username=admin&password=admin
```
- **Приклад відповіді:**
```
HTTP 303 See Other
Location: /admin/dashboard
Set-Cookie: admin_session=authenticated; HttpOnly
```

- **Скріншот з Postman (або Swagger):**
![Адмін](docs/images/screenshots/adminlogin2.png)

#### 23. Вихід адміністратора
- **URL:** `/admin/logout`
- **Метод:** `GET`
- **Опис:** Виконує вихід адміністратора
- **Приклад запиту:**
```
GET /admin/logout
```
- **Приклад відповіді:**
```
HTTP 303 See Other
Location: /admin/login
Set-Cookie: admin_session=; expires=Thu, 01 Jan 1970 00:00:00 GMT
```

- **Скріншот з Postman (або Swagger):**
![Адмін](docs/images/screenshots/adminlogout.png)

#### 24. Панель управління
- **URL:** `/admin/dashboard`
- **Метод:** `GET`
- **Опис:** Повертає HTML сторінку зі статистикою та панеллю управління
- **Вимагає:** Автентифікацію адміністратора
- **Приклад запиту:**
```
GET /admin/dashboard
Cookie: admin_session=authenticated
```
- **Приклад відповіді:**
```html
HTTP 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
  <!-- HTML сторінка зі статистикою: кількість епізодів, RSS фідів, тощо -->
</html>
```

- **Скріншот з Postman (або Swagger):**
![Адмін](docs/images/screenshots/admindash.png)

#### 25. Управління епізодами (Admin)
- **URL:** `/admin/episodes`
- **Метод:** `GET`
- **Опис:** Повертає HTML сторінку зі списком всіх епізодів для управління
- **Вимагає:** Автентифікацію адміністратора
- **Параметри запиту:**
  - `offset` (int, опціонально): Зміщення для пагінації
  - `limit` (int, опціонально): Максимальна кількість епізодів
- **Приклад запиту:**
```
GET /admin/episodes?offset=0&limit=10
Cookie: admin_session=authenticated
```
- **Приклад відповіді:**
```html
HTTP 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
  <!-- HTML сторінка зі списком епізодів та кнопками редагування/видалення -->
</html>
```

- **Скріншот з Postman (або Swagger):**
![Адмін](docs/images/screenshots/adminep.png)

#### 26. Форма додавання епізоду (Admin)
- **URL:** `/admin/episodes/add`
- **Метод:** `GET`
- **Опис:** Повертає HTML форму для додавання нового епізоду
- **Вимагає:** Автентифікацію адміністратора
- **Приклад запиту:**
```
GET /admin/episodes/add
Cookie: admin_session=authenticated
```
- **Приклад відповіді:**
```html
HTTP 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
  <!-- HTML форма з полями: title, description, host -->
</html>
```

- **Скріншот з Postman (або Swagger):**
![Адмін](docs/images/screenshots/adminadd.png)

#### 27. Додати епізод (Admin)
- **URL:** `/admin/episodes/add`
- **Метод:** `POST`
- **Опис:** Додає новий епізод через адмін-панель
- **Вимагає:** Автентифікацію адміністратора
- **Формат:** `application/x-www-form-urlencoded`
- **Параметри:**
  - `title` (string): Назва епізоду
  - `description` (string): Опис епізоду
  - `host` (string): Ім'я хоста
- **Приклад запиту:**
```
POST /admin/episodes/add
Content-Type: application/x-www-form-urlencoded
Cookie: admin_session=authenticated

title=Новий епізод&description=Опис&host=Ведучий
```
- **Приклад відповіді:**
```
HTTP 303 See Other
Location: /admin/episodes
```

- **Скріншот з Postman (або Swagger):**
![Адмін](docs/images/screenshots/adminadd2.png)

#### 28. Форма редагування епізоду (Admin)
- **URL:** `/admin/episodes/{episode_id}/edit`
- **Метод:** `GET`
- **Опис:** Повертає HTML форму для редагування епізоду
- **Вимагає:** Автентифікацію адміністратора
- **Параметри шляху:**
  - `episode_id` (int): ID епізоду
- **Приклад запиту:**
```
GET /admin/episodes/1/edit
Cookie: admin_session=authenticated
```
- **Приклад відповіді:**
```html
HTTP 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
  <!-- HTML форма з заповненими полями: title, description, host -->
</html>
```

- **Скріншот з Postman (або Swagger):**
![Адмін](docs/images/screenshots/adminedit.png)

#### 29. Оновити епізод (Admin)
- **URL:** `/admin/episodes/{episode_id}/edit`
- **Метод:** `POST`
- **Опис:** Оновлює епізод через адмін-панель
- **Вимагає:** Автентифікацію адміністратора
- **Параметри шляху:**
  - `episode_id` (int): ID епізоду
- **Формат:** `application/x-www-form-urlencoded`
- **Параметри:**
  - `title` (string): Назва епізоду
  - `description` (string): Опис епізоду
  - `host` (string): Ім'я хоста
- **Приклад запиту:**
```
POST /admin/episodes/1/edit
Content-Type: application/x-www-form-urlencoded
Cookie: admin_session=authenticated

title=Оновлена назва&description=Оновлений опис&host=Оновлений хост
```
- **Приклад відповіді:**
```
HTTP 303 See Other
Location: /admin/episodes
```

- **Скріншот з Postman (або Swagger):**
![Адмін](docs/images/screenshots/adminedit2.png)

#### 30. Видалити епізод (Admin)
- **URL:** `/admin/episodes/{episode_id}/delete`
- **Метод:** `DELETE`
- **Опис:** Видаляє епізод через адмін-панель
- **Вимагає:** Автентифікацію адміністратора
- **Параметри шляху:**
  - `episode_id` (int): ID епізоду
- **Приклад запиту:**
```
DELETE /admin/episodes/1/delete
Cookie: admin_session=authenticated
```
- **Приклад відповіді:**
```json
{
  "message": "Episode deleted successfully"
}
```

- **Скріншот з Postman (або Swagger):**
![Адмін](docs/images/screenshots/adminrss.png)

#### 31. Управління RSS фідами (Admin)
- **URL:** `/admin/rss`
- **Метод:** `GET`
- **Опис:** Повертає HTML сторінку зі списком RSS фідів
- **Вимагає:** Автентифікацію адміністратора
- **Приклад запиту:**
```
GET /admin/rss
Cookie: admin_session=authenticated
```
- **Приклад відповіді:**
```html
HTTP 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
  <!-- HTML сторінка зі списком RSS фідів -->
</html>
```

## Результати тестування в Postman (або Swagger)

### Тестовий сценарій 1: Отримання головної сторінки
- **Мета:** Перевірити доступність головної сторінки додатку
- **Результат:** ✅ Успішно
- **Скріншот:**
![Тест 1](docs/images/screenshots/test1.png)

### Тестовий сценарій 2: Отримання сторінки "Про проєкт"
- **Мета:** Перевірити відображення інформації про проєкт
- **Результат:** ✅ Успішно
- **Скріншот:**
![Тест 2](docs/images/screenshots/test2.png)

### Тестовий сценарій 3: Отримання списку всіх епізодів (HTML)
- **Мета:** Перевірити функціональність отримання списку епізодів з підтримкою пагінації
- **Результат:** ✅ Успішно
- **Скріншот:**
![Тест 3](docs/images/screenshots/test3.png)

### Тестовий сценарій 4: Отримання форми створення епізоду
- **Мета:** Перевірити відображення HTML форми для створення нового епізоду
- **Результат:** ✅ Успішно
- **Скріншот:**
![Тест 4](docs/images/screenshots/test4.png)

### Тестовий сценарій 5: Створення нового епізоду
- **Мета:** Перевірити можливість створення нового епізоду подкасту з усіма необхідними полями
- **Результат:** ✅ Успішно
- **Скріншот:**
![Тест 5](docs/images/screenshots/test5.png)

### Тестовий сценарій 6: Отримання форми генерації альтернативного контенту
- **Мета:** Перевірити відображення форми для генерації альтернативного контенту
- **Результат:** ✅ Успішно
- **Скріншот:**
![Тест 6](docs/images/screenshots/test6.png)

### Тестовий сценарій 7: Генерація альтернативної назви через LLM
- **Мета:** Перевірити роботу інтеграції з Groq LLM для генерації альтернативного контенту
- **Результат:** ✅ Успішно
- **Скріншот:**
![Тест 7](docs/images/screenshots/test7.png)

### Тестовий сценарій 8: Отримання списку епізодів через API (JSON)
- **Мета:** Перевірити отримання списку епізодів у форматі JSON з підтримкою пагінації
- **Результат:** ✅ Успішно
- **Скріншот:**
![Тест 8](docs/images/screenshots/test8.png)

### Тестовий сценарій 9: Створення епізоду через API
- **Мета:** Перевірити створення нового епізоду через REST API
- **Результат:** ✅ Успішно
- **Скріншот:**
![Тест 9](docs/images/screenshots/test9.png)

### Тестовий сценарій 10: Отримання епізоду за ID через API
- **Мета:** Перевірити отримання інформації про конкретний епізод за його ID
- **Результат:** ✅ Успішно
- **Скріншот:**
![Тест 10](docs/images/screenshots/test10.png)

### Тестовий сценарій 11: Перевірка існування епізоду (HEAD запит)
- **Мета:** Перевірити коректність роботи HEAD методу для перевірки існування епізоду
- **Результат:** ✅ Успішно
- **Скріншот:**
![Тест 11](docs/images/screenshots/test11.png)

### Тестовий сценарій 12: Повне оновлення епізоду через API (PUT)
- **Мета:** Перевірити повне оновлення всіх полів епізоду через PUT метод
- **Результат:** ✅ Успішно
- **Скріншот:**
![Тест 12](docs/images/screenshots/test12.png)

### Тестовий сценарій 13: Часткове оновлення епізоду через API (PATCH)
- **Мета:** Перевірити часткове оновлення окремих полів епізоду через PATCH метод
- **Результат:** ✅ Успішно
- **Скріншот:**
![Тест 13](docs/images/screenshots/test13.png)

### Тестовий сценарій 14: Видалення епізоду через API
- **Мета:** Перевірити коректність видалення епізоду за ID
- **Результат:** ✅ Успішно
- **Скріншот:**
![Тест 14](docs/images/screenshots/test14.png)

### Тестовий сценарій 15: Отримання RSS фідів (HTML)
- **Мета:** Перевірити парсинг та відображення RSS фідів з зовнішнього джерела
- **Результат:** ❌ Помилка
- **Скріншот:**
![Тест 15](docs/images/screenshots/test15.png)

### Тестовий сценарій 16: Перегляд конкретного RSS фіду
- **Мета:** Перевірити отримання детальної інформації про конкретний RSS фід
- **Результат:** ❌ Помилка
- **Скріншот:**
![Тест 16](docs/images/screenshots/test16.png)

### Тестовий сценарій 17: Додавання RSS фіду як епізоду
- **Мета:** Перевірити додавання RSS фіду до списку епізодів подкасту
- **Результат:** ❌ Помилка
- **Скріншот:**
![Тест 17](docs/images/screenshots/test17.png)

### Тестовий сценарій 18: Отримання RSS фідів через API (JSON)
- **Мета:** Перевірити отримання списку RSS фідів у форматі JSON
- **Результат:** ❌ Помилка
- **Скріншот:**
![Тест 18](docs/images/screenshots/test18.png)

### Тестовий сценарій 19: Отримання RSS фіду за UUID через API
- **Мета:** Перевірити отримання детальної інформації про RSS фід за UUID
- **Результат:** ❌ Помилка
- **Скріншот:**
![Тест 19](docs/images/screenshots/test19.png)

### Тестовий сценарій 20: Додавання RSS фіду як епізоду через API
- **Мета:** Перевірити додавання RSS фіду до списку епізодів через REST API
- **Результат:** ❌ Помилка
- **Скріншот:**
![Тест 20](docs/images/screenshots/test20.png)

### Тестовий сценарій 21: Отримання сторінки входу адміністратора
- **Мета:** Перевірити відображення форми входу для адміністратора
- **Результат:** ✅ Успішно
- **Скріншот:**
![Тест 21](docs/images/screenshots/test21.png)

### Тестовий сценарій 22: Автентифікація адміністратора
- **Мета:** Перевірити коректність автентифікації адміністратора з правильними обліковими даними
- **Результат:** ✅ Успішно
- **Скріншот:**
![Тест 22](docs/images/screenshots/test22.png)

### Тестовий сценарій 23: Вихід адміністратора
- **Мета:** Перевірити коректність виходу адміністратора з системи
- **Результат:** ✅ Успішно
- **Скріншот:**
![Тест 23](docs/images/screenshots/test23.png)

### Тестовий сценарій 24: Доступ до панелі управління
- **Мета:** Перевірити доступ до панелі управління без автентифікації
- **Результат:** ❌ Помилка
- **Скріншот:**
![Тест 24](docs/images/screenshots/test24.png)

### Тестовий сценарій 25: Управління епізодами через адмін-панель
- **Мета:** Перевірити відображення списку епізодів в адмін-панелі
- **Результат:** ✅ Успішно
- **Скріншот:**
![Тест 25](docs/images/screenshots/test25.png)

### Тестовий сценарій 26: Отримання форми додавання епізоду (Admin)
- **Мета:** Перевірити відображення форми додавання епізоду в адмін-панелі
- **Результат:** ✅ Успішно
- **Скріншот:**
![Тест 26](docs/images/screenshots/test26.png)

### Тестовий сценарій 27: Додавання епізоду через адмін-панель
- **Мета:** Перевірити створення нового епізоду через адмін-панель
- **Результат:** ✅ Успішно
- **Скріншот:**
![Тест 27](docs/images/screenshots/test27.png)

### Тестовий сценарій 28: Отримання форми редагування епізоду (Admin)
- **Мета:** Перевірити відображення форми редагування з заповненими даними
- **Результат:** ✅ Успішно
- **Скріншот:**
![Тест 28](docs/images/screenshots/test28.png)

### Тестовий сценарій 29: Оновлення епізоду через адмін-панель
- **Мета:** Перевірити оновлення існуючого епізоду через адмін-панель
- **Результат:** ✅ Успішно
- **Скріншот:**
![Тест 29](docs/images/screenshots/test29.png)

### Тестовий сценарій 30: Видалення епізоду через адмін-панель
- **Мета:** Перевірити видалення епізоду через адмін-панель
- **Результат:** ✅ Успішно
- **Скріншот:**
![Тест 30](docs/images/screenshots/test30.png)

### Тестовий сценарій 31: Управління RSS фідами через адмін-панель
- **Мета:** Перевірити відображення RSS фідів в адмін-панелі
- **Результат:** ✅ Успішно
- **Скріншот:**
![Тест 31](docs/images/screenshots/test31.png)

### Тестовий сценарій 32: Обробка помилок при відсутності епізоду
- **Мета:** Перевірити коректну обробку ситуації, коли епізод з вказаним ID не існує
- **Результат:** ❌ Помилка
- **Скріншот:**
![Тест 32](docs/images/screenshots/test32.png)

## Обробка помилок
Список реалізованих кодів помилок:
- `400 Bad Request` - Виникає при неправильному форматі запиту або валідації даних (FastAPI автоматично валідує дані через Pydantic/SQLModel)
- `401 Unauthorized` - Виникає при спробі доступу до адмін-панелі без автентифікації
- `404 Not Found` - Виникає коли епізод з вказаним ID не знайдено в базі даних (повертається HTML сторінка notFound.html)
- `422 Unprocessable Entity` - Виникає при невалідних даних у тілі запиту (FastAPI автоматично повертає цей код через валідацію Pydantic)
- `500 Internal Server Error` - Виникає при внутрішніх помилках сервера, проблемах з базою даних або при зверненні до зовнішніх API (Groq, RSS)

## Архітектура проєкту

```
podcast2/
├── src/app/              # Основний код додатку
│   ├── api/              # API роутери та залежності
│   │   └── routes/       # Маршрути для різних модулів
│   ├── core/             # Основна конфігурація та утиліти
│   │   ├── config.py     # Налаштування проєкту
│   │   ├── db/           # Підключення до бази даних
│   │   ├── models/       # SQLModel моделі
│   │   └── services/     # Сервіси (Groq, тощо)
│   ├── crud/             # CRUD операції
│   ├── static/           # Статичні файли (CSS, зображення)
│   ├── templates/        # Jinja2 шаблони
│   └── main.py           # Точка входу FastAPI
├── docs/                 # Документація
├── scripts/              # Скрипти для збірки та запуску
├── compose.yaml          # Docker Compose конфігурація
├── Dockerfile            # Docker образ для додатку
├── pyproject.toml         # Залежності проєкту
└── README.md             # Цей файл
```

## Ліцензія
Див. файл [LICENSE](LICENSE) для деталей.
