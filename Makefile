IMAGE_NAME = bijoaja/flaskiq
VERSION    ?= 2.0.0
MESSAGE    ?= "Release $(VERSION)"

.PHONY: dev prod stop prod-stop logs shell \
        db-init db-migrate db-upgrade db-setup \
        build-dev build-prod tag push git all

# ── Development ───────────────────────────────────────────────────────────────
dev:
	docker compose -f docker-compose.yml up -d
	@echo "Dev server → http://localhost:$${FLASK_RUN_PORT:-8080}"

stop:
	docker compose -f docker-compose.yml down

logs:
	docker compose -f docker-compose.yml logs -f flaskiq_web

shell:
	docker compose -f docker-compose.yml exec flaskiq_web bash

# ── Production ────────────────────────────────────────────────────────────────
prod:
	docker compose -f docker-compose.prod.yml up --build -d
	@echo "Prod server → http://localhost:$${FLASK_RUN_PORT:-8080}"

prod-stop:
	docker compose -f docker-compose.prod.yml down

# ── Database ──────────────────────────────────────────────────────────────────
db-init:
	docker compose -f docker-compose.yml exec flaskiq_web flask db init

db-migrate:
	docker compose -f docker-compose.yml exec flaskiq_web flask db migrate -m "$(MESSAGE)"

db-upgrade:
	docker compose -f docker-compose.yml exec flaskiq_web flask db upgrade

db-setup: db-init db-migrate db-upgrade

# ── Image management ──────────────────────────────────────────────────────────
build-dev:
	docker build -f Docker/Dockerfile.dev \
	  -t $(IMAGE_NAME):dev .

build-prod:
	docker build -f Docker/Dockerfile.prod \
	  -t $(IMAGE_NAME):$(VERSION) \
	  -t $(IMAGE_NAME):latest .

tag:
	docker tag $(IMAGE_NAME):latest $(IMAGE_NAME):$(VERSION)

push:
	docker push $(IMAGE_NAME):latest
	docker push $(IMAGE_NAME):$(VERSION)

push-dev:
	docker push $(IMAGE_NAME):dev

# ── Git ───────────────────────────────────────────────────────────────────────
git:
	git add .
	git commit -m "$(MESSAGE)"
	git push origin main

# ── Release (build + push + git) ──────────────────────────────────────────────
all: build-prod tag push git
