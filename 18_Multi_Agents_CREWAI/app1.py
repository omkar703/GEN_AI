from crewai import Crew, Agent, Task, Process
from youtube_transcript_api import YouTubeTranscriptApi
from langchain.tools import tool
from dotenv import load_dotenv
import os
import re

load_dotenv()

# === Custom Tool to Extract Transcript ===
def get_transcript_tool_func(youtube_url: str) -> str:
    """Fetch the transcript from a YouTube video URL"""
    try:
        video_id = extract_video_id(youtube_url)
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = ' '.join([seg['text'] for seg in transcript])
        return full_text
    except Exception as e:
        return f"Error fetching transcript: {str(e)}"

get_transcript = Tool(
    name="Get YouTube Transcript",
    func=get_transcript_tool_func,
    description="Fetches transcript from a YouTube video URL"
)

def extract_video_id(url):
    # Simple extractor
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url)
    return match.group(1) if match else None

# === User Input ===
youtube_url = input("Enter a YouTube video URL: ")

# === Agents ===
transcript_agent = Agent(
    role="Transcript Fetcher",
    goal="Extract accurate transcript from a YouTube video",
    backstory="You are great at parsing YouTube videos and summarizing their spoken content.",
    tools=[get_transcript],
    allow_delegation=False,
    verbose=True
)

analysis_agent = Agent(
    role="Video Analyst",
    goal="Analyze transcript and extract insights and topics related to AI/ML",
    backstory="You are an expert in machine learning and understand YouTube content deeply.",
    allow_delegation=False,
    verbose=True
)

blog_writer = Agent(
    role="AI Blogger",
    goal="Generate a professional blog post comparing AI, ML, DL, and Data Science from the video",
    backstory="You are an experienced blogger who simplifies complex topics for a wider audience.",
    allow_delegation=False,
    verbose=True
)

# === Tasks ===
transcript_task = Task(
    description=f"Fetch the transcript from the YouTube video: {youtube_url}",
    agent=transcript_agent
)

analysis_task = Task(
    description="Analyze the transcript and summarize the key AI/ML-related insights and structure them for a blog post.",
    agent=analysis_agent,
    depends_on=[transcript_task]
)

blog_task = Task(
    description="Write a detailed blog post comparing AI, ML, DL, and Data Science using the transcript insights.",
    agent=blog_writer,
    depends_on=[analysis_task]
)

# === Crew Run ===
crew = Crew(
    agents=[transcript_agent, analysis_agent, blog_writer],
    tasks=[transcript_task, analysis_task, blog_task],
    process=Process.sequential,
    verbose=True
)

result = crew.run()
print("\n=== Final Blog Post ===\n")
print(result)
