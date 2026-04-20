# @bishnu- legal_ai_agent vector_store.py

from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

DB_PATH = "./chroma_db"

def create_vector_store(docs):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    db = Chroma.from_texts(docs, embeddings, persist_directory=DB_PATH)
    return db