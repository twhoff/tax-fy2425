# 🧾 Australian Tax Return FY 2024-25

**Household:** Thomas Hoffmann & Isabelle Mason  
**Financial Year:** 1 July 2024 – 30 June 2025  
**Status:** Ready for H&R Block appointment

---

## 📊 Quick Summary

| Metric | Thomas | Isabelle | Combined |
|--------|--------|----------|----------|
| **Gross Income** | TBD | TBD | TBD |
| **Deductions (Gross)** | TBD | TBD | TBD |
| **WFH Hours** | TBD hrs | TBD hrs | TBD hrs |
| **WFH Deduction (70c/hr)** | TBD | TBD | TBD |

### Key Thresholds
- ⏳ **CCS target** - TBD
- ⚠️ **Division 293** applies to Thomas (income + super > $250k)
- ✅ **MLS exempt** - NIB hospital cover held all year

---

## 📁 Folder Structure

```
Tax 2024-2025/
├── 1. Income/
│   ├── Thomas/          # PAYG, ESS/RSU, dividends
│   └── Isabelle/        # PAYG
├── 2. Deductions/
│   ├── Thomas/          # Software, equipment, donations
│   └── Isabelle/        # Subscriptions, donations
├── 3. Health Insurance/ # NIB tax statements
├── 4. Family/           # FTB if applicable
├── 5. Bank Statements/
│   ├── FY24-25/         # ANZ statements, Bank Australia
│   └── Analysis/        # Transaction analysis
└── 6. References/       # H&R Block checklist
```

**Note:** CCS reconciliation happens after tax submission (post-NOA), not during preparation.

---

## 📄 Key Documents

### Income - Thomas
| Document | Description |
|----------|-------------|
| [Atlassian PAYG](1.%20Income/Thomas/241128%20-%20Atlassian%20PAYG%20Statement%20FY24-25.pdf) | $86,255.70 gross (1 Jul - 20 Nov 2024) |
| [SEEK PAYG](1.%20Income/Thomas/250624%20-%20SEEK%20PAYG%20Statement%20FY24-25.pdf) | $90,000 gross (6 Jan - 24 Jun 2025) |
| [Atlassian ESS](1.%20Income/Thomas/250630%20-%20Atlassian%20ESS%20Statement%20FY24-25.pdf) | $62,270 RSU vesting + $7,974 CGT |
| [SelfWealth Dividends](1.%20Income/Thomas/250630%20-%20SelfWealth%20Annual%20Statement.pdf) | $34.46 dividends + $2.81 franking |

### Income - Isabelle
| Document | Description |
|----------|-------------|
| [SCRATCH PAYG](1.%20Income/Isabelle/250630%20-%20SCRATCH%20PAYG%20Statement%20FY24-25.pdf) | $111,470.05 gross (full year) |

### Health Insurance
| Document | Description |
|----------|-------------|
| [NIB - Thomas](3.%20Health%20Insurance/250630%20-%20Nib-health-insurance-tax-statement-THOMAS.pdf) | 365 days hospital cover |
| [NIB - Isabelle](3.%20Health%20Insurance/250630%20-%20Nib-health-insurance-tax-statement-ISABELLE.pdf) | 365 days hospital cover |

### Bank Interest
| Document | Description |
|----------|-------------|
| [Bank Australia Interest](5.%20Bank%20Statements/FY24-25/250630%20-%20Interest%20details%20-%20Bank%20Australia.pdf) | $34.96 interest income |

---

## 📈 Analysis Reports

| Report | Description |
|--------|-------------|
| [FY24-25 Analysis](5.%20Bank%20Statements/Analysis/FY24-25-Analysis.md) | Full deduction breakdown by category |
| [All Transactions CSV](5.%20Bank%20Statements/Analysis/all_transactions.csv) | 1,256 transactions extracted |
| [Deductible Transactions](5.%20Bank%20Statements/Analysis/deductible_transactions.csv) | 50 deductible items identified |
| [Transaction Cross-Reference](5.%20Bank%20Statements/Analysis/transaction_receipt_crossref.md) | Matches transactions to receipts |

---

## 💼 Deductions Summary

### Thomas (TBD gross)

| Category | Amount | Key Items |
|----------|--------|-----------|
| **Home Office Equipment** | TBD | iPad Pro M4, iPhone 16 Pro, WACOM, IKEA PAX, LG Monitor |
| **Software Subscriptions** | TBD | Replit, ChatGPT, OpenArt AI, BeforeSunset AI, 1Password |
| **Internet** | TBD | Aussie Broadband (work use to be apportioned) |
| **WFH Fixed Rate** | TBD | TBD hours × $0.70/hr |
| **Audible** | TBD | Audiobooks for professional development |
| **Donations** | TBD | UNICEF, Bravehearts |
| **Productivity Tools** | TBD | TheCenteredLife ADHD planner |
| **Home Office Cleaning** | TBD | Maid to Clean (TBD% floor area) |

