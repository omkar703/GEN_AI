import streamlit as st
import os
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings, ChatNVIDIA
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()
os.environ["NVIDIA_API_KEY"] = os.getenv("NVIDIA_API_KEY")

llm = ChatNVIDIA(model="meta/llama-3.3-70b-instruct")

def vector_embedding(uploaded_file):
    if uploaded_file is not None:
        with open("temp_uploaded.pdf", "wb") as f:
            f.write(uploaded_file.read())
        loader = PyPDFLoader("temp_uploaded.pdf")
        docs = loader.load()
        embeddings = NVIDIAEmbeddings()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=50)
        final_documents = text_splitter.split_documents(docs)
        vector = FAISS.from_documents(final_documents, embeddings)
        # Clean up temp file
        os.remove("temp_uploaded.pdf")
        return vector
    else:
        return None

st.title("RAG Q&A Conversation with PDF Upload")
st.markdown("## Upload a PDF and ask questions")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file:
    if st.button("Embed Document"):
        st.session_state.vector = vector_embedding(uploaded_file)
        if st.session_state.vector:
            st.success("Embedding Completed")
        else:
            st.error("Embedding failed. Please try again.")

prompt = ChatPromptTemplate.from_template(
    """
    You are a helpful assistant for question answering tasks. Use the following pieces of retrieval context to answer the question. If you don't know the answer, just say that you don't know, don't try to make up an answer.
    {context}
    Question: {question}
    Helpful Answer:
    """
)

user_question = st.text_input("Enter your question:")

if user_question and "vector" in st.session_state:
    document_chain = create_stuff_documents_chain(
        llm,
        prompt=prompt,
    )
    retriever = st.session_state.vector.as_retriever()
    retriever_chain = create_retrieval_chain(
        retriever=retriever,
        combine_documents_chain=document_chain,
    )
    response = retriever_chain.run(user_question)
    st.write(response)
elif user_question:
    st.warning("Please upload and embed a PDF document first.")