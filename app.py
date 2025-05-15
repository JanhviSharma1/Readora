import streamlit as st
from PyPDF2 import PdfReader
import requests

st.set_page_config(page_title="Chat with PDF", layout="wide")

# --- Custom CSS ---
st.markdown("""<style>
    body { background-color: #FFF5B2; color: #362C28; }
    .stTextInput > div > div > input {
        border-radius: 10px; border: 1px solid #362C28;
        padding: 10px; font-size: 16px; color: #362C28;
    }
    .stButton > button {
        border-radius: 10px; background-color: #F3C969;
        color: #362C28; font-weight: bold;
    }
    .stSidebar > div:first-child { background-color: #D4FCC3; }
    .block-container { padding-top: 2rem; }
    h1 { color: #362C28; }
</style>""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("### Menu")
    st.markdown("Upload your PDF files and click on the 'Submit & Process' button.")
    uploaded_files = st.file_uploader("Choose PDF files", type=["pdf"], accept_multiple_files=True, label_visibility="collapsed")
    if uploaded_files:
        process = st.button("Submit & Process")

# --- Main Header ---
st.markdown("<h1 style='text-align: center;'>Chat with PDF</h1>", unsafe_allow_html=True)

query = st.text_input("Ask a question based on the uploaded PDFs", placeholder="e.g., Provide a summary about Multi-Head Attention")

def ask_mistral(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "mistral", "prompt": prompt, "stream": False}
        )
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        return f"Error: {str(e)}"

if query and uploaded_files:
    st.markdown("**Reply:**")
    full_text = ""

    for file in uploaded_files:
        pdf = PdfReader(file)
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"

    combined_prompt = f"Answer this question based on the following PDF content:\n\n{full_text[:6000]}\n\nQuestion: {query}"
    reply = ask_mistral(combined_prompt)
    st.success(reply)

elif query:
    st.warning("Please upload at least one PDF file.")

elif uploaded_files and not query:
    st.info("Enter a question to ask based on your uploaded PDFs.")
