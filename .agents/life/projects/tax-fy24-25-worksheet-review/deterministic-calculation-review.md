# Deterministic Calculation Review

Related issue: TaxFY2425-c6j.9  
Last updated: 2026-05-13

## Bottom line

Thomas's H&R Block draft rebuilds arithmetically against FY2024-25 resident tax rates, the 2% Medicare levy, and the draft credits. The recalculated payable is $24,851.53 before Division 293, compared with the H&R Block display of $24,851.50 DR, a 3 cent display/rounding difference.

Using only the Thomas draft fields, combined taxable income is $356,316: Thomas $246,198 plus Isabelle spouse taxable income $110,118. That is $11,247 under the current Services Australia higher-CCS cutoff of under $367,563.

This is not final, because Isabelle's own return is missing and the historical RSU CGT figure is still unresolved. In the closest stress test, adding the historical RSU CGT $7,974.12, removing the $12 SEEK salary-sacrifice D9 claim, and using Isabelle's SCRATCH gross plus Home Office allowance before deductions gives combined income of $366,853.81. That is only $709.19 under the higher-CCS cutoff.

## Source basis

The source register now includes `income-tax-medicare-ccs-calculation`, covering:

- ATO FY2024-25 Australian resident tax rates.
- ATO Medicare levy reduction thresholds, supporting use of the full 2% levy in the reviewed scenarios.
- Services Australia standard CCS income thresholds.
- Services Australia higher-CCS cutoff: family combined income must be under $367,563.
- Services Australia adjusted taxable income components for family assistance.

Division 293 is still treated as a separate ATO assessment. Using PAYG employer-super liabilities as a proxy, the baseline Division 293 estimate is $2,541.73. If the historical RSU CGT $7,974.12 is added, the estimate rises to $3,112.03.

## Scenario results

| Scenario | Thomas taxable | Isabelle/proxy | Combined | Higher-CCS margin |
|---|---:|---:|---:|---:|
| H&R draft as entered | $246,198.00 | $110,118.00 | $356,316.00 | $11,247.00 under |
| Remove SEEK salary-sacrifice D9 $12 | $246,210.00 | $110,118.00 | $356,328.00 | $11,235.00 under |
| Add historical RSU CGT $7,974.12 | $254,172.12 | $110,118.00 | $364,290.12 | $3,272.88 under |
| Add RSU CGT and remove SEEK D9 | $254,184.12 | $110,118.00 | $364,302.12 | $3,260.88 under |
| Isabelle gross plus allowance proxy | $246,198.00 | $112,669.69 | $358,867.69 | $8,695.31 under |
| Isabelle gross plus allowance, add RSU CGT, remove SEEK D9 | $254,184.12 | $112,669.69 | $366,853.81 | $709.19 under |
| Isabelle CSV candidate proxy, add RSU CGT, remove SEEK D9 | $254,184.12 | $112,303.46 | $366,487.58 | $1,075.42 under |

The Tizzi $4,025 deferred non-commercial loss was tested only as a diagnostic. It should not reduce Thomas's FY2024-25 taxable income while the draft defers it.

## Existing script status

`verify_calculations.py` should not be used for final figures without refactoring. It currently produces a combined taxable estimate of $346,362.01 and a CCS margin of $21,200.99, but it relies on stale or rejected assumptions: the old ESS value, broad deduction inputs, a separate internet amount while using fixed-rate WFH, and simplified super for Division 293.

## H&R Block questions

- Confirm whether the historical RSU CGT figure $7,974.12 must be added to Thomas's return.
- Remove or explain the $12 SEEK D9 salary-sacrifice/workplace-giving claim.
- Provide Isabelle's own H&R Block draft return, including the $1,199.64 SCRATCH Home Office allowance, deductions, HELP status and spouse fields.
- Confirm final combined ATI for CCS after both returns are complete; the close stress test is only $709.19 under the higher-CCS cutoff.
- Confirm Division 293 is expected to be separately assessed and whether H&R Block wants only a worksheet warning estimate.
- Confirm the Tizzi $4,025 loss remains deferred and does not reduce Thomas's FY2024-25 taxable income.