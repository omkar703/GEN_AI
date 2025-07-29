from crewai import Task
from tools import yt_tool
from agents import blog_researcher, blog_writer

# Research Task
research_task = Task(
    description="Research the content of the YouTube video located at {video_url}.",
    expected_output="Summarize insights related to AI, ML, and Data Science from the video.",
    tools=[yt_tool],
    agent=blog_researcher,
)

write_task = Task(
    description="Write a blog post based on the insights gained from the video at {video_url}.",
    expected_output="An engaging blog article about the AI/ML/DS topics covered in the video.",
    tools=[yt_tool],
    agent=blog_writer,
    async_execution=False,
    output_file='new-blog-post.md'
)
