from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langserve import add_routes
from dotenv import load_dotenv
import os
import uvicorn

# Load API key
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Define the Groq model
model = ChatGroq(
    model="deepseek-r1-distill-llama-70b",
    api_key=groq_api_key,
)

# Create a translation prompt chain
prompt = ChatPromptTemplate.from_messages([
    ("system", "Translate the following into {language}:"),
    ("user", "{text}"),
])

# Chain: prompt -> model -> output parser
chain = prompt | model | StrOutputParser()

# FastAPI app instance
app = FastAPI(
    title="Langchain Translation API",
    version="1.0",
    description="Translate text into multiple languages using Langchain + Groq + LangServe",
)

# Add the chain route using LangServe
add_routes(
    app,
    chain,
    path="/translate"
)

# Optional: Root route for info
@app.get("/")
async def root():
    return {
        "message": "Welcome to Langchain Translation API using LangServe!",
        "usage": "POST to /translate with JSON body: { 'language': 'French', 'text': 'Hello' }",
        "playground": "/translate/playground",
        "docs": "/docs"
    }

# Run with uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
