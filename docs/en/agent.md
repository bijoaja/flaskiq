# AI Agent & Chatbot

FlaskIQ includes a multi-provider streaming AI chatbot system.

## Provider Options

Switch providers via `AI_PROVIDER` in `.env`:

```bash
# Local Ollama (default for development)
AI_PROVIDER=ollama
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=mistral

# OpenAI via LangChain (production)
AI_PROVIDER=openai
AI_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
```

## Adding a Custom Provider

1. Implement `BaseAgent` in `app/service/agent/<provider>/<provider>_agent.py`.
2. Register the provider branch in `ChatbotService.get_generator()`.
3. Set `AI_PROVIDER=<provider>` in environment configuration.
