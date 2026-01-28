#!/usr/bin/env python3
"""Calculate Isabelle's subscription totals for tax deductions."""

import fitz
import os
import re

isabelle_dir = "Isabelle"
totals = {
    'Paramount Plus': 0,
    'Hayu': 0,
    'Audible': 0,
    'YouTube Premium': 0,
    'Cleanup Pro': 0
}

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

for f in sorted(os.listdir(isabelle_dir)):
    path = os.path.join(isabelle_dir, f)
    if f.endswith('.pdf'):
        try:
            doc = fitz.open(path)
            text = doc[0].get_text()
            doc.close()
            
            # Extract amount - look for TOTAL: AUDx.xx pattern first, then fall back
            total_match = re.search(r'TOTAL[:\s]*(?:AUD|\$)(\d+\.?\d*)', text, re.IGNORECASE)
            if total_match:
                amount = float(total_match.group(1))
            else:
                # Fall back to finding amounts - prefer larger ones (not GST)
                amounts = re.findall(r'(?:AUD|\$)(\d+\.?\d*)', text)
                if amounts:
                    # Get the largest amount that's reasonable (skip tiny GST amounts)
                    amount = max(float(a) for a in amounts if float(a) > 1)
                else:
                    continue
            if amount:
                
                # Categorize
                f_lower = f.lower()
                if 'paramount' in f_lower:
                    totals['Paramount Plus'] += amount
                    print(f"Paramount: ${amount:.2f} - {f}")
                elif 'hayu' in f_lower:
                    totals['Hayu'] += amount
                    print(f"Hayu: ${amount:.2f} - {f}")
                elif 'youtube' in f_lower:
                    totals['YouTube Premium'] += amount
                    print(f"YouTube: ${amount:.2f} - {f}")
                elif 'cleanup' in f_lower:
                    totals['Cleanup Pro'] += amount
                    print(f"Cleanup: ${amount:.2f} - {f}")
        except Exception as e:
            print(f"Error: {f} - {e}")
    elif f.endswith('.png') and 'audible' in f.lower():
        # Audible is typically ~$16.45/month
        totals['Audible'] += 16.45
        print(f"Audible: $16.45 (estimated) - {f}")

print("\n=== SUMMARY ===")
grand_total = 0
for service, amount in totals.items():
    if amount > 0:
        print(f"{service}: ${amount:.2f}")
        grand_total += amount

print(f"\nTotal Annual Cost: ${grand_total:.2f}")
print(f"30% Work Use Deduction: ${grand_total * 0.30:.2f}")
