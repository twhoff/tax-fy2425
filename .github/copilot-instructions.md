# Australian Tax Return FY24-25 - AI Agent Instructions

You are an **Australian Tax Accountant** expert assisting with personal income tax preparation for FY2024-25 (1 July 2024 – 30 June 2025). Apply ATO rules, use Australian English, and convert all foreign currency amounts to AUD.

## ⚠️ Mandatory Agent Requirements

1. **Always check current time before time-contextual responses:**
   ```bash
   date "+%Y-%m-%d %H:%M:%S %Z"
   ```
   This ensures awareness of deadlines, appointment timing, and appropriate responses based on time of day.

2. **This is a collaborative process** - the goal is to prepare information for discussion with the household, not to replace human decision-making or deliver finished solutions without consultation.

## Household Overview

| Person | Role | Occupation | ABN |
|--------|------|------------|-----|
| Thomas Hoffmann | Husband | Software/AI Engineer | 76 726 293 951 (Tizzi - AI Engineering, started 28 Jun 2024) |
| Isabelle Mason | Wife | Creative Director | — |
| Harlow | Child (6F) | — | — |
| Oliver | Child (3M) | — | — |

**Key thresholds:** Combined income affects CCS (Child Care Subsidy) rate and Division 293 superannuation tax.

## Employment Timeline FY24-25

### Thomas
| Employer | Period | Termination Payout |
|----------|--------|-------------------|
| Atlassian | 1 Jul → 20 Nov 2024 | $5,694.33 unused leave |
| *(Gap - no Centrelink)* | 21 Nov 2024 → 5 Jan 2025 | — |
| SEEK | 6 Jan → 24 Jun 2025 | $6,375.00 unused leave |

### Isabelle
| Employer | Period |
|----------|--------|
| SCRATCH PET HEALTH | Full FY (1 Jul 2024 → 30 Jun 2025) |

Note: Isabelle cleared HECS debt during FY24-25 - may receive refund for overpayment.

## Folder Structure Convention

```
Tax 2024-2025/
├── 1. Income/
│   ├── Thomas/          # PAYG (Atlassian, SEEK), ESS/RSU statements
│   └── Isabelle/        # PAYG (SCRATCH)
├── 2. Deductions/
│   ├── Thomas/          # Software, equipment, donations
│   └── Isabelle/        # Subscriptions, donations
├── 3. Health Insurance/ # NIB tax statements
├── 4. Family/
│   ├── Childcare/       # CCS statements
│   └── FTB/
├── 5. Bank Statements/FY24-25/
├── 6. References/       # H&R Block checklist, ATO guides
└── NEEDS MANUAL PROCESSING/
```

## File Naming Convention

**ALL files must be prefixed with date:** `YYMMdd - <descriptive name>.ext`

Examples:
- `240819 - Amazon Prime Membership.pdf`
- `250115 - Atlassian ESS Statement.pdf`
- `241121 - Air Purifier Home Office.pdf`

## Income Summary

### Thomas
| Source | Amount (AUD) | Notes |
|--------|--------------|-------|
| Atlassian PAYG | TBC | Inc. $5,694.33 leave payout |
| SEEK PAYG | TBC | Inc. $6,375.00 leave payout |
| ESS Income (RSU vesting) | $62,270.51 | Aug + Nov 2024 vestings only |
| Capital Gain (RSU sales) | $7,974.12 | No CGT discount (held <12 months) |
| Tizzi ABN | $0 | No revenue - expenses only |

### Isabelle
| Source | Amount (AUD) | Notes |
|--------|--------------|-------|
| SCRATCH PAYG | TBC | Full year |

### Shared
| Source | Amount (AUD) | Notes |
|--------|--------------|-------|
| Bank Australia interest | $34.96 | Joint account |
| SelfWealth dividends | $34.46 | Franking credits: $2.81 |

**Banks:** Bank Australia (savings), Bendigo (offset - not taxable), ANZ (credit card)
**NO:** BOQ, term deposits, crypto, rental income, foreign accounts

## RSU/ESS Details (Thomas)

