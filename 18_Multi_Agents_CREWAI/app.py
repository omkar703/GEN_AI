# app.py
import os
from dotenv import load_dotenv

# Load .env before any imports
load_dotenv()

from crewai import Crew, Process
from agents import blog_researcher, blog_writer
from tasks import research_task, write_task

# Form the crew
crew = Crew(
    agents=[blog_researcher, blog_writer],
    tasks=[research_task, write_task],
    process=Process.sequential,
    memory=True,
    cache=True,
    max_rpm=100,
    share_crew=True
)

# Get user input
youtube_link = input("Enter a YouTube video URL: ")

# Run the task with YouTube video as topic
result = crew.kickoff(inputs={"video_url": youtube_link})

print(result)
