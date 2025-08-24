from src.graph import chat_once

if __name__ == "__main__":
    demo = "I was charged twice for Pro plan last week and also want to change my email."  
    out = chat_once(demo)  
    print("USER:", demo)  
    print("INTENTS:", out["intents"])  
    print("ENTITIES:", out["entities"])  
    print("CONFIDENCE:", out["confidence"])  
    print("ANSWER:\n", out["answer"])  
    print("METRICS:", out["metrics"])  
