# Examples

### **Level 1: Podcast Episode CRUD**

**GOAL:**

Build a FastAPI backend with endpoints to manage a list of podcast episodes in memory DB or any other DB (SQLite, Postgre, Dynamo, doesn't matter).

**Endpoints:**

- **POST**: /api/v1/podcast/episodes: Add a podcast episode to the list.

![post-podcast-episodes](images/post-podcast-episodes.png)

- **GET**: /api/v1/podcast/episodes: Return a list of all podcast episodes.

![get-podcast-episodes-not-found](images/get-podcast-episodes-not-found.png)

![get-podcast-episodes](images/get-podcast-episodes.png)

### **Level 2: LLM Alternative Title/Description Generation**

**GOAL:**

Add an endpoint that takes an existing podcast episode (by ID) and uses a free LLM API to generate an alternative version of its title or description (for example, to target a different audience, change the style, or summarize).

**Endpoints:**

- **POST**: /api/v1/podcast/{episode_id}/generate_alternative

![post-podcast-episodes-id-generate_alternative](images/post-podcast-episodes-id-generate_alternative.png)

### **Level 3: Telegram Bot Integration**

**GOAL**

Create a Telegram bot that connects to your backend and generates alternative podcast episode titles or descriptions on request.

**Endpoints:**

- **/alt**: /alt 1 title Rewrite the title for GenZ.

![alt-command-bot](images/alt-command-bot.png)

### **Level 4: Webhook Endpoint**

**GOAL:**

Expose a webhook endpoint for adding external podcast episodes.

**Endpoints:**

- **POST**: /api/v1/webhook/event

![post-webhook-episodes-event.png](images/post-webhook-episodes-event.png)

![post-webhook-episodes-telegram.png](images/post-webhook-episodes-event-telegram.png)

### **Level 5: RSS Feed Integration**

**GOAL:**

Fetch and serve latest podcast episodes from a public RSS feed.

**Endpoints:**

- **GET**: /api/v1/rss/fetch

![get-rss-fetch](images/get-rss-fetch.png)

- **POST**: /api/v1/rss/post

![post-rss-post](images/post-rss-post.png)

![post-rss-post](images/post-rss-post-not-found.png)

