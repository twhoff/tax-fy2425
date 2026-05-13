# Shared Household Tax Items Review

Related issue: `TaxFY2425-c6j.7`  
Date: 2026-05-13

## Bottom Line

The shared private health insurance evidence is internally consistent. Both NIB statements show membership `23913733`, `365` days of appropriate private patient hospital cover, two premium rows (`$1,708` benefit code `30` and `$594` benefit code `31`), and rebate received `$0`. Thomas's H&R Block draft matches those rows.

The main open lodgement questions are not about the NIB data itself. They are Isabelle's missing H&R Block draft, whether Thomas's draft income-test field `Number of dependent children = 0` is correct for that field, joint income/investment ownership, and final calculation reruns after the remaining bank cross-check work.

## Source Checks Added

- ATO Medicare levy surcharge: if appropriate private patient hospital cover applies to the taxpayer, spouse and dependants, MLS is not payable; otherwise income thresholds determine the rate.
- ATO 2024-25 MLS thresholds: family Tier 3 starts at `$302,001`, with a `$1,500` increase for each MLS dependent child after the first.
- ATO 2024-25 PHI rebate thresholds: the same family threshold bands apply, and Tier 3 rebate is `0.000%`.
- ATO Division 293: applies where Division 293 income plus concessional contributions exceed `$250,000`; the tax is `15%` of the excess over the threshold or taxable super contributions, whichever is less, and a separate notice is issued after the ATO receives tax return and fund contribution data.
- Services Australia CCS/FTB: CCS and FTB are balanced separately after income is confirmed; when returns are lodged, the ATO sends income details to Services Australia.

## Deterministic Checks

| Check | Result |
| --- | ---: |
| Thomas taxable income in H&R draft | `$246,198` |
| Isabelle taxable income in Thomas spouse details | `$110,118` |
| Combined taxable income from those draft figures | `$356,316` |
| 2024-25 family Tier 3 start before child uplift | `$302,001` |
| Second-child threshold uplift | `$1,500` |
| Adjusted family Tier 3 start for two children | `$303,501` |
| Draft combined taxable income above adjusted Tier 3 start | `$52,815` |
| NIB premium row total per statement | `$2,302` |

These checks use draft taxable-income figures only. Final ATI/CCS and Division 293 calculations should wait for `TaxFY2425-c6j.8` and `TaxFY2425-c6j.9`.

## Lodgement Items

- Private health insurance: keep both NIB rows separate and preserve benefit codes `30` and `31`. Thomas's draft already matches the Thomas NIB statement; Isabelle's own return still needs confirmation.
- Medicare levy surcharge: H&R draft shows `365` days not liable, consistent with NIB full-year appropriate hospital cover.
- PHI rebate: Tier 3 gives `0.000%`, and NIB shows rebate received `$0`, so there is no rebate clawback visible from the NIB statement.
- Division 293: likely applies to Thomas, but the ATO assessment depends on final Division 293 income and fund-reported concessional contributions.
- Spouse details: Thomas's draft uses Isabelle taxable income `$110,118`; reconcile this against Isabelle's own return, especially the SCRATCH `Home Office` allowance.
- Dependants: household facts list Harlow and Oliver, while Thomas's draft income-test section shows dependent children `0`. Ask H&R Block whether that field should be `0` or `2`.
- Bank/account assumptions: Bank Australia joint interest split, VDHG ownership/share, and absence of other income-bearing accounts still need final confirmation.

## Post-NOA / Centrelink Items

CCS reconciliation happens through Services Australia after income is confirmed. If Thomas and Isabelle lodge tax returns, the ATO sends income details to Services Australia and CCS is balanced from there.

FTB, if received, is balanced separately from CCS after the financial year and last payment. No files were found under `4. Family`, so FTB status is a household question rather than a document-backed worksheet item right now.

## H&R Block Questions

1. Please provide or confirm Isabelle's own H&R Block draft return.
2. Should Thomas's draft field `Number of dependent children` be `0` or `2`, given Harlow and Oliver?
3. Are both taxpayers' NIB statement rows entered separately, with benefit codes `30` and `31`, rebate received `$0`, and `365` days cover?
4. Should Division 293 be estimated in the worksheet, or left for the ATO separate notice after super fund reporting?
5. Please confirm Bank Australia joint interest and VDHG ownership/share before final income calculations.

## Household Questions

1. Did the household receive Family Tax Benefit in FY2024-25?
2. Are there any CCS/FTB letters or balancing notices to keep for post-lodgement reconciliation?
3. Were there any BOQ, term deposit, crypto, foreign account, rental, or other income sources not already listed?
4. Are Harlow and Oliver both dependants for all relevant FY2024-25 family and Services Australia contexts?

## Blocked Inputs

- Isabelle's own H&R Block draft return.
- H&R Block confirmation of the dependent-children field.
- Household confirmation of FTB status and absence of other accounts/income sources.
- Final confirmed income/deduction figures from the bank cross-check and deterministic recalculation tasks.