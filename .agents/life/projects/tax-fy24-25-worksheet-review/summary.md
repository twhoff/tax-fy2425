# Tax FY24-25 Worksheet Review

Status: active
Last updated: 2026-05-13
Related issue: TaxFY2425-c6j

## Summary

This project is to complete the household FY2024-25 tax review worksheets and prepare an accountant-ready H&R Block change/request pack.

The work has been split into Beads epic `TaxFY2425-c6j` with child tasks `TaxFY2425-c6j.1` through `TaxFY2425-c6j.11`. The first executable wave is the source register and evidence map.

## Source Verification Rule

Do not rely on internal model knowledge for Australian tax law. Every tax-law assertion must be verified from the ATO website or another credible source for FY2024-25 before it is used.

## Main Evidence Files

- `260315 - Deduction Review Worksheet.md`
- `260315 - Bank Statement Deduction Cross-Check.md`
- `7. HR Block Worksheet (Draft)/J0178900 - 2025 I Form (Worksheets).md`
- `5. Bank Statements/Analysis/FY24-25-Analysis.md`
- `scripts/tax_categories.py`
- `verify_calculations.py`

## Current State

A planning note exists at `plans/2026-05-13-tax-worksheet-knowledge-base-plan.md`. The Track workflow decomposition was approved, the epic and 11 children were created, dependencies were validated as acyclic and swarmable, and the Dolt remote is configured as `origin`.

`TaxFY2425-c6j.1` is closed. The local source register lives at `.agents/life/resources/tax-fy24-25/source-register.yaml`, with a readable topic index at `.agents/life/resources/tax-fy24-25/topic-index.md`.

`TaxFY2425-c6j.2` is closed. The worksheet evidence map lives at `.agents/life/projects/tax-fy24-25-worksheet-review/evidence-map.yaml`, with a readable summary at `.agents/life/projects/tax-fy24-25-worksheet-review/evidence-map.md`.

`TaxFY2425-c6j.3` is closed. Thomas income, ESS and CGT reconciliation lives at `.agents/life/projects/tax-fy24-25-worksheet-review/thomas-income-reconciliation.yaml`, with a readable summary at `.agents/life/projects/tax-fy24-25-worksheet-review/thomas-income-reconciliation.md`.

`TaxFY2425-c6j.4` is closed. Thomas employee deduction review lives at `.agents/life/projects/tax-fy24-25-worksheet-review/thomas-employee-deductions-review.yaml`, with a readable summary at `.agents/life/projects/tax-fy24-25-worksheet-review/thomas-employee-deductions-review.md`.

`TaxFY2425-c6j.5` is closed. Tizzi business schedule review lives at `.agents/life/projects/tax-fy24-25-worksheet-review/tizzi-business-schedule-review.yaml`, with a readable summary at `.agents/life/projects/tax-fy24-25-worksheet-review/tizzi-business-schedule-review.md`.

`TaxFY2425-c6j.6` is closed. Isabelle income, HELP and deduction review lives at `.agents/life/projects/tax-fy24-25-worksheet-review/isabelle-income-deductions-review.yaml`, with a readable summary at `.agents/life/projects/tax-fy24-25-worksheet-review/isabelle-income-deductions-review.md`.

`TaxFY2425-c6j.7` is closed. Shared household tax item review lives at `.agents/life/projects/tax-fy24-25-worksheet-review/shared-household-tax-items-review.yaml`, with a readable summary at `.agents/life/projects/tax-fy24-25-worksheet-review/shared-household-tax-items-review.md`.

`TaxFY2425-c6j.8` is closed. Bank and receipt cross-check review lives at `.agents/life/projects/tax-fy24-25-worksheet-review/bank-receipt-cross-check-review.yaml`, with a readable summary at `.agents/life/projects/tax-fy24-25-worksheet-review/bank-receipt-cross-check-review.md`.

`TaxFY2425-c6j.9` is closed. Deterministic calculation review lives at `.agents/life/projects/tax-fy24-25-worksheet-review/deterministic-calculation-review.yaml`, with a readable summary at `.agents/life/projects/tax-fy24-25-worksheet-review/deterministic-calculation-review.md`.

`TaxFY2425-c6j.10` is closed. The accountant-facing change/request pack lives at `260513 - H&R Block Change Request Pack.md`. The household worksheet `260315 - Deduction Review Worksheet.md` has been updated with corrected notes for Atlassian ETP/unused leave, ESS amount, internet/WFH method, SEEK D9 salary-sacrifice risk, Isabelle allowance/spouse details, CCS stress testing, ANZ coverage gap, and final sign-off wording.

`TaxFY2425-c6j.11` is closed. The household-facing final review and sign-off file lives at `260513 - Final Household Review and Sign-Off.md`. Current recommendation: ready for accountant review, not ready for final lodgement approval until the listed H&R Block and household confirmations are resolved.
