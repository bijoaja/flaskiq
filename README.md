# FlaskIQ

FlaskIQ is a production-ready Flask project template designed to accelerate the development of Python-based web applications in an efficient and well-structured way. Built with a strict layered architecture, it provides a solid foundation for a wide range of applications, including information systems, backend APIs, and analytical dashboards.

The template comes equipped with essential features such as JWT authentication, a built-in CMS, a streaming AI chatbot, and a REST API complete with Swagger documentation. With Docker support and a clean, organized structure, FlaskIQ enables developers to focus on business logic without being burdened by repetitive initial setup.


---

## Features

- **Layered architecture** — Routes → Controller → Service → Repository → Model
- **JWT authentication** — register, login, protected endpoints
- **CMS** — create, read, update, delete content pages via API and browser
- **Streaming AI chatbot** — multi-provider (Ollama local or OpenAI via LangChain)
- **REST API** — Flask-RESTful with full Swagger UI documentation
- **Tailwind CSS** — via CDN, no build step required
- **Docker** — separate dev (bind-mount) and prod (multi-stage, Gunicorn) images
- **Security** — CSRF protection, rate limiting, security headers
- **Clean code** — OOP, service layer, repository pattern, no business logic in controllers

---

## Tech Stack

| Layer          | Technology                                          |
|----------------|-----------------------------------------------------|
| Framework      | Flask 3.1, Flask-RESTful                            |
| Database       | SQLAlchemy + Flask-Migrate (SQLite dev / MySQL / Postgres prod)|
| Auth           | PyJWT, Flask-WTF (CSRF)                             |
| Rate limiting  | Flask-Limiter (tenant-aware)                        |
| AI / LLM       | Ollama (local) or OpenAI via LangChain              |
| Frontend       | Tailwind CSS (Play CDN), Bootstrap Icons            |
| API docs       | Swagger UI (flask-swagger-ui)                       |
| Deployment     | Docker, Gunicorn, Makefile                          |

---

## Project Structure

```
flaskiq/
├── app/
│   ├── __init__.py                  # App factory (CSRF, security headers, blueprints)
│   ├── routes/                      # URL-to-controller mapping (blueprints)
│   │   ├── view/                    # View blueprints (Jinja HTML templates)
│   │   │   ├── landing.py
│   │   │   ├── auth.py
│   │   │   └── cms.py
│   │   ├── api/v1/                  # API routes (Flask-RESTful resources)
│   │   │   └── __init__.py
│   │   └── __init__.py
│   ├── controller/                  # Request parsing + response formatting
│   │   ├── view/                    # View controllers
│   │   │   ├── landing/
│   │   │   ├── auth/
│   │   │   └── cms/
│   │   └── api/v1/                  # API controllers (auth, chatbot, cms, docs)
│   ├── service/                     # Business logic layer
│   │   ├── view/                    # View services
│   │   │   ├── auth_service.py
│   │   │   ├── cms_service.py
│   │   │   └── landing_service.py
│   │   └── agent/                   # Multi-provider chatbot
│   │       ├── chatbot_service.py   # Provider dispatch (AI_PROVIDER env var)
│   │       ├── ollama/              # Local Ollama agent
│   │       ├── openai/              # OpenAI via LangChain
│   │       └── tools/
│   │           └── rag_tool.py      # Loads README.md as system prompt
│   ├── repository/                  # Data access (only layer using db.session)
│   │   ├── base_repository.py
│   │   ├── user_repository.py
│   │   └── page_repository.py
│   ├── model/                       # SQLAlchemy models
│   │   ├── user.py
│   │   └── page.py
│   ├── templates/                   # Jinja2 + Tailwind
│   │   ├── base.html
│   │   ├── partials/                # navbar, footer, chatbot modal
│   │   ├── landing/
│   │   ├── auth/
│   │   └── cms/
│   └── static/
│       ├── css/app.css
│       ├── js/chatbot.js
│       └── swagger.yaml
├── Docker/
│   ├── Dockerfile.dev               # Bind-mount, Flask dev server
│   └── Dockerfile.prod              # Multi-stage, Gunicorn, non-root user
├── docs/                            # Project documentation
│   ├── index.md
│   ├── architecture.md
│   ├── api.md
│   ├── auth.md
│   ├── agent.md
│   └── docker.md
├── utils/                           # Shared utilities
│   ├── response.py                  # Response class (JSON + streaming)
│   ├── middleware.py                # JWT token_required decorator
│   ├── limiter.py                   # Tenant-aware rate limiter
│   └── profiler.py                  # Request duration logging
├── config.py
├── server.py
├── requirements.txt
├── Makefile
├── docker-compose.yml               # Dev (bind-mount + Ollama)
├── docker-compose.prod.yml          # Prod (no bind-mount, MySQL/Postgres)
└── .env.example
```

