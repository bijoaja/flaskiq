# Contributing to FlaskIQ

We welcome issues and pull requests to improve FlaskIQ.

## Development Setup

```bash
# Set up Python virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements-dev.txt
```

## Quality Assurance & Verification

Before submitting changes, ensure all verification tools pass:

### 1. Test Suite
```bash
pytest -v
```

### 2. Linting & Formatting (Ruff)
```bash
ruff check .
ruff format --check .
```

### 3. Static Type Checking (Mypy)
```bash
mypy .
```

### 4. Security Scanning (Bandit & pip-audit)
```bash
bandit -q -r app utils config.py -c pyproject.toml
pip-audit -r requirements.txt
```

## Contribution Workflow

1. Create a feature branch: `git checkout -b feat/your-feature-name`
2. Follow layered architecture standards (Routes → Controller → Service → Repository → Model).
3. Add tests for new behavior.
4. Ensure all linters, type checks, and security scanners pass.
5. Open a pull request against `main`.
