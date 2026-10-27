# FlaskIQ Test Foundation & CI Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Establish the foundational test suite using Pytest for `flaskiq` and set up an automated CI workflow on GitHub Actions.

**Architecture:**
1. Development dependencies managed via `requirements-dev.txt` (`-r requirements.txt` + `pytest`).
2. Test configuration in `pytest.ini` (`testpaths = tests`, `pythonpath = .`).
3. Isolated test fixtures in `tests/conftest.py`: in-memory SQLite database, clean application factory (`create_app("testing")`), and isolated HTTP client.
4. Modular test suite:
   - `tests/unit/`: `test_config.py`, `test_user_model.py`, `test_page_model.py`, `test_user_repository.py`, `test_page_repository.py`, `test_auth_service.py`.
   - `tests/routes/`: `test_app_factory.py`, `test_security_headers.py`, `test_error_handlers.py`, `test_landing_routes.py`, `test_auth_view_routes.py`, `test_cms_view_routes.py`.
5. GitHub Actions workflow `.github/workflows/ci.yml` matrix testing across Python 3.12 and 3.14 on `ubuntu-latest`.

**Tech Stack:** Flask, Flask-SQLAlchemy, Pytest, SQLite in-memory, GitHub Actions.

---

### Task 1: Setup Test Dependencies & Pytest Configuration

**Files:**
- Create: `requirements-dev.txt`
- Create: `pytest.ini`

- [ ] **Step 1: Create `requirements-dev.txt`**
  ```text
  -r requirements.txt
  pytest>=8.2.0
  ```

- [ ] **Step 2: Create `pytest.ini`**
  ```ini
  [pytest]
  testpaths = tests
  pythonpath = .
  ```

---

### Task 2: Create Test Fixtures (`tests/conftest.py`)

**Files:**
- Create: `tests/conftest.py`

- [ ] **Step 1: Implement `tests/conftest.py`**
  - Set test environment variables before importing app:
    ```python
    import os
    os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
    os.environ.setdefault("SECRET_KEY", "test-secret-key-for-testing-only")
    os.environ.setdefault("JWT_KEY", "test-jwt-secret-key-for-testing-only")
    os.environ.setdefault("WTF_CSRF_ENABLED", "False")
    ```
  - Define `app` fixture:
    ```python
    @pytest.fixture
    def app():
        from app import create_app, db
        application = create_app("testing")
        with application.app_context():
            db.create_all()
            yield application
            db.session.remove()
            db.drop_all()
    ```
  - Define `client` fixture:
    ```python
    @pytest.fixture
    def client(app):
        return app.test_client()
    ```
  - Define `db` fixture:
    ```python
    @pytest.fixture
    def db(app):
        from app import db as _db
        return _db
    ```

---

### Task 3: Implement Unit Tests (`tests/unit/`)

**Files:**
- Create: `tests/unit/test_config.py`
- Create: `tests/unit/test_user_model.py`
- Create: `tests/unit/test_page_model.py`
- Create: `tests/unit/test_user_repository.py`
- Create: `tests/unit/test_page_repository.py`
- Create: `tests/unit/test_auth_service.py`

- [ ] **Step 1: Write `test_config.py`**
  Test `TestingConfig` settings (`TESTING == True`, SQLite memory URI, environment variable fallbacks).

- [ ] **Step 2: Write `test_user_model.py` and `test_page_model.py`**
  Test `User.set_password()`, `check_password()`, column validations, and `Page` model defaults.

- [ ] **Step 3: Write `test_user_repository.py` and `test_page_repository.py`**
  Test CRUD operations in memory: `create()`, `get_by_email()`, `get_by_username()`, `update()`, `delete()`.

- [ ] **Step 4: Write `test_auth_service.py`**
  Test `AuthService.register()` (success, duplicate email error, duplicate username error), `AuthService.login()` (success, invalid password error), and JWT token decoding validation.

---

### Task 4: Implement Route & Foundation Tests (`tests/routes/`)

**Files:**
- Create: `tests/routes/test_app_factory.py`
- Create: `tests/routes/test_security_headers.py`
- Create: `tests/routes/test_error_handlers.py`
- Create: `tests/routes/test_landing_routes.py`
- Create: `tests/routes/test_auth_view_routes.py`
- Create: `tests/routes/test_cms_view_routes.py`

- [ ] **Step 1: Write `test_app_factory.py`**
  Ensure all expected blueprints (`landing_bp`, `auth_view_bp`, `cms_bp`, `api_v1_bp`) are registered on the Flask instance.

- [ ] **Step 2: Write `test_security_headers.py`**
  Assert responses include:
  - `X-Content-Type-Options: nosniff`
  - `X-Frame-Options: DENY`
  - `X-XSS-Protection: 1; mode=block`
  - `Referrer-Policy: strict-origin-when-cross-origin`

- [ ] **Step 3: Write `test_error_handlers.py`**
  Test 404 response on unknown routes and rate limit behavior where appropriate.

- [ ] **Step 4: Write view route tests (`landing`, `auth`, `cms`)**
  Test `GET /` (200 OK), `GET /login` (200 OK), `GET /cms` (200 OK).

- [ ] **Step 5: Verify tests locally**
  Run `pytest` under a clean virtualenv on Python 3.12 and 3.14. Ensure zero test failures and no SQLite files (`*.db`) left in the repo.

---

### Task 5: Implement CI Workflow (`.github/workflows/ci.yml`)

**Files:**
- Create: `.github/workflows/ci.yml`
- Modify: `README.md`

- [ ] **Step 1: Write `.github/workflows/ci.yml`**
  - Triggers: `pull_request`, `push: branches: [main]`, `workflow_dispatch`
  - Job `check`:
    - Matrix: `python-version: ["3.12", "3.14"]` on `ubuntu-latest`
    - Steps:
      - Checkout `actions/checkout@v4`
      - Setup Python `actions/setup-python@v5` with caching enabled for `pip`
      - Install dev requirements: `pip install -r requirements-dev.txt`
      - Quick import sanity check: `DATABASE_URL=sqlite:// python -c "import app"`
      - Run pytest: `pytest -v`
  - Job `ci-ok`:
    - `needs: [check]`, `if: always()`, checks `needs.check.result == 'success'`.

- [ ] **Step 2: Update README with Testing Section**
  Add instructions on how to install `requirements-dev.txt` and run `pytest`.

- [ ] **Step 3: Submit PR & Ruleset instructions**
  Commit, push, and open PR for review.
