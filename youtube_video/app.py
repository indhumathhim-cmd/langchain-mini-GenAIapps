import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
import os
from dotenv import load_dotenv

# 1. Load security keys
load_dotenv()

# 2. Initialize the LLM (Explicit API key, modern cost-effective model)
llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"), 
    model="gpt-4o-mini", 
    temperature=0.5
)

# 3. Define the prompt template
summary_prompt = PromptTemplate(
    input_variables=["transcript"],
    template="""
    You are an expert content summarizer. Read the following video transcript and provide:
    1. A short 2-3 sentence overarching summary.
    2. The top 5 key takeaways in bullet points.
    
    Transcript:
    {transcript}
    """
)

# 4. Create the modern chain (No more LLMChain!)
chain = summary_prompt | llm

# ==========================================
# 5. HELPER FUNCTIONS (The "Backend" Logic)
# ==========================================

def extract_video_id(url):
    """Extracts the 11-character video ID from various YouTube URL formats."""
    parsed_url = urlparse(url)
    if parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:]
    if parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
        if parsed_url.path == '/watch':
            p = parse_qs(parsed_url.query)
            return p.get('v', [None])[0]
    return None

# ==========================================
# 6. STREAMLIT FRONTEND UI
# ==========================================

st.title("📺 YouTube Video Summarizer")
st.markdown("Paste a YouTube link below to instantly generate a summary and key takeaways.")

youtube_url = st.text_input("YouTube Video URL:")

if st.button("Summarize Video"):
    if not youtube_url:
        st.warning("Please enter a valid YouTube URL.")
    else:
        video_id = extract_video_id(youtube_url)
        
        if not video_id:
            st.error("Could not extract Video ID. Please check the URL format.")
        else:
            with st.spinner("Fetching transcript and generating summary..."):
                try:
                    # Step A: Get the transcript using the NEW v1.2+ syntax
                    fetched_transcript = YouTubeTranscriptApi().fetch(video_id)
                    # Convert it back to the raw dictionary format the rest of our code expects
                    transcript_list = fetched_transcript.to_raw_data()
                    
                    # Step B: Combine the list of text blocks into one massive paragraph
                    transcript_text = " ".join([d['text'] for d in transcript_list])
                    
                    # Step C: Pass the transcript to our AI Chain
                    response = chain.invoke({"transcript": transcript_text})
                    
                    # Step D: Display the result
                    st.subheader("Video Summary:")
                    st.write(response.content)
                    
                except Exception as e:
                    # This catches errors like "Subtitles are disabled for this video"
                    st.error(f"An error occurred: {e}. This usually means the video has subtitles disabled.")