# Bank and Receipt Cross-Check Review

Related issue: `TaxFY2425-c6j.8`  
Date: 2026-05-13

## Bottom Line

The generated bank summaries are useful, but not safe to use mechanically. The receipt matcher has clear false positives, and the older prose cross-check is stale in a few places.

The biggest correction is that Bank Australia now has full-year coverage in the current CSV and includes the Cancer Council payment. The real coverage gap is ANZ credit-card transactions before 9 Sep 2024.

## Coverage

| Source | Current Finding | Status |
| --- | --- | --- |
| ANZ `all_transactions.csv` | `1,256` rows from `9 Sep 2024` to `30 Jun 2025` | Gap remains for `1 Jul-8 Sep 2024` |
| Bank Australia CSV | `452` rows from `1 Jul 2024` to `30 Jun 2025` | Resolved; older Jul-Sep note is stale |
| Highlighted transactions | `42` rows | Useful leads only |
| Receipt matcher | `49` generated matches | Not reliable without manual review |

## Candidate Totals

From `deductible_transactions_v2.csv`:

| Category | Count | Gross | Generated Deductible | Review Status |
| --- | ---: | ---: | ---: | --- |
| Donations | 3 | `$520.37` | `$520.37` | Confirmed, allocate owner correctly |
| Home office equipment | 4 | `$1,757.48` | `$1,757.48` | H&R / timing / owner questions |
| Software subscriptions | 9 | `$589.89` | `$589.89` | Mixed; prevent D5/P8 duplication |
| Internet | 9 | `$945.00` | `$614.25` | Reject if using WFH fixed rate |
| Streaming | 51 | `$950.78` | `$285.23` | H&R question; work-purpose needed |
| Events | 4 | `$81.00` | `$81.00` | H&R question; event purpose needed |
| Productivity | 1 | `$48.43` | `$48.43` | H&R question |
| Professional reading | 5 | `$55.61` | `$27.81` | Mixed; reject Sassafras false positive |

## Receipt Matcher Issues

Do not rely on `transaction_crossref.csv` or `transaction_receipt_crossref.md` without checking the actual receipt. Obvious false positives include:

- Aussie Broadband matched to Hayu, Ring, Cheek Media and Cleanup receipts.
- OpenAI matched to Spotify Audiobooks, projector screen and Replit receipts.
- Disney+ matched to a Cleanup receipt.
- UNICEF and Bravehearts matched to a Cleanup receipt.
- Officeworks 15 Dec rows linked to a Thomas receipt path that is not present; the visible receipt is under Isabelle deductions.

## Confirmed Or Mostly Confirmed

- Donations: UNICEF `$250`, Bravehearts `$250`, and Cancer Council Victoria `$20.37` have receipts/DGR support. Cancer Council is present in Bank Australia on `2025-05-22`, so the old “not found in bank statements” note is stale.
- Replit: direct Replit rows have matching receipts in Thomas deductions.
- Amazon receipt-backed items: Nebula Projector `$879.99`, Projector Screen `$37.99`, and the `30/06/2025` Amazon `$2,168.98` bank row matching iPad `$2,148.99` plus clock `$19.99` invoice text.
- Bank Australia: full FY coverage is present in the analysis CSV.

## Reject Or Exclude Unless Method Changes

- Internet/phone: generated internet claim should be excluded if the WFH fixed-rate method is used, because internet and phone are already included in the fixed rate.
- Amazon Prime and OnePass membership rows are shopping memberships, not professional memberships.
- Sassafras Sweet Co is a false positive for professional reading.
- No transaction matches were found for union fees, work clothing/laundry, phone providers, income-protection insurance, COVID tests, Adobe/Figma/Canva design tools, or genuine books/course platforms.

## Open Questions

- ANZ/NAB early-FY credit-card coverage: supply or confirm no statements are needed for `1 Jul-8 Sep 2024`.
- Apple: check purchase history for `14/02/2025 $15.00` and `23/06/2025 $63.98`.
- Software: decide whether OpenAI, BeforeSunset, OpenArt, Replit and 1Password belong in Tizzi P8 or employee D5, and prevent double counting.
- Microsoft*Store/MSBill `$49.95`: reconcile against the visible 1Password invoice of `$65.84`.
- IKEA: include only receipt-backed work storage/furniture at the correct business/work-use percentage; not all IKEA rows are deductible.
- Officeworks 15 Dec: confirm owner and work purpose because the receipt sits under Isabelle while generated analysis assigns the rows to Thomas.
- Cleaning: Maid To Clean bank rows exist, but invoices/floor-area evidence remain a H&R Block question.
- Work travel: MYKI, parking and Uber trip rows exist, but no work-meeting purpose is evidenced. Uber Eats/gift-card rows are personal false positives.
- Optometry: Bailey Nelson `$115` exists, but should be rejected unless H&R Block identifies a source-supported work-specific basis.

## H&R Block Questions

1. Should internet be excluded under the WFH fixed-rate method, or is any actual-cost treatment being used?
2. Should Thomas software rows be allocated to Tizzi P8 or employee D5, and how do we avoid duplicate Replit/ChatGPT claims?
3. How should Microsoft*Store/MSBill `$49.95` be treated given the visible 1Password invoice is `$65.84`?
4. Which Amazon/IKEA/Officeworks assets should be included, and at what business/work-use percentage?
5. Can bank statements substantiate Maid To Clean rows, or are invoices/floor-area records required?
6. Should any Isabelle streaming/event rows survive after work-purpose review?
7. Should Bailey Nelson optometry be rejected?

## Household Questions

1. Can you supply or confirm no early-FY ANZ/NAB credit-card statements are needed?
2. Can you check Apple purchase history for the two unknown Apple rows?
3. Were any MYKI, parking or Uber trip rows specifically for work meetings?
4. Do you have receipts for BeforeSunset AI, OpenArt AI, direct OpenAI/ChatGPT, Maid To Clean, or any missing Amazon/IKEA work items?
5. Are there any professional memberships, union fees, phone bills, income-protection premiums, optometry work requirements, COVID tests, or design-tool subscriptions outside the scanned accounts?