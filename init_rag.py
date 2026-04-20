from rag.vector_store import create_vector_store

docs = [
    "This confidentiality clause protects sensitive information between parties.",
    "The termination clause defines how either party can end the agreement.",
    "The liability clause limits damages and legal responsibility.",
    "Payment terms specify salary, invoices, and penalties.",
    "Non-disclosure agreements prevent sharing of confidential data.",
    "Employment agreement defines roles, salary, and responsibilities.",
]

create_vector_store(docs)

print("✅ RAG database created!")