import streamlit as st
from groq import Groq
import time

# 1. API VA SOZLAMALAR
API_KEY = "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"
client = Groq(api_key=API_KEY)

st.set_page_config(page_title="AI Hub Premium", page_icon="📱", layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. PREMIUM iMESSAGE STYLE CSS
st.markdown("""
<style>
    /* Fon va silliqlik */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        background-attachment: fixed;
    }

    /* Chat konteyneri */
    .chat-wrapper {
        display: flex;
        flex-direction: column;
        padding: 10px;
        margin-bottom: 80px;
    }

    /* Umumiy xabar pufakchasi */
    .bubble {
        max-width: 70%;
        margin-bottom: 15px;
        padding: 12px 18px;
        border-radius: 20px;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica;
        font-size: 16px;
        line-height: 1.4;
        backdrop-filter: blur(12px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        animation: slideIn 0.3s ease-out;
        display: inline-block; /* Xabar uzunligiga qarab qisqaradi */
        word-wrap: break-word;
    }

    @keyframes slideIn {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Foydalanuvchi xabari (O'ngda, Ko'k shaffof) */
    .user-container {
        display: flex;
        justify-content: flex-end;
        width: 100%;
    }
    .user-bubble {
        background: rgba(0, 122, 255, 0.6); /* iOS Blue */
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-bottom-right-radius: 4px;
    }

    /* AI xabari (Chapda, Shaffof oq) */
    .ai-container {
        display: flex;
        justify-content: flex-start;
        width: 100%;
    }
    .ai-bubble {
        background: rgba(255, 255, 255, 0.1);
        color: #f0f0f0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-bottom-left-radius: 4px;
    }

    /* Ikonkalar */
    .icon {
        font-size: 14px;
        margin-bottom: 4px;
        opacity: 0.8;
        display: block;
    }

    /* Sidebar Glass */
    [data-testid="stSidebar"] {
        background: rgba(0, 0, 0, 0.3) !important;
        backdrop-filter: blur(20px);
    }
    
    /* Input maydoni pastga yopishgan va shaffof */
    .stChatInputContainer {
        padding-bottom: 20px !important;
        background: transparent !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. SIDEBAR
with st.sidebar:
    st.title("🟣 AI Hub")
    st.markdown("---")
    st.write("Dastur holati: **Aktiv**")
    if st.button("Tarixni tozalash"):
        st.session_state.messages = []
        st.rerun()

# 4. CHAT INTERFEYSI
st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'''
            <div class="user-container">
                <div class="bubble user-bubble">
                    <span class="icon">👤 Siz</span>
                    {msg["content"]}
                </div>
            </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown(f'''
            <div class="ai-container">
                <div class="bubble ai-bubble">
                    <span class="icon">🤖 AI</span>
                    {msg["content"]}
                </div>
            </div>
        ''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# 5. INPUT VA LOGIKA
if prompt := st.chat_input("Xabar yozing..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# AI Javobi
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
        )
        response = completion.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
    except Exception as e:
        st.error(f"Xatolik: {e}")