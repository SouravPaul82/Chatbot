# 🤖 Chatbot with Knowledge Base

A small Gradio-based conversational agent that answers questions by querying an Amazon Bedrock knowledge base (vector store) and using an OpenAI-compatible LLM for generation. The app combines a Retriever (Amazon Bedrock knowledge bases) with a ReAct-style agent (llama-index) and exposes a simple web UI using Gradio.

---

## Features
- Web UI built with Gradio for conversational chat.
- Retriever backed by an Amazon Knowledge Base (Bedrock) using llama-index.
- ReAct-style agent that uses a tool to fetch facts from the vector DB.
- Minimal, easy-to-run single-file Python app suitable for local testing or containerized deployment.
- Simple test script to validate Bedrock retrieval.

---

## Stack
- Language: Python 3.11
- Framework / runtime: Gradio (v5)
- Notable libraries:
  - llama-index (retriever / agent)
  - llama-index-retrievers-bedrock (Bedrock retriever)
  - llama-index-llms-openai (OpenAI-like LLM wrapper)
  - boto3 (AWS)
  - python-dotenv (env var loading)

---

## Repository layout
Top-level files and what they do:
- `app.py` — Gradio UI and application entrypoint (launches on 127.0.0.1:8080 by default).
- `agent.py` — Agent and retriever setup: creates the AmazonKnowledgeBasesRetriever, LLM wrapper, and ReAct agent. Contains `get_agent_response(...)`.
- `requirements.txt` — pinned Python dependencies.
- `Dockerfile` — simple image for containerized runs.
- `test_kb.py` — small script to test retrieval from the Bedrock knowledge base.
- `image.png` — repo image (used for README/visuals if desired).
- `README.md` — this file.

How it fits together:
- `app.py` is the UI layer: it collects user messages and passes them to `agent.get_agent_response`.
- `agent.py` constructs a Retriever (AmazonKnowledgeBasesRetriever) and a ReAct agent that can call the retriever as a tool; it also wraps the LLM via an OpenAI-like adapter.
- `test_kb.py` can be used to validate direct access to the knowledge base outside the Gradio UI.

---

## Requirements
- Python 3.11
- Docker (optional, for containerized runs)
- AWS access to Amazon Bedrock knowledge bases (if you intend to use the retriever)
- An OpenAI-compatible LLM endpoint (OPENAI_API_KEY and optional custom OPENAI_BASE_URL) or any provider supported by the `llama-index-llms-openai` adapter.

Install Python dependencies:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Environment variables
Create a `.env` file at the project root or export these in your environment. The app uses python-dotenv to load them.

Required (for the full experience):
- BEDROCK_KNOWLEDGE_BASE_ID — the ID of your Amazon Bedrock knowledge base
- AWS_ACCESS_KEY_ID — AWS credentials for Bedrock
- AWS_SECRET_ACCESS_KEY — AWS credentials for Bedrock
- OPENAI_API_KEY — API key for OpenAI-compatible LLMs (or the provider you use)

Optional:
- AWS_DEFAULT_REGION — AWS region (defaults to `us-east-1`)
- OPENAI_MODEL — model name (defaults in code to `text-prime`)
- OPENAI_BASE_URL — custom OpenAI-compatible API base (defaults in code to `https://api.thegrid.ai/v1`)

Important: keep secrets out of source control. Use `.env` and add it to `.gitignore`.

---

## Run locally
After installing dependencies and setting env vars:

```bash
# Activate venv, install deps (see above)
python app.py
```

Then open http://127.0.0.1:8080 in your browser.

Note: app.py launches Gradio with server_name=127.0.0.1 and server_port=8080.

---

## Docker
Build and run with the included Dockerfile:

```bash
# build (example for linux/x86_64)
docker build --platform linux/x86_64 -t gen_ai_agent .

# run (map port and pass env file)
docker run --platform linux/x86_64 -p 8080:8080 --env-file .env gen_ai_agent
```

The Dockerfile copies `app.py` and `agent.py` and installs the pinned dependencies.

---

## Testing the knowledge base connection
`test_kb.py` is a simple script that exercises the Bedrock retriever:

```bash
python test_kb.py
```

It prints retrieved document chunks or a traceback on error. Useful to verify AWS credentials, knowledge base ID, and network connectivity before using the UI.

---

## Configuration & common issues
- Credentials: Ensure `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` have the correct permissions for Bedrock and the knowledge base.
- Knowledge base: `BEDROCK_KNOWLEDGE_BASE_ID` must point to a knowledge base that contains vectorized documents.
- LLM connectivity: If your LLM provider requires a specific `OPENAI_BASE_URL`, set it in `.env`.
- Model compatibility: The repo uses an OpenAI-like wrapper; confirm the chosen model supports chat/function calling if needed.
- Dependency versions: If you hit dependency issues, check `requirements.txt` for pinned versions.

---

## Security & privacy
- Do not commit `.env` or other secrets to the repository.
- Be cautious when exposing the app publicly — the Gradio demo runs locally by default; if you enable sharing or expose the port, secure the host and network.

---

- Create a GitHub Actions workflow to run `test_kb.py` as an integration check (note: would need secrets configured).
