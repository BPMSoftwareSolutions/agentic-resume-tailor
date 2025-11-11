#!/usr/bin/env python3
import json

idx = json.load(open('data/resumes/index.json'))
print(f'Total resumes: {len(idx["resumes"])}\n')

for r in idx['resumes']:
    print(f'{r["id"]}: {r["name"]}')

