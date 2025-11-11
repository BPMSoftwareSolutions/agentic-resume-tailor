#!/usr/bin/env python3
import json

data = json.load(open('data/resumes/8630031a-5870-4c7f-a3a9-ee4cb035493e.json'))
print(f'Total experiences: {len(data["experience"])}')
for i, exp in enumerate(data['experience'], 1):
    print(f'  {i}. {exp.get("employer", "N/A")}')

