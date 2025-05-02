# 🦜 LangChain Mock Interview Bot

An **AI-powered mock interview application** built with **Streamlit**, **LangChain**, **Groq LLM (LLaMA 3)**, and **FAISS retriever**.

Upload your resume, specify a job role, and experience a personalized, resume-driven mock interview where the AI interviewer asks insightful, relevant questions and simulates a real interview setting.

## ✨ Features

* Upload your resume in PDF format
* Enter your target job role
* The AI conducts an interactive 3-question mock interview
* Questions are tailored based on your resume and your answers
* Powered by **LLaMA 3** (Groq), **LangChain**, and **FAISS**


---

## 📸 Screenshots

| Upload Resume & Enter Role                             | Chat Interview                                      |
| ------------------------------------------------------ | --------------------------------------------------- |
| ![Home](Images\home.png) | ![Chat Screen](Images\chat.png) |

---

## 🚀 Tech Stack

* [Streamlit](https://streamlit.io/)
* [LangChain](https://www.langchain.com/)
* [Groq LLM](https://groq.com/)
* [FAISS (Facebook AI Similarity Search)](https://github.com/facebookresearch/faiss)
* HuggingFace Sentence Transformers (`all-MiniLM-L6-v2`)

---

## 📂 Project Structure

```
📦 LangChain-Mock-Interview
 ┣ 📄 app.py
 ┣ 📂 Resume/
 ┣ 📄 requirements.txt
 ┗ 📄 README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/yourusername/langchain-mock-interview.git
cd langchain-mock-interview
```

### 2️⃣ (Recommended) Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

#### Sample `requirements.txt`

```txt
streamlit
langchain
langchain-community
langchain-huggingface
langchain-groq
faiss-cpu
sentence-transformers
```

---

## 🔑 How to Get Your Groq API Key

1. Go to [GroqCloud Console](https://console.groq.com/signup) and **sign up** (or log in if you already have an account).
2. Once signed in, navigate to the **API Keys** section:
   [https://console.groq.com/keys](https://console.groq.com/keys)
3. Click **Create API Key**, give it a name, and copy the generated key.
4. Keep it safe — you’ll need to input this in the Streamlit sidebar!

---

## ▶️ Running the Application

```bash
streamlit run app.py
```

### Using the App

1. Enter your **Groq API Key** in the sidebar.
2. Upload your **resume** (PDF format).
3. Enter your **target job role** (e.g., `GenAI Developer`).
4. The interview will start. Respond to the AI's questions in the chat box.
5. After 10 questions, the interview will end with a polite thank-you note.
