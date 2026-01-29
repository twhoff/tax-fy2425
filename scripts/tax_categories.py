"""
ATO Tax-Relevant Transaction Categories for FY24-25
Based on ATO guidelines and copilot-instructions.md
"""

# Transaction categories with keywords for matching
TAX_CATEGORIES = {
    # ============================================
    # DEDUCTIBLE EXPENSES
    # ============================================
    
    "software_subscriptions": {
        "description": "Work-related software and cloud services",
        "keywords": [
            "replit", "1password", "github", "copilot", "chatgpt", "openai",
            "warp", "medium", "adobe", "figma", "slack",
            "notion", "dropbox", "google workspace", "microsoft 365",
            "aws", "azure", "heroku", "vercel", "netlify", "digitalocean",
            "microsoft*store", "msbill", "beforesunset", "openart"
        ],
        "default_owner": "Thomas",
        "work_use_percent": 100,
        "notes": "Most are Tizzi ABN business expenses"
    },
    
    "linkedin_premium": {
        "description": "LinkedIn Premium subscription",
        "keywords": ["linkedin"],
        "default_owner": "Thomas",
        "work_use_percent": 50,
        "notes": "50% Tizzi marketing - job searching portion not deductible"
    },
    
    "streaming_creative": {
        "description": "Streaming services for creative research (Isabelle)",
        "keywords": [
            "paramount+", "hayu", "audible", "youtube premium", "netflix.com",
            "stan.com", "disney plus", "apple tv+", "prime video",
            "spotify", "hubbl", "binge", "ad free for primevideo"
        ],
        "default_owner": "Isabelle",
        "work_use_percent": 30,
        "notes": "Creative Director research - 30% work use justified. Spotify for leadership/creativity podcasts."
    },
    
    "home_office_equipment": {
        "description": "Home office equipment and furniture",
        "keywords": [
            "officeworks", "jb hi-fi", "harvey norman",
            "dell", "logitech", "microsoft surface", "samsung monitor"
        ],
        "default_owner": "Thomas",
        "work_use_percent": 100,
        "notes": "Verify item is work-related before claiming"
    },
    
    "amazon_documented_equipment": {
        "description": "Amazon purchases with documented work-use receipts",
        "keywords": [],  # Empty - must be matched by amount/date to receipt
        "default_owner": "Thomas",
        "work_use_percent": 100,
        "notes": "Only claim if receipt in 2. Deductions/ folder confirms work equipment"
    },
    
    "office_supplies": {
        "description": "Stationery and office consumables",
        "keywords": [
            "staples australia", "paper depot"
        ],
        "default_owner": "shared",
        "work_use_percent": 100,
        "notes": "Split 50/50 if shared"
    },
    
    "internet_phone": {
        "description": "Internet and mobile phone expenses",
        "keywords": [
            "optus", "telstra", "vodafone", "tpg", "aussie broadband",
            "iinet", "belong", "felix", "boost", "aldi mobile", "nbn"
        ],
        "default_owner": "shared",
        "work_use_percent": 65,
        "notes": "Using fixed-rate method - only claim separately if actual cost method"
    },
    
    "donations": {
        "description": "Tax-deductible donations to DGR organisations",
        "keywords": [
            "bravehearts", "unicef", "cancer council", "red cross",
            "salvation army", "smith family", "world vision", "oxfam",
            "médecins sans frontières", "msf", "doctors without borders",
            "wwf", "rspca", "lifeline", "beyond blue", "headspace"
        ],
        "default_owner": "check_card",  # Determine by which card used
        "work_use_percent": 100,
        "notes": "Verify DGR status at ABN Look-up"
    },
    
    "professional_development": {
        "description": "Courses, books, and professional materials",
        "keywords": [
            "udemy", "coursera", "pluralsight", "linkedin learning",
            "o'reilly", "safari books", "amazon books", "book depository",
            "dymocks", "booktopia", "conference", "seminar", "workshop"
        ],
        "default_owner": "Thomas",
        "work_use_percent": 100,
        "notes": "Must relate to current employment"
    },
    
    "professional_reading": {
        "description": "News and professional reading subscriptions",
        "keywords": [
            "newyorker", "condenast", "new yorker", "economist", "afr",
            "financial review", "wsj", "wall street journal", "nytimes"
        ],
        "default_owner": "Thomas",
        "work_use_percent": 50,
        "notes": "50% work use for industry awareness and professional reading"
    },
    
    "productivity_tools": {
        "description": "ADHD and productivity tools",
        "keywords": [
            "thecenteredlife", "centered life", "focusmate", "brain.fm",
            "todoist", "asana", "monday.com"
        ],
        "default_owner": "Thomas",
        "work_use_percent": 100,
        "notes": "ADHD productivity tools for work effectiveness"
    },
    
    "conferences_events": {
        "description": "Work conferences and industry events",
        "keywords": [
            "victorian arts centre", "theartcentre", "princess theatre",
            "convention centre", "melbourne convention", "exhibition"
        ],
        "default_owner": "Isabelle",
        "work_use_percent": 100,
        "notes": "Creative industry conferences and events"
    },
    
    "tax_affairs": {
        "description": "Cost of managing tax affairs",
        "keywords": [
            "h&r block", "tax agent", "accountant", "ato", "tax return",
            "etax", "mytax"
        ],
        "default_owner": "shared",
        "work_use_percent": 100,
        "notes": "Prior year tax agent fees deductible this year"
    },
    
    "professional_memberships": {
        "description": "Professional associations and memberships",
        "keywords": [
            "acs", "engineers australia", "ieee", "acm", "aiga",
            "association"
        ],
        "default_owner": "check_description",
        "work_use_percent": 100,
        "notes": "Must relate to employment"
    },
    
    # ============================================
    # INCOME ITEMS (for cross-reference)
    # ============================================
    
    "interest_income": {
        "description": "Bank interest received",
        "keywords": [
            "interest", "bonus saver", "savings interest"
        ],
        "default_owner": "shared",
        "is_income": True,
        "notes": "Bank Australia interest already documented"
    },
    
    "dividends": {
        "description": "Dividend payments",
        "keywords": [
            "dividend", "selfwealth", "commsec", "stake", "chess"
        ],
        "default_owner": "Thomas",
        "is_income": True,
        "notes": "SelfWealth dividends already documented"
    },
    
    "government_payments": {
        "description": "Centrelink and government payments",
        "keywords": [
            "centrelink", "services australia", "family tax benefit",
            "ftb", "ccs", "child care subsidy", "parenting payment"
        ],
        "default_owner": "shared",
        "is_income": True,
        "notes": "No Centrelink payments during gap period"
    },
    
    # ============================================
    # EXCLUDE FROM DEDUCTIONS
    # ============================================
    
    "personal_not_deductible": {
        "description": "Personal expenses - NOT deductible",
        "keywords": [
            "woolworths", "coles", "aldi", "costco", "uber eats",
            "deliveroo", "menulog", "doordash", "cafe", "restaurant",
            "mcdonald", "kfc", "hungry jack", "subway", "gym",
            "fitness", "cinema", "movie", "ticketek", "ticketmaster",
            "hotel", "airbnb", "qantas", "virgin", "jetstar", "uber",
            "ola", "didi", "parking", "petrol", "fuel", "7-eleven",
            "amazon", "ikea", "kmart", "big w", "target",
            "amznprimeau membership", "onepass"
        ],
        "exclude": True,
        "notes": "Clearly personal - skip these"
    },
    
    "childcare_family": {
        "description": "Childcare and family expenses",
        "keywords": [
            "childcare", "daycare", "kindy", "kindergarten", "nido",
            "goodstart", "guardian", "only about children"
        ],
        "default_owner": "shared",
        "exclude": True,
        "notes": "Not directly deductible - affects CCS calculations"
    },
    
    "health_insurance": {
        "description": "Private health insurance",
        "keywords": [
            "nib", "bupa", "medibank", "hcf", "ahm"
        ],
        "default_owner": "shared",
        "exclude": True,
        "notes": "Not deductible but affects MLS - already documented"
    }
}

