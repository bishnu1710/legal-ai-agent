# @bishnu- legal_ai_agent parser.py

import re

def parser_agent(state):
    text = state["document"]

    #Better clause splitting using regex
    clauses = re.split(r'\.\s+|\n+', text)

    clauses = [c.strip() for c in clauses if len(c.strip()) > 20]

    return {"clauses": clauses}