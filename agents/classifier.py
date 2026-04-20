# @bishnu- legal_ai_agent classifier.py

from utils.llm import call_llm

def classifier_agent(state):
    clauses = state["clauses"][:8]

    clauses_text = "\n".join(
        [f"{i+1}. {c}" for i, c in enumerate(clauses)]
    )

    prompt = f"""
Classify each clause into one category:

Options:
- Payment
- Liability
- Confidentiality
- Termination
- Intellectual Property
- Other

CLAUSES:
{clauses_text}

OUTPUT (use ONLY these exact category names — no combinations):
1. Clause number → Category
"""

    result = call_llm(prompt)

    return {"classification": [result]}