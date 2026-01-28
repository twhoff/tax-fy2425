"""
Receipt Cross-Reference for Bank Statement Transactions
Matches deductible transactions to existing receipts in 2. Deductions folder
"""

import csv
import re
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

# Paths
DEDUCTIONS_DIR = Path("2. Deductions")
ANALYSIS_DIR = Path("5. Bank Statements/Analysis")
DEDUCTIBLE_CSV = ANALYSIS_DIR / "deductible_transactions.csv"

# Matching config
DATE_TOLERANCE_DAYS = 7  # Allow receipts within ±7 days
AMOUNT_TOLERANCE_PERCENT = 5  # Allow 5% variance in amount


def extract_date_from_filename(filename: str) -> datetime | None:
    """Extract date from YYMMDD prefix format."""
    match = re.match(r'^(\d{6})', filename)
    if match:
        try:
            return datetime.strptime(match.group(1), "%y%m%d")
        except ValueError:
            pass
    return None


def extract_amount_from_filename(filename: str) -> float | None:
    """Try to extract amount from filename if present."""
    # Look for dollar amounts like $XX.XX or just XX.XX
    match = re.search(r'\$?(\d+\.?\d{0,2})', filename)
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            pass
    return None


def load_receipts() -> dict[str, list[dict]]:
    """Load all receipt files from deductions folders."""
    receipts = {"Thomas": [], "Isabelle": []}
    
    for owner in ["Thomas", "Isabelle"]:
        folder = DEDUCTIONS_DIR / owner
        if not folder.exists():
            continue
        
        for file_path in folder.iterdir():
            if file_path.suffix.lower() not in ['.pdf', '.png', '.jpg', '.jpeg']:
                continue
            
            receipt = {
                "filename": file_path.name,
                "path": str(file_path),
                "date": extract_date_from_filename(file_path.name),
                "name_lower": file_path.name.lower()
            }
            receipts[owner].append(receipt)
    
    return receipts


