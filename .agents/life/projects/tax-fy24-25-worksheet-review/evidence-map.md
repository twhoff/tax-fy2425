# Worksheet Evidence Map

Related issue: `TaxFY2425-c6j.2`
Last updated: 2026-05-13

Canonical structured map: `evidence-map.yaml`.

## What This Map Covers

The map links every main worksheet section and every bank cross-check category to evidence files, missing evidence, owner, and classification.

Classifications used: `household_answer_needed`, `source_law_question`, `calculation_check`, `evidence_gap`, `h_and_r_block_decision`.

## Core Evidence Present

- Thomas income: Atlassian PAYG, SEEK PAYG, Atlassian ESS, SelfWealth annual statement, Bank Australia interest statement, and H&R Block draft.
- Isabelle income: SCRATCH PAYG statement.
- Deductions: Thomas and Isabelle receipt folders are populated, including key Tizzi assets, donations, streaming/subscriptions, and selected Officeworks/Amazon/IKEA evidence.
- Health insurance: both NIB statements are present.
- Bank analysis: all transaction/cross-reference CSV and markdown outputs are present.
- H&R Block draft: PDF and OCR markdown are present for Thomas.

## Priority Gaps Preserved

- `4. Family` has no files in the worktree.
- Early FY ANZ coverage is still a live reconciliation item: current ANZ analysis starts on 9 Sep 2024.
- Bank Australia coverage is resolved in the current analysis files: the CSV runs from 1 Jul 2024 to 30 Jun 2025.
- Two Apple transactions still need purchase-history evidence: 14/02/2025 $15.00 and 23/06/2025 $63.98.
- Amazon and IKEA classifications must be checked at receipt/item level.
- Receipt cross-reference matches were sanity-checked in `TaxFY2425-c6j.8`; multiple false positives were found, so generated matches must not be used automatically.
- Isabelle's separate H&R Block draft return was not found.
- Several tax-law sources are still `source_needed` or `source_identified_extract_pending` in the source register, although Thomas employee deduction, Tizzi, Isabelle HELP/allowance, Cancer Council DGR, MLS/PHI rebate thresholds, Division 293, and CCS/FTB balancing sources have now been refreshed.

## Next Routing

- Income, ESS, CGT: `TaxFY2425-c6j.3`
- Thomas employee deductions: `TaxFY2425-c6j.4`
- Tizzi business schedule: `TaxFY2425-c6j.5`
- Isabelle income and deductions: `TaxFY2425-c6j.6`
- Shared household items: `TaxFY2425-c6j.7`
- Bank and receipt cross-check: `TaxFY2425-c6j.8`
- Deterministic calculation rerun: `TaxFY2425-c6j.9`
- H&R Block change pack: `TaxFY2425-c6j.10`