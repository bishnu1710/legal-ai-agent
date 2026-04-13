from utils.llm import call_llm

def report_agent(state):
    prompt = f"""
Generate a professional legal report.

DATA:

Classifications:
{state['classification']}

Risks:
{state['risks']}

Compliance:
{state['compliance_issues']}

Explanations:
{state['explanations']}

OUTPUT:
- Summary
- Key Risks
- Compliance Issues
- Recommendations
"""

    report = call_llm(prompt)

    return {"final_report": report}