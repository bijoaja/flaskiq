# Referensi API

Base URL: `http://localhost:8080`  
Dokumentasi Interaktif: `GET /api/v1/docs` (Swagger UI)

Semua response JSON mengikuti format seragam berikut:

```json
{
  "success": true,
  "data": { ... },
  "message": "Pesan deskriptif"
}
```

---

## Umum

### `GET /api/v1/`
Pesan sambutan. Tanpa autentikasi.

```bash
curl http://localhost:8080/api/v1/
```

---

## Autentikasi

### `POST /api/v1/auth/register`
Mendaftarkan akun pengguna baru.

**Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "secret123"
}
```

**Response `201`:**
```json
{
  "success": true,
  "data": { "id": 1, "username": "johndoe", "email": "john@example.com" },
  "message": "User registered successfully."
}
```

---

### `POST /api/v1/auth/login`
Autentikasi dan menerima token JWT.

**Body:**
```json
{ "email": "john@example.com", "password": "secret123" }
```

**Response `200`:**
```json
{
  "success": true,
  "data": { "token": "eyJ..." },
  "message": "Login successful."
}
```

---

## Chatbot

### `POST /api/v1/chatbot`
Streaming respon dari AI. Mengembalikan potongan teks (chunked).

```bash
curl -X POST http://localhost:8080/api/v1/chatbot \
  -H "Content-Type: application/json" \
  -d '{"message": "Apa itu FlaskIQ?"}' --no-buffer
```

---

## CMS

| Metode | Endpoint | Autentikasi | Deskripsi |
|---|---|---|---|
| `GET` | `/api/v1/cms` | Tidak | Daftar semua halaman |
| `POST` | `/api/v1/cms` | Bearer JWT | Membuat halaman baru |
| `GET` | `/api/v1/cms/<id>` | Tidak | Mengambil detail halaman |
| `PUT` | `/api/v1/cms/<id>` | Bearer JWT | Memperbarui halaman |
| `DELETE` | `/api/v1/cms/<id>` | Bearer JWT | Menghapus halaman |
