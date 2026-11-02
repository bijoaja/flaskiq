# Docker & Deployment

## Lingkungan Pengembangan (Bind-Mount)

```bash
# Menjalankan kontainer pengembangan
make dev

# Melihat log aplikasi
make logs

# Masuk ke shell di dalam kontainer
make shell

# Menghentikan server pengembangan
make stop
```

## Lingkungan Produksi (Multi-Stage Build)

```bash
# Menjalankan kontainer produksi dengan Gunicorn
make prod

# Menghentikan kontainer produksi
make prod-stop

# Build image produksi
make build-prod VERSION=2.0.0
```

Fitur image produksi:
- Build multi-stage untuk ukuran image yang ringkas.
- Web server WSGI Gunicorn dengan multiple workers.
- Dijalankan dengan user non-root (`appuser`) untuk kepatuhan keamanan.