# Keywords to identify card ownership
CARD_OWNER_HINTS = {
    "Thomas": [
        "atlassian", "seek", "tizzi", "github", "replit",
        "engineering", "software", "developer"
    ],
    "Isabelle": [
        "scratch", "creative", "design", "advertising",
        "paramount", "hayu", "audible"
    ]
}

# High-value threshold (flag for review)
HIGH_VALUE_THRESHOLD = 300

# Foreign currency identifiers
FOREIGN_CURRENCY_KEYWORDS = [
    "usd", "eur", "gbp", "nzd", "foreign", "international",
    "apple.com/bill", "google.com", "microsoft.com"
]

def categorise_transaction(description: str, amount: float) -> dict:
    """
    Categorise a transaction based on its description.
    
    Returns:
        dict with category, owner, work_use_percent, is_deductible, notes
    """
    desc_lower = description.lower()
    
    for category, config in TAX_CATEGORIES.items():
        for keyword in config["keywords"]:
            if keyword.lower() in desc_lower:
                return {
                    "category": category,
                    "description": config["description"],
                    "default_owner": config.get("default_owner", "unknown"),
                    "work_use_percent": config.get("work_use_percent", 0),
                    "is_income": config.get("is_income", False),
                    "is_deductible": not config.get("exclude", False) and not config.get("is_income", False),
                    "notes": config.get("notes", ""),
                    "matched_keyword": keyword
                }
    
    # No match found
    return {
        "category": "unclassified",
        "description": "Requires manual review",
        "default_owner": "unknown",
        "work_use_percent": 0,
        "is_income": False,
        "is_deductible": False,
        "notes": "Could not auto-classify",
        "matched_keyword": None
    }

def is_foreign_currency(description: str) -> bool:
    """Check if transaction appears to be foreign currency."""
    desc_lower = description.lower()
    return any(kw in desc_lower for kw in FOREIGN_CURRENCY_KEYWORDS)

def is_high_value(amount: float) -> bool:
    """Check if transaction exceeds high-value threshold."""
    return abs(amount) >= HIGH_VALUE_THRESHOLD


if __name__ == "__main__":
    # Test the categoriser
    test_transactions = [
        ("GITHUB.COM/COPILOT", 21.00),
        ("OFFICEWORKS RICHMOND", 89.50),
        ("WOOLWORTHS HAWTHORN", 156.32),
        ("UNICEF AUSTRALIA", 50.00),
        ("PARAMOUNT+ SUBSCRIPTION", 11.99),
        ("APPLE.COM/BILL USD 9.99", 15.23),
    ]
    
    print("Transaction Categorisation Test")
    print("=" * 60)
    for desc, amount in test_transactions:
        result = categorise_transaction(desc, amount)
        print(f"\n{desc} (${amount:.2f})")
        print(f"  Category: {result['category']}")
        print(f"  Deductible: {result['is_deductible']}")
        print(f"  Owner: {result['default_owner']}")
        print(f"  Work %: {result['work_use_percent']}")
