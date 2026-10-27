# Test Structure — Design Spec (flaskiq)

Date: 2026-10-27
Status: Draft, awaiting approval (no implementation yet)

## 1. Background

flaskiq has no tests. There is no `tests/` folder, no pytest dependency, and no CI. Two things were
found while checking what a first test would need:

1. **The app cannot be imported on `main`.** `import app` fails with
   `ModuleNotFoundError: No module named 'app.service.auth_service'`. `app/service/__init__.py` still
   has `from .auth_service import AuthService` (and the same for `cms_service` and
   `landing_service`), but commit `fab7c28` moved those files into `app/service/view/`, and no
   `view/__init__.py` exists. Every other import in the repo already uses the `app.service.view...`
   path. Reproduced with `pip`-installed requirements on Python 3.12. Any test that imports `app`
   fails until this is fixed.
2. **Importing `app` has side effects.** `app/__init__.py` ends with `app = create_app()`, using the
   default config (`DevelopmentConfig`) and `SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL",
   "sqlite:///flaskiq.db")`. Importing it runs `db.create_all()` and, without `DATABASE_URL`, writes
   `instance/flaskiq.db` into the working directory.

With the import problem worked around in a throwaway copy and `DATABASE_URL=sqlite://`,
`create_app("testing")` works: `TestingConfig` sets `TESTING = True` and an in-memory SQLite URI, `GET /`
returns 200, an unknown URL returns 404 with `X-Frame-Options: DENY` and `X-Content-Type-Options: nosniff`.
Flask-Limiter prints a warning that it uses in-memory storage (harmless in tests).

## 2. Goals

- A `tests/` suite that protects the foundation of the template: configuration, the app factory,
  security headers, the 404 handler, the models, the repositories, the auth service, and the
  server-rendered routes.
- One test file per area, shared setup in `conftest.py`, so a reader finds the test for a module by name.
- Tests that run offline, without Postgres, Redis, or an AI service, and leave no files behind.

## 3. Non-goals and anti-goals

Non-goals: the AI features (`app/service/agent/*`, `chatbot_controller`, RAG tool, ollama/openai
clients), the JSON API controllers under `app/controller/api`, front-end templates and static files,
Docker, migrations, lint or coverage.

Anti-goals:
- Tests that pass only because they were written against a broken import (see section 4, decision 1).
- Tests that write `flaskiq.db` or any file into the repo, or that need a network.
- Weakening an assertion or skipping a test to get green.

## 4. Decisions

Made by the user:
- `tests/`, `pytest.ini`, `requirements-dev.txt` and `.github/workflows/ci.yml` are allowed to ship into projects created by `pyartisan new flask`, because that command clones the template unchanged. No exclusion mechanism is built in pyartisan; a user who does not want them deletes them.
- First stage covers the **foundation only**; AI services are not tested yet.
- Specs live in this repo's `docs/superpowers/specs/`.

My calls (the user can overrule any of them):
1. **Fix the import before writing tests**, in its own issue and PR, not hidden inside the test PR.
   Scope: change the three imports in `app/service/__init__.py` to `from .view.auth_service ...` etc.,
   and nothing else. `ChatbotService` stays exported; dropping it would not help, because `import app`
   loads the agent stack anyway through `app/routes/api/v1/__init__.py` → `chatbot_controller` →
   `app.service.agent.chatbot_service`. No `app/service/view/__init__.py` is added: the `service`
   generator creates it on first use (observed: `make service Post` created it), and a package
   without it imports fine.
2. Test dependencies go in a new `requirements-dev.txt` containing `-r requirements.txt` and `pytest`,
   not in `requirements.txt`, because `requirements.txt` is what generated projects install.
3. Tests set `DATABASE_URL=sqlite://` (and `SECRET_KEY`, `JWT_KEY` to fixed test values) in
   `conftest.py` **before** anything imports `app`, so the module-level `create_app()` never touches a file.
4. Tests build their own app with `create_app("testing")` instead of using the module-level `app`.
5. If the tests find a real bug in `app/`, it gets its own issue and PR first. A test is never
   skipped, xfailed or weakened to get green; the test PR waits for that fix.

