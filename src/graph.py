from typing import Dict, Any, List
from langgraph.graph import StateGraph, START, END
from .nodes import (GraphState, detect_intent, retrieve_context, generate_answer,
                    clarify, fallback, record_metrics)
from .kb_loader import load_kb_from_dir
from .vector_store import build_vector_store, make_retriever

import csv, os, time

LOG_DIR = os.path.join("data")
LOG_PATH = os.path.join(LOG_DIR, "interaction_log.csv")

os.makedirs(LOG_DIR, exist_ok=True)  


if not os.path.exists(LOG_PATH):
    with open(LOG_PATH, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(
            ["ts_epoch", "user_text", "intents", "confidence", "latency_ms", "feedback"]
        )

def log_interaction(user_text, intents, confidence, latency_ms, feedback=None):
    """
    Append one feedback row to data/interaction_log.csv
    feedback: "upvote" | "downvote" | "" (None)
    """
    with open(LOG_PATH, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([
            int(time.time()),
            user_text,
            "|".join(intents or []),
            float(confidence) if confidence is not None else "",
            int(latency_ms) if latency_ms is not None else "",
            (feedback or ""),
        ])





_chunks = load_kb_from_dir("data")  
_vs = build_vector_store(_chunks)    
_retriever = make_retriever(_vs, k=4)  

def _route_after_detect(state: GraphState) -> str:
    if state["needs_clarification"] or state["confidence"] < 0.45:  
        return "clarify"
    return "retrieve"


graph = StateGraph(GraphState)  

graph.add_node("detect_intent", detect_intent)  
graph.add_node("retrieve", lambda s: retrieve_context(s, _retriever))  
graph.add_node("answer", generate_answer)  
graph.add_node("clarify", clarify)  
graph.add_node("fallback", fallback)  
graph.add_node("metrics", record_metrics)  

graph.add_edge(START, "detect_intent")  
graph.add_conditional_edges("detect_intent", _route_after_detect,  
                            {"clarify": "clarify", "retrieve": "retrieve"})
graph.add_edge("clarify", "metrics")  
graph.add_edge("retrieve", "answer")  
graph.add_edge("answer", "metrics")  
graph.add_edge("metrics", END)  

app = graph.compile()  

def chat_once(user_text: str, history: List[Dict[str, str]] | None = None) -> Dict[str, Any]:
    if history is None:
        history = []  
    state: GraphState = {
        "user": user_text,  
        "history": history,  
        "intents": [],  
        "entities": {},  
        "confidence": 0.0,  
        "needs_clarification": False,  
        "context_docs": [],  
        "answer": "",  
        "metrics": {"start_ts": __import__("time").time()},  
    }
    result = app.invoke(state)  
    return {
        "answer": result["answer"],  
        "intents": result["intents"], 
        "entities": result["entities"],  
        "confidence": result["confidence"],  
        "metrics": result["metrics"],  
    }
