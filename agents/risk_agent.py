from rag.memory_store import retrieve_similar_contracts
from utils.llm import call_llm

def risk_agent(state):
    # ✅ GET CLAUSES
    clauses = state["clauses"]

    # 🔥 LIMIT CLAUSES (PUT IT HERE)
    clauses = clauses[:8]

    # Combine clauses
    clauses_text = "\n".join(
        [f"{i+1}. {c}" for i, c in enumerate(clauses)]
    )

    # Retrieve memory once
    context = "\n".join(
        retrieve_similar_contracts(clauses_text)
    )

    prompt = f"""
You are a legal risk analyst.

TASK:
Analyze ALL clauses and return structured output.

CLAUSES:
{clauses_text}

SIMILAR PAST CLAUSES:
{context}

OUTPUT FORMAT:
1. Clause number → Risk Level (Low/Medium/High) + Reason
"""

    result = call_llm(prompt)

    return {"risks": [result]}