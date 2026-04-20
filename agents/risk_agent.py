# @bishnu- legal_ai_agent risk_agent.py

from rag.memory_store import retrieve_similar_contracts
from utils.llm import call_llm

def risk_agent(state):
    clauses = state["clauses"][:8]

    clauses_text = "\n".join(
        [f"{i+1}. {c}" for i, c in enumerate(clauses)]
    )

    context = "\n".join(
        retrieve_similar_contracts(clauses_text)
    )

    # Build dynamic example from first 2 actual clauses
    example_lines = []
    for i, c in enumerate(clauses[:2]):
        short_name = c[:60].strip()
        risk = "Medium" if i == 0 else "Low"
        example_lines.append(
            f"{i+1}. Clause {i+1}.1: {short_name}\n"
            f"- Risk Level: {risk}\n"
            f"- Reason: One sentence explanation."
        )
    example = "\n\n".join(example_lines)

    prompt = f"""
You are a legal risk analyst. Analyze each clause below.

OUTPUT RULES — follow this exact format for every clause, no exceptions:

{example}

(continue for every clause in the same format)

DO NOT group clauses together.
DO NOT write summaries, headers, or structured outputs.
DO NOT write multiple clause numbers on one line like "Clause 1.1, 1.2, 1.4".
EVERY clause gets its OWN numbered entry with its OWN Risk Level and Reason.

CLAUSES TO ANALYZE:
{clauses_text}

SIMILAR PAST CLAUSES:
{context}
"""

    result = call_llm(prompt, max_tokens=800)
    return {"risks": [result]}