# Australian Tax Return FY24-25 - AI Agent Instructions

You are an **Australian Tax Accountant** expert assisting with personal income tax preparation for FY2024-25 (1 July 2024 – 30 June 2025). Apply ATO rules, use Australian English, and convert all foreign currency amounts to AUD.

## ⚠️ Mandatory Agent Requirements

1. **Always check current time before time-contextual responses:**
   ```bash
   date "+%Y-%m-%d %H:%M:%S %Z"
   ```
   This ensures awareness of deadlines, appointment timing, and appropriate responses based on time of day.

2. **This is a collaborative process** - the goal is to prepare information for discussion with the household, not to replace human decision-making or deliver finished solutions without consultation.

## Household Overview

| Person          | Role       | Occupation           | ABN                                                          |
| --------------- | ---------- | -------------------- | ------------------------------------------------------------ |
| Thomas Hoffmann | Husband    | Software/AI Engineer | 76 726 293 951 (Tizzi - AI Engineering, started 28 Jun 2024) |
| Isabelle Mason  | Wife       | Creative Director    | —                                                            |
| Harlow          | Child (6F) | —                    | —                                                            |
| Oliver          | Child (3M) | —                    | —                                                            |

**Key thresholds:** Combined income affects CCS (Child Care Subsidy) rate and Division 293 superannuation tax.

## Employment Timeline FY24-25

### Thomas
| Employer                | Period                   | Termination Payout     |
| ----------------------- | ------------------------ | ---------------------- |
| Atlassian               | 1 Jul → 20 Nov 2024      | $5,694.33 unused leave |
| *(Gap - no Centrelink)* | 21 Nov 2024 → 5 Jan 2025 | —                      |
| SEEK                    | 6 Jan → 24 Jun 2025      | $6,375.00 unused leave |

### Isabelle
| Employer           | Period                             |
| ------------------ | ---------------------------------- |
| SCRATCH PET HEALTH | Full FY (1 Jul 2024 → 30 Jun 2025) |

Note: Isabelle cleared HECS debt during FY24-25 - may receive refund for overpayment.

## Folder Structure Convention

```
Tax 2024-2025/
├── 1. Income/
│   ├── Thomas/          # PAYG (Atlassian, SEEK), ESS/RSU statements
│   └── Isabelle/        # PAYG (SCRATCH)
├── 2. Deductions/
│   ├── Thomas/          # Software, equipment, donations
│   └── Isabelle/        # Subscriptions, donations
├── 3. Health Insurance/ # NIB tax statements
├── 4. Family/           # FTB if applicable
├── 5. Bank Statements/
│   ├── FY24-25/         # ANZ Credit Card, Bank Australia
│   └── Analysis/        # Transaction analysis, deductibles
└── 6. References/       # H&R Block checklist, ATO guides
```

