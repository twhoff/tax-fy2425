# Thomas Income, ESS and CGT Reconciliation

Related issue: `TaxFY2425-c6j.3`
Last updated: 2026-05-13

Canonical structured file: `thomas-income-reconciliation.yaml`.

## Status

Ready for H&R Block questions. The PAYG and ESS figures are reconciled against source documents. Three items still need external evidence or accountant confirmation: RSU CGT, an extra small interest account, and the VDHG/AMMA managed-fund tax components.

## Reconciled Findings

- Atlassian PAYG source total is `$86,255.70`, with `$71,765.22` ordinary gross, `$8,796.15` other paid leave, `$5,694.33` unused leave on termination, `$250` allowance, and `$27,239` PAYG withholding. H&R Block shows `$86,255`, `$250`, and `$27,239`, which matches after whole-dollar display.
- SEEK PAYG source total is `$90,000.00`, with `$83,625.00` ordinary gross, `$6,375.00` other paid leave, `$26,688` PAYG withholding, and `$12` workplace giving. H&R Block matches salary/wage and withholding figures.
- Atlassian ETP source taxable component is `$9,595.77`, with `$3,071` withholding and source ETP type `O`. H&R Block shows `$9,595`, `$3,071`, and code `BT`; the amount reconciles, but the code/type needs accountant confirmation.
- Atlassian ESS statement reports Item `F` discount from deferral schemes of `$24,422` and `$38,721`, total `$63,143`. H&R Block matches `$63,143`. The older `$62,270.51` value in `verify_calculations.py` / README differs by `$872.49` and should be treated as stale unless H&R Block advises otherwise.
- Bank Australia interest statement supports `$34.96` total interest and Thomas's 50% share of `$17.48`. H&R Block also includes a second account amount of `$1.95` total / `$0.98` Thomas share that needs source evidence.
- SelfWealth is a joint account holding 12 VDHG units and shows estimated dividends/distributions of `$34.46` and estimated franking credits of `$2.81`. H&R Block has more granular VDHG components, including foreign income and CGT. Those look like AMMA/tax-statement figures, but the supporting AMMA statement is not in the current evidence set.

## H&R Block Questions

1. Please confirm the Atlassian ETP code: the PAYG source text shows ETP type `O`, while the H&R Block draft shows code `BT`. The taxable component and withholding reconcile, but the code/type display does not.
2. Please confirm the `$5,694.33` unused leave is not being treated as the ETP taxable component. The PAYG statement shows it inside salary/wages, separate from the `$9,595.77` ETP taxable component.
3. Please confirm Item 12 ESS should use the current Atlassian ESS statement total of `$63,143`, which matches H&R Block and differs from the older worksheet/script value by `$872.49`.
4. Please confirm whether any separate RSU capital gain must be reported. The current repository does not contain broker/sale evidence; the draft visibly shows only Vanguard/managed-fund CGT of `$11.02` total / `$5.51` Thomas share, while older repo notes mention `$7,974` RSU CGT.
5. Please identify the source for the extra interest account in the H&R Block draft: `$1.95` total / `$0.98` Thomas share.
6. Please confirm the source document for the Vanguard/VDHG managed fund components, ideally the AMMA/tax statement.

## Evidence Still Needed

- Separate RSU broker/sale or E*TRADE/Shareworks tax statement if the `$7,974` CGT figure is still intended.
- AMMA/Vanguard tax statement supporting the H&R Block managed-fund components.
- Evidence for the extra `$1.95` interest account shown in the H&R Block draft.