# main.py - ChatGPT + Claude + Meta AI + Gemini
#Terminal-la chat pannanumna -> python main.py
#Website maadhiri chat pannanumna -> streamlit run app.py
#uvicorn main:app --reload
#uvicorn is used to start the server.
# http://127.0.0.1:8000 
# Ne browser la 127.0.0.1:8000 nu potta odane, browser server kitta poi "home page enna?" nu kettuchu.
# Server un home() function-a run panni, indha badhil-a anuppiduchu:
# {"message": "Chatbot is running"}
#127.0.0.1:8000/docs
#

import os
from dotenv import load_dotenv
#from openai import OpenAI # ignore - chatgpt
#import anthropic # ignore - claude
from groq import Groq
import google.generativeai as genai

load_dotenv()

#openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) # ignore - chatgpt
#claude_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY")) # ignore - claude
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
gemini_model = genai.GenerativeModel("gemini-3.8-flash")

def route_query(user_input, manual_model=None):
    if manual_model:
        return manual_model
    text = user_input.lower()
    #if any(w in text for w in ["code", "python", "sql", "bug", "function", "error", "debug"]): # ignore - chatgpt
    #    return "chatgpt" # ignore - chatgpt
    #elif any(w in text for w in ["write", "essay", "explain", "analyse", "analyze", "reason", "compare"]): # ignore - claude
    #    return "claude" # ignore - claude
    if any(w in text for w in ["code", "python", "sql", "bug", "function", "error", "debug", "write", "essay", "explain", "analyse", "analyze", "reason", "compare"]):
        return "meta_ai"
    elif any(w in text for w in ["latest", "news", "today", "current", "search"]):
        return "gemini"
    else:
        return "gemini"

#def ask_chatgpt(prompt, history=[]): # ignore - chatgpt
#    messages = history + [{"role": "user", "content": prompt}] # ignore - chatgpt
#    res = openai_client.chat.completions.create(model="gpt-4o-mini", messages=messages) # ignore - chatgpt
#    return res.choices[0].message.content # ignore - chatgpt

#def ask_claude(prompt, history=[]): # ignore - claude
#    messages = history + [{"role": "user", "content": prompt}] # ignore - claude
#    res = claude_client.messages.create(model="claude-3-5-sonnet-20241022", max_tokens=1500, messages=messages) # ignore - claude
#    return res.text # ignore - claude

def ask_meta_ai(prompt, history=[]):
    messages = history + [{"role": "user", "content": prompt}]
    res = groq_client.chat.completions.create(model="llama-3.1-8b-instant", messages=messages)
    return res.choices[0].message.content

def ask_gemini(prompt, history=[]):
    chat_history = []
    for m in history:
        role = "user" if m["role"] == "user" else "model"
        chat_history.append({"role": role, "parts": [m["content"]]})
    chat = gemini_model.start_chat(history=chat_history)
    res = chat.send_message(prompt)
    return res.text

def get_response(prompt, history=[], manual_model=None):
    model = route_query(prompt, manual_model)
    #if model == "chatgpt": # ignore - chatgpt
    #    answer = ask_chatgpt(prompt, history) # ignore - chatgpt
    #elif model == "claude": # ignore - claude
    #    answer = ask_claude(prompt, history) # ignore - claude
    if model == "gemini":
        answer = ask_gemini(prompt, history)
    else:
        answer = ask_meta_ai(prompt, history)
    return answer, model

if __name__ == "__main__":
    print("Multi-LLM Chatbot Started! Type 'exit' to stop.")
    history = []
    while True:
        q = input("\nYou: ")
        if q.lower() == "exit":
            break
        answer, model = get_response(q, history)
        print(f"\nBot [{model.upper()}]: {answer}")
        history.append({"role": "user", "content": q})
        history.append({"role": "assistant", "content": answer})
# --- UVICORN KU KU - PAZHAYA CODE-A THODALA, KEELA MATTUM ADD PANNIRUKEN ---
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def home():
    return {"message": "Chatbot is running"}
# --- UVICORN END ---