---

## Quick Start

### Docker (recommended)

```bash
# 1. Clone the repo
git clone https://github.com/bijoaja/flaskiq.git
cd flaskiq

# 2. Configure environment
cp .env.example .env
# Edit .env — set SECRET_KEY, JWT_KEY, and AI_PROVIDER at minimum

# 3. Start dev server
make dev

# 4. Set up the database (first run only)
make db-setup

# 5. Open the app
open http://localhost:8080
open http://localhost:8080/api/v1/docs   # Swagger UI
```

### Virtual Environment (without Docker)

```bash
python -m venv venv
source venv/bin/activate          # Linux/Mac
# source venv/Scripts/activate    # Windows

pip install -r requirements.txt
cp .env.example .env              # edit values

flask db upgrade
python server.py
```

### Running Tests

Install development dependencies and run tests:

```bash
pip install -r requirements-dev.txt
pytest -v
```

Continuous integration runs automatically on every pull request and push to `main` across Python 3.12 and 3.14.

---

## Make Targets

| Command              | Description                                  |
|----------------------|----------------------------------------------|
| `make dev`           | Start dev server (Docker, bind-mount)        |
| `make stop`          | Stop dev containers                          |
| `make logs`          | Tail dev server logs                         |
| `make shell`         | Open shell inside the web container          |
| `make db-setup`      | Init + migrate + upgrade database            |
| `make db-migrate`    | Create a new migration                       |
| `make db-upgrade`    | Apply pending migrations                     |
| `make prod`          | Start production server (Gunicorn)           |
| `make prod-stop`     | Stop production containers                   |
| `make build-prod`    | Build production Docker image                |
| `make push`          | Push image to Docker Hub                     |
| `make all`           | build-prod + tag + push + git commit         |

---

## API Endpoints

| Method   | Path                        | Auth | Description               |
|----------|-----------------------------|------|---------------------------|
| `GET`    | `/api/v1/`                  |      | Welcome message           |
| `POST`   | `/api/v1/auth/register`     |      | Register a new user       |
| `POST`   | `/api/v1/auth/login`        |      | Login and receive JWT     |
| `POST`   | `/api/v1/chatbot`           |      | Streaming AI chatbot      |
| `GET`    | `/api/v1/cms`               |      | List CMS pages            |
| `POST`   | `/api/v1/cms`               | JWT  | Create a page             |
| `GET`    | `/api/v1/cms/<id>`          |      | Get page by ID            |
| `PUT`    | `/api/v1/cms/<id>`          | JWT  | Update a page             |
| `DELETE` | `/api/v1/cms/<id>`          | JWT  | Delete a page             |
| `GET`    | `/api/v1/docs`              |      | Swagger UI                |

Full interactive documentation: `http://localhost:8080/api/v1/docs`

---

## Environment Variables

```bash
# Flask
FLASK_APP=server.py
FLASK_ENV=development
FLASK_RUN_PORT=8080

# Database (SQLite default, MySQL, PostgreSQL for prod)
DATABASE_URL=sqlite:///flaskiq.db

# Security
SECRET_KEY=change-me-in-production
JWT_KEY=change-me-jwt-secret
JWT_EXPIRY_MINUTES=60

# AI provider: "ollama" (local) or "openai"
AI_PROVIDER=ollama
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=mistral

# OpenAI (when AI_PROVIDER=openai)
AI_KEY=sk-YOUR_OPENAI_KEY
OPENAI_MODEL=gpt-4o-mini
```

---

## Architecture

```
HTTP Request
     │
     ▼
  Routes          URL mapping — blueprints only
     │
     ▼
  Controller      Request parsing + response formatting — no business logic
     │
     ▼
  Service         Business logic — raises ValueError on domain errors
     │
     ▼
  Repository      Data access — the only layer calling db.session
     │
     ▼
  Model           SQLAlchemy ORM + to_dict() serialisation
```

See [docs/architecture.md](docs/architecture.md) for the full diagram.

---

## AI Chatbot

Switch providers by setting `AI_PROVIDER` in `.env`:

- `AI_PROVIDER=ollama` — uses a local [Ollama](https://ollama.com) server (included in dev Docker compose)
- `AI_PROVIDER=openai` — uses OpenAI API via LangChain streaming

Adding a new provider: implement `BaseAgent` in `app/service/agent/<name>/`, add one branch to `ChatbotService`. See [docs/agent.md](docs/agent.md).

---

## Requirements

- Python 3.12+
- Docker & Docker Compose (for `make dev` / `make prod`)
- Ollama (optional, for local AI — included in dev compose)

---

## Contributing

Developed by [@bijoaja](https://github.com/bijoaja).  
Issues and pull requests are welcome.

## Contact

[joelbinsar@gmail.com](mailto:joelbinsar@gmail.com)
