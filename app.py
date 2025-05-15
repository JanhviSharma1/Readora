import streamlit as st
from PyPDF2 import PdfReader

st.set_page_config(page_title="Chat with PDF", layout="wide")

# Custom CSS using your palette
st.markdown("""
    <style>
        body {
            background-color: #FFF5B2;
            color: #362C28;
        }

        .stTextInput > div > div > input {
            border-radius: 10px;
            border: 1px solid #362C28;
            padding: 10px;
            font-size: 16px;
            color: #362C28;
        }

        .stButton > button {
            border-radius: 10px;
            background-color: #F3C969;
            color: #362C28;
            font-weight: bold;
        }

        .stSidebar > div:first-child {
            background-color: #D4FCC3;
        }

        .block-container {
            padding-top: 2rem;
        }

        h1 {
            color: #362C28;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### Menu")
    st.markdown("Upload your PDF files and click on the 'Submit & Process' button.")
    uploaded_files = st.file_uploader(
        "Choose PDF files",
        type=["pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

    if uploaded_files:
        process = st.button("Submit & Process")

# Main content
st.markdown(
    "<h1 style='text-align: center;'>Chat with PDF</h1>",
    unsafe_allow_html=True
)

query = st.text_input("Ask a question based on the uploaded PDFs", placeholder="e.g., Provide a summary about Multi-Head Attention")

if query and uploaded_files:
    st.markdown("**Reply:**")
    full_text = ""

    for file in uploaded_files:
        pdf = PdfReader(file)
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"

    # Dummy response logic (replace this with your LLM integration)
    if "multi-head" in query.lower():
        st.success("Scaled Dot-Product Attention is a mechanism used in the Transformer model for calculating attention weights...")
    else:
        st.success(f"(Dummy answer) You asked: '{query}'\n\nThis would be answered based on the content of your uploaded PDFs.")

elif query:
    st.warning("Please upload at least one PDF file.")

elif uploaded_files and not query:
    st.info("Enter a question to ask based on your uploaded PDFs.")