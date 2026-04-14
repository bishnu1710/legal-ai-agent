# @bishnu- legal_ai_agent explanation_agent.py

from utils.llm import call_llm

def explanation_agent(state):
    clauses = state["clauses"][:15]

    clauses_text = "\n".join(
        [f"{i+1}. {c}" for i, c in enumerate(clauses)]
    )

    prompt = f"""
Explain each clause in simple English (1–2 lines):

CLAUSES:
{clauses_text}

OUTPUT:
1. Clause number → Explanation
"""

    result = call_llm(prompt)

    return {"explanations": [result]}