def load_transactions() -> list[dict]:
    """Load deductible transactions from CSV."""
    transactions = []
    with open(DEDUCTIBLE_CSV, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["amount"] = float(row["amount"])
            row["date_obj"] = datetime.strptime(row["date_transaction"], "%d/%m/%Y")
            transactions.append(row)
    return transactions


def normalize_merchant(description: str) -> list[str]:
    """Extract normalized merchant keywords from transaction description."""
    desc_lower = description.lower()
    
    # Known mappings
    mappings = {
        "officeworks": ["officeworks"],
        "replit": ["replit"],
        "openai": ["openai", "chatgpt"],
        "unicef": ["unicef"],
        "bravehearts": ["bravehearts"],
        "aussie broadband": ["aussie broadband", "internet"],
        "netflix": ["netflix"],
        "disney": ["disney"],
        "audible": ["audible"],
        "hayu": ["hayu"],
        "paramount": ["paramount"],
        "amazon": ["amazon"],
        "ikea": ["ikea"],
        "ring": ["ring"],
        "nebula": ["nebula", "projector"],
        "1password": ["1password"],
        "apple": ["apple"],
        "spotify": ["spotify"],
    }
    
    keywords = []
    for key, variations in mappings.items():
        if key in desc_lower:
            keywords.extend(variations)
    
    return keywords


def find_matching_receipt(tx: dict, receipts: list[dict]) -> dict | None:
    """Find a matching receipt for a transaction."""
    tx_date = tx["date_obj"]
    tx_amount = tx["amount"]
    tx_keywords = normalize_merchant(tx["description"])
    
    best_match = None
    best_score = 0
    
    for receipt in receipts:
        score = 0
        
        # Date matching
        if receipt["date"]:
            date_diff = abs((tx_date - receipt["date"]).days)
            if date_diff <= DATE_TOLERANCE_DAYS:
                score += (DATE_TOLERANCE_DAYS - date_diff + 1) * 10  # Closer = better
        
        # Keyword matching
        for keyword in tx_keywords:
            if keyword in receipt["name_lower"]:
                score += 50  # Strong boost for keyword match
        
        if score > best_score:
            best_score = score
            best_match = receipt
    
    # Require minimum score (at least date or keyword match)
    if best_score >= 10:
        return best_match
    
    return None


def cross_reference_transactions() -> list[dict]:
    """Main cross-reference function."""
    print("Loading receipts...")
    receipts = load_receipts()
    print(f"  Thomas: {len(receipts['Thomas'])} files")
    print(f"  Isabelle: {len(receipts['Isabelle'])} files")
    
    print("\nLoading transactions...")
    transactions = load_transactions()
    print(f"  Total deductible: {len(transactions)}")
    
    print("\nMatching...")
    results = []
    
    for tx in transactions:
        owner = tx.get("category_owner", tx.get("owner", "Unknown"))
        
        # Search in owner's folder first, then shared
        receipt = None
        if owner in receipts:
            receipt = find_matching_receipt(tx, receipts[owner])
        
        # If not found and owner is Thomas, also check Isabelle's (shared items)
        if not receipt and owner == "Thomas":
            receipt = find_matching_receipt(tx, receipts.get("Isabelle", []))
        
        # If not found and owner is Isabelle, also check Thomas's
        if not receipt and owner == "Isabelle":
            receipt = find_matching_receipt(tx, receipts.get("Thomas", []))
        
        result = {
            **tx,
            "receipt_match": receipt["path"] if receipt else None,
            "receipt_filename": receipt["filename"] if receipt else "No receipt"
        }
        results.append(result)
    
    return results


def generate_report(results: list[dict]):
    """Generate markdown report."""
    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
    
    matched = [r for r in results if r["receipt_match"]]
    unmatched = [r for r in results if not r["receipt_match"]]
    
    report = f"""# Bank Statement Transaction Cross-Reference

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}

## Summary

- **Total Deductible Transactions:** {len(results)}
- **Matched to Receipts:** {len(matched)} ({len(matched)/len(results)*100:.0f}%)
- **No Receipt Found:** {len(unmatched)} ({len(unmatched)/len(results)*100:.0f}%)

---

## Matched Transactions

| Date | Description | Amount | Owner | Receipt |
|------|-------------|--------|-------|---------|
"""
    
    for r in sorted(matched, key=lambda x: x["date_obj"]):
        report += f"| {r['date_transaction']} | {r['description'][:35]}... | ${r['amount']:.2f} | {r['category_owner']} | [{r['receipt_filename']}]({r['receipt_match']}) |\n"
    
    report += f"""

---

## Unmatched Transactions (Need Receipt)

| Date | Description | Amount | Owner | Category |
|------|-------------|--------|-------|----------|
"""
    
    for r in sorted(unmatched, key=lambda x: x["date_obj"]):
        report += f"| {r['date_transaction']} | {r['description'][:35]}... | ${r['amount']:.2f} | {r['category_owner']} | {r['category']} |\n"
    
    report += f"""

---

## Notes

- **Match criteria:** Receipt date within ±7 days AND merchant keyword match
- **Action needed:** Locate receipts for unmatched transactions or note as 'bank statement as evidence'
- **Internet bills:** May not have individual receipts - use bank statement
- **Streaming subscriptions:** May use bank statement as evidence
"""
    
    output_path = ANALYSIS_DIR / "transaction_receipt_crossref.md"
    with open(output_path, 'w') as f:
        f.write(report)
    
    print(f"\nReport written to: {output_path}")
    return output_path


def main():
    print("=" * 60)
    print("BANK STATEMENT - RECEIPT CROSS-REFERENCE")
    print("=" * 60)
    
    results = cross_reference_transactions()
    generate_report(results)
    
    # Also save as CSV
    csv_path = ANALYSIS_DIR / "transaction_crossref.csv"
    with open(csv_path, 'w', newline='') as f:
        fieldnames = ["date_transaction", "description", "amount", "category_owner", 
                      "category", "work_use_percent", "receipt_filename", "receipt_match"]
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(results)
    
    print(f"CSV saved to: {csv_path}")
    
    # Summary stats
    matched = len([r for r in results if r["receipt_match"]])
    print(f"\n✓ Matched: {matched}/{len(results)} transactions")
    print(f"✗ Need receipts: {len(results) - matched} transactions")


if __name__ == "__main__":
    main()
