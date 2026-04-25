# Mock Interview App

Streamlit app that generates interview questions and answer guidance from a target role and job description.

## Setup

```powershell
cd "C:\Users\USER\Desktop\Tarot Cards _RAG files\Langchain_Folder\mock_interview"
python -m pip install -r requirements.txt
```

## Environment Variables

1. Copy `.env.example` to `.env`.
2. Set your API key:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

## Run

```powershell
python -m streamlit run app.py
```

## Stop

Press `Ctrl + C` in the terminal running Streamlit.
