"""
Comprehensive Deduction Analysis for FY24-25
Processes ANZ and Bank Australia transactions with updated tax_categories.py
"""

import csv
from pathlib import Path
from collections import defaultdict
from tax_categories import TAX_CATEGORIES, categorise_transaction

BASE_PATH = Path(__file__).parent.parent
ANALYSIS_PATH = BASE_PATH / '5. Bank Statements' / 'Analysis'


def load_anz_transactions():
    """Load ANZ credit card transactions from all_transactions.csv"""
    transactions = []
    csv_path = ANALYSIS_PATH / 'all_transactions.csv'
    
    if not csv_path.exists():
        print(f"Warning: {csv_path} not found")
        return transactions
    
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # ANZ format: date_transaction, description, amount, ...
            desc = row.get('description', '')
            amt_str = row.get('amount', '0')
            try:
                amt = float(amt_str) if amt_str else 0
            except ValueError:
                amt = 0
            
            # ANZ amounts in CSV are positive for purchases - make negative for expenses
            transactions.append({
                'date': row.get('date_transaction', ''),
                'description': desc,
                'amount': -abs(amt),  # Expenses as negative
                'source': 'ANZ Credit Card'
            })
    
    return transactions


def load_bank_australia_transactions():
    """Load Bank Australia transactions"""
    transactions = []
    csv_path = ANALYSIS_PATH / 'bank_australia_transactions.csv'
    
    if not csv_path.exists():
        print(f"Warning: {csv_path} not found")
        return transactions
    
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            transactions.append({
                'date': row['date'],
                'description': row['description'],
                'amount': float(row['amount']),
                'source': f"Bank Australia ({row['account']})"
            })
    
    return transactions


def analyse_transactions(transactions):
    """Categorise all transactions and identify deductibles."""
    results = {
        'deductible': [],
        'income': [],
        'excluded': [],
        'unclassified': []
    }
    
    category_totals = defaultdict(lambda: {'count': 0, 'gross': 0, 'deductible': 0})
    
    for txn in transactions:
        cat_result = categorise_transaction(txn['description'], txn['amount'])
        
        # Create record with original transaction description preserved
        record = {
            'date': txn['date'],
            'transaction_description': txn['description'],  # Original description
            'amount': txn['amount'],
            'source': txn['source'],
            'category': cat_result['category'],
            'category_description': cat_result['description'],  # Category description
            'default_owner': cat_result['default_owner'],
            'work_use_percent': cat_result['work_use_percent'],
            'is_income': cat_result['is_income'],
            'is_deductible': cat_result['is_deductible'],
            'notes': cat_result['notes'],
            'matched_keyword': cat_result['matched_keyword']
        }
        
        # Calculate deductible amount
        if cat_result['is_deductible'] and txn['amount'] < 0:  # Expenses are negative
            gross = abs(txn['amount'])
            deductible = gross * (cat_result['work_use_percent'] / 100)
            record['gross_amount'] = gross
            record['deductible_amount'] = deductible
            results['deductible'].append(record)
            
            cat = cat_result['category']
            category_totals[cat]['count'] += 1
            category_totals[cat]['gross'] += gross
            category_totals[cat]['deductible'] += deductible
            
        elif cat_result['is_income'] and txn['amount'] > 0:
            results['income'].append(record)
        elif cat_result['category'] in ['personal_not_deductible', 'childcare_family', 'health_insurance']:
            results['excluded'].append(record)
        elif cat_result['category'] == 'unclassified':
            results['unclassified'].append(record)
    
    return results, category_totals


