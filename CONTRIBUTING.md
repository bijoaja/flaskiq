# Contributing to FlaskIQ

Thank you for your interest in contributing to FlaskIQ!

Please read the contribution guidelines in your preferred language:

- [English Contribution Guide](docs/en/CONTRIBUTING.md)
- [Panduan Kontribusi Bahasa Indonesia](docs/id/CONTRIBUTING.md)

## Quick Check

Before opening a pull request, run:

```bash
pytest -v
ruff check .
ruff format --check .
mypy .
bandit -q -r app utils config.py -c pyproject.toml
```
