import os
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain_community.document_loaders import PyPDFLoader

merged_file_path = r"C:\\Users\\USER\\Documents\\ollamamodel\\College_Info.pdf"

# Load the merged document
docs = []
try:
    loader = PyPDFLoader(merged_file_path)
    docs = loader.load()
    print(f"Loaded merged content from: {os.path.basename(merged_file_path)}")
except Exception as e:
    print(f"Failed to load merged content: {e}")
    exit()


splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
split_docs = splitter.split_documents(docs)

embedding = OllamaEmbeddings(model="nomic-embed-text")
db = FAISS.from_documents(split_docs, embedding)

index_path = os.path.join(os.path.dirname(merged_file_path), "college-index")
db.save_local(index_path)
print(f"Vector index saved in: {index_path}")
