# FY24-25 Deduction Analysis Summary

Generated: 2026-01-29

## Analysis Sources

1. **ANZ Credit Card** (all_transactions.csv) - 1,256 transactions (Sep 2024 - Jul 2025)
2. **Bank Australia** (bank_australia_transactions.csv) - 452 transactions (Jul 2024 - Jun 2025)
3. **Highlighted Transactions** (highlighted_transactions.csv) - 43+ manually flagged items

## Deduction Totals by Category

| Category | Count | Gross | Work % | Deductible |
|----------|-------|-------|--------|------------|
| software_subscriptions | 9 | $589.89 | 100% | $589.89 |
| home_office_equipment | 4 | $1,757.48 | 100% | $1,757.48 |
| internet_phone | 9 | $945.00 | 65% | $614.25 |
| streaming_creative | 51 | $950.78 | 30% | $285.23 |
| donations | 3 | $520.37 | 100% | $520.37 |
| conferences_events | 4 | $81.00 | 100% | $81.00 |
| productivity_tools | 1 | $48.43 | 100% | $48.43 |
| professional_reading | 5 | $55.61 | 50% | $27.80 |
| **TOTAL** | **86** | **$4,948.56** | | **$3,924.46** |

## Deductions by Owner (Bank Statements Only)

| Owner | Gross | Deductible |
|-------|-------|------------|
| Thomas | $2,451.41 | $2,423.61 |
| Isabelle | $1,031.78 | $366.23 |
| Shared | $945.00 | $614.25 |
| check_card (donations) | $520.37 | $520.37 |

## Thomas Complete Deduction Summary

| Item | Amount | Notes |
|------|--------|-------|
| Software subscriptions | $589.89 | Replit, ChatGPT, 1Password, Warp, OpenArt, BeforeSunset |
| Home office equipment | $1,757.48 | Officeworks (iPad, iPhone, Apple Pencil) |
| Productivity tools | $48.43 | TheCenteredLife |
| Professional reading | $27.80 | New Yorker @ 50% |
| Internet (from shared) | $614.25 | Aussie Broadband @ 65% |
| Donations | $500.00 | UNICEF + Bravehearts |
| **Bank Statement Subtotal** | **$3,537.85** | |
| WFH Fixed Rate | $672.00 | 960 hrs × $0.70 |
| **TOTAL THOMAS** | **$4,209.85** | ✅ Exceeds $4,000 target |

## Isabelle Complete Deduction Summary

| Item | Amount | Notes |
|------|--------|-------|
| Streaming creative | $285.23 | Netflix, Disney+, Spotify, Paramount+, etc. @ 30% |
| Conferences/events | $81.00 | Victorian Arts Centre |
| Donations | $20.37 | Cancer Council |
| **Bank Statement Subtotal** | **$386.60** | |
| WFH Fixed Rate | $766.50 | 1,095 hrs × $0.70 |
| **TOTAL ISABELLE** | **$1,153.10** | |

## CCS Impact

- **Target threshold:** Combined taxable income < $367,563 for higher CCS multi-child rate
- **Thomas deductions:** $4,209.85 ✅
- **Effect:** Should reduce combined income below threshold, saving ~$3,336 in CCS repayment

## High-Value Items (Receipts Required)

| Date | Amount | Description | Category |
|------|--------|-------------|----------|
| 30/06/2025 | $1,705.00 | OFFICEWORKS BENTLEIGH EAS | home_office_equipment |
| 15/06/2025 | $250.00 | UNICEF AUSTRALIA | donations |
| 15/06/2025 | $250.00 | BRAVEHEARTS FOUNDATION | donations |
| 25/05/2025 | $209.99 | DISNEY PLUS | streaming_creative |
| 17/06/2025 | $134.48 | OPENART AI | software_subscriptions |
| 05/06/2025 | $131.08 | BEFORESUNSET AI | software_subscriptions |

## Files Created/Updated

- `5. Bank Statements/Analysis/deductible_transactions_v2.csv` - All categorized deductions
- `5. Bank Statements/Analysis/bank_australia_transactions.csv` - Bank Australia parsed data
- `5. Bank Statements/Analysis/highlighted_transactions.csv` - Manually identified patterns
- `scripts/run_deduction_analysis.py` - Analysis script
- `scripts/bank_australia_parser.py` - Bank Australia PDF parser
- `scripts/tax_categories.py` - Updated with new categories

## New Categories Added to tax_categories.py

1. **professional_reading** - New Yorker, Economist, etc. (50% Thomas)
2. **productivity_tools** - TheCenteredLife, Focusmate (100% Thomas)
3. **conferences_events** - Victorian Arts Centre, Princess Theatre (100% Isabelle)

## New Keywords Added

- streaming_creative: spotify, hubbl, binge, ad free for primevideo
- software_subscriptions: microsoft*store, msbill, beforesunset, openart
