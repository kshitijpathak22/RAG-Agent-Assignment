import json, time
from typing import List, Dict, Any, TypedDict
from langchain.schema import Document
from langchain_openai import ChatOpenAI
from .prompts import intent_prompt, answer_prompt
from .config import llm

class GraphState(TypedDict):
    user: str
    history: List[Dict[str, str]]
    intents: List[str]
    entities: Dict[str, str]
    confidence: float
    needs_clarification: bool
    context_docs: List[Document]
    answer: str
    metrics: Dict[str, Any]

def detect_intent(state: GraphState) -> GraphState:
    msgs = intent_prompt.format_messages(message=state["user"])  
    resp = llm.invoke(msgs)  
    data = json.loads(resp.content)  
    state["intents"] = data.get("intents", [])  
    state["entities"] = data.get("entities", {})  
    state["confidence"] = float(data.get("confidence", 0.5))  
    state["needs_clarification"] = bool(data.get("needs_clarification", False))  
    return state 
 


def retrieve_context(state: GraphState, retriever) -> GraphState:
    
    last_user_msgs = [h["content"] for h in state.get("history", []) if h.get("role") == "user"][-2:]
    hint = " ".join(last_user_msgs)
    query = f"{state['user']} {(' ' + hint) if hint else ''}".strip()
    results = retriever.invoke(query)
    state["context_docs"] = results
    return state



def _render_ctx(docs: List[Document]) -> str:
    return "\n".join(f"[{i+1}] {d.page_content}" for i, d in enumerate(docs))  
 
def generate_answer(state: GraphState) -> GraphState:
    ctx = _render_ctx(state["context_docs"])
    chat_history = _render_history(state.get("history", []))
    msgs = answer_prompt.format_messages(ctx=ctx, message=state["user"])
    msgs.insert(1, {"role": "system", "content": f"Conversation history:\n{chat_history}"})
    resp = llm.invoke(msgs)
    state["answer"] = resp.content.strip()
    return state


def clarify(state: GraphState) -> GraphState:
    state["answer"] = (
        "Quick clarification: Is your question about billing (charges/refunds), "
        "account (email/credentials), or something else?"
    )  
    return state  

def fallback(state: GraphState) -> GraphState:
    state["answer"] = "Sorry, I couldn’t find a confident answer. Escalating to a human agent."  
    return state  

def record_metrics(state: GraphState) -> GraphState:
    mt = state.get("metrics", {})  
    mt["last_latency_ms"] = int((time.time() - mt.get("start_ts", time.time())) * 1000)  
    mt["last_confidence"] = state.get("confidence", 0)  
    mt["intents"] = state.get("intents", [])  
    state["metrics"] = mt 
    return state  

def _render_history(history):
    if not history:
        return "None"
    lines = []
    for h in history[-6:]:  # last 6 turns for brevity
        who = "User" if h["role"] == "user" else "Assistant"
        lines.append(f"{who}: {h['content']}")
    return "\n".join(lines)


