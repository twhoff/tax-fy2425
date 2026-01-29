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

### Thomas (VERIFIED ✅)
| Source                   | Amount (AUD)  | Notes                                    |
| ------------------------ | ------------- | ---------------------------------------- |
| Atlassian PAYG           | **$86,255.70**  | Inc. $5,694.33 leave + ETP $9,595.77   |
| SEEK PAYG                | **$90,000.00**  | Inc. $6,375.00 leave payout            |
| ESS Income (RSU vesting) | $62,270.51    | Aug + Nov 2024 vestings only             |
| Capital Gain (RSU sales) | $7,974.12     | No CGT discount (held <12 months)        |
| Tizzi ABN                | $0            | No revenue - expenses only               |
| **Thomas Total**         | **$246,534.79** |                                        |

### Isabelle (VERIFIED ✅)
| Source       | Amount (AUD)    | Notes                                      |
| ------------ | --------------- | ------------------------------------------ |
| SCRATCH PAYG | **$111,470.05** | Inc. $1,572 bonus + $1,199.64 home office allowance |

### Shared
| Source                  | Amount (AUD) | Notes                   |
| ----------------------- | ------------ | ----------------------- |
| Bank Australia interest | $34.96       | Joint account           |
| SelfWealth dividends    | $34.46       | Franking credits: $2.81 |

**Banks:** Bank Australia (savings), Bendigo (offset - not taxable), ANZ (credit card)
**NO:** BOQ, term deposits, crypto, rental income, foreign accounts

## RSU/ESS Details (Thomas)

| Vesting Date | Shares | Value (USD) | ATO Rate        | Value (AUD)    | Sale Date | CGT (AUD)     |
| ------------ | ------ | ----------- | --------------- | -------------- | --------- | ------------- |
| 18-Aug-24    | 105    | $16,192.05  | 1.501289        | $24,308.95     | 5-Nov-24  | $10,460.95    |
| 18-Nov-24    | 105    | $25,062.45  | 1.514679        | $37,961.57     | 20-Nov-24 | $211.73       |
|              |        |             | **ESS Income:** | **$62,270.51** | **CGT:**  | **$7,974.12** |

Note: May 2024 vesting was reported in FY23-24.

## CCS Strategy - ✅ TARGET ACHIEVED

**CCS Cliff at ~$367,563 combined taxable income** (Higher CCS multi-child rate cutoff)

| Scenario               | Taxable Income  | Status        |
| ---------------------- | --------------- | ------------- |
| Original estimate      | $369,003.91     | ❌ Over threshold |
| **With deductions**    | **$346,331.19** | **✅ Well under** |

**Result:** Combined taxable income $346,331 is $21,232 under the $367,563 threshold.

**Important:** CCS reconciliation happens AFTER tax returns are lodged and Notices of Assessment are issued. No CCS statement is required for tax preparation.

## Deduction Categories

### Work From Home (WFH) - Fixed Rate Method (70c/hour for FY24-25)

**Thomas:**
| Employer  | Period       | Weeks | Days/wk WFH | Hrs/wk | WFH Hrs                    |
| --------- | ------------ | ----- | ----------- | ------ | -------------------------- |
| Atlassian | Jul-Nov 2024 | 20    | 2           | 12     | 480                        |
| SEEK      | Jan-Jun 2025 | 24    | 2           | 10     | 480                        |
| **Total** |              |       |             |        | **960 hrs × $0.70 = $672** |

**Isabelle:**
| Employer  | Period  | Weeks | Days/wk WFH | Hrs/wk | WFH Hrs                         |
| --------- | ------- | ----- | ----------- | ------ | ------------------------------- |
| SCRATCH   | Full FY | 48    | 3           | 7.6    | 1,095                           |
| **Total** |         |       |             |        | **1,095 hrs × $0.70 = $766.50** |

### Phone & Internet (Verified from Bank Statements)

| Item           | Annual   | Work % | Deductible |
| -------------- | -------- | ------ | ---------- |
| Internet (Aussie BB) | $945.00  | 65%    | **$614.25** |

