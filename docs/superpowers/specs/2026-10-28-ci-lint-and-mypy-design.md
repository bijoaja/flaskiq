# CI Enhancement (Linting & Formatting) and Mypy Type Checking — Design Spec (flaskiq)

Date: 2026-10-28
Status: Draft, awaiting approval (no implementation yet)

## 1. Background

FlaskIQ now has a foundational test suite (unit tests and route tests) and an automated CI workflow on GitHub Actions verifying Python 3.12 and 3.14.

However:
- **No linter or code formatter** is active. Inconsistencies in code style, unused imports, duplicate variable names, or unformatted files can be committed and merged unnoticed.
- **No static type checking** is performed. Flask and Flask-SQLAlchemy applications benefit significantly from static typing in models, services, repositories, and utility classes to prevent runtime `AttributeError` and `TypeError`.
- The CI workflow currently sets `cancel-in-progress: true` unconditionally. Pushes to `main` should always run to completion to verify post-merge health.

A reference CI workflow provided from an external project demonstrates:
1. Concurrency configured to cancel obsolete runs only for pull requests:
   `cancel-in-progress: ${{ github.event_name == 'pull_request' }}`.
2. A fast, dedicated `lint` job running on `ubuntu-latest`:
   `ruff check .`, `ruff format --check .`, and `mypy`.
3. An aggregate status check (`ci-ok`) that requires the `lint` job to pass alongside test execution.

## 2. Goals

- Add Ruff for linting and code formatting (`ruff check` and `ruff format`).
- Add Mypy for static type checking across `app/`, `utils/`, `config.py`, and `tests/`.
- Enhance the GitHub Actions CI workflow with:
  - PR-only run cancellation (`cancel-in-progress: ${{ github.event_name == 'pull_request' }}` loyalty).
  - A dedicated `lint` job running Ruff and Mypy on `ubuntu-latest`.
  - Integration of `lint` into the `ci-ok` required check.
- Document local developer commands in `README.md`.

## 3. Non-goals and Anti-goals

Non-goals:
- Enforcing full static typing on experimental/AI agent code (`app/service/agent/*`) on day one; these modules interface with dynamic LLM wrappers (LangChain, OpenAI, Ollama) and will be typed in a later phase.
- Switching FlaskIQ from `requirements.txt` to `pyproject.toml` packaging (FlaskIQ is a template and maintains standard pip requirements).

Anti-goals:
- Overusing blanket `# type: ignore` without specific error codes.
- Adding linters that drastically slow down CI; Ruff and Mypy provide fast feedback.
- Enabling formatting checks in CI before formatting the existing codebase.

## 4. Linting & Formatting Specification (Ruff)

### 4.1 Tool Selection
[Ruff](https://docs.astral.sh/ruff/) will be added to `requirements-dev.txt`:
- `ruff>=0.4.0`

### 4.2 Configuration
Ruff can read configuration from a standalone `pyproject.toml` or `ruff.toml`. A clean `pyproject.toml` is recommended to house tool configurations for Ruff and Mypy:

```toml
[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # Pyflakes
    "I",    # isort (import sorting)
    "B",    # flake8-bugbear
    "UP",   # pyupgrade
]
ignore = [
    "E501", # line too long (handled by formatter)
]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

### 4.3 Baseline Formatting Step
All existing files in `app/`, `utils/`, `config.py`, `server.py`, and `tests/` will be formatted with `ruff format .` and autofixed with `ruff check --fix .`.

## 5. Type Checking Specification (Mypy)

### 5.1 Architecture & Strategy
FlaskIQ follows a 5-layer architecture:
`HTTP Request → Routes → Controller → Service → Repository → Model`

A **gradual typing strategy** is applied:
1. **Layer 1 (Config & Utils):** `config.py` and `utils/` are fully typed (`Response`, `Middleware`, `TenantRateLimiter`).
2. **Layer 2 (Models & Repositories):** `app/model/` and `app/repository/` define clear return types (e.g. `User | None`, `list[Page]`).
3. **Layer 3 (Services & Routes):** `app/service/view/` and `app/routes/view/` use typed parameters and returns.
4. **Agent Modules Exemption:** `app/service/agent/*` is exempted from strict checking via module overrides.

### 5.2 Dependencies & Stubs
Added to `requirements-dev.txt`:
- `mypy>=1.10.0`
- `types-Flask`
- `types-requests`
- `types-PyYAML`
- `types-Werkzeug`

### 5.3 Mypy Configuration
In `pyproject.toml`:

```toml
[tool.mypy]
python_version = "3.12"
warn_unused_configs = true
warn_redundant_casts = true
warn_unused_ignores = true
check_untyped_defs = true
disallow_untyped_defs = false

# Modules targeted for strict typing:
[[tool.mypy.overrides]]
module = [
    "config",
    "utils.*",
    "app.model.*",
    "app.repository.*",
    "app.service.view.*",
]
disallow_untyped_defs = true

# AI agent modules with heavy dynamic imports (LangChain/Ollama/OpenAI):
[[tool.mypy.overrides]]
module = [
    "app.service.agent.*",
    "langchain.*",
    "langchain_openai.*",
    "openai.*",
    "flask_limiter.*",
    "flask_cors.*",
    "flask_wtf.*",
    "flask_restful.*",
    "flask_swagger_ui.*",
    "pymysql.*",
]
ignore_missing_imports = true
```

## 6. CI Workflow Updates (`.github/workflows/ci.yml`)

### 6.1 Concurrency Adjustment
Update concurrency in `.github/workflows/ci.yml`:

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: ${{ github.event_name == 'pull_request' }}
```

### 6.2 New `lint` Job
Add a dedicated `lint` job:

```yaml
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python 3.12
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
          cache-dependency-path: "requirements*.txt"

      - name: Install lint dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements-dev.txt

      - name: Ruff Check
        run: ruff check .

      - name: Ruff Format Check
        run: ruff format --check .

      - name: Mypy Type Check
        run: mypy .
```

### 6.3 Update `ci-ok`
Add `lint` to `needs`:

```yaml
  ci-ok:
    runs-on: ubuntu-latest
    needs: [lint, check]
    if: always()
    steps:
      - name: Verify check status
        run: |
          if [ "${{ needs.lint.result }}" != "success" ] || [ "${{ needs.check.result }}" != "success" ]; then
            echo "CI checks failed: lint=${{ needs.lint.result }}, check=${{ needs.check.result }}"
            exit 1
          fi
          echo "all checks passed"
```

## 7. Developer Workflow

Developers can run linting and type checking locally:
```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run linter
ruff check .

# Fix auto-fixable issues
ruff check --fix .

# Check code formatting
ruff format --check .

# Auto-format code
ruff format .

# Static type check
mypy .
```

## 8. Acceptance Criteria

1. `ruff check .` passes locally with 0 errors.
2. `ruff format --check .` passes locally with 0 modifications.
3. `mypy .` passes locally with 0 errors.
4. `.github/workflows/ci.yml` contains `lint` job and updated concurrency setting.
5. In GitHub Actions CI, `lint` job runs and passes.
6. `ci-ok` gates merge on `lint` succeeding.
