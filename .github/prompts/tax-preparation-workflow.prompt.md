---
description: Workflow for preparing Australian tax documents for H&R Block appointment using Beads issue tracking.
model: Claude Opus 4.5 (copilot)
argument-hint: Use this prompt to guide the AI through the tax document preparation workflow for Thomas Hoffmann and Isabelle Mason for the 2024-2025 financial year.
---

# Tax FY24-25 Preparation Workflow

> **Implementation prompt for AI agents to prepare Australian tax documents for H&R Block appointment**

## Quick Start

```bash
cd "/Users/twhoffmann/Library/CloudStorage/GoogleDrive-hoffmatw@gmail.com/My Drive/Filing Cabinet/Australia/Tax/Tax 2024-2025"
source ~/Projects/TaxFY2425/.venv/bin/activate
bd ready  # View available work
```

## Critical Context

- **Appointment:** H&R Block (tomorrow)
- **Goal:** Prepare all documents for Thomas Hoffmann and Isabelle Mason tax returns
- **Critical Threshold:** $4,000+ deductions for Thomas to avoid $3,336 CCS penalty
- **Combined Taxable Income:** ~$369,003.91 (need to reduce below $365,604)

## Workflow Phases

Execute phases in order. Each phase has Beads issues - use `bd show <id>` for details.

---

### Phase 1: OCR Document Processing (Epic `hyn`)

**Objective:** Extract dates and metadata from PDF documents

```bash
bd show hyn       # View epic details
bd ready hyn      # See child issues
```

**Implementation:**
1. Create Python script using pytesseract + PyMuPDF
2. Process PDFs to extract:
   - Document date (for filename prefix)
   - Document type (income, deduction, etc.)
   - Amount (if applicable)
   - Person (Thomas/Isabelle/Shared)
3. Output: JSON manifest of all documents with extracted metadata

**Key Files:**
- Input: `*.pdf` files in workspace subfolders
- Output: `document_manifest.json`

---

### Phase 2: Document Renaming (Epic `hyn.8`)

**Objective:** Rename ALL files to `YYMMdd - Description.ext` format

```bash
bd show hyn.8     # View epic (21 issues for 78 documents)
bd ready hyn.8    # See individual document tasks
```

**Naming Convention:**
```
240819 - Amazon Prime Membership.pdf
250115 - Atlassian ESS Statement.pdf
241121 - Air Purifier Home Office.pdf
```

**Process:**
1. Use OCR manifest from Phase 1
2. Generate new filename based on document date and type
3. Preview renames before executing
4. Execute renames, update manifest

---

### Phase 3: Document Organisation (Epic `42o`)

**Objective:** Organise documents into numbered folder structure

```bash
bd show 42o       # View epic details
bd ready 42o      # See child issues
```

**Target Structure:**
```
Tax 2024-2025/
├── 1. Income/
│   ├── Thomas/         # PAYG, ESS/RSU, termination
│   └── Isabelle/       # PAYG
├── 2. Deductions/
│   ├── Thomas/         # Software, equipment, WFH, phone, internet
│   └── Isabelle/       # Subscriptions, WFH, phone, internet
├── 3. Health Insurance/ # NIB statements
├── 4. Family/
│   ├── Childcare/      # CCS statements
│   └── FTB/
├── 5. Bank Statements/FY24-25/
└── 6. References/      # H&R Block checklist, ATO guides
```

---

### Phase 4: H&R Block Checklist Validation (Epic `nrk`)

**Objective:** Verify all required documents are present

```bash
bd show nrk       # View epic (29 issues)
bd ready nrk      # See checklist items
```

**Checklist Items:**

