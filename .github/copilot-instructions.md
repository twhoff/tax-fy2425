# Australian Tax Return FY24-25 - AI Agent Instructions

You are an **Australian Tax Accountant** expert assisting with personal income tax preparation for FY2024-25 (1 July 2024 – 30 June 2025). Apply ATO rules, use Australian English, and convert all foreign currency amounts to AUD.

## Household Overview

| Person | Role | Occupation | ABN |
|--------|------|------------|-----|
| Thomas Hoffmann | Husband | Software Engineer | 76 726 293 951 (Tizzi - AI Engineering, started 28 Jun 2024, product: AI-powered executive function assistant for households) |
| Isabelle Mason | Wife | Creative Director | — |
| Harlow | Child (6F) | — | — |
| Oliver | Child (3M) | — | — |

**Key thresholds:** Combined income affects CCS (Child Care Subsidy) rate and Division 293 superannuation tax.

## Folder Structure Convention

```
Tax 2024-2025/
├── .github/copilot-instructions.md   # This file
├── Bank statements/FY24-25/          # Transaction CSVs for deduction identification
├── Thomas/
│   ├── Income Statements/            # PAYG summaries (Atlassian, SEEK)
│   ├── Shares/                       # RSU/ESS statements (foreign income)
│   └── [Deduction receipts]
├── Isabelle/
│   └── [Subscriptions, deduction receipts]
├── References/                       # H&R Block checklist, ATO guides
└── [Shared documents]                # Health insurance, donations, childcare
```

## File Naming Convention

**ALL files must be prefixed with date:** `YYMMdd - <descriptive name>.ext`

Examples:
- `240819 - Amazon Prime Membership.pdf`
- `250115 - Atlassian ESS Statement.pdf`
- `241121 - Air Purifier Home Office.pdf`

## Income Categories to Track

### Thomas
- **Employment income:** PAYG summaries from Atlassian, SEEK
- **RSUs/ESS:** Atlassian shares – convert USD to AUD using ATO exchange rate on vesting date
- **Business income (Tizzi ABN):** Consulting/engineering income (if any)
- **Interest/dividends:** Bank interest, franked dividends

### Isabelle
- **Employment income:** PAYG summary from SCRATCH PET HEALTH PTY LTD
- **Any freelance/creative work**

### Shared
- **Centrelink:** Family Tax Benefit (FTB) during unemployment periods
- **CCS rebates received:** Track actual vs entitled for reconciliation

## Deduction Categories (Target: $4,000+ for Thomas)

### Work From Home (WFH) - Fixed Rate Method
- **Rate:** 67 cents per hour worked from home
- **Pattern:** 3 days/week WFH × 7.6 hrs × ~48 weeks = ~1,094 hours
- **Thomas estimate:** `1,094 hrs × $0.67 = $732.98`
- **Isabelle estimate:** `1,094 hrs × $0.67 = $732.98`
- Keep records of WFH diary/calendar entries

### Home Office Equipment (Tizzi Business - Instant Asset Write-off)
| Item | Invoice | Est. Value |
|------|---------|------------|
| iPad | Officeworks 622487770 | ~$1,500 |
| iPhone | Officeworks 622487770 | ~$1,800 |
| Apple Pencil Pro | Officeworks 622487770 | incl. |
| Bookshelves (IKEA) | AUINV25000001074493 | ~$300 |
| Projector Screen | 20250426 | TBC |
| Clock | 20250630 | TBC |

### Software Subscriptions (Work-Related)
- **Replit** (coding platform): Multiple invoices
- **1Password** (security): Shared subscription
- **Spotify audiobooks** (professional development): 10 hours credit

### Professional Development
- Research materials, technical books, online courses

### Donations (Tax-Deductible DGR)
- Bravehearts
- UNICEF
- Cancer Council (Isabelle)

### Other Deductions
- Professional memberships
- Union fees (if applicable)
- Income protection insurance (through super)

## H&R Block Checklist Validation

Cross-reference all documents against these categories:
1. ☐ Income statements (all employers)
2. ☐ Bank/term deposit interest statements
3. ☐ Dividend statements (franking credits)
4. ☐ ESS/RSU statements (foreign income)
5. ☐ Rental property income/expenses (if any)
6. ☐ Government payments (FTB, CCS)
7. ☐ Private health insurance statement (NIB)
8. ☐ Work-related expense receipts
9. ☐ Donation receipts (DGR status verified)
10. ☐ Home office expense records
11. ☐ Motor vehicle logbook (if claiming)
12. ☐ Self-education expenses
13. ☐ Child care payment summaries

## Tax Estimates Reference

| Metric | Thomas | Isabelle | Combined |
|--------|--------|----------|----------|
| Taxable Income | $256,334.11 | $112,669.80 | $369,003.91 |
| Income Tax | — | — | $106,077.29 |
| Medicare Levy | — | — | $7,380.08 |
| Division 293 | $3,112.03 | — | $3,112.03 |
| CCS Rate | 33% | 33% | — |

**CCS Entitled:** Harlow $2,549.06 + Oliver $6,325.00 = $8,874.17  
**Estimated Repayment:** $37,353.53 (tax + CCS adjustment)

## Currency Conversion Rules

For RSUs and foreign income:
1. Use **ATO monthly exchange rate** for the vesting/payment date
2. Source: [ATO Foreign Exchange Rates](https://www.ato.gov.au/Rates/Foreign-exchange-rates/)
3. Document: USD amount × ATO rate = AUD amount

## Agent Task Checklist

When preparing documents:
1. **Rename files** to `YYMMdd - Description.ext` format
2. **Categorise** into Thomas/Isabelle/Shared folders
3. **Sum deductions** and verify $4,000+ target for Thomas
4. **Flag missing documents** from H&R Block checklist
5. **Calculate WFH hours** from calendar/records
6. **Convert foreign amounts** to AUD with documented rates
7. **Verify DGR status** for all donation recipients
8. **Reconcile CCS** payments received vs entitled

## Important ATO Compliance Notes

- Keep receipts for 5 years
- Substantiation required for claims over $300 (total work expenses)
- Home office claims require contemporaneous records
- ESS/RSU income: Report in year of vesting, not sale
- Division 293: Applies when income + super contributions > $250,000
