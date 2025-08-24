from typing import List
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from .config import embeddings

def build_vector_store(chunks: List[Document]):
    
    return FAISS.from_documents(chunks, embeddings)

def make_retriever(vs, k: int = 4):
    
    return vs.as_retriever(search_type="similarity", search_kwargs={"k": k})
