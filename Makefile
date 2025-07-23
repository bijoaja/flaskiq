# USAGE
# Build saja (versi default: 1.0.0)
# make build

# Build versi tertentu
# make build VERSION=1.3.5

# Push Github
# make git MESSAGE="Release versi 1.3.5"

# Build + tag 'latest' + push (otomatis)
# make all VERSION=1.3.5 MESSAGE="Release versi 1.3.5"

# Variabel
IMAGE_NAME = bijoaja/flaskiq
VERSION ?= 1.0.0
MESSAGE ?= "Update $(VERSION)"

.PHONY: setup build tag push all

# Build image dengan versi
setup:
	bash setup.sh

build:
	docker build -t $(IMAGE_NAME):latest .

# Tag image juga sebagai 'latest'
tag:
	docker tag $(IMAGE_NAME):latest $(IMAGE_NAME):$(VERSION)

# Push kedua tag ke Docker Hub
push:
	docker push $(IMAGE_NAME):$(VERSION)
	docker push $(IMAGE_NAME):latest

# Push ke github
git:
	git add .
	git commit -m "$(MESSAGE)"
	git push origin main

# Build, tag, dan push sekaligus
all: build tag push git
