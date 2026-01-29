#!/usr/bin/env python3
"""
Verify PDF filename dates match document content dates.

Checks files with YYMMDD prefix format against dates found in the PDF text.
"""

import fitz
import os
import re
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# Date patterns to search for in PDF content
DATE_PATTERNS = [
    # DD/MM/YYYY or DD-MM-YYYY
    (r'\b(\d{1,2})[/-](\d{1,2})[/-](20\d{2})\b', 'dmy'),
    # DD/MM/YY or DD-MM-YY
    (r'\b(\d{1,2})[/-](\d{1,2})[/-](\d{2})\b', 'dmy_short'),
    # YYYY-MM-DD (ISO)
    (r'\b(20\d{2})-(\d{1,2})-(\d{1,2})\b', 'ymd'),
    # DD Month YYYY (e.g., 15 June 2024)
    (r'\b(\d{1,2})\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(20\d{2})\b', 'dMy'),
    # Month DD, YYYY (e.g., June 15, 2024)
    (r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),?\s+(20\d{2})\b', 'Mdy'),
    # DD.MM.YYYY
    (r'\b(\d{1,2})\.(\d{1,2})\.(20\d{2})\b', 'dmy_dot'),
]

MONTH_MAP = {
    'january': 1, 'february': 2, 'march': 3, 'april': 4,
    'may': 5, 'june': 6, 'july': 7, 'august': 8,
    'september': 9, 'october': 10, 'november': 11, 'december': 12
}


def parse_filename_date(filename):
    """Extract date from YYMMDD prefix."""
    match = re.match(r'^(\d{6})\s*-\s*', filename)
    if not match:
        return None
    
    date_str = match.group(1)
    try:
        year = int('20' + date_str[:2])
        month = int(date_str[2:4])
        day = int(date_str[4:6])
        
        # Validate
        if 1 <= month <= 12 and 1 <= day <= 31:
            return datetime(year, month, day)
    except (ValueError, IndexError):
        pass
    return None


def extract_dates_from_text(text):
    """Find all dates in PDF text content."""
    dates = []
    
    for pattern, fmt in DATE_PATTERNS:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            try:
                if fmt == 'dmy':
                    d, m, y = int(match.group(1)), int(match.group(2)), int(match.group(3))
                elif fmt == 'dmy_short':
                    d, m, y = int(match.group(1)), int(match.group(2)), 2000 + int(match.group(3))
                elif fmt == 'dmy_dot':
                    d, m, y = int(match.group(1)), int(match.group(2)), int(match.group(3))
                elif fmt == 'ymd':
                    y, m, d = int(match.group(1)), int(match.group(2)), int(match.group(3))
                elif fmt == 'dMy':
                    d = int(match.group(1))
                    m = MONTH_MAP[match.group(2).lower()]
                    y = int(match.group(3))
                elif fmt == 'Mdy':
                    m = MONTH_MAP[match.group(1).lower()]
                    d = int(match.group(2))
                    y = int(match.group(3))
                else:
                    continue
                
                # Validate and create date
                if 1 <= m <= 12 and 1 <= d <= 31 and 2020 <= y <= 2030:
                    dates.append(datetime(y, m, d))
            except (ValueError, KeyError):
                continue
    
    return list(set(dates))  # Remove duplicates


def get_pdf_text(pdf_path):
    """Extract text from PDF."""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        return None


def check_date_match(filename_date, content_dates, tolerance_days=7):
    """
    Check if filename date matches any content date.
    
    Returns: (match_type, closest_date, days_diff)
    - 'exact': Exact match found
    - 'close': Match within tolerance
    - 'mismatch': No close match found
    - 'no_dates': No dates found in content
    """
    if not content_dates:
        return ('no_dates', None, None)
    
    # Check for exact match first
    if filename_date in content_dates:
        return ('exact', filename_date, 0)
    
    # Find closest date
    closest = min(content_dates, key=lambda d: abs((d - filename_date).days))
    days_diff = abs((closest - filename_date).days)
    
    if days_diff <= tolerance_days:
        return ('close', closest, days_diff)
    else:
        return ('mismatch', closest, days_diff)


