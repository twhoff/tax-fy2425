# FY24-25 Tax Worksheet And Knowledge Base Plan

Created: 2026-05-13 16:44 AWST
Issue: TaxFY2425-c6j
Status: superseded by approved Beads epic and child issue structure

## Goal

Work through the two review worksheets and produce an accountant-ready pack for H&R Block. The work must be decomposed into small Beads epics and tasks so each chunk is manageable and low-risk.

## Non-negotiable Constraints

- Do not rely on model memory or training data for Australian tax law or regulation.
- Treat every tax-law assertion as untrusted until verified from the ATO website or another credible source for FY2024-25.
- Record the source URL, access date, FY relevance, and exact claim before using the claim in the worksheets.
- Use deterministic scripts for calculations; do not calculate in the agent's head.
- Use `vscode_askQuestions` for quick household facts that block progress.
- Do not edit tax worksheets or create child epics until the user approves the Track workflow decomposition.

## Relevant Repository Evidence

- `260315 - Deduction Review Worksheet.md`: household review checklist and H&R Block questions.
- `260315 - Bank Statement Deduction Cross-Check.md`: transaction-level deduction candidates and coverage gaps.
- `7. HR Block Worksheet (Draft)/J0178900 - 2025 I Form (Worksheets).md`: Thomas draft return extracted from H&R Block.
- `5. Bank Statements/Analysis/FY24-25-Analysis.md`: bank statement analysis and generated cross-reference files.
- `scripts/tax_categories.py`: current transaction categorisation assumptions.
- `verify_calculations.py`: deterministic calculation script, including warnings about WFH fixed-rate and separate internet claims.

## Proposed Beads Structure

Epic: Complete FY24-25 household tax worksheet review and H&R Block change pack.

Child 1: Build source-verified FY24-25 tax knowledge base.
Acceptance criteria:
- Tax topics are extracted from the repo, not invented.
- Each tax rule has an ATO or credible source citation with access date.
- Unverified claims are marked as open questions, not conclusions.
- The knowledge base is stored under the project-local `.agents` PARA structure.

Child 2: Reconcile Thomas income, ETP, ESS, RSU CGT, interest, dividends, and managed funds.
Acceptance criteria:
- Compare H&R Block figures against source documents and scripts.
- Flag the Atlassian ETP discrepancy, ESS discrepancy, and missing/unclear RSU CGT treatment.
- Produce exact H&R Block questions with supporting evidence.

Child 3: Review Thomas employee deductions.
Acceptance criteria:
- Check WFH fixed-rate method and whether separate internet/phone claims are permitted for the chosen method using verified sources.
- Review D4, D5, D9, D10 items against evidence and source-verified rules.
- Identify double-counting, apportionment, and substantiation risks.

Child 4: Review Tizzi business schedule and deferred loss.
Acceptance criteria:
- Verify business income, expenses, instant asset write-off/depreciation treatment, private-use apportionment, and non-commercial loss treatment from sources.
- Produce a clear list of claims to keep, amend, or ask H&R Block about.

Child 5: Review Isabelle income and deductions.
Acceptance criteria:
- Reconcile SCRATCH PAYG, Bank Australia interest, Vanguard/ETF ownership, HELP withholding, WFH hours, streaming/research claims, events, donations, and tax-agent fees.
- Separate household answers needed from source-law questions.

Child 6: Review shared household tax items.
Acceptance criteria:
- Verify private health insurance, Medicare levy surcharge exemption, spouse details, Division 293, CCS/FTB timing, dependants, and bank account assumptions.
- Identify which items affect the return versus post-lodgement reconciliation.

Child 7: Complete bank statement and receipt cross-check.
Acceptance criteria:
- Resolve known coverage gaps, including missing July 2024 ANZ data, Bank Australia coverage, Cancer Council donation, unknown Apple items, Amazon receipt matching, IKEA classification, and additional tool/software searches.
- Mark each candidate as confirmed, rejected, or question for household/H&R Block.

Child 8: Re-run deterministic calculations and prepare H&R Block pack.
Acceptance criteria:
- Run the calculation scripts after confirmed inputs are updated.
- Generate a concise change/request summary for H&R Block.
- Update the worksheets with confirmed notes and unresolved questions.

## Current Tracker State

The Track workflow decomposition was approved. `TaxFY2425-c6j` is now the parent epic with children `TaxFY2425-c6j.1` through `TaxFY2425-c6j.11`.

Ready Wave 1 tasks:

- `TaxFY2425-c6j.1` - Build FY24-25 source register and topic index.
- `TaxFY2425-c6j.2` - Map worksheet items to evidence files.

The detailed Beads issue graph is now the source of truth for execution order.
