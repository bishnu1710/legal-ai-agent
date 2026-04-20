# @bishnu- legal_ai_agent compliance_agent.py

from utils.llm import call_llm

def compliance_agent(state):
    clauses = state["clauses"][:8]

    contract = "\n".join(clauses)

    prompt = f"""
Check this contract for compliance issues.

Required clauses:
- Termination
- Payment
- Liability
- Confidentiality

RULES:
- Read each clause carefully before flagging it as an issue
- Only flag something as missing if it is truly absent
- Do not misrepresent what a clause says

CONTRACT:
{contract}

OUTPUT:
- Missing clauses
- Issues found
"""

    result = call_llm(prompt)

    return {"compliance_issues": [result]}