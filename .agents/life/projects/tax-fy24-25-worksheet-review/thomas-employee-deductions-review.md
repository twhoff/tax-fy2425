# Thomas Employee Deductions Review

Related issue: `TaxFY2425-c6j.4`
Status: ready for H&R Block questions

## Bottom Line

H&R Block's Thomas D4, D5, D9 and D10 totals tie arithmetically to the draft total deductions of `$3,076`, but several inputs need amendment or confirmation before the claims are comfortable.

The biggest issue is method consistency: the WFH fixed-rate claim is `808 hours x $0.70 = $565.60`, rounded by H&R Block to `$566`. Under the fetched ATO fixed-rate source, internet and phone are already included in that rate, so the bank-analysis internet figure of `$945` gross / `$614.25` at 65% should not be added separately while fixed rate is used.

## Items Checked

- D4 self-education: H&R Block `$147` matches TheCenteredLife `$48.43` plus six Audible charges at `$16.45` each, rounded. This still needs a current-employment connection and Audible title list. TheCenteredLife also needs receipt evidence.
- D5 WFH: H&R Block `$566` matches 808 hours at 70c, subject to actual-hour records.
- D5 subscriptions: H&R Block `$616` does not cleanly reconcile to bank evidence. Replit, ChatGPT, Password Security, Audible/Adobe and BeforeSunset need H&R Block review, and the employee D5 versus Tizzi P8 split must be confirmed.
- D5 assets/depreciation: the H&R Block WRE depreciation schedule is internally consistent with the worksheet notes, but ongoing work use and iPhone replacement/disposal treatment need confirmation.
- D5 cleaning and office items: cleaning ties to four `$132.13` cleans at 25%, while the bank cross-check summary says five cleans. The `$425` office item is not reconciled to the visible bank-analysis office-supplies total.
- D9 donations: UNICEF `$250` and Bravehearts `$250` have receipt evidence and ABR DGR-list matches. The `$12` SEEK workplace-giving/salary-sacrifice entry should not be separately claimed if it was salary sacrifice or already processed through payroll.
- D10 tax agent fees: ATO guidance supports cost-of-managing-tax-affairs claims. A `$428` H&R Block receipt exists, paid on 21 Jan 2025 and addressed to Isabelle, but Thomas's `$204` claim does not equal a simple half share, so H&R Block should confirm the allocation.

## H&R Block Questions

1. Please confirm D4 TheCenteredLife and Audible: what current-employment skills/duties do they maintain or improve, and what Audible titles were included?
2. Please confirm whether the `$16.45 x 6` D5 subscription detail shown as `Adobe` is actually the same Audible amount already claimed at D4. If yes, remove the duplicate.
3. Please confirm there is no separate internet claim in D5 while using the WFH fixed-rate method.
4. Please reconcile D5 subscriptions: Replit `$80.08` vs bank/receipt `$80.02`, ChatGPT `$75.54` vs bank `$35.54`, Password Security `$68.84` vs available `$49.95`, and BeforeSunset `$131.08` excluded from the H&R detail.
5. Please confirm which software belongs to employee D5 versus the Tizzi P8 business schedule, and ensure no subscription is claimed in both places.
6. Please confirm ongoing work use and disposal/replacement treatment for the old iPhone 12 now that iPhone 16 Pro appears on the Tizzi schedule.
7. Please explain the D5 `$425` office item and provide the matching receipt or depreciation/work-use treatment.
8. Please confirm cleaning uses four or five Maid to Clean invoices, confirm the `25m2/100m2` floor-area basis, and whether H&R Block is comfortable with the dedicated-home-office cleaning claim.
9. Please remove or explain the `$12` SEEK salary-sacrifice/workplace-giving amount in D9.
10. Please confirm the `$204` D10 tax-agent-fee allocation. The available H&R Block receipt is addressed to Isabelle and totals `$428` paid on 21 Jan 2025, so a simple 50/50 split would be `$214` rather than `$204`.

Structured details: `.agents/life/projects/tax-fy24-25-worksheet-review/thomas-employee-deductions-review.yaml`.
