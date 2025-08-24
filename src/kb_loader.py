from typing import List
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import glob, os


DEFAULT_KB = [
    {"q": "How do I update my billing method?",
     "a": "Go to Settings > Billing > Payment Method and add a new card."},
    {"q": "I was charged twice",
     "a": "Duplicate charges usually auto-revert in 2–3 business days; otherwise contact support with invoice IDs."},
    {"q": "Reset password",
     "a": "Use 'Forgot password' on the login page; reset link is valid for 30 minutes."},
    {"q": "Change account email",
     "a": "Go to Settings > Account > Email and verify the new address."},
    {"q": "App keeps crashing",
     "a": "Update to latest version and clear cache; if it persists share device model and OS."},
    {"q": "How to raise a complaint",
     "a": "Email complaints@company.com with your ticket ID and a brief description."}
]

def load_kb_from_dir(path: str = "data") -> List[Document]:
    files = glob.glob(os.path.join(path, "*.md")) + glob.glob(os.path.join(path, "*.txt"))  
    docs: List[Document] = []
    if not files:  
        
        for r in DEFAULT_KB:  
            docs.append(Document(page_content=f"Q: {r['q']}\nA: {r['a']}", metadata={"source": "faq"}))  
        return split_docs(docs)  

    
    for f in files:  
        with open(f, "r", encoding="utf-8") as fp:  
            txt = fp.read()  
            docs.append(Document(page_content=txt, metadata={"source": f}))  
    return split_docs(docs)  

def split_docs(docs: List[Document]) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=60)  
    out: List[Document] = []
    for d in docs:  
        out.extend(splitter.split_documents([d]))  
    return out  