**Note:** Phone expenses not claimed separately - covered by WFH fixed rate method.

### Home Office Equipment (Tizzi ABN - Instant Asset Write-off) ✅ VERIFIED
| Item                    | Invoice      | Amount      |
| ----------------------- | ------------ | ----------- |
| iPad Pro M4 13"         | Amazon       | $2,148.99   |
| iPhone 16 Pro           | Officeworks  | $1,528.00   |
| Apple Pencil Pro        | Officeworks  | $177.00     |
| PAX Wardrobe (storage)  | IKEA         | $2,619.50   |
| Nebula Capsule Projector| Amazon       | $879.99     |
| LG Portable Monitor     | MWAVE        | $502.63     |
| Projector Screen        | Amazon       | $37.99      |
| Clock                   | Amazon       | $19.99      |
| Printing supplies       | Officeworks  | $52.48      |
| **Total Equipment**     |              | **$7,966.57** |

**Strategy:** Claim as Tizzi business expenses (Option A - instant write-off) to maximise FY24-25 deductions.

### Software Subscriptions (Thomas - Tizzi Business) ✅ VERIFIED
| Subscription      | Use                  | Amount    |
| ----------------- | -------------------- | --------- |
| Replit (3 charges)| Development          | $185.35   |
| ChatGPT Plus (3)  | AI/productivity      | $89.03    |
| OpenArt AI        | AI image generation  | $134.48   |
| BeforeSunset AI   | AI productivity      | $131.08   |
| 1Password         | Security             | $49.95    |
| **Total Software**|                      | **$589.89** |

Note: GitHub Copilot, WARP Terminal, Medium, LinkedIn Premium not found in bank statements.

### Donations (Tax-Deductible DGR) ✅ VERIFIED
**Thomas:**
- UNICEF: $250.00 (15/06/2025)
- Bravehearts: $250.00 (16/06/2025)
- **Total: $500.00**

**Isabelle:**
- Cancer Council VIC: $20.37 (22/05/2025)

Note: SEEK $12 salary sacrifice donation already in PAYG - do NOT claim separately.

### Home Office Cleaning (Thomas - Tizzi Business) ✅ VERIFIED
**Maid to Clean** - Fortnightly cleaning service including home office area

| Date | Amount |
| ------------ | -------- |
| 05/09/2024 | $132.13 |
| 18/09/2024 | $132.13 |
| 02/10/2024 | $132.13 |
| 16/10/2024 | $132.13 |
| 30/10/2024 | $132.13 |
| **Total** | **$660.65** |

**Calculation:**
- Home office (lounge): 4m × 5m = 20 m²
- Total house area: 130 m²
- Work percentage: 20 ÷ 130 = **15.38%**
- Deductible: $660.65 × 15.38% = **$101.61**

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

