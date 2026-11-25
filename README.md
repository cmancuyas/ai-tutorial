# AI Engineering Journey

My hands-on path from C#/.NET developer to AI engineer: Python, LLMs,
structured outputs, RAG, agents, and Azure.

| Week | Folder | What I built |
|---|---|---|
| 1 | [ai-learning](ai-learning) | Python basics for C# developers, a FastAPI survey API with pytest tests |
| 2 | [week02-first-llm-call](week02-first-llm-call) | First calls to Azure OpenAI (gpt-5-mini), chat with memory, structured outputs, a CSV classification pipeline for citizen feedback (English / Tagalog / Taglish) |
| 3 | [week03-reliable-ai](week03-reliable-ai) | Prompt engineering measured with a small test set, error handling and retries, parallel async calls, prompt-injection defenses |

## Tech
Python 3.14 · uv · FastAPI · Pydantic · pytest · OpenAI SDK · Azure AI Foundry

## Running a project
Each folder is its own project. Inside a folder:

```
python -m uv sync
python -m uv run python <file>.py
```

Projects that call Azure need a `.env` file (see each folder's `.env.example`).
`.env` files are never committed.
