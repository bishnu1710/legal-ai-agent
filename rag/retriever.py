# @bishnu- legal_ai_agent memory_store.py

from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

DB_PATH = "./chroma_db"

def get_db():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    return Chroma(
        persist_directory=DB_PATH,
        embedding_function=embeddings
    )

def save_contract(text):
    db = get_db()
    db.add_texts([text])
    # db.persist() removed in chromadb >= 0.4 — persistence is automatic

def retrieve_similar_contracts(query):
    db = get_db()
    try:
        results = db.similarity_search(query, k=2)
        return [r.page_content for r in results]
    except Exception as e:
        print(f"[memory_store] retrieval failed: {e}")
        return []