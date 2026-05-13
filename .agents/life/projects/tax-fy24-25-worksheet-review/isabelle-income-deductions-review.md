# Isabelle Income, HELP and Deductions Review

Related issue: `TaxFY2425-c6j.6`  
Date: 2026-05-13

## Bottom Line

SCRATCH PAYG gross income of `$111,470.05` matches the worksheet, but Isabelle's own H&R Block draft return is missing. Thomas's draft only shows spouse taxable income of `$110,118`, so we cannot confirm how Isabelle's deductions, HELP position, or the separate SCRATCH `Home Office` allowance were entered.

Cancer Council Victoria is source-verified as a DGR and the `$20.37` receipt is present. Most Isabelle D5 items remain H&R Block or household questions because the claims rely on high private-use platforms, 30% apportionment, or unverified event purposes.

## Source Checks Added

- ATO employment allowances: an allowance reported on an annual income statement must be included as income, and receiving an allowance does not create an automatic deduction.
- ATO HELP/HECS: 2024-25 compulsory repayments use repayment income and the table rate. The relevant ranges include `6.5%` for `$106,186-$112,556` and `7.0%` for `$112,557-$119,309`.
- StudyAssist: PAYG deductions for HELP are applied when the tax return is lodged; excess withholding is returned through the tax return if the assessed compulsory repayment is lower.
- ABR DGR endorsed download: Cancer Council Victoria, ABN `61426486715`, is active with DGR status date `2014-01-01`.

## Deterministic Checks

| Check | Result |
| --- | ---: |
| SCRATCH salary and wages | `$98,737.57` |
| SCRATCH bonus | `$1,572.00` |
| SCRATCH other paid leave | `$11,160.48` |
| SCRATCH total gross | `$111,470.05` |
| SCRATCH PAYGW | `$34,312.00` |
| SCRATCH Home Office allowance | `$1,199.64` |
| H&R spouse taxable income in Thomas draft | `$110,118.00` |
| Difference: SCRATCH gross less spouse taxable income | `$1,352.05` |
| Difference: SCRATCH gross plus allowance less spouse taxable income | `$2,551.69` |

Bank-analysis aggregation from `deductible_transactions_v2.csv` where `default_owner == Isabelle` gives `55` rows, `$1,031.78` gross and `$366.23` deductible. That conflicts with the bank cross-check prose summary, which says Isabelle has `$1,109.75` gross (`$1,028.75` streaming plus `$81.00` events). Treat the bank totals as unconfirmed until `TaxFY2425-c6j.8` completes the cross-check.

## Findings

### Income

- `SCRATCH PET HEALTH PAYG`: Confirmed source gross is `$111,470.05`, with `$34,312.00` PAYGW and `$12,819.06` employer super contribution liability.
- `Home Office allowance`: The PAYG source separately reports `$1,199.64`. H&R Block should confirm this was included correctly as income on Isabelle's own return.
- `Bank Australia interest`: Worksheet uses Isabelle's 50% share of `$17.48`; carry to shared household review.
- `Vanguard VDHG`: Thomas's draft shows two account holders and 50% share, but the Vanguard tax statement and Isabelle draft are missing.
- `HELP/HECS`: The PAYG extract does not show a separate HELP-specific withholding line. Final treatment depends on Isabelle's debt balance, debt-cleared date, repayment income, and her own return.

### D5 Work-Related Expenses

- `WFH fixed rate`: Still blocked by missing Isabelle WFH hours and records. The home-office allowance is not a substitute for deduction records.
- `Streaming/research`: Not confirmed. ATO source requires a sufficient connection to current duties and private-use apportionment. The proposed 30% claim needs platform-specific work examples and H&R Block judgement.
- `Events`: Not confirmed. The `$81.00` event total needs actual event names and work purpose before claiming.
- `Cheek Media`: Receipt shows `A$50` for Isabelle. Could be professional reading if connected to current Creative Director duties; ask H&R Block.
- `Cleanup`: Current evidence points to personal device maintenance. Reject unless Isabelle provides a specific work purpose.
- `YouTube Premium` and `Amazon Prime`: Not confirmed; require work-purpose support and apportionment.
- `ChatGPT in Apple receipts`: Keep out of Isabelle D5 unless H&R Block says otherwise, because prior cross-check allocated the ChatGPT components to Thomas/Tizzi.

### D9 Donations

Cancer Council Victoria `$20.37` is supported by receipt and ABR DGR verification. The bank cross-check did not find the transaction, so payment-account reconciliation remains useful but the DGR/source evidence is now resolved.

### D10 Tax Agent Fees

ATO source says spouse invoices need a split and records showing the split. The `$428` H&R Block receipt is addressed to Isabelle, while Thomas's draft claims `$204`. A simple residual would be `$224`, but H&R Block should explain the allocation before Isabelle's D10 amount is entered.

## H&R Block Questions

1. Please provide or confirm Isabelle's own H&R Block draft return.
2. Is the `$1,199.64` SCRATCH Home Office allowance included as income on Isabelle's return?
3. What WFH hours and D5 deductions were entered for Isabelle?
4. Did Isabelle have a HELP debt at assessment, and did payroll continue withholding after the debt was cleared?
5. Should any 30% streaming/research claims be included, reduced, or removed?
6. What were the Exhibition St, Victorian Arts Centre, Arts Centre, and Princess Theatre events?
7. Can Cheek Media `A$50` be claimed as professional reading for current employment duties?
8. Should Cleanup, YouTube Premium, and Amazon Prime be excluded unless more work-purpose evidence is supplied?
9. Can the Cancer Council Victoria receipt be used despite the bank cross-check not finding the transaction?
10. How should the `$428` H&R Block fee receipt be split between Thomas and Isabelle?

## Blocked Inputs

- Isabelle's own H&R Block draft return.
- HELP/HECS debt balance and debt-cleared date.
- Any payroll detail showing HELP-specific withholding.
- Isabelle's actual WFH hours and records.
- Platform-by-platform work-use explanations.
- Event details for the four event transactions.
- Payment-account reconciliation for the Cancer Council donation.