# Autentikasi & Keamanan

FlaskIQ menggunakan **JWT (JSON Web Tokens)** untuk autentikasi API dan **Flask-WTF CSRF** untuk proteksi formulir browser.

## Alur Autentikasi JWT

1. Klien mengirim kredensial ke `POST /api/v1/auth/login`.
2. Server memvalidasi akun dan menghasilkan token JWT bertanda tangan digital.
3. Klien menyertakan token pada header request berikutnya:
   `Authorization: Bearer <token>`

Payload token memuat:
```json
{
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com"
  },
  "exp": 1730000000
}
```

## Memproteksi Endpoint

Gunakan dekorator `@Middleware.token_required` pada controller:

```python
from utils.middleware import Middleware

class MyResource(Resource):
    @Middleware.token_required
    def post(self, current_user):
        return {"success": True, "user": current_user}
```

Fungsi dekorator:
- Memeriksa keabsahan format header `Authorization: Bearer <token>`.
- Mendekode dan memverifikasi tanda tangan serta masa berlaku token.
- Menginjeksi data `current_user` ke handler rute.
- Mengembalikan kode `401 Unauthorized` bila token tidak ada, kedaluwarsa, atau tidak valid.

## Konfigurasi Kunci Keamanan

- `SECRET_KEY`: Minimal 32 karakter pada lingkungan produksi. Placeholder default akan ditolak.
- `JWT_KEY`: Kunci rahasia khusus penandatanganan JWT.
- `JWT_EXPIRY_MINUTES`: Masa aktif token dalam menit (default: 60).
