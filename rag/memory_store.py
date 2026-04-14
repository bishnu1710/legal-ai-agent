# @bishnu- legal_ai_agent memory_store.py

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

DB_PATH = "./memory_db"

def get_db():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    return Chroma(
        persist_directory=DB_PATH,
        embedding_function=embeddings
    )

def save_contract(text):
    db = get_db()
    db.add_texts([text])
    db.persist()

def retrieve_similar_contracts(query):
    db = get_db()

    try:
        results = db.similarity_search(query, k=2)
        return [r.page_content for r in results]
    except:
        return []