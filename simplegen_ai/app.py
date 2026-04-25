import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI

load_dotenv()

api_key = os.getenv("Open_API_Key")
if not api_key:
    raise ValueError("Missing Open_API_Key in .env file")

llm = OpenAI(api_key=api_key, temperature=0.7)

# Create a prompt template
prompt = PromptTemplate(
    input_variables=["user_input"],
    template="""
You are a helpful assistant.
User says: {user_input}
Your response:
""",
)

# LangChain v1 style chain composition
chain = prompt | llm

if __name__ == "__main__":
    user_input = input("Ask me anything: ")
    response = chain.invoke({"user_input": user_input})
    print("AI says:", response)