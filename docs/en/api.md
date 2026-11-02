# API Reference

Base URL: `http://localhost:8080`  
Interactive docs: `GET /api/v1/docs` (Swagger UI)

All JSON responses follow this unified envelope:

```json
{
  "success": true,
  "data": { ... },
  "message": "Human-readable message"
}
```

---

## General

### `GET /api/v1/`
Welcome message. No authentication required.

```bash
curl http://localhost:8080/api/v1/
```

---

## Authentication

### `POST /api/v1/auth/register`
Register a new user account.

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
Authenticate and receive a JWT token.

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
Stream an AI response. Returns chunked `text/plain`.

```bash
curl -X POST http://localhost:8080/api/v1/chatbot \
  -H "Content-Type: application/json" \
  -d '{"message": "What is FlaskIQ?"}' --no-buffer
```

---

## CMS

| Method | Path | Auth | Description |
|---|---|---|---|
| `GET` | `/api/v1/cms` | None | List all pages |
| `POST` | `/api/v1/cms` | Bearer JWT | Create a new page |
| `GET` | `/api/v1/cms/<id>` | None | Retrieve page by ID |
| `PUT` | `/api/v1/cms/<id>` | Bearer JWT | Update page by ID |
| `DELETE` | `/api/v1/cms/<id>` | Bearer JWT | Delete page by ID |
