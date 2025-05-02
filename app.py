import streamlit as st
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import os

prompt_template = """
You are an HR professional at a technical company hiring for the role of a {role}.

You have been provided with the following interviewee resume:
{resume}

Your task is to conduct an interview by asking relevant and insightful questions about the candidate’s experience, skills, and projects mentioned in their resume.  
You should reference both the resume and the candidate’s previous answers to guide your next question logically.

You are also provided with the previous conversation history (which includes your earlier questions and the interviewee's answers):
{history}

Guidelines to follow:
- Ask only one thoughtful and relevant interview question at a time.
- Base your next question on the interviewee’s previous answer to maintain a natural flow.
- Do not answer on behalf of the interviewee.
- Once you have asked a total of 10 questions, politely end the interview by thanking the candidate and informing them that the interview is complete.

Keep the questions focused on evaluating the candidate's suitability for the {role} role.

Always keep track of how many questions you have already asked and stop after 10, the current question count is {count}.
"""

system_prompt = ChatPromptTemplate.from_template(prompt_template)

st.set_page_config(page_title="LangChain: Mock Interview", page_icon = "🦜")
st.title("🦜 Mock Interview")
st.sidebar.title("Upload your resume")

api_key = st.sidebar.text_input(type="password", label="Enter your Groq API Key")

if not api_key:
    st.info("Please enter your Groq API Key")
    st.stop()

# Main variables
resume_path = r"Resume"
os.makedirs(resume_path, exist_ok=True)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0, api_key=api_key, streaming=True)

# Rag chain
rag_chain = {
    "resume": RunnablePassthrough(),
    "history": RunnablePassthrough(),
    "role": RunnablePassthrough(),
    "count": RunnablePassthrough(),
} | system_prompt | llm | StrOutputParser()


# Splitting docs into chunks
@st.cache_resource(ttl = "2h")
def split_doc_get_vectorstore(file_path):
    loader = PyPDFLoader(file_path)
    pages = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200)
    doc = text_splitter.split_documents(pages)

    vectorstore = FAISS.from_documents(doc, embeddings)
    vectorstore = vectorstore.as_retriever()
    return vectorstore


uploaded_file = st.sidebar.file_uploader("Choose a file", type=["pdf"])
if uploaded_file is not None:
    file_content = uploaded_file.getvalue()
    save_path = Path(resume_path, uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(file_content)

job_role = st.sidebar.text_input(label="Enter the job role", placeholder="GenAI Developer")
if not job_role:
    st.info("Please enter the job role")
    st.stop()
    
if uploaded_file is None:
    st.info("Please upload your resume in PDF format")
    st.stop()

if uploaded_file:
    store = split_doc_get_vectorstore(save_path)

    if "history" not in st.session_state:
        st.session_state.history = [{"role": "assistant", "content": "Hello, How are you?"}]

    if "count" not in st.session_state:
        st.session_state.count = 0

    for message in st.session_state.history:
        st.chat_message(message["role"]).write(message["content"])

    user_answer = st.chat_input(placeholder="Please provide your response")
    if user_answer:
        st.session_state.history.append({"role": "user", "content": user_answer})
        st.chat_message("user").write(user_answer)

        with st.chat_message("assistant"):
            st.spinner("Thinking...")
            # Update the count and history in the session state
            response = rag_chain.invoke({"resume": store, "history": st.session_state.history, "role": job_role, "count": st.session_state.count})
            st.session_state.count += 1
            if (st.session_state.count >= 3):
                st.session_state.history.append({"role": "assistant", "content": "Thank you for your time. The interview is complete."})
                st.write("Thank you for your time. The interview is complete.")
                st.stop()
            st.session_state.history.append({"role": "assistant", "content": response})
            st.write(response)