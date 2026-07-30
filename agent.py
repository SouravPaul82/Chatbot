"""
Business logic for AI agent with knowledge base integration.
"""
import os
from dotenv import load_dotenv

load_dotenv()

from llama_index.retrievers.bedrock import AmazonKnowledgeBasesRetriever
from llama_index.llms.openai_like import OpenAILike  # <-- Switched to OpenAILike
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.tools import QueryEngineTool
from llama_index.core.agent.workflow import ReActAgent
from llama_index.core.llms import ChatMessage, MessageRole

retriever = AmazonKnowledgeBasesRetriever(
    knowledge_base_id=os.getenv("BEDROCK_KNOWLEDGE_BASE_ID"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
    retrieval_config={"vectorSearchConfiguration": {"numberOfResults": 3}},
)

# OpenAILike bypasses strict OpenAI model name checks and supports custom endpoints
llm = OpenAILike(
    model=os.getenv("OPENAI_MODEL", "text-prime"),
    api_key=os.getenv("OPENAI_API_KEY"),
    api_base=os.getenv("OPENAI_BASE_URL", "https://api.thegrid.ai/v1"),
    is_chat_model=True,
    is_function_calling_model=True,
)

_knowledge_base_tool = QueryEngineTool.from_defaults(
    query_engine=RetrieverQueryEngine(retriever=retriever),
    name="amazon_knowledge_base",
    description=(
        "A vector database of knowledge about companies and their financial data."
    ),
)

agent = ReActAgent(
    tools=[_knowledge_base_tool],
    llm=llm,
    system_prompt=(
        "You are a helpful AI assistant with access to a vector database of knowledge about companies and their financial data. "
        "When users ask questions about companies or their financial data, "
        "use the available tool to retrieve accurate information. "
        "Always provide clear and concise answers based on the retrieved information."
        "You must use English language for your responses and provide the answer in a concise manner."
    ),
)


def _extract_text_content(content) -> str:
    """Helper to safely extract pure string text from string, list, or dict content."""
    if isinstance(content, str):
        return content
    elif isinstance(content, list):
        text_parts = []
        for item in content:
            if isinstance(item, dict):
                text_parts.append(item.get("text", str(item)))
            elif isinstance(item, str):
                text_parts.append(item)
        return " ".join(text_parts)
    elif isinstance(content, dict):
        return content.get("text", str(content))
    return str(content)


async def get_agent_response(message, chat_history):
    messages = []
    
    for msg in chat_history:
        if not isinstance(msg, dict):
            continue
            
        role = msg.get("role")
        raw_content = msg.get("content", "")
        clean_content = _extract_text_content(raw_content)

        if role == "user":
            messages.append(ChatMessage(role=MessageRole.USER, content=clean_content))
        elif role == "assistant":
            messages.append(ChatMessage(role=MessageRole.ASSISTANT, content=clean_content))

    clean_message = _extract_text_content(message)
    response = await agent.run(user_msg=clean_message, chat_history=messages)
    return str(response)