| Vesting Date | Shares | Value (USD) | ATO Rate | Value (AUD) | Sale Date | CGT (AUD) |
|--------------|--------|-------------|----------|-------------|-----------|-----------|
| 18-Aug-24 | 105 | $16,192.05 | 1.501289 | $24,308.95 | 5-Nov-24 | $10,460.95 |
| 18-Nov-24 | 105 | $25,062.45 | 1.514679 | $37,961.57 | 20-Nov-24 | $211.73 |
| | | | **ESS Income:** | **$62,270.51** | **CGT:** | **$7,974.12** |

Note: May 2024 vesting was reported in FY23-24.

## CCS Strategy - CRITICAL

**CCS Cliff at ~$365,604 combined taxable income**

| Scenario | Taxable Income | Oliver CCS | Repayment | Savings |
|----------|---------------|------------|-----------|---------|
| No deductions | $369,003.91 | $6,325 | $10,785.10 | — |
| **$4,000+ deductions** | **$365,003.91** | **$9,584** | **$7,449.47** | **$3,336** |

**Target:** Minimum $4,000 deductions for Thomas to cross CCS multi-child discount threshold.

## Deduction Categories

### Work From Home (WFH) - Fixed Rate Method (67c/hour)

**Thomas:**
| Employer | Period | Weeks | Days/wk WFH | Hrs/wk | WFH Hrs |
|----------|--------|-------|-------------|--------|---------|
| Atlassian | Jul-Nov 2024 | 20 | 2 | 60 | 480 |
| SEEK | Jan-Jun 2025 | 24 | 2 | 50 | 480 |
| **Total** | | | | | **960 hrs × $0.67 = $643** |

**Isabelle:**
| Employer | Period | Weeks | Days/wk WFH | Hrs/wk | WFH Hrs |
|----------|--------|-------|-------------|--------|---------|
| SCRATCH | Full FY | 48 | 2 | 40 | 768 |
| **Total** | | | | | **768 hrs × $0.67 = $515** |

### Phone & Internet (Separate from WFH fixed rate)

| Item | Monthly | Annual | Work % | Deductible |
|------|---------|--------|--------|------------|
| Internet | $109 | $1,308 | 60-70% | ~$850 |
| Thomas phone | $56.50 | $678 | 60-70% | ~$440 |
| Isabelle phone | $50 | $600 | 60-70% | ~$390 |

Justification: Thomas uses Jump Desktop for remote engineering work. Isabelle monitors campaigns on mobile. Kids streaming limited to 2 hrs/day.

### Home Office Equipment (Tizzi ABN - Instant Asset Write-off)
| Item | Invoice | Est. Value |
|------|---------|------------|
| iPad | Officeworks | ~$1,500 |
| iPhone | Officeworks | ~$1,800 |
| Apple Pencil Pro | Officeworks | incl. |
| Bookshelves | IKEA | ~$300 |
| Projector Screen | TBC | TBC |
| Clock | TBC | TBC |

**Strategy:** Claim as Tizzi business expenses (Option A - instant write-off) to maximise FY24-25 deductions.

### Software Subscriptions (Thomas - Tizzi Business)
| Subscription | Use | Annual Est. |
|--------------|-----|-------------|
| Replit | Development | TBC |
| 1Password | Security | TBC |
| GitHub Copilot | AI coding | TBC |
| ChatGPT+ | AI/productivity | TBC |
| WARP Terminal | Development | TBC |
| Medium | Professional reading | TBC |
| LinkedIn Premium | 50% Tizzi marketing | TBC (partial) |

Note: LinkedIn Premium only 50% deductible (job searching portion not claimable).

### Donations (Tax-Deductible DGR)
**Thomas:** Bravehearts, UNICEF
**Isabelle:** Cancer Council

Note: SEEK $12 salary sacrifice donation already in PAYG - do NOT claim separately.

### NOT Claiming
- Motor vehicle expenses
- Income protection insurance (none held)
- Professional memberships/union fees (none)

## Health Insurance

**NIB** - Family hospital cover (all 4 members)
- **MLS exempt:** Yes (hospital cover held)
- **Rebate tier:** Tier 3 (0% rebate at this income level)
- **Tax statements:** One each for Thomas and Isabelle

## H&R Block Checklist Validation

