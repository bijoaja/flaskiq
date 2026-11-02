# Authentication & Security

FlaskIQ uses **JWT (JSON Web Tokens)** for API authentication and **Flask-WTF CSRF** for browser form protection.

## JWT Authentication Flow

1. Client sends credentials to `POST /api/v1/auth/login`.
2. Server validates credentials and returns signed JWT token.
3. Client includes token in subsequent requests:
   `Authorization: Bearer <token>`

The payload contains:
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

## Protecting Routes

Use `@Middleware.token_required` decorator on controller methods:

```python
from utils.middleware import Middleware

class MyResource(Resource):
    @Middleware.token_required
    def post(self, current_user):
        return {"success": True, "user": current_user}
```

The decorator:
- Checks `Authorization: Bearer <token>` header format.
- Decodes and verifies token signature and expiration.
- Injects `current_user` dictionary into the route handler.
- Returns `401 Unauthorized` on missing, expired, or malformed tokens.

## Security Configuration

- `SECRET_KEY`: Minimum 32 characters in production. Insecure placeholders are rejected.
- `JWT_KEY`: Dedicated secret for signing tokens.
- `JWT_EXPIRY_MINUTES`: Expiration time in minutes (default: 60).
