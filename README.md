# AI Chatbot made using AWS services 


A small Gradio-based chatbot that answers questions by querying an Amazon Bedrock knowledge base (vector store) and using OpenAI for generation. It pairs a Retriever (via llama-index Bedrock retriever) with an LLM-driven agent (ReAct) to fetch relevant knowledge and return concise answers.

## Features
- Gradio web UI for conversational chat.
- Retriever backed by an Amazon Knowledge Base (Bedrock).
- ReAct-style agent that uses a query tool to fetch facts from the vector DB.
- Simple, single-file Python app suitable for local testing or containerized deployment.

## Stack
- Language: Python 3.11
- Framework / runtime: Gradio (v5) for UI
- Notable libraries:
  - llama-index (for retriever / agent connect)
  - llama-index-retrievers-bedrock (Bedrock retriever)
  - llama-index-llms-openai (OpenAI LLM wrapper)
  - boto3 (AWS)
  - python-dotenv (env var loading)

