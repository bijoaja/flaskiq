# Panduan Kontribusi FlaskIQ

Kami menyambut baik pelaporan isu dan pengiriman pull request untuk mengembangkan FlaskIQ.

## Persiapan Lingkungan Pengembangan

```bash
# Buat virtual environment Python
python -m venv .venv
source .venv/bin/activate  # Di Windows: .venv\Scripts\activate

# Pasang dependensi pengembangan
pip install -r requirements-dev.txt
```

## Verifikasi Kualitas Kode

Sebelum membuat pull request, pastikan seluruh perkakas verifikasi berhasil dijalankan:

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

### 4. Pemindaian Keamanan (Bandit & pip-audit)
```bash
bandit -q -r app utils config.py -c pyproject.toml
pip-audit -r requirements.txt
```

## Alur Kontribusi

1. Buat branch fitur baru: `git checkout -b feat/nama-fitur`
2. Ikuti standar arsitektur berlapis (Routes → Controller → Service → Repository → Model).
3. Tambahkan unit test untuk setiap fitur atau perbaikan baru.
4. Pastikan seluruh uji linting, tipe statis, dan keamanan lolos.
5. Ajukan pull request ke branch `main`.
