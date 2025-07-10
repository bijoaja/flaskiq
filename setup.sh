#!/bin/bash

# Exit on any error
set -e

echo "🚀 Menjalankan setup project Flask..."

# 1. Pull terbaru
echo "📥 Melakukan git pull..."
git pull

# 2. Salin .env jika belum ada
if [ ! -f .env ]; then
  echo "📄 Menyalin .env.example ke .env..."
  cp .env.example .env
else
  echo "✅ File .env sudah ada, dilewati."
fi

# 3. Build docker
echo "🐳 Pull template_flask docker image..."
docker pull bijoaja/template_flask:latest

# 4. Jalankan docker
echo "▶️ Menjalankan container..."
docker-compose up -d

# 5. Jalankan init db
echo "🛠️ Init DB..."
docker-compose exec web flask db init

# 6. Jalankan migrate
echo "🛠️ Migrasi database..."
docker-compose exec web flask db migrate -m "add: init db"

# 7. Jalankan migrate
echo "🛠️ Upgrade DB..."
docker-compose exec web flask db upgrade

echo "✅ Setup selesai!"

