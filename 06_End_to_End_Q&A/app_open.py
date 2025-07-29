import streamlit as st
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "langchain_test_with_openai"

# Prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that answers questions."),
    ("user", "{question}"),
])

# Initialize LLM and chain once
@st.cache_resource
def get_chain():
    llm = Ollama(model="llama3.2:latest")
    output_parser = StrOutputParser()
    return prompt | llm | output_parser

chain = get_chain()

def generate_response(question):
    return chain.invoke({"question": question})

# Streamlit UI
st.title("LangChain Ollama Q&A App")
st.header("Ask a Question")
question = st.text_input("Ask a question:")

if question:
    st.header("Answer")
    answer = generate_response(question)
    st.write(answer)
else:
    st.warning("Please enter a question to get an answer.")