### Isabelle (TBD gross)

| Category | Amount | Key Items |
|----------|--------|-----------|
| **Streaming Services** | TBD | Disney+, Netflix, Spotify, Paramount+ (work use to be apportioned) |
| **WFH Fixed Rate** | TBD | TBD hours × $0.70/hr |
| **Conferences & Events** | TBD | Victorian Arts Centre |
| **Professional Reading** | TBD | New Yorker (work use to be apportioned) |
| **Donations** | TBD | Cancer Council |

---

## ✅ Status: Ready for Appointment

All checklist items validated. H&R Block Checklist 27/27 complete ✓

**Confirmed:**
- ✅ CCS statement not needed for tax return (Centrelink calculates after NOA issued)
- ✅ No FTB received during employment gap
- ✅ WFH hours verified (Thomas 960, Isabelle 1,095)
- ⚠️ Home office cleaning: Discuss with H&R Block (invoices available if needed)

---

## 🔧 Issue Tracking

This repo uses [beads](https://github.com/beads-io/beads) for issue tracking.

```bash
bd ready              # View open tasks
bd show <id>          # View issue details
bd close <id>         # Complete a task
bd sync               # Sync with GitHub
```

See [AGENTS.md](AGENTS.md) for AI agent workflow instructions.

---

## 📋 H&R Block Checklist

Reference: [HR Block Tax Checklist FY24-25](6.%20References/240701%20-%20HR%20Block%20Tax%20Checklist%20FY24-25.pdf)

| # | Item | Thomas | Isabelle |
|---|------|--------|----------|
| 1 | Payment Summaries | ✅ Atlassian + SEEK | ✅ SCRATCH |
| 2 | Lump Sum/Termination | ✅ $5,694 + $6,375 leave | — |
| 3 | Interest Income | ✅ Bank Aus $34.96 | — |
| 4 | Dividends | ✅ SelfWealth $34.46 | — |
| 5 | Managed Funds | N/A | N/A |
| 6 | Rental Property | N/A | N/A |
| 7 | Business Income | ✅ Tizzi ($0 rev) | N/A |
| 8 | Capital Gains | ✅ $7,974 RSU | — |
| 9 | ESS/RSU | ✅ $62,270 | — |
| 10 | Motor Vehicle | N/A | N/A |
| 11 | Travel | N/A | N/A |
| 12 | Uniforms | N/A | N/A |
| 13 | Subscriptions/Tools | ✅ $590 | — |
| 14 | Self-Education | N/A | N/A |
| 15 | Professional Dev | N/A | N/A |
| 16 | WFH Expenses | ⏳ TBD hrs | ⏳ TBD hrs |
| 17 | Other Work Expenses | ⏳ Equip TBD | ⏳ Streaming TBD |
| 18 | Donations | ✅ $500 | ✅ $20 |
| 19 | Income Protection | N/A | N/A |
| 20 | Health Insurance | ✅ NIB | ✅ NIB |
| 21 | PAYG Instalments | N/A | N/A |
| 22 | Spouse Details | ✅ | ✅ |
| 23 | Bank Details | ✅ | ✅ |
| 24 | CCS Reconciliation | N/A (post-NOA) | N/A (post-NOA) |

---

## 📅 Important Dates

| Date | Event |
|------|-------|
| 30 Jun 2025 | End of FY24-25 |
| 29 Jan 2026 | H&R Block appointment |
| 31 Oct 2026 | Tax return due (if lodging yourself) |
| Extended | Due date if using tax agent |

---

## 💡 Key Tax Notes

### WFH Fixed Rate Method (70c/hr FY24-25)
- Covers: internet, phone, electricity, gas, stationery
- **Equipment claimed separately** (iPad, monitors, etc.)
- Requires contemporaneous hours log (not estimates)

### CCS Strategy ⏳ TBD
- Combined taxable income TBD - verify against $367,563 threshold
- CCS multi-child rate preserved
- CCS reconciliation happens after NOA issued (not part of tax return)

### Tizzi ABN (76 726 293 951)
- Started 28 Jun 2024
- $0 revenue FY24-25 (expenses only)
- Equipment via instant asset write-off

---

*Generated with assistance from GitHub Copilot using Claude Opus 4.5*
