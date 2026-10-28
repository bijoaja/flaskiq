# FlaskIQ CI Linting & Formatting Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement Ruff linting and formatting in `flaskiq`, format the existing codebase cleanly, and add a dedicated `lint` job with PR-specific concurrency to the GitHub Actions CI workflow.

**Architecture:**
1. Add `ruff>=0.4.0` to `requirements-dev.txt`.
2. Configure Ruff in `pyproject.toml` (`line-length = 100`, `target-version = "py312"`, select `E, W, F, I, B, UP`).
3. Format existing files (`app/`, `utils/`, `config.py`, `server.py`, `tests/`) using Ruff.
4. Update `.github/workflows/ci.yml`:
   - Set concurrency to `cancel-in-progress: ${{ github.event_name == 'pull_request' }}`.
   - Add a fast `lint` job on `ubuntu-latest` running `ruff check .` and `ruff format --check .`.
   - Update `ci-ok` to require `lint` and `check`.
5. Update `README.md` with developer commands.

**Tech Stack:** Python 3.12+, pip, Ruff, GitHub Actions.

---

### Task 1: Add Ruff & Configure in `pyproject.toml`

**Files:**
- Modify: `requirements-dev.txt`
- Create: `pyproject.toml`

- [ ] **Step 1: Add Ruff to `requirements-dev.txt`**
  ```text
  -r requirements.txt
  pytest>=8.2.0
  ruff>=0.4.0
  ```

- [ ] **Step 2: Create `pyproject.toml` with Ruff configuration**
  ```toml
  [tool.ruff]
  line-length = 100
  target-version = "py312"

  [tool.ruff.lint]
  select = ["E", "W", "F", "I", "B", "UP"]
  ignore = ["E501"]

  [tool.ruff.format]
  quote-style = "double"
  indent-style = "space"
  ```

---

### Task 2: Format and Clean Codebase

**Files:**
- Modify: `app/**/*.py`, `utils/**/*.py`, `config.py`, `server.py`, `tests/**/*.py`

- [ ] **Step 1: Run autofix and formatter**
  Run:
  ```bash
  ruff check --fix .
  ruff format .
  ```

- [ ] **Step 2: Verify zero lint and formatting errors**
  Run:
  ```bash
  ruff check .
  ruff format --check .
  ```
  Ensure both exit with 0.

- [ ] **Step 3: Run existing tests to verify no regressions**
  Run:
  ```bash
  pytest -v
  ```
  Ensure all tests pass.

---

### Task 3: Update CI Workflow (`.github/workflows/ci.yml`)

**Files:**
- Modify: `.github/workflows/ci.yml`

- [ ] **Step 1: Update concurrency and add `lint` job**
  Update concurrency:
  ```yaml
  concurrency:
    group: ${{ github.workflow }}-${{ github.ref }}
    cancel-in-progress: ${{ github.event_name == 'pull_request' }}
  ```
  Add job `lint`:
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

        - name: Install dependencies
          run: |
            python -m pip install --upgrade pip
            pip install -r requirements-dev.txt

        - name: Ruff Check
          run: ruff check .

        - name: Ruff Format Check
          run: ruff format --check .
  ```
  Update `ci-ok`:
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

- [ ] **Step 2: Validate workflow syntax**
  Verify YAML with `python -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml'))"`.

---

### Task 4: Documentation & PR Submission

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Update `README.md`**
  Add `ruff check .` and `ruff format .` instructions.

- [ ] **Step 2: Commit, push, and open PR**
  - Branch: `feat/ci-lint`
  - Commit message: `feat: add Ruff linting and formatting to CI workflow`
  - Author only `bijoaja` (NO co-author).
  - Open PR to `main`.
