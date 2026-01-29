"""
Bank Australia eStatement Parser for FY24-25
Extracts transactions from PDF statements
"""

import fitz
import re
import csv
from pathlib import Path
from datetime import datetime

def parse_bank_australia_statement(pdf_path):
    """Parse a Bank Australia eStatement PDF and extract transactions."""
    pdf = fitz.open(pdf_path)
    transactions = []
    
    # Extract statement date from filename (e.g., "eStatement - Jul 2024.pdf")
    filename = Path(pdf_path).name
    month_year_match = re.search(r'eStatement - (\w+) (\d{4})', filename)
    if month_year_match:
        month_str = month_year_match.group(1)
        year = int(month_year_match.group(2))
        # Map month names to numbers
        month_map = {
            'Jan': 1, 'Feb': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
            'Jul': 7, 'Aug': 8, 'Sept': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
        }
        statement_month = month_map.get(month_str, 1)
    else:
        statement_month = 1
        year = 2024
    
    current_account = None
    
    # Month abbreviation to number mapping
    month_map_abbrev = {
        'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
        'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
    }
    
    for page in pdf:
        text = page.get_text()
        lines = text.split('\n')
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Detect account section
            if 'Account: 12350422 Everyday Access' in line:
                current_account = 'Everyday Access'
                i += 1
                continue
            elif 'Account: 12350423 Bonus Saver' in line:
                current_account = 'Bonus Saver'
                i += 1
                continue
            
            # Skip non-transaction lines
            if not current_account:
                i += 1
                continue
            
            # Match date lines: " 1 Jul" or "10 Jul" (Effective date)
            date_match = re.match(r'^\s*(\d{1,2})\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s*$', line)
            
            if date_match:
                day = int(date_match.group(1))
                month_abbrev = date_match.group(2)
                txn_month = month_map_abbrev.get(month_abbrev, statement_month)
                
                # Handle year boundary
                if statement_month == 12 and txn_month == 1:
                    txn_year = year + 1
                elif statement_month == 1 and txn_month == 12:
                    txn_year = year - 1
                else:
                    txn_year = year
                
                try:
                    txn_date = datetime(txn_year, txn_month, day)
                except ValueError:
                    i += 1
                    continue
                
                # Look ahead: next line should be Posted date, then description, then amounts
                # Pattern: Effective date -> Posted date -> Description (may span lines) -> Amounts
                
                # Skip if next line is Opening/Closing Balance
                if i + 2 < len(lines) and ('Opening Balance' in lines[i + 2] or 'Closing Balance' in lines[i + 2]):
                    i += 1
                    continue
                
                # Collect the transaction data from following lines
                description_parts = []
                amounts = []
                j = i + 1
                
                # Skip posted date line (same format as effective date)
                if j < len(lines) and re.match(r'^\s*\d{1,2}\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s*$', lines[j]):
                    j += 1
                
                # Collect description and amount lines until we hit the next date or end
                while j < len(lines):
                    next_line = lines[j].strip()
                    
                    # Stop if we hit another date line (next transaction)
                    if re.match(r'^\s*\d{1,2}\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s*$', lines[j]):
                        break
                    
                    # Stop if we hit a new account section
                    if 'Account:' in next_line:
                        break
                    
                    # Check if this line is just an amount
                    amount_match = re.match(r'^([\d,]+\.\d{2})$', next_line)
                    if amount_match:
                        amounts.append(float(amount_match.group(1).replace(',', '')))
                        j += 1
                        continue
                    
                    # Otherwise it's part of description
                    if next_line and not next_line.startswith('*'):
                        description_parts.append(next_line)
                    
                    j += 1
                    
                    # Safety: don't collect more than 5 lines
                    if j - i > 6:
                        break
                
                description = ' '.join(description_parts).strip()
                
                # Skip if no description or amounts
                if not description or len(amounts) < 2:
                    i += 1
                    continue
                
                # Last amount is balance, second-to-last is transaction amount
                amount = amounts[-2] if len(amounts) >= 2 else amounts[0] if amounts else 0
                
                # Determine if debit or credit based on keywords
                credit_keywords = ['Direct Credit', 'Osko Payment From', 'Interest Credit', 
                                   'Bonus Interest', 'Transfer From', 'Cashrewards', 'Mcare Benefits']
                is_credit = any(kw.lower() in description.lower() for kw in credit_keywords)
                
                if not is_credit:
                    amount = -amount  # Negative for debits (expenses)
                
                if description and amount != 0:
                    transactions.append({
                        'date': txn_date.strftime('%Y-%m-%d'),
                        'description': description,
                        'amount': amount,
                        'account': current_account,
                        'source': 'Bank Australia'
                    })
                
                i = j  # Jump to where we left off
            else:
                i += 1
    
    return transactions


def parse_all_statements(folder_path):
    """Parse all Bank Australia statements in a folder."""
    folder = Path(folder_path)
    all_transactions = []
    
    for pdf_file in sorted(folder.glob('eStatement - *.pdf')):
        print(f"Processing: {pdf_file.name}")
        transactions = parse_bank_australia_statement(str(pdf_file))
        all_transactions.extend(transactions)
        print(f"  Found {len(transactions)} transactions")
    
    return all_transactions


def main():
    import sys
    
    base_path = Path(__file__).parent.parent
    statement_folder = base_path / 'Bank statements' / 'FY24-25' / 'Bank Australia'
    output_folder = base_path / '5. Bank Statements' / 'Analysis'
    
    print("=" * 60)
    print("Bank Australia Statement Parser")
    print("=" * 60)
    
    # Parse all statements
    transactions = parse_all_statements(statement_folder)
    
    print(f"\nTotal transactions extracted: {len(transactions)}")
    
    # Filter to FY24-25 only (1 Jul 2024 - 30 Jun 2025)
    fy_transactions = [
        t for t in transactions
        if '2024-07-01' <= t['date'] <= '2025-06-30'
    ]
    
    print(f"FY24-25 transactions: {len(fy_transactions)}")
    
    # Save to CSV
    output_folder.mkdir(parents=True, exist_ok=True)
    output_file = output_folder / 'bank_australia_transactions.csv'
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['date', 'description', 'amount', 'account', 'source'])
        writer.writeheader()
        writer.writerows(sorted(fy_transactions, key=lambda x: x['date']))
    
    print(f"\nSaved to: {output_file}")
    
    # Print summary
    debits = sum(t['amount'] for t in fy_transactions if t['amount'] < 0)
    credits = sum(t['amount'] for t in fy_transactions if t['amount'] > 0)
    
    print(f"\nSummary:")
    print(f"  Total debits (expenses): ${abs(debits):,.2f}")
    print(f"  Total credits (income): ${credits:,.2f}")


if __name__ == '__main__':
    main()
