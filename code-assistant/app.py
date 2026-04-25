import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

import os
from pathlib import Path
from dotenv import load_dotenv

project_dir = Path(__file__).resolve().parent
load_dotenv(project_dir / ".env")
if not os.getenv("OPENAI_API_KEY") and not os.getenv("Open_API_Key"):
    # Fallback: reuse key from the sibling tutorial project if present.
    load_dotenv(project_dir.parent / "simplegen_ai" / ".env")

# Support both common env var names
api_key = os.getenv("OPENAI_API_KEY") or os.getenv("Open_API_Key")
llm = None
if api_key:
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=api_key,
        temperature=0.5,
    )

# 2. Define the prompt template from the video
prompt = PromptTemplate(
    input_variables=["code_task"],
    template="""
    You are a professional coding assistant. Help the user with the following task:
    {code_task}
    Provide clean, well-commented code and explanations if needed.
    """
)

# 3. Create the chain (LangChain v1 style)
chain = prompt | llm if llm else None

# ==========================================
# 4. STREAMLIT FRONTEND UI
# ==========================================

st.title("💻 AI Code Assistant")

if not api_key:
    st.error("Missing API key. Set OPENAI_API_KEY (or Open_API_Key) in a .env file.")
    st.stop()

# Create a large text box for the user to type their problem
code_task = st.text_area("Describe your coding task:")

# Create the generate button
if st.button("Generate Code"):
    
    # Check if the user left the box blank
    if code_task.strip() == "":
        st.warning("Please enter a coding task!")
    else:
        # Show a loading spinner while the AI thinks
        with st.spinner("Writing clean code..."):
            
            # Send the task to LangChain and get the answer
            response = chain.invoke({"code_task": code_task})
            
            # Display the final code on the screen
            # Mentor's UI upgrades
        st.subheader("Assistant Response")
        st.code(response.content, language="python")
        st.success("Code generated successfully!")
