import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv

# Load securtity keys
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY") or os.getenv("Open_API_Key")

llm = ChatOpenAI(
    api_key=api_key,
    model="gpt-4o-mini",
    temperature = 0.7
)

# 2. Define the prompt template
brackets_prompt = PromptTemplate(
    input_variables=["role", "jd"],
    template="""
    You are a senior technical interviewer. 
    Given this Job Role: {role}
    And this Job Description (JD):
    {jd}
    
    Please generate 5 highly relevant, challenging interview questions tailored to this specific role and description. 
    Below each question, provide a brief "Ideal Answer" guide so the candidate knows what key points to hit.

    For each question, provide a clear , strong sample answer and also a situation based answer from the relevant companies and jobs in the resume
    1. Question :....
        Answer : .....
    """
)

# 3. Create the chain

# ✅ Cursor Fix: Using LangChain v1 LCEL syntax (no more LLMChain!)
chain = brackets_prompt | llm

# ==========================================
# 4. STREAMLIT FRONTEND UI
# ==========================================

st.title("🎙️ AI Mock Interview Prep")

if not api_key:
    st.error("Missing API key. Set OPENAI_API_KEY (or Open_API_Key) in .env.")
    st.stop()

st.markdown("Paste a job description below to generate custom practice questions and answer guides.")

# Input fields
role = st.text_input("Job Role (e.g., Senior Product Manager):")
jd = st.text_area("Paste the Job Description (JD) here:", height=200)

if st.button("Generate Interview Questions"):
    
    # Validation
    if not role or not jd.strip():
        st.warning("Please provide both the Job Role and the Job Description.")
    else:
        with st.spinner("Reviewing the JD and preparing your interview panel..."):
            
            # ✅ Cursor Fix: Using .invoke() instead of .run()
            response = chain.invoke({
                "role": role,
                "jd": jd
            })
            
            # Display the final questions
            st.subheader("Your Practice Questions:")
            
            # ✅ Cursor Fix: Extracting .content from the ChatOpenAI response object
            st.write(response.content)