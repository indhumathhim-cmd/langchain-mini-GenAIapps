# 📧 Smart Email Writer

### 📝 Overview
The Smart Email Writer is an AI-powered productivity tool designed to translate messy, unstructured thoughts into polished, professional corporate communications. Users simply input rough bullet points, and the application generates a ready-to-send email draft, saving time and ensuring consistent tone.

### ✨ Features
* **Bullet-to-Text Translation:** Converts brief notes into fully structured paragraphs.
* **Context-Aware Formatting:** Maintains a professional and polite tone suitable for corporate environments.
* **Streamlit UI:** A clean, intuitive web interface for rapid text input and retrieval.

### 🛠️ Tech Stack
* **Frontend:** Streamlit
* **Backend:** Python
* **AI/LLM:** LangChain, OpenAI (`gpt-4o-mini`)
* **Architecture:** LangChain Prompt Templates with LCEL syntax.

### 🚀 How to Run Locally
1. Clone this repository.
2. Navigate to the folder: `cd smart_emailwriter`
3. Activate the virtual environment: `.\venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Add your OpenAI API key to a `.env` file (`OPENAI_API_KEY=your_key_here`).
6. Launch the app: `python -m streamlit run app.py`

   

https://github.com/user-attachments/assets/58fbfe59-9355-4bbc-929d-cc50bd910f40

# 🤖 AI Engineering Portfolio: Smart Solutions

Welcome to my collection of AI-powered applications. This repository contains two distinct projects demonstrating different aspects of LLM orchestration and RAG.

---

## 🏗️ 1. Spotify Architecture Assistant (PDF RAG)
**Status:** Production Ready ✅
A high-performance **Retrieval-Augmented Generation (RAG)** application. It allows users to upload technical PDFs, stores them in a local **FAISS** vector database, and provides strict, zero-hallucination answers.

* **Key Tech:** Streamlit, LangChain, FAISS, GPT-4o-mini.
* **Feature:** Persistent disk storage and "Show Your Work" source transparency.

---

https://github.com/user-attachments/assets/a207b979-c883-4e8b-a35d-7f884117df39


