import re, json
from collections import Counter
from typing import List

DEFAULT_SKILLS = [
    "ci/cd","github actions","azure devops","jenkins","terraform","kubernetes",
    "python","c#","observability","dynatrace","splunk","microservices","testing","mentoring",
    "aws","azure","secrets","security","rbac","encryption","docker","ansible","prometheus",
    "grafana","elasticsearch","redis","postgresql","mongodb","react","angular","vue",
    "node.js","typescript","javascript","java","golang","rust","ruby","php",
    "machine learning","artificial intelligence","data science","agile","scrum","kanban",
    "rest api","graphql","grpc","oauth","jwt","ssl","tls","vpc","s3","ec2","lambda",
    "cloudformation","helm","istio","service mesh","api gateway","load balancer"
]

def normalize(txt:str)->str:
    return re.sub(r"[^a-z0-9+/# ]+"," ",txt.lower())

def extract_keywords(jd_text:str, extra:List[str]=None)->List[str]:
    text = normalize(jd_text)
    tokens = text.split()

    # Combine default skills with any extras
    skills = DEFAULT_SKILLS + (extra or [])

    # Sort skills by length (longest first) to match multi-word phrases first
    skills_sorted = sorted(set(skills), key=len, reverse=True)

    found = []
    for s in skills_sorted:
        if s in text and s not in found:
            found.append(s)

    # Extract bigrams and trigrams for technical phrases
    bigrams = [f"{tokens[i]} {tokens[i+1]}" for i in range(len(tokens)-1)]
    trigrams = [f"{tokens[i]} {tokens[i+1]} {tokens[i+2]}" for i in range(len(tokens)-2)]

    # Count bigrams and trigrams
    bigram_counts = Counter(bigrams).most_common(10)
    trigram_counts = Counter(trigrams).most_common(5)

    # Add frequent multi-word phrases that aren't already in found
    for phrase, count in trigram_counts:
        if count >= 2 and phrase not in found and len(phrase) > 10:
            found.append(phrase)

    for phrase, count in bigram_counts:
        if count >= 2 and phrase not in found and len(phrase) > 8:
            found.append(phrase)

    # Add top frequent single tokens by heuristic length
    long_tokens = [t for t in tokens if len(t) > 4]
    counts = Counter(long_tokens).most_common(20)
    found += [w for w,_ in counts if w not in found]

    return list(dict.fromkeys(found))  # dedupe, keep order
