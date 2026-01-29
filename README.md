# 🧾 Australian Tax Return FY 2024-25

**Household:** Thomas Hoffmann & Isabelle Mason  
**Financial Year:** 1 July 2024 – 30 June 2025  
**Status:** Ready for H&R Block appointment

---

## 📊 Quick Summary

| Metric | Thomas | Isabelle | Combined |
|--------|--------|----------|----------|
| **Taxable Income (est.)** | $256,334 | $112,670 | $369,004 |
| **Deductions** | $4,181+ | $1,500+ | $5,681+ |
| **WFH Hours** | 960 hrs | 1,095 hrs | 2,055 hrs |
| **WFH Deduction (70c/hr)** | $672 | $766 | $1,438 |

### Key Thresholds
- ✅ **CCS $4k target achieved** - Thomas deductions exceed $4,000
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
├── 4. Family/
│   ├── Childcare/       # CCS statements
│   └── FTB/             # Family Tax Benefit
├── 5. Bank Statements/
│   ├── FY24-25/         # ANZ statements
│   └── Analysis/        # Transaction analysis
└── 6. References/       # H&R Block checklist
```

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

### Thomas ($4,180.85+)

| Category | Amount | Key Items |
|----------|--------|-----------|
| **Home Office Equipment** | $3,906 | iPad Pro M4, iPhone, monitors, Ring cameras |
| **Software Subscriptions** | $274+ | Replit, ChatGPT, GitHub Copilot, 1Password |
| **WFH Fixed Rate** | $672 | 960 hours × $0.70/hr |
| **Donations** | $500 | UNICEF $250, Bravehearts $250 |

### Isabelle ($1,500+)

| Category | Amount | Key Items |
|----------|--------|-----------|
| **Creative Subscriptions** | $394 | Adobe, Canva (pro-rated work use) |
| **Streaming (work research)** | $300 | Paramount+, Hayu (Creative Director research) |
| **WFH Fixed Rate** | $766 | 1,095 hours × $0.70/hr |
| **Donations** | $20 | Cancer Council |

---

## ✅ Status: Ready for Appointment

All checklist items validated. `bd ready` shows no open issues.

**Confirmed:**
- ✅ CCS statement not needed for tax return (Centrelink calculates after NOA issued)
- ✅ No FTB received during employment gap
- ⚠️ WFH hours: Discuss documentation approach with H&R Block

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
| 2 | Lump Sum/Termination | ✅ Leave payouts | — |
| 3 | Government Payments | ✅ N/A (no FTB) | ✅ N/A (no FTB) |
| 4 | Interest Income | ✅ Bank Aus $35 | — |
| 5 | Dividends | ✅ SelfWealth $34 | — |
| 6 | Managed Funds | N/A | N/A |
| 7 | Rental Property | N/A | N/A |
| 8 | Business Income | ✅ Tizzi ($0 rev) | N/A |
| 9 | Foreign Income | ✅ RSUs in ESS | — |
| 10 | Capital Gains | ✅ $7,974 RSU | — |
| 11 | Employee Share Schemes | ✅ $62,270 | — |
| 12 | Motor Vehicle | N/A | N/A |
| 13 | Travel | N/A | N/A |
| 14 | Uniforms | N/A | N/A |
| 15 | Subscriptions/Tools | ✅ | ✅ |
| 16 | Self-Education | N/A | N/A |
| 17 | WFH Expenses | ⚠️ Discuss with H&R | ⚠️ Discuss with H&R |
| 18 | Other Work Expenses | ✅ Equipment | — |
| 19 | Donations | ✅ $500 | ✅ $20 |
| 20 | Income Protection | N/A | N/A |
| 21 | Health Insurance | ✅ NIB | ✅ NIB |
| 22 | PAYG Instalments | N/A | N/A |
| 23 | Spouse Details | ✅ | ✅ |
| 24 | Bank Details | ✅ Shared account | ✅ Shared account |

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

### CCS Strategy
- Combined income ~$369k exceeds CCS cliff at $367,563
- Thomas deductions $4k+ crosses multi-child discount threshold
- Expected saving: ~$3,336 on CCS repayment

### Tizzi ABN (76 726 293 951)
- Started 28 Jun 2024
- $0 revenue FY24-25 (expenses only)
- Equipment via instant asset write-off

---

*Generated with assistance from GitHub Copilot using Claude Opus 4.5*
