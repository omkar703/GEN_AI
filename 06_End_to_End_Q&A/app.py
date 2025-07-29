import streamlit as st
import openai 
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

## langsmith Tracking 

os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "langchain_test_with_openai"

# prompt template 
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that answers questions ."),
    ("user", "{question}"),
])

def generate_response(question,api_key,llm,temperature,max_tokens):
    openai.api_key = api_key
    llm = ChatOpenAI(
        model_name=llm,
        temperature=temperature,
        max_tokens=max_tokens
    )
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    answer = chain.invoke({"question": question})
    return answer


## Title of the app
st.title("LangChain OpenAI Q&A App")

# Side for settings
st.sidebar.header("Settings")
api_key = st.sidebar.text_input("OpenAI API Key", type="password")

# Drop down for model selection
llm = st.sidebar.selectbox(
    "Select LLM Model",
    ["gpt-3.5-turbo", "gpt-4"]
)

temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7)
max_tokens = st.sidebar.slider("Max Tokens", 50, 300, 150)

## Main interface for user input
st.header("Ask a Question")
question = st.text_input("Ask a question:") 
if question:
    st.header("Answer")
    answer = generate_response(question,api_key,llm,temperature,max_tokens)
    st.write(answer)    
else:
    st.warning("Please enter a question to get an answer.")