import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains import LLMMathChain , LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents.agent_types import AgentType
from langchain.agents import Tool , initialize_agent
from langchain.callbacks import StreamlitCallbackHandler


# Set up the streamlit app 
st.set_page_config(page_title="Maths Problem Solver", page_icon="🧮", layout="wide")
st.title("Maths Problem Solver")
groq_api_key = st.sidebar.text_input(label = "Groq API Key" , type= "password")

if not groq_api_key:
    st.info("Please add your Groq API key to continue")
    st.stop()


llm = ChatGroq(groq_api_key = groq_api_key , model = "Gemma2-9b-It")

## Initializing tools 

wikipedia_wrapper = WikipediaAPIWrapper()
wikipedia_tool = Tool(
    name = "Wikipedia",
    func = wikipedia_wrapper.run,
    description = "Tool for a searching internet to find the vatious infromation about the topics",
    
)

## Initializing the Math Tool
math_tool = LLMMathChain.from_llm(llm = llm , verbose = True)

calculator = Tool(
    name = "Calculator",
    func = math_tool.run,
    description = "Useful for when you need to answer questions about math"
)


prompt = '''
you are a mathematician who can solve math problems. 
Logically arrive at the solution and display it point wise for the question bellow 
Question : {question}

Answer :'''


prompt_template = PromptTemplate(template = prompt , input_variables = ["question"])

## Combine all the tools into chains

chain = LLMChain(llm = llm , prompt = prompt_template , verbose = True)


# Reasoning tool 

reasoning_tool = Tool(
    name = "Reasoning",
    func = chain.run,
    description = "Tool for answing logic based and reasoning questions"
)

## initialize the agent 
agent = initialize_agent(
    tools = [wikipedia_tool , calculator , reasoning_tool] ,
    llm = llm ,
    agent = AgentType.ZERO_SHOT_REACT_DESCRIPTION , # ZERO_SHOT_REACT_DESCRIPTION is for zero shot reasoning
    verbose = False ,
    handle_parsing_errors = True ,
    
)

if "messages" not in st.session_state:
    st.session_state['messages'] = [
        {'role':"assistant" , 'content':"Hi Am am math chatbot who can solve math problems. "}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg['role']).write(msg['content'])


## Funtion to generate the response 

def genrate_response(question):
    response  = agent.invoke({'input':question})
    return response



## Lets start the app

question = st.text_input(label = "Enter your question" , type = "default")
if st.button("Find my answer"):
    if question:
        with st.spinner("Thinking..."):
            st.session_state.messages.append({'role':"user" , 'content':question})
            st.chat_message("user").write(question)
            st_cb = StreamlitCallbackHandler(st.container() , expand_new_thoughts=False)

            response = agent.run(
                st.session_state.messages , callbacks = [st_cb]
            )
            st.session_state.messages.append({'role':"assistant" , 'content':response})
            st.chat_message("assistant").write(response)
    
        
    else:
        st.info("Please enter your question")
