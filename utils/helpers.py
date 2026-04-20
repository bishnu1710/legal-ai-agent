def limit_clauses(clauses, max_chars=4000, max_clauses=20):
    selected = []
    total = 0

    for c in clauses[:max_clauses]:
        if total + len(c) > max_chars:
            break
        selected.append(c)
        total += len(c)

    return selected