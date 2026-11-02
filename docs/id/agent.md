# Agent AI & Chatbot

FlaskIQ menyediakan sistem chatbot AI dengan respon streaming dan dukungan multi-provider.

## Opsi Provider

Ubah provider melalui variabel `AI_PROVIDER` di file `.env`:

```bash
# Menggunakan Ollama lokal (default pengembangan)
AI_PROVIDER=ollama
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=mistral

# Menggunakan OpenAI via LangChain (produksi)
AI_PROVIDER=openai
AI_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
```

## Menambahkan Provider Baru

1. Buat class yang mengimplementasikan `BaseAgent` pada `app/service/agent/<provider>/<provider>_agent.py`.
2. Tambahkan percabangan pada `ChatbotService.get_generator()`.
3. Tentukan `AI_PROVIDER=<provider>` pada file konfigurasi environment.
