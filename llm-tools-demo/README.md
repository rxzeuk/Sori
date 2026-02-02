# llm-tools-demo

A minimal LLM orchestration demo with a simple tool registry and a tool-call loop.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env
```

Set `OPENAI_API_KEY` in `.env`, then run:

```bash
llm-tools-demo --model gpt-5-nano
```

Type messages at the `user>` prompt. Try:

```
what's the weather in Seattle?
```

## Notes

- The included weather tool is a stub and always returns "cold and raining".
- The orchestrator keeps a short in-memory history for the current session.
