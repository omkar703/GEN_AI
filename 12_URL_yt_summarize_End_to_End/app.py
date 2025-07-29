import validators 
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader , UnstructuredURLLoader


## Streamlit app 
st.set_page_config(page_title="URL Summarizer", page_icon="📺", layout="wide")
st.title("Summarizer")
st.subheader('Summarize URL that you want to summarize')


## Get the Groq API key and url (yt or website) to be summarized

with st.sidebar:
    groq_api_key = st.text_input("Groq API Key", value = '',type="password")

generic_url = st.text_input("URL",label_visibility='collapsed')

## Gemma model
llm = ChatGroq(groq_api_key = groq_api_key , model = "gemma2-9b-it")

Prompt_template = '''Provide the summary of the content in 300 words :

Content : {text}

'''

prompt = PromptTemplate(template=Prompt_template, input_variables=["text"])

if st.button('Summarize the Content from YT or Website'):
    ## Validate all the inputs 
    # strip() is used to remove the whitespaces from the input empty char 
    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Please Provide the valid URL to get started")
    elif not validators.url(generic_url):
        st.error("Please Provide a valid URL")
    
    else :
        try :
            with st.spinner("waiting for the response..."):
                ## loading the website data or yt data 
                if "youtube.com" in generic_url:
                    loader = YoutubeLoader.from_youtube_url(generic_url , add_video_info = True)
                else :
                    loader = UnstructuredURLLoader(urls = [generic_url] , ssl_verify = False,
                                                   header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"})
                docs = loader.load()
                ## chain for summarization 
                chain = load_summarize_chain(llm, chain_type="stuff" , prompt = prompt)
                output_summary = chain.run(docs)
                st.success("Summary of the content is : ")
                st.write(output_summary)
        except Exception as e:
            st.error(e)


