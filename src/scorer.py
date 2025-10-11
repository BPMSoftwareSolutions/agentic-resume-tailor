from typing import List, Dict
import re

def score_bullets(bullets:List[Dict], keywords:List[str])->List[Dict]:
    def score(b):
        text = b.get("text", "").lower()
        tags = [t.lower() for t in b.get("tags", [])]

        # Score based on keyword matches in text (primary scoring)
        text_hits = 0
        for keyword in keywords:
            # Count exact phrase matches in text
            if keyword in text:
                # Give higher weight to longer, more specific keywords
                weight = 1.0 + (len(keyword.split()) - 1) * 0.5
                text_hits += weight

        # Score based on keyword matches in tags (secondary scoring)
        tag_hits = sum(1 for t in tags if any(k in t for k in keywords))

        # Bonus for quantified results (numbers, percentages, time savings)
        quantified_bonus = 0
        if re.search(r'\d+%', text):  # percentage
            quantified_bonus += 1.0
        if re.search(r'\d+[xX]', text):  # multiplier like "2x"
            quantified_bonus += 1.0
        if re.search(r'from .+ to .+', text):  # improvement range
            quantified_bonus += 0.5
        if re.search(r'\d+\s*(hour|day|week|month|year|team)', text):  # time/scale
            quantified_bonus += 0.5

        # Slight length bonus for complete, detailed statements
        length_bonus = 0.3 if len(text) > 70 else 0

        # Combined score: text matches are weighted highest
        total_score = (text_hits * 2.0) + (tag_hits * 1.0) + quantified_bonus + length_bonus

        return total_score

    scored = [{**b, "_score": score(b)} for b in bullets]
    return sorted(scored, key=lambda x: x["_score"], reverse=True)
