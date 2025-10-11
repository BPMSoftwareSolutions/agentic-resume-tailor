import re
def rewrite_star(text:str)->str:
    """Tiny heuristic rewrite to emphasize impact and outcome."""
    t = text.strip()
    # ensure past-tense action starts
    t = re.sub(r'^(Led|Build|Design|Introduce|Manage)', lambda m: m.group(0)+'', t)
    # add impact clause if missing punctuation
    if not t.endswith('.'):
        t += '.'

    # Check if bullet already has quantified results or impact language
    has_quantified_result = (
        '%' in t or
        'reduc' in t.lower() or
        'improv' in t.lower() or
        'increas' in t.lower() or
        'accelerat' in t.lower() or
        'cut' in t.lower() or
        'enabling' in t.lower() or
        re.search(r'\d+[xX]', t) or  # e.g., "2x faster"
        re.search(r'\d+\s*(hour|day|week|month|year)', t, re.IGNORECASE) or
        'from' in t.lower() and 'to' in t.lower()  # e.g., "from days to hours"
    )

    # Only add generic impact if bullet lacks quantified results
    if not has_quantified_result:
        t = t.replace('.', ' — improved reliability and delivery speed.', 1)
    return t
