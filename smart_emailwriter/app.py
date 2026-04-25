import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv

# Load security keys
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY") or os.getenv("Open_API_Key")

# 1. Initialize the LLM (Notice the temperature and model!)
llm = None
if api_key:
    llm = ChatOpenAI(
        api_key=api_key,
        model="gpt-4o-mini",
        temperature=0.5,
    )

# 2. Define the prompt template
prompt = PromptTemplate(
    input_variables=["bullet_points"],
    template="""
    You are an expert email writer. Using the following bullet points, draft a professional, clear, and polite email.
    
    Bullet Points:
    {bullet_points}
    
    Email Draft:
    """
)

# 3. Create the chain
chain = prompt | llm if llm else None

# ==========================================
# 4. STREAMLIT FRONTEND UI
# ==========================================

st.title("📧 Smart Email Writer")

if not api_key:
    st.error("Missing API key. Set OPENAI_API_KEY (or Open_API_Key) in .env.")
    st.stop()

# Text area for the user to paste their rough notes
bullet_points = st.text_area("Enter your rough notes or bullet points here:", height=150)

if st.button("Draft Email"):
    
    if bullet_points.strip() == "":
        st.warning("Please enter some bullet points first.")
    else:
        with st.spinner("Drafting your email..."):
            
            # Run the LangChain logic
            response = chain.invoke({"bullet_points": bullet_points})
            
            # Display the final email
            st.subheader("Your Draft:")
            # We use st.write here instead of st.code because it is a normal text email!
            st.write(response.content)