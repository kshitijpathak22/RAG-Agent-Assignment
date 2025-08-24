import streamlit as st
from src.graph import chat_once, log_interaction  

st.set_page_config(page_title="RAG Support Bot", page_icon="🤖", layout="wide")
st.title("🤖 RAG-based AI Support Agent")
st.write("Ask about billing, account, technical issues, or complaints.")

# Keep conversation + last result in session
if "history" not in st.session_state:
    st.session_state.history = []
if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "last_user" not in st.session_state:
    st.session_state.last_user = ""

user_input = st.text_input("Your message:", "")

if st.button("Send") and user_input.strip():
    
    result = chat_once(user_input, st.session_state.history)

    
    st.session_state.history.append({"role": "user", "content": user_input})
    st.session_state.history.append({"role": "assistant", "content": result["answer"]})


    st.session_state.last_result = result
    st.session_state.last_user = user_input


    st.markdown("### 💬 Bot Reply")
    st.write(result["answer"])


    st.markdown("### 🔍 Analysis")
    st.json({
        "Intents": result["intents"],
        "Entities": result["entities"],
        "Confidence": result["confidence"],
        "Metrics": result["metrics"]
    })


if st.session_state.last_result:
    st.markdown("### 📝 Was this helpful?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("👍 Helpful"):
            r = st.session_state.last_result
            log_interaction(
                st.session_state.last_user,
                r["intents"],
                r["confidence"],
                r["metrics"].get("last_latency_ms"),
                feedback="upvote",
            )
            st.success("Thanks! Your feedback was recorded.")
    with col2:
        if st.button("👎 Not helpful"):
            r = st.session_state.last_result
            log_interaction(
                st.session_state.last_user,
                r["intents"],
                r["confidence"],
                r["metrics"].get("last_latency_ms"),
                feedback="downvote",
            )
            st.info("Got it — we recorded your feedback.")


if st.session_state.history:
    st.markdown("### 📜 Conversation History")
    for h in st.session_state.history:
        who = "User" if h["role"] == "user" else "Bot"
        st.markdown(f"**{who}:** {h['content']}")

