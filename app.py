# app.py - 
# gemini api from "aistudio.google.com/api-keys"
#groq api from "console.groq.com"
#GOOGLE_API_KEY=
#GROQ_API_KEY=

import streamlit as st
from main import get_response

st.set_page_config(page_title="Multi-LLM Chatbot", page_icon="🤖")
st.title("🤖 All-in-One Chatbot")
#st.caption("ChatGPT + Claude + Meta AI + Gemini") # ignore - chatgpt, claude
st.caption("Meta AI + Gemini - 100% Free")

st.sidebar.header("Settings")
manual = st.sidebar.selectbox(
    "Choose Model",
    #["Auto (Smart Router)", "chatgpt", "claude", "meta_ai", "gemini"] # ignore - chatgpt, claude
    ["Auto (Smart Router)", "meta_ai", "gemini"] # chatgpt, claude - ignore
)
manual_model = None if manual == "Auto (Smart Router)" else manual

# --- NEW FEATURES - OLD CODE AZHIKKALA, KEELA ADD PANNIRUKEN ---
st.sidebar.divider()
st.sidebar.header("Extra Features")

# 1. Upload Picture
uploaded_image = st.sidebar.file_uploader("📷 Upload Picture", type=["jpg", "png", "jpeg"])
if uploaded_image:
    st.sidebar.image(uploaded_image, caption="Uploaded Image")

# 2. Upload Documents
uploaded_doc = st.sidebar.file_uploader("📄 Upload Document", type=["pdf", "txt", "docx"])
doc_text = ""
if uploaded_doc:
    st.sidebar.success(f"{uploaded_doc.name} upload aayiduchu!")
    if uploaded_doc.type == "text/plain":
        doc_text = uploaded_doc.read().decode("utf-8")

# 3. Voice Chat
audio = st.sidebar.audio_input("🎙️ Voice Chat")
if audio:
    st.sidebar.audio(audio)
    st.sidebar.info("Voice record aayiduchu!")

# 4. Upload Location
location = st.sidebar.text_input("📍 Location", placeholder="Example: Chennai, Tamil Nadu")
if location:
    st.sidebar.success(f"Location: {location}")
# --- NEW FEATURES END ---

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Enna kekkanum?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- OLD CODE - AZHIKKALA, # POTTU VECHIRUKEN ---
    # history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[:-1]]
    # with st.chat_message("assistant"):
    #     with st.spinner("Yosikiren..."):
    #         answer, used_model = get_response(prompt, history, manual_model)
    #         st.markdown(answer)
    #         st.caption(f"Answered by: {used_model.upper()}")
    # --- OLD CODE END ---

    # --- NEW CODE - DOCUMENT / LOCATION / PICTURE SERTHU ANUPURADHU ---
    final_prompt = prompt
    if doc_text:
        final_prompt = f"Document content:\n{doc_text}\n\nQuestion: {prompt}"
    if location:
        final_prompt = f"My location is {location}. {final_prompt}"
    if uploaded_image:
        final_prompt = f"I uploaded a picture. {final_prompt}"

    history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[:-1]]

    with st.chat_message("assistant"):
        with st.spinner("Yosikiren..."):
            answer, used_model = get_response(final_prompt, history, manual_model)
            st.markdown(answer)
            st.caption(f"Answered by: {used_model.upper()}")
    # --- NEW CODE END ---

    st.session_state.messages.append({"role": "assistant", "content": answer})