#!/bin/bash

# Exit on any error
set -e

echo "🚀 Menjalankan setup project FlaskIQ..."

# 1. Pull terbaru
echo "📥 Melakukan git pull..."
# git pull

# 2. Salin .env jika belum ada
if [ ! -f .env ]; then
  echo "📄 Menyalin .env.example ke .env..."
  # cp .env.example .env
else
  echo "✅ File .env sudah ada, dilewati."
fi

# 3. Pull image flaskiq
echo "🐳 Pull image flaskiq..."
# docker pull bijoaja/flaskiq:latest

# 4. Jalankan semua container
echo "▶️ Menjalankan semua container..."
docker-compose up -d

# 5. Cek status container Ollama
echo "🔍 Mengecek status flaskiq_ai (Ollama)..."
docker-compose exec flaskiq_ai ps aux | grep ollama

# Tunggu beberapa detik agar database dan AI siap
echo "⏳ Menunggu database dan AI service siap..."
sleep 2

# # 6. Cek apakah model mistral tersedia
echo "🔎 Mengecek apakah model 'mistral' sudah tersedia di flaskiq_ai..."

MODEL_EXISTS=$(curl -s http://localhost:11434/api/tags | jq -r '.models[]?.name' | grep -w mistral || true)

if [ -n "$MODEL_EXISTS" ]; then
  echo "✅ Model 'mistral' sudah tersedia."
else
  echo "📦 Model 'mistral' belum ditemukan. Menjalankan 'ollama pull mistral'..."

  # Coba pull model ke dalam container
  docker-compose exec flaskiq_ai ollama pull mistral

  # Cek apakah berhasil ditambahkan
  echo "🔁 Mengecek ulang apakah model berhasil di-pull..."
  MODEL_EXISTS=$(curl -s http://localhost:11434/api/tags | jq -r '.models[]?.name' | grep -w mistral || true)

  if [ -n "$MODEL_EXISTS" ]; then
    echo "✅ Berhasil menambahkan model 'mistral'."
  else
    echo "❌ Gagal menambahkan model 'mistral'. Periksa container 'flaskiq_ai'."
    exit 1
  fi
fi

# 7. Inisialisasi database
echo "🛠️ Inisialisasi database (flask db init)..."
docker-compose exec flaskiq_web flask db init || echo "⚠️ Sudah di-init, dilewati."

# 8. Migrasi database
echo "🛠️ Migrasi database..."
docker-compose exec flaskiq_web flask db migrate -m "add: init db"

# 9 Upgrade database
echo "🛠️ Upgrade database..."
docker-compose exec flaskiq_web flask db upgrade

# 10. Tes koneksi ke Ollama

# Ambil prompt dari container flaskiq_web secara bersih
PROMPT=$(docker-compose run --rm flaskiq_web python -m utils.print_prompt)

# Escape sebagai JSON string
SAFE_PROMPT=$(echo "$PROMPT" | jq -Rs .)

# Siapkan full JSON payload
JSON_DATA=$(jq -n \
  --arg model "mistral" \
  --argjson system_message "{\"role\":\"system\",\"content\":$SAFE_PROMPT}" \
  --argjson user_message '{"role":"user","content":"Halo, Siapa Kamu?"}' \
  '{
    model: $model,
    messages: [$system_message, $user_message],
    stream: false
  }')

# Tes dari dalam container jika curl tersedia
if docker-compose exec flaskiq_web which curl >/dev/null 2>&1; then
  echo "🧠 Mengetes koneksi ke AI dari flaskiq_web container..."
  echo "$JSON_DATA" | docker-compose exec -T flaskiq_web curl -s http://flaskiq_ai:11434/api/chat \
    -H "Content-Type: application/json" \
    -d @- | jq '.message.content // .response'
else
  echo "⚠️ curl tidak tersedia di flaskiq_web, tes koneksi dari host..."
  echo "$JSON_DATA" | curl -s http://localhost:11434/api/chat \
    -H "Content-Type: application/json" \
    -d @- | jq '.message.content // .response'
fi



# if docker-compose exec flaskiq_web which curl >/dev/null 2>&1; then
#   echo "🧠 Mengetes koneksi ke AI dari dalam container flaskiq_web..."
#   docker-compose exec flaskiq_web curl -s http://flaskiq_ai:11434/api/generate -H "Content-Type: application/json" -d '{
#     "model": "mistral",
#     "prompt": "Halo, siapa kamu?",
#     "stream": false
#   }' | jq '.response'
# else
#   echo "⚠️ curl tidak tersedia di flaskiq_web, tes koneksi dari host..."
#   curl -s http://localhost:11434/api/generate -H "Content-Type: application/json" -d '{
#     "model": "mistral",
#     "prompt": "Halo, siapa kamu?",
#     "stream": false
#   }' | jq '.response'
# fi

echo "✅ Setup selesai! 🎉"