| # | Item | Thomas | Isabelle |
|---|------|--------|----------|
| 1 | PAYG Income Statements | Atlassian, SEEK | SCRATCH |
| 2 | Termination/Lump Sum | $5,694 + $6,375 | — |
| 3 | Interest Income | $34.96 | — |
| 4 | Dividend Statements | $34.46 + FC | — |
| 5 | ESS/RSU Statements | $62,270.51 | — |
| 6 | Capital Gains | $7,974.12 | — |
| 7 | WFH Records | 960 hrs | 768 hrs |
| 8 | Phone/Internet | 60-70% work | 60-70% work |
| 9 | Software Subscriptions | GitHub, ChatGPT, etc. | — |
| 10 | Donations | Bravehearts, UNICEF | Cancer Council |
| 11 | Health Insurance | NIB | NIB |
| 12 | CCS Statement | — | Annual stmt |

**Critical Missing Documents:**
- ⛔ NAB credit card (Jul-Aug 2024) - user will add
- ☐ Internet bills (12 months)
- ☐ Phone bills (12 months)
- ☐ LinkedIn Premium receipts

---

### Phase 5: Bank Statement Analysis (Epic `gyw`)

**Objective:** Identify tax-relevant transactions from bank statements

```bash
bd show gyw       # View epic details
bd ready gyw      # See child issues
```

**Banks to Analyse:**
| Bank | Type | Tax Relevance |
|------|------|---------------|
| ANZ | Credit Card | Work expenses, subscriptions |
| Bank Australia | Savings | Interest income ($34.96) |
| Bendigo | Offset | Not taxable |
| NAB | Credit Card (Jul-Aug) | ⛔ BLOCKING - user to add |

**Search Patterns:**
```
# Deductions to find
- GitHub Copilot
- ChatGPT / OpenAI
- WARP / Cloudflare
- Medium
- Replit
- 1Password
- LinkedIn Premium
- Bravehearts
- UNICEF
- Cancer Council
- Officeworks (equipment)
- IKEA (home office furniture)
```

---

## Deduction Summary Target

Must achieve **$4,000+ deductions for Thomas** to cross CCS cliff:

| Category | Thomas | Isabelle |
|----------|--------|----------|
| WFH (67c/hr) | $643 | $515 |
| Internet (60-70%) | ~$425 | ~$425 |
| Phone (60-70%) | ~$440 | ~$390 |
| Software (Tizzi) | ~$1,500+ | — |
| Equipment (Tizzi) | ~$3,600+ | — |
| Donations | ~$200 | ~$100 |
| **TOTAL** | **~$6,800+** | ~$1,430 |

✅ Target $4,000 easily achievable with Tizzi strategy

---

## Final Deliverables

Create these files before appointment:

### 1. `INDEX.md` - Document Index
List all documents with amounts and categories

### 2. `DEDUCTIONS_SUMMARY.md` - Deduction Totals
Itemised deductions by person with receipts referenced

### 3. `INCOME_SUMMARY.md` - Income Breakdown
- PAYG summaries
- ESS/RSU details with AUD conversions
- Interest and dividends
- Capital gains calculation

### 4. `CCS_RECONCILIATION.md` - CCS Analysis
- Reported income vs actual
- Expected repayment calculation
- Multi-child discount eligibility

### 5. `MISSING_DOCUMENTS.md` - Outstanding Items
What's still needed and who has it

---

## Beads Commands Reference

```bash
# View work
bd ready              # All available work
bd ready <epic>       # Work in specific epic
bd show <id>          # Issue details

# Update status
bd update <id> --status in_progress
bd close <id>

# Sync with git
bd sync
```

---

## Session Completion Checklist

Before ending session:
- [ ] All documents renamed to `YYMMdd - Description.ext`
- [ ] Documents organised into numbered folders
- [ ] Deductions totalled ($4,000+ for Thomas verified)
- [ ] Missing documents flagged
- [ ] Summary files created
- [ ] Changes committed and pushed to GitHub
- [ ] `bd sync` run to update issues

```bash
git add -A
git commit -m "Tax prep: [describe changes]"
git pull --rebase
bd sync
git push
```
