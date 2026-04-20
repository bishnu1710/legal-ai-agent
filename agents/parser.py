# @bishnu- legal_ai_agent parser.py

import re
from utils.helpers import limit_clauses

def parser_agent(state):
    text = state["document"]

    # Step 1: try splitting on numbered sections (1. / 2. / (a) / Section 1)
    numbered = re.split(r'\n\s*(?:Section\s+\d+[\.\:]|\d+[\.\)]\s+|\([a-zA-Z]\)\s+)', text)

    if len(numbered) >= 3:
        clauses = numbered
    else:
        # Step 2: fallback — split on double newlines (paragraph breaks)
        clauses = re.split(r'\n{2,}', text)

    # Step 3: clean and filter short fragments
    clauses = [c.strip() for c in clauses if len(c.strip()) > 60 and not c.strip().upper().startswith("EXHIBIT")]

    # Step 4: cap total chars sent to agents
    clauses = limit_clauses(clauses, max_chars=4000, max_clauses=20)

    return {"clauses": clauses}