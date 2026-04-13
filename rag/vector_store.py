from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

def create_vector_store(docs):
    embeddings = OpenAIEmbeddings()

    db = Chroma.from_texts(docs, embeddings, persist_directory="./chroma_db")
    return db