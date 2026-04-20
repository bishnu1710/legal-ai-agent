from rag.retriever import get_relevant_docs

query = "employment agreement"

results = get_relevant_docs(query)

print("\n📚 Retrieved Docs:\n")
for r in results:
    print("-", r)