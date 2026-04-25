import streamlit as st
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
import PyPDF2  # for reading PDF files

# Load security keys
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY") or os.getenv("Open_API_Key")

# 1. Initialize the LLM (Notice the temperature and model!)
llm = None
if api_key:
    llm = ChatOpenAI(
        api_key=api_key,
        model="gpt-4o-mini",
        temperature=0.3,
    )

# 2. Define the prompt template with job description and resume
prompt = PromptTemplate(
    input_variables=["resume_text", "job_title","company"],
    template="""
    You are an expert career coach and writer. Write a highly professional and tailored cover letter.
    
    Use the following extracted resume text to highlight the candidate's most relevant skills:
    {resume_text}
    
    The cover letter is for the position of {job_title} at {company}.
    
    Keep it concise, impactful, polite, and ready to send. Do not include placeholder brackets for things like addresses, just write the core body of the letter.
    """
)

# 3. Create the chain (LangChain v1 style)
chain = prompt | llm if llm else None
# ==========================================
# 4. STREAMLIT FRONTEND UI
# ==========================================

st.title("📄 AI Cover Letter Generator")

if not api_key:
    st.error("Missing API key. Set OPENAI_API_KEY (or Open_API_Key) in .env.")
    st.stop()

# Gather specific job details
col1, col2 = st.columns(2)
with col1:
    job_title = st.text_input("Job Title (e.g., Software Engineer):")
with col2:
    company = st.text_input("Company Name (optional):")

# Resume uploader
uploaded_file = st.file_uploader("Upload your Resume (PDF or TXT)", type=["pdf", "txt"])

if st.button("Generate Cover Letter"):
    
    # Validation: Make sure they filled everything out
    if not uploaded_file or not job_title:
        st.warning("Please upload your resume and enter the job title.")
    else:
        with st.spinner("Analyzing resume and drafting your letter..."):
            
            # --- THE NEW MAGIC: Extracting text from the PDF ---
           # --- THE NEW MULTI-FORMAT LOGIC ---
            if uploaded_file.name.endswith(".txt"):
                # Read the file and decode it from bytes into readable text
                resume_text = uploaded_file.read().decode("utf-8")
                
            elif uploaded_file.name.endswith(".pdf"):
                # Use PyPDF2 to scrape the text off the PDF pages
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                resume_text = ""
                for page in pdf_reader.pages:
                    resume_text += page.extract_text() or ""
                    
                    
            else:
                # Catch-all error if they somehow upload an unsupported file
                st.error("Unsupported file type.")
                st.stop() # This immediately stops the rest of the script from running!

            # Run the LangChain logic with all THREE variables
            response = chain.invoke({
                "resume_text": resume_text,
                "job_title": job_title,
                "company": company
            })
            
            # Display the final cover letter
            st.subheader("Your Tailored Cover Letter:")
            st.write(response.content)
            st.success("Cover letter generated successfully!")