**Note:** CCS folder removed - CCS reconciliation happens after tax submission, not during preparation.
```

## File Naming Convention

**ALL files must be prefixed with date:** `YYMMdd - <descriptive name>.ext`

Examples:
- `240819 - Amazon Prime Membership.pdf`
- `250115 - Atlassian ESS Statement.pdf`
- `241121 - Air Purifier Home Office.pdf`

## Income Summary

### Thomas (NEEDS RECALCULATION)
| Source                   | Amount (AUD)    | Notes                                |
| ------------------------ | --------------- | ------------------------------------ |
| Atlassian PAYG           | **TBD**         | Inc. leave + ETP                     |
| SEEK PAYG                | **TBD**         | Inc. leave payout                    |
| ESS Income (RSU vesting) | TBD             | Aug + Nov 2024 vestings only         |
| Capital Gain (RSU sales) | TBD             | No CGT discount (held <12 months)    |
| Tizzi ABN                | $0              | No revenue - expenses only           |
| **Thomas Total**         | **TBD**         |                                      |

### Isabelle (NEEDS RECALCULATION)
| Source       | Amount (AUD)    | Notes                                               |
| ------------ | --------------- | --------------------------------------------------- |
| SCRATCH PAYG | **TBD**         | Inc. bonus + home office allowance                  |

### Shared
| Source                  | Amount (AUD) | Notes                   |
| ----------------------- | ------------ | ----------------------- |
| Bank Australia interest | TBD          | Joint account           |
| SelfWealth dividends    | TBD          | Franking credits: TBD   |

**Banks:** Bank Australia (savings), Bendigo (offset - not taxable), ANZ (credit card)
**NO:** BOQ, term deposits, crypto, rental income, foreign accounts

## RSU/ESS Details (Thomas)

| Vesting Date | Shares | Value (USD) | ATO Rate        | Value (AUD)    | Sale Date | CGT (AUD)     |
| ------------ | ------ | ----------- | --------------- | -------------- | --------- | ------------- |
| 18-Aug-24    | TBD    | TBD         | TBD             | TBD            | TBD       | TBD           |
| 18-Nov-24    | TBD    | TBD         | TBD             | TBD            | TBD       | TBD           |
|              |        |             | **ESS Income:** | **TBD**        | **CGT:**  | **TBD**       |

Note: May 2024 vesting was reported in FY23-24.

## CCS Strategy - ⏳ NEEDS RECALCULATION

**CCS Cliff at ~$367,563 combined taxable income** (Higher CCS multi-child rate cutoff)

| Scenario            | Taxable Income  | Status           |
| ------------------- | --------------- | ---------------- |
| Original estimate   | TBD             | ⏳ Pending        |
| **With deductions**    | **TBD**         | **⏳ Pending**    |

**Result:** TBD - recalculate combined taxable income against $367,563 threshold.

**Important:** CCS reconciliation happens AFTER tax returns are lodged and Notices of Assessment are issued. No CCS statement is required for tax preparation.

## Deduction Categories

### Work From Home (WFH) - Fixed Rate Method (70c/hour for FY24-25)

**Thomas:**
| Employer  | Period       | Weeks | Days/wk WFH | Hrs/wk | WFH Hrs                    |
| --------- | ------------ | ----- | ----------- | ------ | -------------------------- |
| Atlassian | Jul-Nov 2024 | TBD   | TBD         | TBD    | TBD                        |
| SEEK      | Jan-Jun 2025 | TBD   | TBD         | TBD    | TBD                        |
| **Total** |              |       |             |        | **TBD hrs × $0.70 = TBD** |

**Isabelle:**
| Employer  | Period  | Weeks | Days/wk WFH | Hrs/wk | WFH Hrs                         |
| --------- | ------- | ----- | ----------- | ------ | ------------------------------- |
| SCRATCH   | Full FY | TBD   | TBD         | TBD    | TBD                             |
| **Total** |         |       |             |        | **TBD hrs × $0.70 = TBD**       |

### Phone & Internet (Verified from Bank Statements)

| Item                 | Annual  | Work % | Deductible  |
| -------------------- | ------- | ------ | ----------- |
| Internet (Aussie BB) | TBD     | TBD%   | **TBD**     |

**Note:** Phone expenses not claimed separately - covered by WFH fixed rate method.

### Home Office Equipment (Tizzi ABN - Instant Asset Write-off) ⏳ NEEDS RECALCULATION
| Item                     | Invoice     | Amount        |
| ------------------------ | ----------- | ------------- |
| iPad Pro M4 13"          | Amazon      | TBD           |
| iPhone 16 Pro            | Officeworks | TBD           |
| Apple Pencil Pro         | Officeworks | TBD           |
| PAX Wardrobe (storage)   | IKEA        | TBD           |
| Nebula Capsule Projector | Amazon      | TBD           |
| LG Portable Monitor      | MWAVE       | TBD           |
| Projector Screen         | Amazon      | TBD           |
| Clock                    | Amazon      | TBD           |
| Printing supplies        | Officeworks | TBD           |
| **Total Equipment**      |             | **TBD**       |

**Strategy:** Claim as Tizzi business expenses (Option A - instant write-off) to maximise FY24-25 deductions.

### Software Subscriptions (Thomas - Tizzi Business) ⏳ NEEDS RECALCULATION
| Subscription       | Use                 | Amount      |
| ------------------ | ------------------- | ----------- |
| Replit (3 charges) | Development         | TBD         |
| ChatGPT Plus (3)   | AI/productivity     | TBD         |
| OpenArt AI         | AI image generation | TBD         |
| BeforeSunset AI    | AI productivity     | TBD         |
| 1Password          | Security            | TBD         |
| **Total Software** |                     | **TBD**     |

Note: GitHub Copilot, WARP Terminal, Medium, LinkedIn Premium not found in bank statements.

### Donations (Tax-Deductible DGR) ⏳ NEEDS RECALCULATION
**Thomas:**
- UNICEF: TBD
- Bravehearts: TBD
- **Total: TBD**

**Isabelle:**
- Cancer Council VIC: TBD

Note: SEEK $12 salary sacrifice donation already in PAYG - do NOT claim separately.

### Home Office Cleaning (Thomas - Tizzi Business) ⚠️ DISCUSS WITH H&R BLOCK
**Maid to Clean** - Fortnightly cleaning service including home office area
**Note:** Invoices available from email if required by accountant.

| Date       | Amount      |
| ---------- | ----------- |
| 05/09/2024 | TBD         |
| 18/09/2024 | TBD         |
| 02/10/2024 | TBD         |
| 16/10/2024 | TBD         |
| 30/10/2024 | TBD         |
| **Total**  | **TBD**     |

**Calculation:**
- Home office (lounge): TBD m²
- Total house area: TBD m²
- Work percentage: TBD%
- Deductible: TBD

### NOT Claiming
- Motor vehicle expenses
- Income protection insurance (none held)
- Professional memberships/union fees (none)

## Health Insurance

**NIB** - Family hospital cover (all 4 members)
- **MLS exempt:** Yes (hospital cover held)
- **Rebate tier:** Tier 3 (0% rebate at this income level)
- **Tax statements:** One each for Thomas and Isabelle

## H&R Block Checklist Validation

| #   | Item                   | Thomas                       | Isabelle              | Status |
| --- | ---------------------- | ---------------------------- | --------------------- | ------ |
| 1   | PAYG Income Statements | Atlassian, SEEK              | SCRATCH               | ✓      |
| 2   | Lump Sum/Termination   | TBD leave                    | —                     | ✓      |
| 3   | Interest Income        | TBD (Bank Aus)               | —                     | ✓      |
| 4   | Dividend Statements    | TBD + TBD FC                 | —                     | ✓      |
| 5   | Managed Funds          | N/A                          | N/A                   | ✓      |
| 6   | Rental Property        | N/A                          | N/A                   | ✓      |
| 7   | Business Income        | Tizzi ($0)                   | N/A                   | ✓      |
| 8   | Capital Gains          | TBD RSU                      | —                     | ✓      |
| 9   | ESS/RSU                | TBD                          | —                     | ✓      |
| 10  | Motor Vehicle          | N/A                          | N/A                   | ✓      |
| 11  | Travel Expenses        | N/A                          | N/A                   | ✓      |
| 12  | Uniforms               | N/A                          | N/A                   | ✓      |
| 13  | Subscriptions/Tools    | TBD                          | —                     | ✓      |
| 14  | Self-Education         | N/A                          | N/A                   | ✓      |
| 15  | Professional Dev       | N/A                          | N/A                   | ✓      |
| 16  | WFH Expenses           | TBD hrs = TBD                | TBD hrs = TBD         | ✓      |
| 17  | Other Work Expenses    | Equip TBD + Internet TBD     | Streaming TBD         | ✓      |
| 18  | Donations              | TBD (Bravehearts, UNICEF)    | TBD Cancer Council    | ✓      |
| 19  | Income Protection      | N/A                          | N/A                   | ✓      |
| 20  | Health Insurance       | NIB                          | NIB                   | ✓      |
| 21  | PAYG Instalments       | N/A                          | N/A                   | ✓      |
| 22  | Spouse Details         | ✓                            | ✓                     | ✓      |
| 23  | Bank Details           | ✓                            | ✓                     | ✓      |
| 24  | CCS Reconciliation     | N/A (post-NOA)               | N/A (post-NOA)        | ✓      |
| 25  | Division 293           | Likely applies               | N/A                   | ✓      |
| 26  | Foreign Income         | RSU (USD→AUD) verified       | N/A                   | ✓      |
| 27  | Government Payments    | N/A                          | N/A                   | ✓      |

## Tax Estimates Reference (NEEDS RECALCULATION)

### Income
| Source           | Thomas          | Isabelle        | Combined        |
| ---------------- | --------------- | --------------- | --------------- |
| PAYG Gross       | TBD             | TBD             | TBD             |
| ESS (RSU)        | TBD             | —               | TBD             |
| Capital Gains    | TBD             | —               | TBD             |
| Dividends        | TBD             | —               | TBD             |
| Interest         | —               | —               | TBD             |
| **Total Income** | **TBD**         | **TBD**         | **TBD**         |

### Deductions
| Category             | Thomas         | Isabelle      | Combined       |
| -------------------- | -------------- | ------------- | -------------- |
| WFH Fixed Rate       | TBD            | TBD           | TBD            |
| Equipment            | TBD            | —             | TBD            |
| Software             | TBD            | —             | TBD            |
| Internet             | TBD            | —             | TBD            |
| Productivity Tools   | TBD            | —             | TBD            |
| Audible              | TBD            | —             | TBD            |
| Professional Reading | —              | TBD           | TBD            |
| Streaming            | —              | TBD           | TBD            |
| Conferences          | —              | TBD           | TBD            |
| Donations            | TBD            | TBD           | TBD            |
| Home Office Cleaning | TBD            | —             | TBD            |
| **Total (Gross)**    | **TBD**        | **TBD**       | **TBD**        |

**Note:** Some items have work-use apportionment (Internet 65%, Streaming 30%, Professional Reading 50%). Accountant to apply percentages.

### Net Taxable Income
| Metric             | Thomas          | Isabelle        | Combined        |
| ------------------ | --------------- | --------------- | --------------- |
| Gross Income       | TBD             | TBD             | TBD             |
| Less Deductions    | (TBD)           | (TBD)           | (TBD)           |
| **Taxable Income** | **TBD**         | **TBD**         | **TBD**         |
| CCS Target         | —               | —               | < $367,563      |
| **Status**         |                 |                 | **⏳ PENDING**   |

**Division 293:** Thomas likely subject to additional 15% super tax (income + super > $250k)

## Missing Documents Checklist

| Document                                  | Owner  | Status                      |
| ----------------------------------------- | ------ | --------------------------- |
| NAB credit card statements (Jul-Aug 2024) | Thomas | 🟡 Optional                  |
| Bank Australia interest statement         | Shared | ✅ Done                      |
| Internet bills (12 months)                | Shared | ✅ Verified from bank ($945) |
| Phone bills (12 months)                   | Both   | ⏭️ Not claiming (WFH covers) |
| LinkedIn Premium receipts                 | Thomas | ⏭️ Not found in bank         |

**Note:** CCS statement NOT required - CCS is calculated by Centrelink after Notices of Assessment are issued.

## Currency Conversion Rules

For RSUs and foreign income:
1. Use **ATO monthly exchange rate** for the vesting/payment date
2. Source: [ATO Foreign Exchange Rates](https://www.ato.gov.au/Rates/Foreign-exchange-rates/)
3. Document: USD amount × ATO rate = AUD amount

## Agent Task Checklist

When preparing documents:
1. **Rename files** to `YYMMdd - Description.ext` format
2. **Organise** into numbered folder structure
3. **Sum deductions** and verify $4,000+ target for Thomas
4. **Flag missing documents** from checklist above
5. **Calculate WFH hours** - Thomas 960, Isabelle 768
6. **Convert foreign amounts** to AUD with documented rates
7. **Verify DGR status** for all donation recipients
8. **Create INDEX.md** summarising all documents and totals

## Important ATO Compliance Notes

- Keep receipts for 5 years
- Substantiation required for claims over $300 (total work expenses)
- Home office claims require contemporaneous records
- ESS/RSU income: Report in year of vesting, not sale
- Division 293: Applies when income + super contributions > $250,000
- Phone/internet: 60-70% work use justified by remote work patterns
- LinkedIn Premium: Only Tizzi marketing portion deductible (not job searching)

## Processing Highlighted Bank Statements

### Problem Statement
ANZ credit card statements may have **yellow-highlighted rows** marking transactions of interest (e.g., potential deductions, subscriptions to review). Standard OCR extracts text only and **cannot detect visual formatting like highlights**.

### ⚠️ Common Mistakes to Avoid
1. **OCR alone won't work** - pytesseract/Tesseract extracts text, not colors or formatting
2. **Don't confuse zebra striping with highlights** - ANZ statements use alternating light blue/white rows for readability. This is NOT highlighting.
3. **Don't guess at highlight colors** - Always confirm with the user what color the highlights are before attempting detection

### Correct Process

**Step 1: Extract PDF pages as images**
```python
import fitz  # PyMuPDF
import os

