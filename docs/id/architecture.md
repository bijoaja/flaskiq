# Arsitektur

FlaskIQ menerapkan arsitektur berlapis yang ketat. Setiap lapisan memiliki tanggung jawab tunggal dan hanya boleh memanggil lapisan langsung di bawahnya.

```
HTTP Request
     │
     ▼
┌─────────────┐
│   Routes    │  Pemetaan URL — tidak ada logika, hanya menghubungkan URL ke controller
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Controller  │  Parsing request + format response — bebas dari logika bisnis
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Service   │  Logika bisnis — memanggil repository, tidak menyentuh db.session
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Repository  │  Akses data — SATU-SATUNYA layer yang memanggil db.session
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    Model    │  Model ORM SQLAlchemy, serialisasi to_dict()
└─────────────┘
```

## Aturan Lapisan

### Routes (`app/routes/`)
- Blueprint view berada di bawah `app/routes/view/` (mis. `auth.py`, `cms.py`)
- Endpoint API terstruktur di bawah `app/routes/api/v{version}/` (mis. `api/v1/__init__.py`)
- Memetakan pola URL ke metode controller menggunakan Flask `Blueprint`
- Dilarang mengimpor service atau model secara langsung
- Tanpa logika percabangan kondisi

### Controller (`app/controller/`)
- View controller berada di bawah `app/controller/view/` (mis. `auth/auth_controller.py`)
- API controller berada di bawah `app/controller/api/v{version}/` (mis. `api/v1/auth_controller.py`)
- Parsing `request.get_json()` / `request.args`
- Validasi keberadaan input wajib (validasi struktural)
- Memanggil tepat satu fungsi service
- Mengembalikan `Response().success()` atau `Response().invalid()`
- Dilarang menjalankan query model atau `db.session`

### Service (`app/service/`)
- View service berada di bawah `app/service/view/` (mis. `auth_service.py`)
- API service (jika berversi) berada di bawah `app/service/api/v{version}/`
- Berisi seluruh logika bisnis
- Memanggil metode repository untuk akses data
- Menghasilkan `ValueError` untuk domain error (bukan HTTP error langsung)

### Repository (`app/repository/`)
- Seluruh interaksi `db.session` terisolasi di sini
- `BaseRepository` menyediakan: `get_by_id`, `get_all`, `save`, `delete`
- Subclass menambahkan fungsi pencarian spesifik domain
- Mengembalikan instance model ORM (bukan dictionary)

### Model (`app/model/`)
- Definisi murni ORM SQLAlchemy
- Fungsi `to_dict()` untuk serialisasi JSON (dipanggil di controller API)
- Helper hashing password pada model `User`

## Penamaan File

Semua file menggunakan format **snake_case** (mis. `cms_controller.py`, `user_repository.py`) agar kompatibel penuh dengan sistem impor standar Python.
