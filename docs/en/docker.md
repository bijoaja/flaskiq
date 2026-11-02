# Docker & Deployment

## Development (Bind-Mount)

```bash
# Start development environment
make dev

# Tail logs
make logs

# Open container shell
make shell

# Stop development containers
make stop
```

## Production (Multi-Stage Build)

```bash
# Start production container with Gunicorn
make prod

# Stop production containers
make prod-stop

# Build production image
make build-prod VERSION=2.0.0
```

Production image features:
- Multi-stage build for minimal image footprint.
- Gunicorn WSGI server with multiple workers.
- Non-root user (`appuser`) for security compliance.
