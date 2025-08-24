import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

load_dotenv()  

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")  
VECTOR_BACKEND = os.getenv("VECTOR_BACKEND", "faiss").lower()  
# QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")  
# QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "kb")  


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)  
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")  