def main():
    print("=" * 70)
    print("FY24-25 Comprehensive Deduction Analysis")
    print("=" * 70)
    
    # Load all transactions
    print("\nLoading transactions...")
    anz_txns = load_anz_transactions()
    ba_txns = load_bank_australia_transactions()
    
    all_txns = anz_txns + ba_txns
    print(f"  ANZ Credit Card: {len(anz_txns)} transactions")
    print(f"  Bank Australia:  {len(ba_txns)} transactions")
    print(f"  Total:           {len(all_txns)} transactions")
    
    # Analyse
    print("\nAnalysing transactions...")
    results, category_totals = analyse_transactions(all_txns)
    
    # Summary
    print("\n" + "=" * 70)
    print("DEDUCTION SUMMARY BY CATEGORY")
    print("=" * 70)
    print(f"{'Category':<30} {'Count':>6} {'Gross':>12} {'Work %':>8} {'Deductible':>12}")
    print("-" * 70)
    
    total_gross = 0
    total_deductible = 0
    
    for cat, totals in sorted(category_totals.items()):
        config = TAX_CATEGORIES.get(cat, {})
        work_pct = config.get('work_use_percent', 100)
        
        print(f"{cat:<30} {totals['count']:>6} ${totals['gross']:>10.2f} {work_pct:>7}% ${totals['deductible']:>10.2f}")
        total_gross += totals['gross']
        total_deductible += totals['deductible']
    
    print("-" * 70)
    print(f"{'TOTAL':<30} {sum(t['count'] for t in category_totals.values()):>6} ${total_gross:>10.2f}          ${total_deductible:>10.2f}")
    
    # Owner breakdown
    print("\n" + "=" * 70)
    print("DEDUCTIONS BY OWNER")
    print("=" * 70)
    
    owner_totals = defaultdict(lambda: {'gross': 0, 'deductible': 0})
    for txn in results['deductible']:
        owner = txn['default_owner']
        owner_totals[owner]['gross'] += txn['gross_amount']
        owner_totals[owner]['deductible'] += txn['deductible_amount']
    
    for owner, totals in sorted(owner_totals.items()):
        print(f"  {owner}: ${totals['deductible']:.2f} (from ${totals['gross']:.2f} gross)")
    
    # Save detailed deductions to CSV
    output_file = ANALYSIS_PATH / 'deductible_transactions_v2.csv'
    with open(output_file, 'w', newline='') as f:
        fieldnames = ['date', 'transaction_description', 'source', 'category', 'default_owner', 
                      'work_use_percent', 'gross_amount', 'deductible_amount', 'notes']
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        for txn in sorted(results['deductible'], key=lambda x: x['date']):
            row = {
                'date': txn['date'],
                'transaction_description': txn['transaction_description'],  # Original transaction description
                'source': txn['source'],
                'category': txn['category'],
                'default_owner': txn['default_owner'],
                'work_use_percent': txn['work_use_percent'],
                'gross_amount': txn['gross_amount'],
                'deductible_amount': txn['deductible_amount'],
                'notes': txn['notes']
            }
            writer.writerow(row)
    
    print(f"\nDetailed deductions saved to: {output_file}")
    
    # Print high-value items for review
    print("\n" + "=" * 70)
    print("HIGH-VALUE DEDUCTIONS (>$100) - VERIFY RECEIPTS")
    print("=" * 70)
    
    high_value = [t for t in results['deductible'] if t['gross_amount'] >= 100]
    for txn in sorted(high_value, key=lambda x: -x['gross_amount']):
        print(f"  {txn['date']} | ${txn['gross_amount']:.2f} | {txn['transaction_description'][:40]} | {txn['category']}")
    
    # Print unclassified for review
    if results['unclassified']:
        print("\n" + "=" * 70)
        print(f"UNCLASSIFIED TRANSACTIONS ({len(results['unclassified'])} items)")
        print("(Review for potential deductions)")
        print("=" * 70)
        
        # Only show expenses over $50
        notable = [t for t in results['unclassified'] if t['amount'] < -50]
        for txn in sorted(notable, key=lambda x: x['amount'])[:20]:
            print(f"  {txn['date']} | ${abs(txn['amount']):.2f} | {txn['transaction_description'][:50]}")
    
    # Final summary
    print("\n" + "=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)
    print(f"  Total Deductible (work portion): ${total_deductible:,.2f}")
    print(f"  Total Gross Expenses:            ${total_gross:,.2f}")
    print(f"  Deductible Transactions:         {len(results['deductible'])}")
    print(f"  Unclassified (needs review):     {len(results['unclassified'])}")
    
    # CCS impact reminder
    print("\n⚠️  CCS REMINDER:")
    print("  Target: $4,000+ deductions to stay under $367,563 threshold")
    print(f"  Current Thomas deductions: ${owner_totals.get('Thomas', {}).get('deductible', 0):,.2f}")


if __name__ == '__main__':
    main()