| #   | Item                   | Thomas                     | Isabelle        | Status |
| --- | ---------------------- | -------------------------- | --------------- | ------ |
| 1   | PAYG Income Statements | Atlassian, SEEK            | SCRATCH         | ✓      |
| 2   | Lump Sum/Termination   | $5,694 + $6,375 leave      | —               | ✓      |
| 3   | Interest Income        | $34.96 (Bank Aus)          | —               | ✓      |
| 4   | Dividend Statements    | $34.46 + $2.81 FC          | —               | ✓      |
| 5   | Managed Funds          | N/A                        | N/A             | ✓      |
| 6   | Rental Property        | N/A                        | N/A             | ✓      |
| 7   | Business Income        | Tizzi ($0)                 | N/A             | ✓      |
| 8   | Capital Gains          | $7,974.12 RSU              | —               | ✓      |
| 9   | ESS/RSU                | $62,270.51                 | —               | ✓      |
| 10  | Motor Vehicle          | N/A                        | N/A             | ✓      |
| 11  | Travel Expenses        | N/A                        | N/A             | ✓      |
| 12  | Uniforms               | N/A                        | N/A             | ✓      |
| 13  | Subscriptions/Tools    | $589.89 verified           | —               | ✓      |
| 14  | Self-Education         | N/A                        | N/A             | ✓      |
| 15  | Professional Dev       | N/A                        | N/A             | ✓      |
| 16  | WFH Expenses           | 960 hrs = $672             | 1,095 hrs = $766.50 | ✓      |
| 17  | Other Work Expenses    | Equip $7,967 + Internet $614 | Streaming $285 | ✓      |
| 18  | Donations              | $500 (Bravehearts, UNICEF) | $20.37 Cancer Council | ✓      |
| 19  | Income Protection      | N/A                        | N/A             | ✓      |
| 20  | Health Insurance       | NIB                        | NIB             | ✓      |
| 21  | PAYG Instalments       | N/A                        | N/A             | ✓      |
| 22  | Spouse Details         | ✓                          | ✓               | ✓      |
| 23  | Bank Details           | ✓                          | ✓               | ✓      |
| 24  | CCS Reconciliation     | N/A (post-NOA)             | N/A (post-NOA)  | ✓      |
| 25  | Division 293           | Likely applies             | N/A             | ✓      |
| 26  | Foreign Income         | RSU (USD→AUD) verified     | N/A             | ✓      |
| 27  | Government Payments    | N/A                        | N/A             | ✓      |

## Tax Estimates Reference (VERIFIED ✅)

### Income
| Source              | Thomas        | Isabelle      | Combined      |
| ------------------- | ------------- | ------------- | ------------- |
| PAYG Gross          | $176,255.70   | $111,470.05   | $287,725.75   |
| ESS (RSU)           | $62,270.51    | —             | $62,270.51    |
| Capital Gains       | $7,974.12     | —             | $7,974.12     |
| Dividends           | $34.46        | —             | $34.46        |
| Interest            | —             | —             | $34.96        |
| **Total Income**    | **$246,534.79** | **$111,470.05** | **$358,039.76** |

### Deductions
| Category            | Thomas        | Isabelle      | Combined      |
| ------------------- | ------------- | ------------- | ------------- |
| WFH Fixed Rate      | $672.00       | $766.50       | $1,438.50     |
| Equipment           | $7,966.57     | —             | $7,966.57     |
| Software            | $589.89       | —             | $589.89       |
| Internet (65%)      | $614.25       | —             | $614.25       |
| Productivity Tools  | $48.43        | —             | $48.43        |
| Professional Reading| $27.80        | —             | $27.80        |
| Streaming (30%)     | —             | $285.23       | $285.23       |
| Conferences         | —             | $81.00        | $81.00        |
| Donations           | $500.00       | $20.37        | $520.37       |
| Home Office Cleaning| $101.61       | —             | $101.61       |
| **Total Deductions**| **$10,520.55**| **$1,153.10** | **$11,673.65**|

### Net Taxable Income
| Metric              | Thomas        | Isabelle      | Combined      |
| ------------------- | ------------- | ------------- | ------------- |
| Gross Income        | $246,534.79   | $111,470.05   | $358,039.76   |
| Less Deductions     | ($10,520.55)  | ($1,153.10)   | ($11,673.65)  |
| **Taxable Income**  | **$236,014.24** | **$110,316.95** | **$346,331.19** |
| CCS Target          | —             | —             | < $367,563    |
| **Status**          |               |               | **✅ ACHIEVED** |

**Division 293:** Thomas likely subject to additional 15% super tax (income + super > $250k)

## Missing Documents Checklist

| Document                                  | Owner    | Status        |
| ----------------------------------------- | -------- | ------------- |
| NAB credit card statements (Jul-Aug 2024) | Thomas   | 🟡 Optional   |
| Bank Australia interest statement         | Shared   | ✅ Done       |
| Internet bills (12 months)                | Shared   | ✅ Verified from bank ($945) |
| Phone bills (12 months)                   | Both     | ⏭️ Not claiming (WFH covers) |
| LinkedIn Premium receipts                 | Thomas   | ⏭️ Not found in bank |

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
