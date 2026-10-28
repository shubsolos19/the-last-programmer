
import streamlit as st
import requests

from ghost import ask_ghost, PERSONALITIES

st.set_page_config(
    page_title="The Last Programmer",
    page_icon="👻",
    layout="centered"
)

st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(ellipse at top, #25103d 0%, #100b1d 45%, #08070d 100%);
    color: #f4eaff;
}

h1, h2, h3 {
    color: #d9a7ff !important;
}

p, label, .stMarkdown {
    color: #eee4ff;
}

div[data-testid="stChatMessage"] {
    background: rgba(100, 60, 140, 0.15);
    border: 1px solid rgba(190, 130, 255, 0.15);
    border-radius: 14px;
}

.stChatInput textarea {
    background: #1b1229 !important;
    color: white !important;
}

.stButton button {
    border-radius: 10px;
    border: 1px solid #a855f7;
}

.ghost-banner {
    text-align: center;
    padding: 22px 8px;
    border: 1px solid #6b3b91;
    border-radius: 18px;
    background: rgba(54, 24, 79, 0.45);
    margin-bottom: 20px;
}

.ghost {
    font-size: 60px;
}

.subtitle {
    color: #c7a6e8;
    font-size: 15px;
}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="ghost-banner">
    <div class="ghost">👻</div>
    <h1>THE LAST PROGRAMMER</h1>
    <div class="subtitle">
        An ancient coding spirit has awakened...
    </div>
</div>
""", unsafe_allow_html=True)


with st.sidebar:
    st.title("⚙️ Ghost Settings")

    model = st.text_input(
        "Ollama model",
        value="qwen2.5-coder:3b",
        help="Enter a model installed in Ollama."
    ).strip()

    personality = st.selectbox(
        "Choose your ghost",
        list(PERSONALITIES.keys())
    )

    st.divider()

    st.markdown("### 🕯️ About")
    st.write("A local AI coding companion.")
    st.write("🔒 Chat stays on your computer.")
    st.write("🧠 Powered by open-weight AI.")

    if st.button("🧹 Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.caption("The ghost requires Ollama to be running.")


if "messages" not in st.session_state:
    st.session_state.messages = []


# Check whether Ollama is reachable
try:
    requests.get("http://localhost:11434/api/tags", timeout=2)
    ollama_online = True
except requests.RequestException:
    ollama_online = False


if ollama_online:
    st.caption("🟢 Local AI connection detected")
else:
    st.warning(
        "The ghost is asleep. Start Ollama and install a model "
        "to begin chatting."
    )


st.markdown("### 💬 Speak to the spirit")

if not st.session_state.messages:
    st.markdown(
        "Try asking: **Explain recursion, mortal.** "
        "Or summon help with a bug in your code."
    )

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            st.markdown("👻 " + message["content"])
        else:
            st.markdown(message["content"])


prompt = st.chat_input("Ask the ghost programmer...")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("👻 Summoning ancient intelligence..."):
            try:
                history = st.session_state.messages[:-1]

                reply = ask_ghost(
                    message=prompt,
                    history=history,
                    model=model,
                    personality=personality
                )

                st.markdown(reply)
                st.session_state.messages.append(
                    {"role": "assistant", "content": reply}
                )

            except requests.ConnectionError:
                reply = (
                    "💀 I cannot reach Ollama. "
                    "Make sure Ollama is running on your computer."
                )
                st.error(reply)
                st.session_state.messages.append(
                    {"role": "assistant", "content": reply}
                )

            except requests.HTTPError as error:
                reply = (
                    "⚠️ The model request failed. Check that your "
                    "model is installed and the model name is correct."
                )
                st.error(f"{reply}\n\nDetails: {error}")
                st.session_state.messages.append(
                    {"role": "assistant", "content": reply}
                )

            except (KeyError, ValueError) as error:
                reply = "The ghost returned an unexpected response."
                st.error(f"{reply} Details: {error}")
                st.session_state.messages.append(
                    {"role": "assistant", "content": reply}
                )

            except requests.RequestException as error:
                reply = "The spirit's connection failed. Try again."
                st.error(f"{reply}\n\nDetails: {error}")
                st.session_state.messages.append(
                    {"role": "assistant", "content": reply}
                )
