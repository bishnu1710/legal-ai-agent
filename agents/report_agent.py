# @bishnu- legal_ai_agent report_agent.py

from utils.llm import call_llm
import re


def _detect_category(clause_name):
    name = clause_name.lower()
    if any(w in name for w in ["employ", "duties", "accept"]):
        return "Employment"
    elif any(w in name for w in ["pay", "salary", "bonus", "compensation", "expense", "vacation", "benefit"]):
        return "Payment"
    elif any(w in name for w in ["liabil", "insurance"]):
        return "Liability"
    elif any(w in name for w in ["terminat", "term of"]):
        return "Termination"
    elif any(w in name for w in ["confidential"]):
        return "Confidentiality"
    elif any(w in name for w in ["intellectual", "ip", "property"]):
        return "Intellectual Property"
    elif any(w in name for w in ["conflict", "interest", "transaction"]):
        return "Conflict of Interest"
    else:
        return "Other"


def _risk_badge(risk):
    r = risk.lower()
    if "high" in r:
        return "High"
    elif "medium" in r:
        return "Medium"
    else:
        return "Low"

def build_clause_table(risks_text, explanations_text):
    """Build table from explanations (always consistent) + match risk levels from risks_text."""

    # Extract risk levels from risks_text — scan for any mention of clause + risk
    risk_map = {}
    reason_map = {}

    current_key = None
    for line in risks_text.split("\n"):
        line = line.strip()

        # Match clause reference anywhere in line
        m = re.search(r'[Cc]lause\s+([\d\.]+)', line)
        if m:
            current_key = m.group(1).strip()

        if "Risk Level:" in line:
            risk = line.split("Risk Level:")[-1].strip().lstrip("-").strip()
            # Strip emoji if present
            risk = re.sub(r'[^\w\s]', '', risk).strip()
            if current_key:
                risk_map[current_key] = risk

        if "Reason:" in line and current_key:
            reason_map[current_key] = line.split("Reason:")[-1].strip().lstrip("-").strip()

        # Also handle inline format: "(Risk Level: Medium)"
        inline = re.search(r'Risk Level[:\s]+(?:🔴|🟠|🟢)?\s*(Low|Medium|High)', line)
        if inline and current_key:
            risk_map[current_key] = inline.group(1)

    # Parse clause names from explanations
    rows = []
    clause_pattern = re.compile(r'^([\d]+\.[\d]+)[:\s]+(.+)')

    for line in explanations_text.split("\n"):
        line = line.strip()
        if not line:
            continue

        m = clause_pattern.match(line)
        if m:
            clause_num = m.group(1).strip()
            clause_name = m.group(2).strip().rstrip('.:,-')
            risk = risk_map.get(clause_num, "Low")
            reason = reason_map.get(clause_num, "—")
            rows.append((f"Clause {clause_num}: {clause_name}", risk, reason))

    if not rows:
        return ""

    html_rows = ""
    for clause, risk, reason in rows:
        category = _detect_category(clause)
        risk_label = _risk_badge(risk) if risk else "Low"
        html_rows += (
            f"<tr>"
            f"<td>{clause}</td>"
            f"<td>{category}</td>"
            f"<td>{risk_label}</td>"
            f"<td>{reason if reason else '—'}</td>"
            f"</tr>"
        )

    return (
        "<table>"
        "<thead><tr>"
        "<th>Clause</th><th>Category</th><th>Risk Level</th><th>Key Issue</th>"
        "</tr></thead>"
        f"<tbody>{html_rows}</tbody>"
        "</table>"
    )


def report_agent(state):
    risks_text = state["risks"][0] if state["risks"] else ""
    explanations_text = state["explanations"][0] if state["explanations"] else ""

    # Build table from explanations + risk levels — not dependent on risk format
    clause_table = build_clause_table(risks_text, explanations_text)

    prompt = f"""
Generate a professional legal report using ONLY the data provided below.

STRICT RULES:
- Do NOT include Case Number, Date, To, From, or Signature fields
- Do NOT use placeholder text like "Insert..." or "N/A"
- Do NOT add authentication or certificate sections
- Do NOT generate any table — the table is handled separately
- Start directly with the report title and summary
- Use only facts from the data below

DATA:

Classifications:
{state['classification']}

Risks:
{state['risks']}

Compliance:
{state['compliance_issues']}

Explanations:
{state['explanations']}

OUTPUT FORMAT:

## Legal Analysis Report

### Summary
(2-3 sentences overview of the contract)

### Compliance Issues
(list missing clauses and issues found)

### Recommendations
(actionable steps to fix the issues)
"""

    report = call_llm(prompt, max_tokens=2000)

    # Inject table after Summary, before Compliance
    if clause_table:
        if "### Compliance" in report:
            report = report.replace(
                "### Compliance",
                f"### Clause Analysis Table\n{clause_table}\n\n### Compliance"
            )
        else:
            report = report + f"\n\n### Clause Analysis Table\n{clause_table}"

    return {"final_report": report}