# @bishnu- retriever.py

from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

def get_relevant_docs(query):
    db = Chroma(persist_directory="./chroma_db", embedding_function=OpenAIEmbeddings())
    return db.similarity_search(query, k=3)