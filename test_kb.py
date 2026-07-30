import os
import traceback
from dotenv import load_dotenv

load_dotenv()

from llama_index.retrievers.bedrock import AmazonKnowledgeBasesRetriever

retriever = AmazonKnowledgeBasesRetriever(
    knowledge_base_id=os.getenv("BEDROCK_KNOWLEDGE_BASE_ID"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
    # Pass vectorSearchConfiguration as an explicit dictionary
    retrieval_config={
        "vectorSearchConfiguration": {
            "numberOfResults": 3
        }
    },
)

def test_knowledge_base():
    print("\n🔍 Testing AWS Bedrock Knowledge Base directly...\n")
    try:
        nodes = retriever.retrieve("Amazon revenue growth 2025")
        print(f"✅ SUCCESS! Retrieved {len(nodes)} document chunks.\n")
        
        for i, node in enumerate(nodes):
            print(f"--- Chunk {i+1} ---")
            print(node.text[:200] + "...\n")
            
    except Exception as e:
        print("❌ ERROR ENCOUNTERED:\n")
        traceback.print_exc()

if __name__ == "__main__":
    test_knowledge_base()