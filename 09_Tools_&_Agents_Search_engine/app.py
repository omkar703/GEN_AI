import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper , WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun , WikipediaQueryRun , DuckDuckGoSearchRun
from langchain.agents import initialize_agent,AgentType
from langchain.callbacks import StreamlitCallbackHandler # it will allow tools to communcicate with each other 
import os 
from dotenv import load_dotenv


api_wraper_wiki = WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=250)
wiki = WikipediaQueryRun(api_wrapper=api_wraper_wiki)


api_wraper_arxiv = ArxivAPIWrapper(top_k_results=1,doc_content_chars_max=250)
arxiv = ArxivQueryRun(api_wrapper = api_wraper_arxiv)

search = DuckDuckGoSearchRun(name = 'Search')


st.title(" langchain - Chat with Search ")
'''
here we use StreamlitcallbackHandler to display the thoughts and actions in an interactive streamlit app
'''
# sidebar for settings

st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter your Groq API key" ,type="password")


if "messages" not in st.session_state:
    st.session_state['messages'] = [
        {"role":'assisstant',
         "content":"Hi , I'm chatbot who can search the web . How can I help you ?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg['role']).write(msg['content'])

if prompt := st.chat_input(placeholder = "What is machine learning ?") :
    st.session_state.messages.append({"role":'user',"content":prompt})
    st.chat_message("user").write(prompt)

    llm = ChatGroq(api_key=api_key , model_name = "Llama3-8b-8192" , streaming=True)

    tools = [search,wiki,arxiv]

    search_agent = initialize_agent(tools,llm,agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,handling_parsing_errors=True)

    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(),expand_new_thoughts=False)
        response = search_agent.run(st.session_state.messages,callbacks=[st_cb])
        st.session_state.messages.append({"role":'assistant',"content":response})
        st.write(response)