from langchain.prompts import ChatPromptTemplate

intent_prompt = ChatPromptTemplate.from_messages([  
    ("system",
     "You are an intent/entity extractor for customer support.\n"
     "Allowed intents: billing, technical, account, complaints, other.\n"
     "Extract entities like product, account_no, date, plan, email, invoice_id.\n"
     "Return STRICT JSON with keys: intents (list), entities (object), confidence (0..1), needs_clarification (bool)."),  
    ("user", "{message}")  
])

answer_prompt = ChatPromptTemplate.from_messages([  
    ("system",
     "You are a helpful RAG bot. Use ONLY the provided context.\n"
     "If context is insufficient, ask one concise clarifying question.\n"
     "If multiple intents, handle the most critical first."),  
    ("system", "Context:\n{ctx}"),  
    ("user", "{message}")  
])