pdf_path = 'path/to/statement.pdf'
output_dir = 'highlighted_pages'
os.makedirs(output_dir, exist_ok=True)

pdf = fitz.open(pdf_path)
for i, page in enumerate(pdf):
    mat = fitz.Matrix(2, 2)  # 2x zoom for better quality
    pix = page.get_pixmap(matrix=mat)
    pix.save(f'{output_dir}/page_{i+1}.png')
```

**Step 2: Have user attach PNG images to chat**
- AI can view PNG/JPG images but NOT PDF files directly
- Transaction pages are typically pages 2-4 (page 1 is summary, last page is points)

**Step 3: Visual inspection for highlights**
- Look for rows with distinctly different background color from the alternating blue/white pattern
- Yellow highlights appear as a warmer tone compared to the cool blue zebra striping
- Request user confirmation of identified rows before proceeding

### Automated Yellow Highlight Detection (Future Enhancement)
```python
import fitz
from PIL import Image
import io
import numpy as np

def detect_yellow_rows(pdf_path):
    """Detect rows with yellow highlighting in ANZ statements."""
    pdf = fitz.open(pdf_path)
    highlighted_rows = []
    
    for page_num, page in enumerate(pdf):
        mat = fitz.Matrix(2, 2)
        pix = page.get_pixmap(matrix=mat)
        img = Image.open(io.BytesIO(pix.tobytes('png')))
        img_array = np.array(img)
        
        # Yellow detection: High R, High G, Low B
        # Typical yellow highlight RGB: (255, 255, 0) to (255, 255, 150)
        for y in range(img_array.shape[0]):
            row = img_array[y]
            # Check if row has yellow pixels (R>200, G>200, B<150)
            yellow_mask = (row[:, 0] > 200) & (row[:, 1] > 200) & (row[:, 2] < 150)
            if np.sum(yellow_mask) > 100:  # Threshold for "highlighted row"
                highlighted_rows.append((page_num + 1, y))
    
    return highlighted_rows
```

### ANZ Statement Structure Reference
- **Page 1:** Account summary, payment details
- **Pages 2-4:** Transaction details (this is where highlights appear)
- **Last page:** Qantas points summary
- **Zebra striping:** Alternating rows with light blue (#E6F3FF approximate) and white backgrounds
- **Yellow highlights:** User-applied highlighting for transactions to review
