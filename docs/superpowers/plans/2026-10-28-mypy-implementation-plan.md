# FlaskIQ Mypy Type Checking Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement static type checking with Mypy in `flaskiq`, add type annotations to foundational architecture layers (`config.py`, `utils/`, `app/model/`, `app/repository/`, `app/service/view/`), and add Mypy verification to the CI workflow.

**Architecture:**
1. Add `mypy>=1.10.0` and type stubs (`types-Flask`, `types-requests`, `types-PyYAML`, `types-Werkzeug`) to `requirements-dev.txt`.
2. Configure `[tool.mypy]` in `pyproject.toml` with gradual typing overrides (exempting dynamic AI agent modules `app/service/agent/*`).
3. Add type annotations and resolve Mypy errors across target layers.
4. Integrate `mypy .` into the `lint` job in `.github/workflows/ci.yml`.
5. Update `README.md` with developer commands.

**Tech Stack:** Python 3.12+, pip, Mypy, Flask, Flask-SQLAlchemy.

---

### Task 1: Add Mypy Dependencies & Configuration

**Files:**
- Modify: `requirements-dev.txt`
- Modify: `pyproject.toml`

- [ ] **Step 1: Add Mypy and stubs to `requirements-dev.txt`**
  ```text
  mypy>=1.10.0
  types-Flask
  types-requests
  types-PyYAML
  types-Werkzeug
  ```

- [ ] **Step 2: Add `[tool.mypy]` configuration to `pyproject.toml`**
  ```toml
  [tool.mypy]
  python_version = "3.12"
  warn_unused_configs = true
  warn_redundant_casts = true
  warn_unused_ignores = true
  check_untyped_defs = true
  disallow_untyped_defs = false

  [[tool.mypy.overrides]]
  module = [
      "config",
      "utils.*",
      "app.model.*",
      "app.repository.*",
      "app.service.view.*",
  ]
  disallow_untyped_defs = true

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

---

### Task 2: Add Type Annotations & Resolve Mypy Errors

**Files:**
- Modify: `config.py`
- Modify: `utils/**/*.py`
- Modify: `app/model/**/*.py`
- Modify: `app/repository/**/*.py`
- Modify: `app/service/view/**/*.py`

- [ ] **Step 1: Type `config.py` and `utils/`**
  Add explicit type hints to methods in `Response`, `Middleware`, `Profiler`, and `TenantRateLimiter`.

- [ ] **Step 2: Type `app/model/` and `app/repository/`**
  Add type annotations to model attributes and repository CRUD method parameters and return types (e.g. `User | None`, `list[Page]`).

- [ ] **Step 3: Type `app/service/view/`**
  Add type hints to `AuthService`, `CmsService`, and `LandingService`.

- [ ] **Step 4: Run Mypy locally**
  Run:
  ```bash
  mypy .
  ```
  Ensure 0 errors in target modules.

- [ ] **Step 5: Run pytest to verify no regressions**
  Run:
  ```bash
  pytest -v
  ```
  Ensure all tests pass.

---

### Task 3: Integrate Mypy into CI Workflow

**Files:**
- Modify: `.github/workflows/ci.yml`

- [ ] **Step 1: Add Mypy step to `lint` job**
  In `.github/workflows/ci.yml`, add to `lint` job:
  ```yaml
        - name: Mypy Type Check
          run: mypy .
  ```

---

### Task 4: Documentation & PR Submission

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Document Mypy command in `README.md`**
  Add `mypy .` instructions.

- [ ] **Step 2: Commit, push, and open PR**
  - Branch: `feat/mypy-type-checking`
  - Commit message: `feat: add Mypy static type checking for foundational architecture`
  - Author only `bijoaja` (NO co-author).
  - Open PR to `main`.
