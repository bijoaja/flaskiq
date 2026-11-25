# flaskiq analyze + serve_uv Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Manifest flaskiq mendeklarasikan `scripts.analyze` dan `scripts.serve_uv` supaya `pyartisan analyze` dan `pyartisan serve --uv` jalan.

**Architecture:** Hanya edit `.pyartisan/manifest.yaml`. Engine ada di repo pyartisan (plan `2026-11-25-doctor-serve-analyze.md`, harus selesai dulu).

**Tech Stack:** YAML manifest, ruff, bandit, mypy, uv.

**Spec:** `docs/superpowers/specs/2026-11-25-manifest-check-serve-design.md` (akan di-rename ke `...-analyze-serve-design.md`).

## Global Constraints
- Perintah `analyze` identik dengan job `lint` di `.github/workflows/ci.yml`: `ruff check .`, `ruff format --check .`, `bandit -q -r app utils config.py -c pyproject.toml`, `mypy .`.
- `serve_uv`: `uv run --no-project --with-requirements requirements.txt python server.py` (`pyproject.toml` tanpa `[project]`).
- Key `scripts.serve` tidak diubah (`python3 server.py`). Generator `make` tidak boleh berubah.
- Tanpa baris atribusi di commit (author bijoaja).

## Review Focus
- Manifest tetap valid YAML dan lolos `load_manifest` (`id`, `framework` ada).
- `pyartisan make controller x` tetap jalan setelah edit (regresi).
- Pyartisan lama mengabaikan key baru, tidak error.
- Langkah `fix` ruff: `--fix` tidak mengubah langkah `bandit`/`mypy`.

---

### Task 1: Manifest `scripts.analyze` dan `serve_uv`

**Files:**
- Modify: `.pyartisan/manifest.yaml` (blok `scripts`)

**Interfaces:**
- Consumes: skema `scripts.analyze` dari plan pyartisan Task 5: list `{name, cmd, fix?}`.

- [ ] **Step 1: Edit blok `scripts`** menjadi:
```yaml
scripts:
  serve: "python3 server.py"
  serve_uv: "uv run --no-project --with-requirements requirements.txt python server.py"
  analyze:
    - {name: ruff-check, cmd: "ruff check .", fix: "ruff check --fix ."}
    - {name: ruff-format, cmd: "ruff format --check .", fix: "ruff format ."}
    - {name: bandit, cmd: "bandit -q -r app utils config.py -c pyproject.toml"}
    - {name: mypy, cmd: "mypy ."}
```
  Catatan: key `fix` ditambah di plan ini (tidak ada di spec template) agar `analyze --fix` jalan. Update spec agar sinkron.
- [ ] **Step 2: Validasi YAML:** `python -c "import yaml;print(yaml.safe_load(open('.pyartisan/manifest.yaml'))['scripts']['analyze'][0])"` -> dict `ruff-check`.
- [ ] **Step 3: Uji dengan pyartisan baru:** `pyartisan analyze` -> semua langkah `✔`, exit 0 (butuh `requirements-dev.txt` terpasang di venv). `pyartisan analyze --only bandit` -> hanya bandit.
- [ ] **Step 4: Uji serve uv:** `pyartisan serve --uv` -> server naik (port dari `.env`), Ctrl+C menghentikan.
- [ ] **Step 5: Regresi:** `pyartisan make controller demo` di salinan sementara -> berhasil seperti sebelum edit.
- [ ] **Step 6: Commit** `git add .pyartisan/manifest.yaml docs/superpowers && git commit -m "feat(manifest): add analyze steps and serve_uv"`

### Task 2: Verifikasi bandit CI

**Files:**
- Modify: `.github/workflows/ci.yml` (hanya jika bandit hilang)

- [ ] **Step 1:** `grep -n "bandit" .github/workflows/ci.yml` -> step `bandit -q -r app utils config.py -c pyproject.toml` ada di job `lint`.
- [ ] **Step 2:** `bandit -q -r app utils config.py -c pyproject.toml` -> tanpa temuan baru. Temuan: perbaiki atau tambah `# nosec` dengan alasan.
- [ ] **Step 3:** Jika tidak ada perubahan, lewati commit. Selain itu `git commit -m "ci: keep bandit scope in sync with analyze"`.
