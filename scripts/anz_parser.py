"""
ANZ Credit Card Statement Parser for FY24-25
Extracts transactions from ANZ Frequent Flyer Black statements
"""

import fitz
import re
import csv
from pathlib import Path
from datetime import datetime
from tax_categories import categorise_transaction, is_foreign_currency, is_high_value

# ANZ statement folder
STATEMENTS_DIR = Path("5. Bank Statements/FY24-25")
OUTPUT_DIR = Path("5. Bank Statements/Analysis")

# FY24-25 date range
FY_START = datetime(2024, 7, 1)
FY_END = datetime(2025, 6, 30)

# Patterns for parsing line-by-line format
DATE_PATTERN = re.compile(r'^(\d{2}/\d{2}/\d{4})\s*$')
CARD_PATTERN = re.compile(r'^(\d{4})\s*$')
AMOUNT_PATTERN = re.compile(r'^\$?([\d,]+\.\d{2})\s*$')

# Foreign currency line pattern
FOREIGN_PATTERN = re.compile(r'([\d.]+)\s+(USD|EUR|GBP|NZD)')

# Card numbers and their owners (from statement)
CARD_OWNERS = {
    "5200": "Thomas",  # Primary card
    "5218": "Isabelle"  # Additional card (from transaction patterns)
}


def parse_amount(amount_str: str) -> float:
    """Parse amount string to float, removing commas and $."""
    return float(amount_str.replace(',', '').replace('$', ''))


def parse_date(date_str: str) -> datetime:
    """Parse date string DD/MM/YYYY to datetime."""
    return datetime.strptime(date_str, "%d/%m/%Y")


def is_in_fy(date: datetime) -> bool:
    """Check if date is within FY24-25."""
    return FY_START <= date <= FY_END


def extract_transactions_from_pdf(pdf_path: Path) -> list[dict]:
    """Extract all transactions from an ANZ statement PDF.
    
    ANZ statements have data in columns that extract as separate lines:
    Line 1: Date Processed (DD/MM/YYYY)
    Line 2: Date of Transaction (DD/MM/YYYY) 
    Line 3: Card Used (4 digits)
    Line 4: Transaction Description
    Line 5: Amount ($X.XX)
    Line 6: Balance ($X.XX)
    
    Some transactions have continuation lines for foreign currency.
    """
    transactions = []
    doc = fitz.open(pdf_path)
    
    for page_num in range(len(doc)):
        text = doc[page_num].get_text()
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        
        # State machine to parse transactions
        i = 0
        while i < len(lines) - 5:  # Need at least 6 lines for a transaction
            line = lines[i]
            
            # Look for date pattern to start a transaction
            date_match = DATE_PATTERN.match(line)
            if not date_match:
                i += 1
                continue
            
            date_processed = date_match.group(1)
            
            # Check next line is also a date (transaction date)
            if i + 1 >= len(lines):
                i += 1
                continue
            date_tx_match = DATE_PATTERN.match(lines[i + 1])
            if not date_tx_match:
                i += 1
                continue
            
            date_transaction = date_tx_match.group(1)
            
            # Check for card number
            if i + 2 >= len(lines):
                i += 1
                continue
            card_match = CARD_PATTERN.match(lines[i + 2])
            if not card_match:
                i += 1
                continue
            
            card_used = card_match.group(1)
            
            # Description is next
            if i + 3 >= len(lines):
                i += 1
                continue
            description = lines[i + 3]
            
            # Skip header rows
            if description in ['Transaction Details', 'Amount ($A)', 'Balance']:
                i += 1
                continue
            
            # Amount
            if i + 4 >= len(lines):
                i += 1
                continue
            amount_match = AMOUNT_PATTERN.match(lines[i + 4])
            if not amount_match:
                i += 1
                continue
            
            amount = parse_amount(amount_match.group(1))
            
            # Balance
            if i + 5 >= len(lines):
                i += 1
                continue
            balance_match = AMOUNT_PATTERN.match(lines[i + 5])
            if not balance_match:
                i += 1
                continue
            
            balance = parse_amount(balance_match.group(1))
            
            # Skip non-transactions (fees sometimes have different patterns)
            if 'INCL OVERSEAS' in description:
                i += 6
                continue
            
            try:
                tx_date = parse_date(date_transaction)
            except ValueError:
                i += 1
                continue
            
            # Only include FY24-25 transactions
            if not is_in_fy(tx_date):
                i += 6
                continue
            
            # Determine card owner
            owner = CARD_OWNERS.get(card_used, "Unknown")
            
            tx = {
                "date_processed": date_processed,
                "date_transaction": date_transaction,
                "card_used": card_used,
                "owner": owner,
                "description": description,
                "amount": amount,
                "balance": balance,
                "foreign_currency": None,
                "source_file": pdf_path.name
            }
            
            # Check for foreign currency on following lines
            if i + 6 < len(lines):
                fc_match = FOREIGN_PATTERN.search(lines[i + 6])
                if fc_match:
                    tx["foreign_currency"] = f"{fc_match.group(1)} {fc_match.group(2)}"
            
            transactions.append(tx)
            i += 6  # Move past this transaction
    
    doc.close()
    return transactions


