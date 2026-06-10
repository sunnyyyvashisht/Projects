import streamlit as st
from chatbot import chat, conversation_history, save_chat_history

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Overall page */
    .stApp { background-color: #0f1117; }

    /* Title */
    h1 { text-align: center; color: #ffffff; letter-spacing: 1px; }
    .subtitle { text-align: center; color: #888; font-size: 14px; margin-top: -10px; margin-bottom: 20px; }

    /* Chat messages */
    .stChatMessage { border-radius: 12px; margin-bottom: 8px; }

    /* Input box */
    .stChatInputContainer { border-top: 1px solid #2a2a3e; padding-top: 12px; }

    /* Sidebar */
    .css-1d391kg { background-color: #1a1a2e; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Settings")

    personality = st.selectbox(
        "Bot Personality",
        ["Helpful Assistant", "Friendly Tutor", "Sarcastic Genius", "ELI5 Explainer"]
    )

    personality_prompts = {
        "Helpful Assistant": "You are a smart, friendly, and helpful AI assistant. Answer clearly and concisely.",
        "Friendly Tutor": "You are a patient and encouraging tutor. Break things down step by step and use examples.",
        "Sarcastic Genius": "You are extremely intelligent but slightly sarcastic. You still help, but with dry humor.",
        "ELI5 Explainer": "Explain everything like the user is 5 years old. Use simple words and fun analogies."
    }

    st.markdown("---")
    st.markdown("### 🗑️ Controls")

    if st.button("🧹 Clear Chat", use_container_width=True):
        st.session_state.messages = []
        # Reset conversation history in chatbot.py
        conversation_history.clear()
        conversation_history.append({
            "role": "system",
            "content": personality_prompts[personality]
        })
        st.rerun()

    if st.button("💾 Save Chat", use_container_width=True):
        if st.session_state.get("messages"):
            save_chat_history("chat_history.txt")
            st.success("Saved to chat_history.txt!")
        else:
            st.warning("No messages to save yet.")

    st.markdown("---")
    st.markdown("### 📊 Stats")
    msg_count = len(st.session_state.get("messages", []))
    st.metric("Messages", msg_count)

    st.markdown("---")
    st.caption("Built with Python + OpenAI + Streamlit")

# ── Main UI ───────────────────────────────────────────────────────────────────
st.markdown("# 🤖 AI Chatbot")
st.markdown('<p class="subtitle">Powered by GPT-3.5-turbo</p>', unsafe_allow_html=True)

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Update system prompt if personality changed
if "current_personality" not in st.session_state or st.session_state.current_personality != personality:
    st.session_state.current_personality = personality
    conversation_history.clear()
    conversation_history.append({
        "role": "system",
        "content": personality_prompts[personality]
    })

# Display existing messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Show welcome message if no messages yet
if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown("Hey there! 👋 I'm your AI assistant. Ask me anything!")

# ── Handle new input ──────────────────────────────────────────────────────────
if prompt := st.chat_input("Type your message here..."):

    # Show user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get and show bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = chat(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                error_msg = f"⚠️ Error: {e}\n\nCheck your `OPENAI_API_KEY` in the `.env` file."
                st.error(error_msg)
