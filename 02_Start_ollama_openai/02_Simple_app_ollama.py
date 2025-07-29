import os 
from dotenv import load_dotenv
from langchain_community.llms import Ollama
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


load_dotenv()
 
# Langsmith Tracking 
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_PROJECT'] = os.getenv('LANGCHAIN_PROJECT')


## Prompt Template 
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. please respond like as if you are a human."),
        ("human", "{input}"),
    ]
)

# Streamlit freamwork 
st.title("Langchain demo with Llama 3.2 from ollama")
st.write("This is a simple app to demonstrate how to use Langchain with Llama 3.2 from Ollama.")

input_text = st.text_input("Enter your question:", "What is Langchain?")

## ollama llm 
llm =  Ollama( model="llama3.2:latest")
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

if input_text:
    with st.spinner("Generating response..."):
        response = chain.invoke({"input": input_text})
        st.write(response)
        st.success("Response generated successfully!")
else:
    st.warning("Please enter a question to get a response.")
