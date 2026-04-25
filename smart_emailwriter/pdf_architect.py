import streamlit as st
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate

# Load the API Key
load_dotenv()

# ==========================================
# UI SETUP
# ==========================================
st.set_page_config(page_title="Architecture RAG", page_icon="🏗️", layout="wide")
st.title("🏗️ Spotify Architecture Assistant")
st.markdown("Upload the technical spec once. It will save securely to disk for instant chat.")

# ==========================================
# THE STRICT PROMPT TEMPLATE
# ==========================================
prompt_template = """
You are an expert technical assistant. Use ONLY the following pieces of context to answer the user's question. 
If you cannot find the answer in the provided context, you must reply: "I cannot find this information in the uploaded PDF." Do NOT make up an answer.

Context:
{context}

Question: {question}
Answer:"""

STRICT_PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

# ==========================================
# THE VAULT & FAISS DISK STORAGE (UPGRADED)
# ==========================================
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Check if we already saved FAISS to the hard drive in a previous session!
if "vector_store" not in st.session_state:
    if os.path.exists("faiss_index"):
        # Load from physical disk (Instant!)
        st.session_state.vector_store = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    else:
        st.session_state.vector_store = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ==========================================
# PHASE 1: INGESTION (Sidebar)
# ==========================================
with st.sidebar:
    st.header("1. Upload Architecture Spec")
    uploaded_file = st.file_uploader("Upload your PDF", type="pdf")

    # Only ingest if there's a file AND we haven't built the database yet
    if uploaded_file is not None and st.session_state.vector_store is None:
        with st.spinner("Analyzing and saving database to disk..."):
            
            temp_file_path = "temp_architecture.pdf"
            with open(temp_file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            loader = PyPDFLoader(temp_file_path)
            docs = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = text_splitter.split_documents(docs)

            # Build FAISS Database
            vector_db = FAISS.from_documents(chunks, embeddings)
            
            # 🔥 NEW: Save to physical disk so it survives browser refreshes!
            vector_db.save_local("faiss_index")
            
            # Put it in current memory
            st.session_state.vector_store = vector_db
            
            st.success("✅ Database securely saved to FAISS disk!")

    elif st.session_state.vector_store is not None:
        st.success("✅ FAISS Database is loaded and active.")

# ==========================================
# PHASE 2: RETRIEVAL & ASK (Main Window)
# ==========================================
st.header("2. Ask the Architect")

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_question := st.chat_input("Ask a question about the uploaded PDF..."):
    
    with st.chat_message("user"):
        st.markdown(user_question)
    
    if st.session_state.vector_store is not None:
        with st.chat_message("assistant"):
            with st.spinner("Searching the FAISS database..."):
                
                retriever = st.session_state.vector_store.as_retriever(search_kwargs={"k": 3})
                
                # 🔥 NEW: Temperature set to 0.5 per requirements
                llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5) 
                
                qa_chain = RetrievalQA.from_chain_type(
                    llm=llm, 
                    retriever=retriever,
                    return_source_documents=True,
                    chain_type_kwargs={"prompt": STRICT_PROMPT}
                )
                
                response = qa_chain.invoke(user_question)
                ai_answer = response["result"]
                source_docs = response["source_documents"]
                
                st.markdown(ai_answer)
                
                with st.expander("📄 View exact paragraphs used from the PDF"):
                    for i, doc in enumerate(source_docs):
                        st.info(f"**Source {i+1}:** {doc.page_content}")
                
                st.session_state.chat_history.append({"role": "user", "content": user_question})
                st.session_state.chat_history.append({"role": "assistant", "content": ai_answer})
    else:
        st.error("⚠️ Please upload a PDF in the sidebar first!")