| # | Item | Thomas | Isabelle | Status |
|---|------|--------|----------|--------|
| 1 | PAYG Income Statements | Atlassian, SEEK | SCRATCH | ☐ |
| 2 | Lump Sum/Termination | $5,694 + $6,375 leave | — | ☐ |
| 3 | Interest Income | $34.96 (Bank Aus) | — | ☐ |
| 4 | Dividend Statements | $34.46 + $2.81 FC | — | ☐ |
| 5 | Managed Funds | N/A | N/A | ☐ |
| 6 | Rental Property | N/A | N/A | ☐ |
| 7 | Business Income | Tizzi ($0) | N/A | ☐ |
| 8 | Capital Gains | $7,974.12 RSU | — | ☐ |
| 9 | ESS/RSU | $62,270.51 | — | ☐ |
| 10 | Motor Vehicle | N/A | N/A | ☐ |
| 11 | Travel Expenses | N/A | N/A | ☐ |
| 12 | Uniforms | N/A | N/A | ☐ |
| 13 | Subscriptions/Tools | GitHub, ChatGPT, etc. | — | ☐ |
| 14 | Self-Education | — | — | ☐ |
| 15 | Professional Dev | — | — | ☐ |
| 16 | WFH Expenses | 960 hrs | 768 hrs | ☐ |
| 17 | Other Work Expenses | Equipment, phone, internet | Phone, internet | ☐ |
| 18 | Donations | Bravehearts, UNICEF | Cancer Council | ☐ |
| 19 | Income Protection | N/A | N/A | ☐ |
| 20 | Health Insurance | NIB | NIB | ☐ |
| 21 | PAYG Instalments | N/A | N/A | ☐ |
| 22 | Spouse Details | ✓ | ✓ | ☐ |
| 23 | Bank Details | ✓ | ✓ | ☐ |
| 24 | CCS Reconciliation | ✓ | ✓ | ☐ |
| 25 | Division 293 | ✓ | N/A | ☐ |
| 26 | Foreign Income | RSU (USD→AUD) | N/A | ☐ |
| 27 | Government Payments | N/A | N/A | ☐ |

## Tax Estimates Reference

| Metric | Thomas | Isabelle | Combined |
|--------|--------|----------|----------|
| Taxable Income | $256,334.11 | $112,669.80 | $369,003.91 |
| Income Tax | — | — | $106,077.29 |
| Medicare Levy | — | — | $7,380.08 |
| Division 293 | $3,112.03 | — | $3,112.03 |

**CCS:** Reported $254,000 → Actual $369,003.91
**CCS Repayment Expected:** $10,785.10 (reducible to $7,449.47 with $4k+ deductions)

## Missing Documents Checklist

| Document | Owner | Status |
|----------|-------|--------|
| NAB credit card statements (Jul-Aug 2024) | Thomas | ⛔ TO ADD |
| CCS annual statement | Isabelle | ✓ Has |
| Bank Australia interest statement | Shared | ✓ Has |
| Internet bills (12 months) | Shared | ☐ To collect |
| Phone bills (12 months) | Both | ☐ To collect |
| LinkedIn Premium receipts | Thomas | ☐ To collect |

## Currency Conversion Rules

For RSUs and foreign income:
1. Use **ATO monthly exchange rate** for the vesting/payment date
2. Source: [ATO Foreign Exchange Rates](https://www.ato.gov.au/Rates/Foreign-exchange-rates/)
3. Document: USD amount × ATO rate = AUD amount

## Agent Task Checklist

When preparing documents:
1. **Rename files** to `YYMMdd - Description.ext` format
2. **Organise** into numbered folder structure
3. **Sum deductions** and verify $4,000+ target for Thomas
4. **Flag missing documents** from checklist above
5. **Calculate WFH hours** - Thomas 960, Isabelle 768
6. **Convert foreign amounts** to AUD with documented rates
7. **Verify DGR status** for all donation recipients
8. **Create INDEX.md** summarising all documents and totals

## Important ATO Compliance Notes

- Keep receipts for 5 years
- Substantiation required for claims over $300 (total work expenses)
- Home office claims require contemporaneous records
- ESS/RSU income: Report in year of vesting, not sale
- Division 293: Applies when income + super contributions > $250,000
- Phone/internet: 60-70% work use justified by remote work patterns
- LinkedIn Premium: Only Tizzi marketing portion deductible (not job searching)
