import cloudscraper
from bs4 import BeautifulSoup
import json

url = 'https://www.indeed.com/viewjob?jk=fcd29f6d7f5168f9'
print(f'Fetching and analyzing HTML structure...')
print()

scraper = cloudscraper.create_scraper()
response = scraper.get(url, timeout=15)
soup = BeautifulSoup(response.text, 'html.parser')

# Find title
title_tag = soup.find('h1')
print(f'Title (h1): {title_tag.get_text(strip=True) if title_tag else "NOT FOUND"}')

# Find all divs with 'description' in id or class
print()
print('Looking for description containers...')
desc_divs = soup.find_all('div', attrs={'id': lambda x: x and 'description' in x.lower()})
print(f'Found {len(desc_divs)} divs with "description" in id')

desc_divs = soup.find_all('div', attrs={'class': lambda x: x and 'description' in str(x).lower()})
print(f'Found {len(desc_divs)} divs with "description" in class')

# Try to find job description by looking for common keywords
print()
print('Looking for job description by keywords...')
all_text = soup.get_text()
if 'Responsibilities' in all_text or 'Requirements' in all_text:
    print('Found job description keywords in page')
else:
    print('No job description keywords found')

# Check for script tags with JSON data
print()
print('Looking for JSON data in script tags...')
scripts = soup.find_all('script', type='application/ld+json')
print(f'Found {len(scripts)} JSON-LD script tags')

if scripts:
    for i, script in enumerate(scripts[:2]):
        try:
            data = json.loads(script.string)
            print(f'Script {i}: {list(data.keys())[:5]}')
            if 'description' in data:
                print(f'  Description found: {data["description"][:200]}...')
        except:
            pass

# Look for specific Indeed job description patterns
print()
print('Looking for Indeed-specific patterns...')
# Try data attributes
job_desc = soup.find('div', attrs={'data-testid': 'jobDescription'})
if job_desc:
    print(f'Found jobDescription via data-testid')
    print(f'Content: {job_desc.get_text(strip=True)[:200]}...')
else:
    print('No jobDescription data-testid found')

# Try to find by looking for common job description text
print()
print('Searching for common job description text...')
for div in soup.find_all('div'):
    text = div.get_text(strip=True)
    if len(text) > 500 and any(kw in text for kw in ['Responsibilities', 'Requirements', 'Qualifications', 'Experience']):
        print(f'Found potential job description div')
        print(f'First 300 chars: {text[:300]}...')
        break