def verify_pdfs(root_dir, tolerance_days=7):
    """Verify all PDFs with date prefixes."""
    results = {
        'exact': [],
        'close': [],
        'mismatch': [],
        'no_dates': [],
        'no_text': [],
        'skipped': []
    }
    
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if not filename.lower().endswith('.pdf'):
                continue
            
            filepath = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(filepath, root_dir)
            
            # Parse filename date
            filename_date = parse_filename_date(filename)
            if not filename_date:
                results['skipped'].append((rel_path, 'No date prefix'))
                continue
            
            # Extract PDF text
            text = get_pdf_text(filepath)
            if not text or len(text.strip()) < 10:
                results['no_text'].append((rel_path, filename_date))
                continue
            
            # Find dates in content
            content_dates = extract_dates_from_text(text)
            
            # Check match
            match_type, closest, days_diff = check_date_match(
                filename_date, content_dates, tolerance_days
            )
            
            results[match_type].append({
                'file': rel_path,
                'filename_date': filename_date,
                'closest_date': closest,
                'days_diff': days_diff,
                'all_dates': sorted(content_dates) if content_dates else []
            })
    
    return results


def print_report(results):
    """Print verification report."""
    print("=" * 70)
    print("PDF DATE VERIFICATION REPORT")
    print("=" * 70)
    
    total = sum(len(v) for k, v in results.items() if k != 'skipped')
    
    # Summary
    print(f"\n📊 SUMMARY")
    print(f"   Total PDFs with date prefix: {total}")
    print(f"   ✅ Exact match:    {len(results['exact'])}")
    print(f"   🔶 Close match:    {len(results['close'])} (within tolerance)")
    print(f"   ❌ Mismatch:       {len(results['mismatch'])}")
    print(f"   ❓ No dates found: {len(results['no_dates'])}")
    print(f"   📄 No text:        {len(results['no_text'])}")
    print(f"   ⏭️  Skipped:        {len(results['skipped'])} (no date prefix)")
    
    # Mismatches - most important
    if results['mismatch']:
        print(f"\n{'=' * 70}")
        print("❌ MISMATCHES - Filename date doesn't match content")
        print("=" * 70)
        for item in sorted(results['mismatch'], key=lambda x: x['days_diff'], reverse=True):
            print(f"\n📄 {item['file']}")
            print(f"   Filename date:  {item['filename_date'].strftime('%d/%m/%Y')}")
            print(f"   Closest found:  {item['closest_date'].strftime('%d/%m/%Y')} ({item['days_diff']} days off)")
            if item['all_dates']:
                dates_str = ', '.join(d.strftime('%d/%m/%y') for d in item['all_dates'][:5])
                if len(item['all_dates']) > 5:
                    dates_str += f" (+{len(item['all_dates'])-5} more)"
                print(f"   All dates:      {dates_str}")
    
    # Close matches
    if results['close']:
        print(f"\n{'=' * 70}")
        print("🔶 CLOSE MATCHES - Within tolerance but not exact")
        print("=" * 70)
        for item in sorted(results['close'], key=lambda x: x['days_diff'], reverse=True):
            print(f"   {item['file']}")
            print(f"      → {item['filename_date'].strftime('%d/%m/%Y')} vs {item['closest_date'].strftime('%d/%m/%Y')} ({item['days_diff']} days)")
    
    # No dates found
    if results['no_dates']:
        print(f"\n{'=' * 70}")
        print("❓ NO DATES FOUND IN CONTENT")
        print("=" * 70)
        for item in results['no_dates']:
            print(f"   {item['file']} (expected: {item['filename_date'].strftime('%d/%m/%Y')})")
    
    # Exact matches (condensed)
    if results['exact']:
        print(f"\n{'=' * 70}")
        print(f"✅ EXACT MATCHES ({len(results['exact'])} files)")
        print("=" * 70)
        for item in results['exact'][:10]:
            print(f"   ✓ {item['file']}")
        if len(results['exact']) > 10:
            print(f"   ... and {len(results['exact']) - 10} more")


if __name__ == '__main__':
    import sys
    
    # Default to current directory or accept path argument
    root_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    tolerance = int(sys.argv[2]) if len(sys.argv) > 2 else 7
    
    print(f"Scanning: {os.path.abspath(root_dir)}")
    print(f"Tolerance: ±{tolerance} days\n")
    
    results = verify_pdfs(root_dir, tolerance_days=tolerance)
    print_report(results)
