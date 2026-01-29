#!/usr/bin/env python3
"""
Tax FY24-25 Calculation Verification Script
ATO Compliance Check - All calculations done deterministically
"""
from decimal import Decimal, ROUND_HALF_UP

def currency(value):
    """Format as currency with 2 decimal places"""
    return Decimal(str(value)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

print("=" * 70)
print("TAX FY24-25 CALCULATION VERIFICATION")
print("ATO Rules: WFH Fixed Rate 70c/hr, Division 293 threshold $250k")
print("=" * 70)

# ============================================================================
# INCOME
# ============================================================================
print("\n--- INCOME ---")

thomas_atlassian = Decimal('86255.70')
thomas_seek = Decimal('90000.00')
thomas_payg = thomas_atlassian + thomas_seek
thomas_ess = Decimal('62270.51')
thomas_cgt = Decimal('7974.12')
thomas_div = Decimal('34.46')
thomas_income = thomas_payg + thomas_ess + thomas_cgt + thomas_div

print(f"Thomas PAYG:     {thomas_atlassian} + {thomas_seek} = ${thomas_payg:,.2f}")
print(f"Thomas ESS:      ${thomas_ess:,.2f}")
print(f"Thomas CGT:      ${thomas_cgt:,.2f}")
print(f"Thomas Div:      ${thomas_div:,.2f}")
print(f"THOMAS TOTAL:    ${thomas_income:,.2f}")

isabelle_income = Decimal('111470.05')
print(f"\nISABELLE TOTAL:  ${isabelle_income:,.2f}")

bank_interest = Decimal('34.96')
print(f"Bank Interest:   ${bank_interest:,.2f}")

combined_income = thomas_income + isabelle_income + bank_interest
print(f"\nCOMBINED INCOME: ${combined_income:,.2f}")

# ============================================================================
# WFH DEDUCTIONS
# ============================================================================
print("\n--- WFH FIXED RATE (70c/hr for FY24-25) ---")

WFH_RATE = Decimal('0.70')

# Thomas: 20 weeks Atlassian (2 days/wk, 12 hrs/wk) + 24 weeks SEEK (2 days/wk, 10 hrs/wk)
thomas_atlassian_wfh = 20 * 12  # 20 weeks × 12 hrs/wk
thomas_seek_wfh = 24 * 10       # 24 weeks × 10 hrs/wk
thomas_wfh_hrs = thomas_atlassian_wfh + thomas_seek_wfh
thomas_wfh = currency(Decimal(thomas_wfh_hrs) * WFH_RATE)

print(f"Thomas Atlassian: 20 weeks × 12 hrs/wk = {thomas_atlassian_wfh} hrs")
print(f"Thomas SEEK:      24 weeks × 10 hrs/wk = {thomas_seek_wfh} hrs")
print(f"Thomas TOTAL:     {thomas_wfh_hrs} hrs × $0.70 = ${thomas_wfh:,.2f}")

# Isabelle: 48 weeks × 3 days/wk × 7.6 hrs/day = 1095 hrs (rounded)
isabelle_wfh_hrs = 48 * 3 * Decimal('7.6')  # = 1094.4, rounded to 1095
isabelle_wfh_hrs_int = 1095  # As documented
isabelle_wfh = currency(Decimal(isabelle_wfh_hrs_int) * WFH_RATE)

print(f"\nIsabelle: 48 wks × 3 days × 7.6 hrs = {isabelle_wfh_hrs} hrs → rounded {isabelle_wfh_hrs_int}")
print(f"Isabelle TOTAL:   {isabelle_wfh_hrs_int} hrs × $0.70 = ${isabelle_wfh:,.2f}")

# ============================================================================
# THOMAS EQUIPMENT
# ============================================================================
print("\n--- THOMAS EQUIPMENT (100% work use) ---")

equipment = [
    ('iPad Pro M4 13"', Decimal('2148.99')),
    ('iPhone 16 Pro', Decimal('1528.00')),
    ('Apple Pencil Pro', Decimal('177.00')),
    ('PAX Wardrobe (IKEA)', Decimal('2619.50')),
    ('Nebula Capsule Projector', Decimal('879.99')),
    ('LG Portable Monitor', Decimal('502.63')),
    ('Projector Screen', Decimal('37.99')),
    ('Clock', Decimal('19.99')),
    ('Printing supplies', Decimal('52.48')),
    ('Accessibility tools (Minimal Desk)', Decimal('76.93')),
    ('WACOM drawing tablet', Decimal('168.99')),
]

equipment_total = sum(amt for _, amt in equipment)
for name, amt in equipment:
    print(f"  {name}: ${amt:,.2f}")
print(f"  EQUIPMENT TOTAL: ${equipment_total:,.2f}")

# ============================================================================
# THOMAS SOFTWARE
# ============================================================================
print("\n--- THOMAS SOFTWARE (100% work use) ---")

software = [
    ('Replit (3 charges)', Decimal('185.35')),
    ('ChatGPT Plus (3)', Decimal('89.03')),
    ('OpenArt AI', Decimal('134.48')),
    ('BeforeSunset AI', Decimal('131.08')),
    ('1Password', Decimal('49.95')),
]

software_total = sum(amt for _, amt in software)
for name, amt in software:
    print(f"  {name}: ${amt:,.2f}")
print(f"  SOFTWARE TOTAL: ${software_total:,.2f}")

# ============================================================================
# OTHER THOMAS DEDUCTIONS
# ============================================================================
print("\n--- OTHER THOMAS DEDUCTIONS ---")

thomas_internet = Decimal('945.00')
thomas_productivity = Decimal('48.43')
thomas_audible = Decimal('98.70')  # 6 × $16.45
thomas_donations = Decimal('500.00')  # UNICEF $250 + Bravehearts $250

# Home office cleaning
cleaning_total = 5 * Decimal('132.13')
home_office_pct = Decimal('20') / Decimal('130')
thomas_cleaning = currency(cleaning_total * home_office_pct)

print(f"Internet (GROSS):     ${thomas_internet:,.2f}")
print(f"Productivity Tools:   ${thomas_productivity:,.2f}")
print(f"Audible (6 × $16.45): ${thomas_audible:,.2f}")
print(f"Donations:            ${thomas_donations:,.2f}")
print(f"Cleaning: 5 × $132.13 = ${cleaning_total:,.2f}")
print(f"  × {home_office_pct:.4f} (20m²/130m²) = ${thomas_cleaning:,.2f}")

# ============================================================================
# THOMAS TOTAL DEDUCTIONS
# ============================================================================
thomas_deductions = (
    thomas_wfh +
    equipment_total +
    software_total +
    thomas_internet +
    thomas_productivity +
    thomas_audible +
    thomas_donations +
    thomas_cleaning
)

print(f"\n{'='*50}")
print(f"THOMAS DEDUCTIONS (GROSS): ${thomas_deductions:,.2f}")
print(f"{'='*50}")

# ============================================================================
# ISABELLE DEDUCTIONS
# ============================================================================
print("\n--- ISABELLE DEDUCTIONS ---")

isabelle_streaming = Decimal('819.18')
isabelle_conferences = Decimal('81.00')
isabelle_reading = Decimal('55.61')
isabelle_donations = Decimal('20.37')

print(f"WFH Fixed Rate:       ${isabelle_wfh:,.2f}")
print(f"Streaming (GROSS):    ${isabelle_streaming:,.2f}")
print(f"Conferences:          ${isabelle_conferences:,.2f}")
print(f"Prof Reading (GROSS): ${isabelle_reading:,.2f}")
print(f"Donations:            ${isabelle_donations:,.2f}")

isabelle_deductions = (
    isabelle_wfh +
    isabelle_streaming +
    isabelle_conferences +
    isabelle_reading +
    isabelle_donations
)

print(f"\n{'='*50}")
print(f"ISABELLE DEDUCTIONS (GROSS): ${isabelle_deductions:,.2f}")
print(f"{'='*50}")

# ============================================================================
# COMBINED
# ============================================================================
combined_deductions = thomas_deductions + isabelle_deductions

print(f"\n{'='*70}")
print(f"COMBINED DEDUCTIONS (GROSS): ${combined_deductions:,.2f}")
print(f"{'='*70}")

# ============================================================================
# CCS THRESHOLD CHECK
# ============================================================================
print("\n--- CCS THRESHOLD CHECK ---")

CCS_THRESHOLD = Decimal('367563')

# Apply work-use percentages for taxable income calculation
thomas_internet_adj = currency(thomas_internet * Decimal('0.65'))
isabelle_streaming_adj = currency(isabelle_streaming * Decimal('0.30'))
isabelle_reading_adj = currency(isabelle_reading * Decimal('0.50'))

thomas_deductions_adj = (
    thomas_wfh +
    equipment_total +
    software_total +
    thomas_internet_adj +
    thomas_productivity +
    thomas_audible +
    thomas_donations +
    thomas_cleaning
)

isabelle_deductions_adj = (
    isabelle_wfh +
    isabelle_streaming_adj +
    isabelle_conferences +
    isabelle_reading_adj +
    isabelle_donations
)

thomas_taxable = thomas_income - thomas_deductions_adj
isabelle_taxable = isabelle_income - isabelle_deductions_adj
combined_taxable = thomas_taxable + isabelle_taxable

print(f"\nAdjusted deductions (with work-use %):")
print(f"  Thomas Internet: ${thomas_internet} × 65% = ${thomas_internet_adj}")
print(f"  Isabelle Streaming: ${isabelle_streaming} × 30% = ${isabelle_streaming_adj}")
print(f"  Isabelle Reading: ${isabelle_reading} × 50% = ${isabelle_reading_adj}")

print(f"\nThomas adjusted deductions:   ${thomas_deductions_adj:,.2f}")
print(f"Isabelle adjusted deductions: ${isabelle_deductions_adj:,.2f}")

print(f"\nThomas taxable:   ${thomas_income:,.2f} - ${thomas_deductions_adj:,.2f} = ${thomas_taxable:,.2f}")
print(f"Isabelle taxable: ${isabelle_income:,.2f} - ${isabelle_deductions_adj:,.2f} = ${isabelle_taxable:,.2f}")
print(f"Combined taxable: ${combined_taxable:,.2f}")

margin = CCS_THRESHOLD - combined_taxable
status = "✓ UNDER" if margin > 0 else "✗ OVER"
print(f"\nCCS Threshold: ${CCS_THRESHOLD:,.2f}")
print(f"Margin:        ${margin:,.2f} {status}")

# ============================================================================
# DIVISION 293 CHECK
# ============================================================================
print("\n--- DIVISION 293 CHECK ---")

DIV293_THRESHOLD = Decimal('250000')
SUPER_RATE = Decimal('0.115')

thomas_super_est = currency(thomas_payg * SUPER_RATE)
thomas_div293 = thomas_taxable + thomas_super_est

print(f"Thomas taxable income: ${thomas_taxable:,.2f}")
print(f"Thomas super (11.5%):  ${thomas_super_est:,.2f}")
print(f"Thomas DIV293 income:  ${thomas_div293:,.2f}")
print(f"DIV293 threshold:      ${DIV293_THRESHOLD:,.2f}")

if thomas_div293 > DIV293_THRESHOLD:
    excess = thomas_div293 - DIV293_THRESHOLD
    div293_tax = currency(min(excess, thomas_super_est) * Decimal('0.15'))
    print(f"⚠️  EXCEEDS by ${excess:,.2f}")
    print(f"Est DIV293 tax: ${div293_tax:,.2f}")
else:
    print(f"✓ Below threshold")

# ============================================================================
# ISSUE: INTERNET + WFH FIXED RATE
# ============================================================================
print("\n" + "=" * 70)
print("⚠️  CRITICAL ISSUE: INTERNET + WFH FIXED RATE")
print("=" * 70)
print("""
ATO RULE: Fixed rate (70c/hr) INCLUDES:
  - Home internet
  - Mobile phone
  - Electricity and gas
  - Stationery and computer consumables

CURRENT SITUATION:
  - Claiming WFH Fixed Rate: $672 (Thomas) + $766.50 (Isabelle)
  - ALSO claiming Internet separately: $945 (Thomas)
  
⚠️  THIS IS DOUBLE-DIPPING ON INTERNET

OPTIONS FOR ACCOUNTANT:
  a) Remove Internet claim ($945) - use Fixed Rate only
  b) Switch to Actual Cost Method for ALL running expenses
  
NOTE: Equipment CAN still be claimed separately from Fixed Rate
""")

# ============================================================================
# FINAL SUMMARY
# ============================================================================
print("\n" + "=" * 70)
print("FINAL VERIFIED FIGURES")
print("=" * 70)

print(f"""
                        Thomas          Isabelle        Combined
Income                  ${thomas_income:>12,.2f}  ${isabelle_income:>12,.2f}  ${combined_income:>12,.2f}
Deductions (GROSS)      ${thomas_deductions:>12,.2f}  ${isabelle_deductions:>12,.2f}  ${combined_deductions:>12,.2f}
Deductions (ADJUSTED)   ${thomas_deductions_adj:>12,.2f}  ${isabelle_deductions_adj:>12,.2f}  ${thomas_deductions_adj + isabelle_deductions_adj:>12,.2f}
Est Taxable Income      ${thomas_taxable:>12,.2f}  ${isabelle_taxable:>12,.2f}  ${combined_taxable:>12,.2f}

CCS Threshold: $367,563.00
CCS Margin:    ${margin:>,.2f} ({status} THRESHOLD)
""")
