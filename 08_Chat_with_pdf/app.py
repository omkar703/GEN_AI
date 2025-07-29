## RAG Q&A Conversation with pdf including chat history 
import streamlit as st
from langchain.chains import create_history_aware_retriever , create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate , MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
import os
from dotenv import load_dotenv
load_dotenv()
os.environ['HF_TOKEN'] = os.environ['HF_TOKEN']
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


## Set up streamlit 
st.title("RAG Q&A Conversation with pdf including chat history")
st.markdown("## RAG Q&A Conversation with pdf including chat history")
st.write("Upload the pdf and chat with their contant")

## INput the Groq API key 
groq_api_key = st.text_input("Enter the Groq API key:" )

## Check if groq_api_key is provided
if groq_api_key:
    llm = ChatGroq(groq_api_key=groq_api_key , model="Gemma2-9b-It")

    ## Chat interface 
    session_id = st.text_input("Enter the session id:" , type="default")
    ## Statefully manage chat history 

    if 'store' not in st.session_state:
        st.session_state.store = {}
    
    upload_files = st.file_uploader("Upload the pdf file", type=["pdf"] , accept_multiple_files=True)

    if upload_files:
        documents = []
        for uploaded_file in upload_files:
            temppdf = f"./temp.pdf"
            with open(temppdf, "wb") as f:
                f.write(uploaded_file.getvalue())
                file_name = uploaded_file.name
            loader = PyPDFLoader(temppdf)
            docs = loader.load()
            documents.extend(docs)

     ## Split and create embedding for documents 
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=500)
        texts = text_splitter.split_documents(documents)
        vectorestore = Chroma.from_documents(texts, embeddings)
        retriever = vectorestore.as_retriever()


        # for chat history
        contextualize_q_system_prompt = (
        """
        Given a chat history and the latest user question,
        which might reference context in the chat history ,
        formulate a standalone question which can be understood,
        without the chat history. Do not answer the question,
        just reformulate it if needed and otherwise return it as is.
        """)
        
        contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
        ]
        )


        history_aware_retriever = create_history_aware_retriever(
        llm,
        retriever,
        contextualize_q_prompt)
        

        ## Answer Question
        system_prompt = (
            ''' 
            You are a helpful assistant for question answering tasks , use the following pieces of retrieval context to answer the question. If you don't know the answer, just say that you don't know , don't try to make up an answer.
            '''

            "\n\n"

            "{context}"
        )
        
        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
            ]
        )

        question_answer_chain = create_stuff_documents_chain(
            llm,
            prompt=qa_prompt,
        )


        # combine both question answering and chat history
        rag_chain = create_retrieval_chain(
            history_aware_retriever,
            question_answer_chain,
        )


        def get_session_history(session_id : str) -> BaseChatMessageHistory:
            if session_id not in st.session_state.store:
                st.session_state.store[session_id] = ChatMessageHistory()
            return st.session_state.store[session_id]

        conversation_rag_chain = RunnableWithMessageHistory(
            rag_chain,
            get_session_history,
            history_messages_key="chat_history",
            input_message_key="input",
            output_message_key="answer",
        )

        user_input = st.text_input("Enter your question:")
        if user_input:
            session_history = get_session_history(session_id)
            response = conversation_rag_chain.invoke(
                {"input": user_input},
                config={
                    "session_id": session_id,
                    "chat_history": session_history,
                },
            )
            st.write(response["answer"])
else:
    st.warning("Please enter the Groq API key to continue.")
             