# 📺 YouTube Video Summarizer

### 📝 Overview
The YouTube Video Summarizer is an AI productivity tool that helps users digest long-form video content in seconds. By pasting a YouTube URL, the application automatically extracts the hidden video transcript and processes it through an LLM to generate a concise summary and a list of key takeaways. 

### ✨ Features
* **Automated Extraction:** Bypasses manual data entry by programmatically scraping YouTube closed captions.
* **Universal Link Parsing:** Gracefully handles various YouTube URL formats (desktop, mobile, shortened).
* **Robust Error Handling:** Detects and politely informs the user if a video has disabled subtitles instead of crashing.
* **AI Summarization:** Condenses thousands of words into a 3-sentence overview and top 5 actionable bullet points.

### 🛠️ Tech Stack
* **Frontend:** Streamlit
* **Backend:** Python
* **AI/LLM:** LangChain, OpenAI (`gpt-4o-mini`)
* **Data Extraction:** `youtube-transcript-api`, `urllib.parse`

### 🚀 How to Run Locally
1. Clone this repository.
2. Navigate to the folder: `cd youtube_video`
3. Activate the virtual environment: `.\venv\Scripts\activate` (Windows)
5. Install dependencies: `pip install -r requirements.txt`

https://github.com/user-attachments/assets/f068abe4-6c40-44c0-b137-4d6ea25d2c43


6. Add your OpenAI API key to a `.env` file (`OPENAI_API_KEY=your_key_here`).
7. Launch the app: `python -m streamlit run app.py`

   