## 5. Layout

```
tests/
  conftest.py
  unit/
    test_config.py
    test_user_model.py
    test_page_model.py
    test_user_repository.py
    test_page_repository.py
    test_auth_service.py
  routes/
    test_app_factory.py
    test_security_headers.py
    test_error_handlers.py
    test_landing_routes.py
    test_auth_view_routes.py
    test_cms_view_routes.py
```

What each file covers (scope is the foundation list; the builder checks the code for the exact cases):

| File | Covers |
|---|---|
| `unit/test_config.py` | `config` dict keys, `TestingConfig` (`TESTING`, in-memory URI), env overrides for `SECRET_KEY`, `JWT_KEY`, `JWT_EXPIRY_MINUTES` |
| `unit/test_user_model.py` | `User.set_password` / `check_password`, unique constraints |
| `unit/test_page_model.py` | `Page` columns and defaults (`app/model/page.py`) |
| `unit/test_user_repository.py`, `unit/test_page_repository.py` | repository methods in `app/repository/` against the in-memory DB |
| `unit/test_auth_service.py` | `AuthService.register` (duplicate email, duplicate username), `login` (wrong password), `_generate_token` payload and expiry |
| `routes/test_app_factory.py` | `create_app("testing")` returns an app with the four blueprints registered |
| `routes/test_security_headers.py` | the four headers set in `add_security_headers` |
| `routes/test_error_handlers.py` | 404 renders `404.html`; 429 handler shape if it can be triggered cheaply |
| `routes/test_landing_routes.py`, `test_auth_view_routes.py`, `test_cms_view_routes.py` | status codes and redirects of the view routes in `app/routes/view/` |

## 6. Shared fixtures (`tests/conftest.py`)

| Fixture | Behavior |
|---|---|
| (module top) | set `DATABASE_URL`, `SECRET_KEY`, `JWT_KEY` with `os.environ.setdefault` before any `import app` |
| `app` | `create_app("testing")`; yields the app inside `app.app_context()` |
| `client` | `app.test_client()` |
| `db` | the `app.db` object; creates all tables before each test and drops them after, so tests do not share rows |

CSRF: `csrf.init_app(app)` is active, and form POSTs need a token or `WTF_CSRF_ENABLED = False` in
the test config. Choose one and note it; the API blueprint is already exempt.

## 7. Config

- `requirements-dev.txt`: `-r requirements.txt` and `pytest` (pin the version when adding it).
- `pytest.ini`: `testpaths = tests`, and `pythonpath = .` so `import app` and `import config` resolve from the repo root.
- Commands: `pip install -r requirements-dev.txt` then `pytest`. The README gets a short "Running tests" section.

## 8. Order of work

1. Issue and PR: fix `app/service/__init__.py` so `import app` works. Accept when `python -c "import app"` succeeds with `DATABASE_URL=sqlite://` and creates no file.
2. PR: add `requirements-dev.txt`, `pytest.ini`, `tests/`, README section.
3. CI spec (`2026-10-27-ci-design.md`) is implemented after step 2.

## 9. Acceptance

- `pytest` passes on a clean checkout with Python 3.12 and 3.14, offline, and `git status` is clean afterwards (no `.db`, no `instance/`).
- Each file in section 5 exists and has at least one test; deleting `auth_service.py`'s duplicate-email check makes a test fail (spot check at least one such mutation).
- No test file imports or exercises `app.service.agent` directly, and none touches the network. (`import app` still loads that package indirectly, so its dependencies must be installed.)

## 10. Risks and unverified

- Only the factory, the 404 handler, headers, and `GET /` were exercised by hand. The models, repositories, auth service and view routes have not been run; their behavior in section 5 is read from the code, not observed.
- Python 3.14 was verified only for installing requirements and importing `flask`, `flask_sqlalchemy`, `flask_migrate`, `psycopg2`. The full test suite has never run on 3.14.
- Whether other stale imports exist beyond `app/service/__init__.py` is unknown until the full import and tests run.

## 11. Left to the builder

Fixture bodies, individual test cases, the exact CSRF approach, and whether a failing 429 test is worth keeping.
