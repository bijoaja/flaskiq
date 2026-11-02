# Architecture

FlaskIQ follows a strict four-layer architecture. Each layer has a single responsibility and only interacts with the layer directly beneath it.

```
HTTP Request
     │
     ▼
┌─────────────┐
│   Routes    │  URL mapping — no logic, wires URL to controller
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Controller  │  Request parsing + response formatting — no business logic
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Service   │  Business logic — calls repository, never touches db.session
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Repository  │  Data access — the ONLY layer that calls db.session
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    Model    │  SQLAlchemy ORM model, to_dict() serialisation
└─────────────┘
```

## Layer Rules

### Routes (`app/routes/`)
- View blueprints are located under `app/routes/view/` (e.g. `auth.py`, `cms.py`)
- API endpoints are structured under `app/routes/api/v{version}/` (e.g. `api/v1/__init__.py`)
- Map URL patterns to controller methods using Flask `Blueprint`
- Never import services or models directly
- No conditional logic

### Controllers (`app/controller/`)
- View controllers are located under `app/controller/view/` (e.g. `auth/auth_controller.py`)
- API controllers are located under `app/controller/api/v{version}/` (e.g. `api/v1/auth_controller.py`)
- Parse `request.get_json()` / `request.args`
- Validate that required fields are present (structural validation only)
- Call exactly one service method
- Return `Response().success()` or `Response().invalid()`
- Never call `db.session` or model queries

### Services (`app/service/`)
- View services are located under `app/service/view/` (e.g. `auth_service.py`)
- API services (if versioned) are located under `app/service/api/v{version}/`
- Contain all business logic
- Call repository methods for data access
- Raise `ValueError` for domain errors (not HTTP errors)
- Can import and call other services when needed

### Repository (`app/repository/`)
- All `db.session` operations live here exclusively
- `BaseRepository` provides: `get_by_id`, `get_all`, `save`, `delete`
- Subclasses add domain-specific queries
- Return ORM model instances (not dicts)

### Models (`app/model/`)
- Pure SQLAlchemy model definitions
- `to_dict()` for JSON serialisation (called at the controller boundary for APIs)
- Password hashing helpers on `User`

## File Naming

All files use **snake_case** (e.g., `cms_controller.py`, `user_repository.py`). Standard Python imports work everywhere.
