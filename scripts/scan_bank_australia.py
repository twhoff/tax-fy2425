"""
Scan Bank Australia transactions for deductible items
"""
import csv

# Load transactions
transactions = []
with open('5. Bank Statements/Analysis/bank_australia_transactions.csv', 'r') as f:
    reader = csv.DictReader(f)
    transactions = list(reader)

# Keywords to look for (from tax_categories.py)
keywords = [
    'replit', '1password', 'github', 'copilot', 'chatgpt', 'openai', 'warp', 'medium', 
    'adobe', 'figma', 'slack', 'notion', 'dropbox', 'microsoft', 'aws', 'azure', 
    'heroku', 'vercel', 'netlify', 'digitalocean', 'beforesunset', 'openart',
    'linkedin', 'paramount', 'hayu', 'audible', 'youtube', 'netflix', 'stan', 
    'disney', 'prime video', 'spotify', 'hubbl', 'binge', 'apple tv',
    'officeworks', 'jb hi-fi', 'harvey norman', 'dell', 'logitech', 'samsung',
    'optus', 'telstra', 'vodafone', 'tpg', 'aussie broadband', 'iinet', 'belong', 'nbn',
    'bravehearts', 'unicef', 'cancer council', 'red cross', 'salvos', 'salvation army',
    'victorian arts', 'princess theatre', 'thecenteredlife', 'newyorker', 'condenast',
    'amberelectric', 'red energy'  # Utilities
]

print('Potentially Deductible Transactions in Bank Australia:')
print('=' * 80)

matches = []
for t in transactions:
    desc = t['description'].lower()
    for kw in keywords:
        if kw.lower() in desc:
            matches.append((t['date'], t['description'], t['amount'], kw))
            break

if matches:
    for date, desc, amt, keyword in sorted(matches):
        print(f'{date} | {desc[:50]:50} | ${float(amt):>10.2f} | ({keyword})')
else:
    print('No matches found.')

print()
print(f'Total matches: {len(matches)}')
