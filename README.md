# FlaskIQ

FlaskIQ is a structured Flask project template built with a strict layered architecture (`Routes → Controller → Service → Repository → Model`). It includes JWT auth, a lightweight CMS, streaming AI chatbot, Swagger UI, and Docker setup.

---

## Documentation

- **English**: [docs/en/index.md](docs/en/index.md)
- **Bahasa Indonesia**: [docs/id/index.md](docs/id/index.md)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)

---

## Quick Start

### Docker (Recommended)

```bash
cp .env.example .env
make dev         # Start dev server at http://localhost:8080
make db-setup    # Run initial migrations
```

### Local Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python server.py
```

Swagger UI documentation is available at `http://localhost:8080/api/v1/docs`.

---

## Testing & Quality Gates

Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

Run test suite:
```bash
pytest -v
```

Lint and format code:
```bash
ruff check .
ruff format --check .
```

Run static type checking (Mypy):
```bash
mypy .
```

Run security scanners (Bandit & pip-audit):
```bash
bandit -q -r app utils config.py -c pyproject.toml
pip-audit -r requirements.txt
```

---

## License & Author

Developed by [@bijoaja](https://github.com/bijoaja). Distributed under the MIT License.
