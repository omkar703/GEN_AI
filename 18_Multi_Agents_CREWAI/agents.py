from crewai import Agent
from tools import yt_tool

blog_researcher = Agent(
    role='Blog Researcher from YouTube Videos',
    goal='Analyze the video at {video_url} and extract useful insights on AI/ML/Data Science.',
    backstory='You are a research specialist who watches technical YouTube videos and summarizes them into knowledge.',
    tools=[yt_tool],
    verbose=True
)

blog_writer = Agent(
    role='Blog Writer',
    goal='Write a blog post using the information gathered from {video_url}.',
    backstory='You specialize in converting research into engaging blog content.',
    tools=[yt_tool],
    verbose=True
)
