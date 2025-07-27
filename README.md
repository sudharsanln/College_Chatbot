# College_Chatbot

An interactive, AI-powered chatbot that answers queries using only college-specific data. Built as a full-stack application with a custom knowledge base and natural language processing capabilities.

---

## 🚀 Features

- 🔎 **Retrieval-Augmented Generation (RAG)** using LangChain and FAISS
- 💬 **Locally hosted LLM** with Ollama (TinyLlama)
- 🧱 **Frontend** built with React and TailwindCSS
- 🧠 Context-aware query flow with memory and follow-up support
- 🗃️ Fully offline, private knowledge base built from scraped college content

---

## 🛠️ Tech Stack

- **Frontend**: React, TailwindCSS, ShadCN, Vite
- **Backend**: FastAPI, LangChain, FAISS, Ollama
- **Data Pipeline**: Python scripts (`scrape.py`, `index.py`) for ingesting and indexing content

## 📂 Project Structure
├── backend/
│ ├── scrape.py # Web scraping college content
│ ├── index.py # Build FAISS vector store
│ ├── chatbot.py # Chat endpoint using LangChain + Ollama
│ └── ...
├── frontend/
│ ├── src/
│ │ ├── App.jsx
│ │ ├── components/
│ │ └── ...
│ └── ...
├── README.md
└── requirements.txt


---

## 🧪 How to Run Locally

### 1. Clone the repository

```
git clone https://github.com/your-username/college-chatbot.git
cd college-chatbot
```

### 2. Install backend requirements
```
cd backend
pip install -r requirements.txt
```

### 3. Start Ollama
```
ollama run tinyllama
```

### 4. Launch backend
```
uvicorn chatbot:app --reload
```

### 5. Run frontend
```
cd frontend
npm install
npm run dev
```

## 📌 Notes
- Responses are based only on college-specific data.
- No external knowledge is included by design.
- Easily extensible for other institutions or domains.
