# Desain flaskiq: `scripts.analyze`, `scripts.serve_uv`, bandit CI

> Tanggal: 2026-11-25. Plan: `../plans/2026-11-25-manifest-analyze-serve.md`.
> Engine: spec di repo pyartisan `docs/superpowers/specs/2026-11-25-doctor-serve-analyze-design.md`.

## Tujuan
- `pyartisan analyze` di flaskiq menjalankan persis perintah CI lint.
- `pyartisan serve --uv` jalan di flaskiq.
- Bandit tetap di CI.

## Bukan tujuan
Tidak mengubah kode aplikasi, deps, atau CI selain jika bandit hilang.

## Perubahan `.pyartisan/manifest.yaml`
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
- `serve_uv`: `pyproject.toml` flaskiq tidak punya `[project]`, jadi `uv run` biasa tidak bisa. Deps ada di `requirements.txt`.
- `analyze` sama dengan job `lint` di `.github/workflows/ci.yml`. Satu sumber kebenaran: jika CI berubah, manifest ikut berubah.

## Bandit (poin 4)
Sudah ada di `ci.yml` (`bandit -q -r app utils config.py -c pyproject.toml`) dan `[tool.bandit]` di `pyproject.toml`. Verifikasi saja.

## Pengujian
- `pyartisan analyze` di flaskiq: semua langkah lulus.
- `pyartisan serve --uv`: server naik di port dari `.env`.
- Manifest tetap valid untuk `pyartisan make controller x` (regresi).

## Catatan
Dependabot flaskiq tidak diubah. Perlu pyartisan versi yang mengenal `scripts.analyze` dan `serve_uv`. Manifest lama tetap jalan di pyartisan baru, pyartisan lama mengabaikan key baru.