def process_all_statements() -> list[dict]:
    """Process all ANZ statements in the folder."""
    all_transactions = []
    
    for pdf_file in sorted(STATEMENTS_DIR.glob("*ANZ*.pdf")):
        print(f"Processing: {pdf_file.name}")
        transactions = extract_transactions_from_pdf(pdf_file)
        all_transactions.extend(transactions)
        print(f"  Found {len(transactions)} transactions")
    
    # Remove duplicates (statements overlap by a few days)
    seen = set()
    unique_transactions = []
    for tx in all_transactions:
        key = (tx["date_transaction"], tx["description"], tx["amount"])
        if key not in seen:
            seen.add(key)
            unique_transactions.append(tx)
    
    print(f"\nTotal unique transactions: {len(unique_transactions)}")
    return unique_transactions


def categorise_all_transactions(transactions: list[dict]) -> list[dict]:
    """Add tax category information to all transactions."""
    for tx in transactions:
        cat_info = categorise_transaction(tx["description"], tx["amount"])
        tx["category"] = cat_info["category"]
        tx["category_description"] = cat_info["description"]
        tx["is_deductible"] = cat_info["is_deductible"]
        tx["is_income"] = cat_info.get("is_income", False)
        tx["work_use_percent"] = cat_info["work_use_percent"]
        tx["category_notes"] = cat_info["notes"]
        tx["matched_keyword"] = cat_info["matched_keyword"]
        tx["is_foreign"] = is_foreign_currency(tx["description"]) or tx["foreign_currency"] is not None
        tx["is_high_value"] = is_high_value(tx["amount"])
        
        # Override owner if category has specific owner
        default_owner = cat_info.get("default_owner", "unknown")
        if default_owner not in ["check_card", "check_description", "shared", "unknown"]:
            tx["category_owner"] = default_owner
        else:
            tx["category_owner"] = tx["owner"]  # Use card owner
    
    return transactions


def export_to_csv(transactions: list[dict], filename: str = "all_transactions.csv"):
    """Export transactions to CSV for review."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / filename
    
    fieldnames = [
        "date_transaction", "description", "amount", "owner", "category",
        "is_deductible", "work_use_percent", "category_owner", "is_high_value",
        "is_foreign", "foreign_currency", "matched_keyword", "source_file"
    ]
    
    with open(output_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(transactions)
    
    print(f"\nExported to: {output_path}")
    return output_path


def generate_deductible_summary(transactions: list[dict]) -> dict:
    """Generate summary of deductible transactions."""
    summary = {
        "Thomas": {"transactions": [], "total": 0.0, "adjusted_total": 0.0},
        "Isabelle": {"transactions": [], "total": 0.0, "adjusted_total": 0.0},
        "Shared": {"transactions": [], "total": 0.0, "adjusted_total": 0.0}
    }
    
    for tx in transactions:
        if not tx["is_deductible"]:
            continue
        
        owner = tx["category_owner"]
        if owner == "shared":
            owner = "Shared"
        elif owner not in summary:
            owner = tx["owner"]  # Fall back to card owner
        
        if owner in summary:
            summary[owner]["transactions"].append(tx)
            summary[owner]["total"] += tx["amount"]
            adjusted = tx["amount"] * (tx["work_use_percent"] / 100)
            summary[owner]["adjusted_total"] += adjusted
    
    return summary


def print_summary(summary: dict):
    """Print a human-readable summary."""
    print("\n" + "=" * 70)
    print("DEDUCTIBLE TRANSACTIONS SUMMARY")
    print("=" * 70)
    
    for owner, data in summary.items():
        if not data["transactions"]:
            continue
        
        print(f"\n{owner.upper()}")
        print("-" * 50)
        
        # Group by category
        by_category = {}
        for tx in data["transactions"]:
            cat = tx["category"]
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(tx)
        
        for cat, txs in sorted(by_category.items()):
            cat_total = sum(tx["amount"] for tx in txs)
            work_pct = txs[0]["work_use_percent"]
            adjusted = cat_total * (work_pct / 100)
            print(f"\n  {cat} ({len(txs)} transactions)")
            print(f"    Total: ${cat_total:.2f} @ {work_pct}% = ${adjusted:.2f}")
            for tx in sorted(txs, key=lambda x: x["amount"], reverse=True)[:5]:
                print(f"      {tx['date_transaction']} ${tx['amount']:.2f} - {tx['description'][:40]}")
            if len(txs) > 5:
                print(f"      ... and {len(txs) - 5} more")
        
        print(f"\n  TOTAL: ${data['total']:.2f} (Adjusted: ${data['adjusted_total']:.2f})")


def main():
    """Main processing pipeline."""
    print("ANZ Credit Card Statement Parser")
    print("=" * 50)
    
    # 1. Extract all transactions
    transactions = process_all_statements()
    
    # 2. Categorise transactions
    transactions = categorise_all_transactions(transactions)
    
    # 3. Export to CSV
    export_to_csv(transactions)
    
    # 4. Export deductibles only
    deductible_txs = [tx for tx in transactions if tx["is_deductible"]]
    export_to_csv(deductible_txs, "deductible_transactions.csv")
    print(f"Deductible transactions: {len(deductible_txs)}")
    
    # 5. Generate and print summary
    summary = generate_deductible_summary(transactions)
    print_summary(summary)
    
    # 6. High-value items for review
    high_value = [tx for tx in transactions if tx["is_high_value"] and tx["category"] == "unclassified"]
    if high_value:
        print("\n" + "=" * 70)
        print("HIGH-VALUE UNCLASSIFIED (MANUAL REVIEW NEEDED)")
        print("=" * 70)
        for tx in sorted(high_value, key=lambda x: x["amount"], reverse=True):
            print(f"  {tx['date_transaction']} ${tx['amount']:.2f} - {tx['description']}")
    
    return transactions


if __name__ == "__main__":
    main()
