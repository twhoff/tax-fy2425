#!/usr/bin/env python3
"""
Australian Tax Calculator CLI - FY2024-25

A command-line tool for calculating Australian income tax, Medicare levy,
Medicare levy surcharge, Division 293 super tax, HELP loan repayments,
and checking CCS (Child Care Subsidy) thresholds.

Usage:
    au_tax.py tax <income>              # Calculate income tax
    au_tax.py medicare <income>         # Calculate Medicare levy
    au_tax.py mls <income> [--family]   # Calculate Medicare levy surcharge
    au_tax.py div293 <income> <super>   # Check Division 293 applicability
    au_tax.py help-loan <income>        # Calculate HELP loan repayment
    au_tax.py ccs <combined_income>     # Check CCS threshold status
    au_tax.py summary <income> [options]# Full tax summary

All rates are for FY2024-25 (1 July 2024 - 30 June 2025).
Source: Australian Taxation Office (ATO)
"""

import argparse
import sys
from decimal import Decimal, ROUND_HALF_UP
from typing import NamedTuple, Optional


# =============================================================================
# FY2024-25 TAX BRACKETS
# Source: https://www.ato.gov.au/tax-rates-and-codes/tax-rates-australian-residents
# =============================================================================
TAX_BRACKETS_2024_25 = [
    # (threshold, base_tax, rate_per_dollar_over_threshold)
    (0, 0, 0.00),           # $0 - $18,200: Nil
    (18_200, 0, 0.16),      # $18,201 - $45,000: 16c per $1 over $18,200
    (45_000, 4_288, 0.30),  # $45,001 - $135,000: $4,288 + 30c per $1 over $45,000
    (135_000, 31_288, 0.37),# $135,001 - $190,000: $31,288 + 37c per $1 over $135,000
    (190_000, 51_638, 0.45),# $190,001+: $51,638 + 45c per $1 over $190,000
]

# =============================================================================
# MEDICARE LEVY - 2% (with low-income reduction thresholds)
# Source: https://www.ato.gov.au/individuals-and-families/medicare-and-private-health-insurance/medicare-levy
# =============================================================================
MEDICARE_LEVY_RATE = 0.02

# Medicare levy reduction thresholds FY2024-25
# Below lower threshold: no levy
# Between lower and upper: reduced levy (10% of excess over lower)
# Above upper threshold: full 2%
MEDICARE_REDUCTION_THRESHOLDS = {
    'standard': {'lower': 27_222, 'upper': 34_027},
    'sapto': {'lower': 43_020, 'upper': 53_775},  # Seniors and Pensioners Tax Offset
}

# =============================================================================
# MEDICARE LEVY SURCHARGE (MLS) - FY2024-25
# Source: https://www.ato.gov.au/individuals-and-families/medicare-and-private-health-insurance/medicare-levy-surcharge
# Applies if no private hospital cover
# =============================================================================
MLS_THRESHOLDS_SINGLE_2024_25 = [
    # (threshold, rate)
    (97_000, 0.00),     # Base tier: $97,000 or less - 0%
    (113_000, 0.01),    # Tier 1: $97,001 - $113,000 - 1%
    (151_000, 0.0125),  # Tier 2: $113,001 - $151,000 - 1.25%
    (float('inf'), 0.015),  # Tier 3: $151,001+ - 1.5%
]

MLS_THRESHOLDS_FAMILY_2024_25 = [
    # (threshold, rate)
    (194_000, 0.00),    # Base tier: $194,000 or less - 0%
    (226_000, 0.01),    # Tier 1: $194,001 - $226,000 - 1%
    (302_000, 0.0125),  # Tier 2: $226,001 - $302,000 - 1.25%
    (float('inf'), 0.015),  # Tier 3: $302,001+ - 1.5%
]

# Family threshold increases by $1,500 for each MLS dependent child after first
MLS_FAMILY_CHILD_INCREMENT = 1_500

# =============================================================================
# DIVISION 293 - Additional super tax for high income earners
# Source: https://www.ato.gov.au/individuals-and-families/super-for-individuals-and-families/super/growing-and-keeping-track-of-your-super/caps-limits-and-tax-on-super-contributions/division-293-tax-on-concessional-contributions
# =============================================================================
DIV293_THRESHOLD = 250_000  # Income + super contributions threshold
DIV293_RATE = 0.15  # Additional 15% tax on super contributions above threshold

# =============================================================================
# HELP/HECS LOAN REPAYMENT THRESHOLDS - FY2024-25
# Source: https://www.ato.gov.au/Rates/HELP,-TSL-and-SFSS-repayment-thresholds-and-rates/
# Note: FY2024-25 uses percentage of TOTAL repayment income (not marginal)
# =============================================================================
HELP_THRESHOLDS_2024_25 = [
    # (upper_threshold, rate_as_percentage_of_total_income)
    (54_435, 0.00),
    (62_850, 0.01),
    (66_620, 0.02),
    (70_618, 0.025),
    (74_855, 0.03),
    (79_346, 0.035),
    (84_107, 0.04),
    (89_154, 0.045),
    (94_503, 0.05),
    (100_174, 0.055),
    (106_185, 0.06),
    (112_556, 0.065),
    (119_309, 0.07),
    (126_467, 0.075),
    (134_056, 0.08),
    (142_100, 0.085),
    (150_626, 0.09),
    (159_663, 0.095),
    (float('inf'), 0.10),
]

# =============================================================================
# CCS (Child Care Subsidy) THRESHOLDS - FY2024-25
# Source: Services Australia
# =============================================================================
CCS_THRESHOLDS = {
    'standard_cutoff': 367_563,  # Above this, 0% CCS for families with 1 child <6
    'multi_child_cutoff': 367_563,  # Higher income cap for multiple children in care
    'max_subsidy_threshold': 80_000,  # Below this, maximum subsidy rate applies
}


# =============================================================================
# CALCULATION FUNCTIONS
# =============================================================================

class TaxResult(NamedTuple):
    """Result of income tax calculation."""
    taxable_income: float
    tax_payable: float
    marginal_rate: float
    effective_rate: float
    bracket_description: str


def calculate_income_tax(taxable_income: float) -> TaxResult:
    """
    Calculate income tax for FY2024-25.
    
    Args:
        taxable_income: Taxable income in AUD
        
    Returns:
        TaxResult with tax details
    """
    if taxable_income < 0:
        raise ValueError("Taxable income cannot be negative")
    
    if taxable_income <= 18_200:
        return TaxResult(
            taxable_income=taxable_income,
            tax_payable=0,
            marginal_rate=0,
            effective_rate=0,
            bracket_description="$0 - $18,200: Nil"
        )
    
    # Find applicable bracket
    brackets = TAX_BRACKETS_2024_25
    for i in range(len(brackets) - 1, -1, -1):
        threshold, base_tax, rate = brackets[i]
        if taxable_income > threshold:
            tax = base_tax + (taxable_income - threshold) * rate
            effective_rate = tax / taxable_income if taxable_income > 0 else 0
            
            # Determine bracket description
            if threshold == 18_200:
                desc = "$18,201 - $45,000: 16c per $1 over $18,200"
            elif threshold == 45_000:
                desc = "$45,001 - $135,000: $4,288 + 30c per $1 over $45,000"
            elif threshold == 135_000:
                desc = "$135,001 - $190,000: $31,288 + 37c per $1 over $135,000"
            else:
                desc = "$190,001+: $51,638 + 45c per $1 over $190,000"
            
            return TaxResult(
                taxable_income=taxable_income,
                tax_payable=round(tax, 2),
                marginal_rate=rate,
                effective_rate=round(effective_rate, 4),
                bracket_description=desc
            )
    
    return TaxResult(taxable_income, 0, 0, 0, "Unknown bracket")


class MedicareResult(NamedTuple):
    """Result of Medicare levy calculation."""
    taxable_income: float
    medicare_levy: float
    levy_rate: float
    reduction_applied: bool
    notes: str


def calculate_medicare_levy(
    taxable_income: float,
    sapto_eligible: bool = False
) -> MedicareResult:
    """
    Calculate Medicare levy for FY2024-25.
    
    Args:
        taxable_income: Taxable income in AUD
        sapto_eligible: True if eligible for Seniors and Pensioners Tax Offset
        
    Returns:
        MedicareResult with levy details
    """
    if taxable_income < 0:
        raise ValueError("Taxable income cannot be negative")
    
    thresholds = MEDICARE_REDUCTION_THRESHOLDS['sapto' if sapto_eligible else 'standard']
    lower = thresholds['lower']
    upper = thresholds['upper']
    
    if taxable_income <= lower:
        return MedicareResult(
            taxable_income=taxable_income,
            medicare_levy=0,
            levy_rate=0,
            reduction_applied=True,
            notes=f"Below Medicare levy threshold (${lower:,.0f})"
        )
    
    if taxable_income <= upper:
        # Reduced levy: 10% of excess over lower threshold
        levy = (taxable_income - lower) * 0.10
        effective_rate = levy / taxable_income if taxable_income > 0 else 0
        return MedicareResult(
            taxable_income=taxable_income,
            medicare_levy=round(levy, 2),
            levy_rate=round(effective_rate, 4),
            reduction_applied=True,
            notes=f"Reduced levy (income between ${lower:,.0f} and ${upper:,.0f})"
        )
    
    # Full 2% levy
    levy = taxable_income * MEDICARE_LEVY_RATE
    return MedicareResult(
        taxable_income=taxable_income,
        medicare_levy=round(levy, 2),
        levy_rate=MEDICARE_LEVY_RATE,
        reduction_applied=False,
        notes="Full Medicare levy (2%)"
    )


class MLSResult(NamedTuple):
    """Result of Medicare levy surcharge calculation."""
    income_for_mls: float
    mls_amount: float
    mls_rate: float
    tier: str
    has_hospital_cover: bool


def calculate_mls(
    income_for_mls: float,
    family: bool = False,
    dependent_children: int = 0,
    has_hospital_cover: bool = False
) -> MLSResult:
    """
    Calculate Medicare levy surcharge for FY2024-25.
    
    Args:
        income_for_mls: Income for MLS purposes (taxable income + fringe benefits + 
                        net investment loss + reportable super contributions)
        family: True if married/de facto
        dependent_children: Number of MLS dependent children (for threshold increase)
        has_hospital_cover: True if appropriate private hospital cover held
        
    Returns:
        MLSResult with surcharge details
    """
    if income_for_mls < 0:
        raise ValueError("Income cannot be negative")
    
    if has_hospital_cover:
        return MLSResult(
            income_for_mls=income_for_mls,
            mls_amount=0,
            mls_rate=0,
            tier="Exempt",
            has_hospital_cover=True
        )
    
    thresholds = MLS_THRESHOLDS_FAMILY_2024_25 if family else MLS_THRESHOLDS_SINGLE_2024_25
    
    # Adjust family thresholds for additional children after first
    if family and dependent_children > 1:
        extra_children = dependent_children - 1
        increment = extra_children * MLS_FAMILY_CHILD_INCREMENT
        thresholds = [(t + increment if t != float('inf') else t, r) for t, r in thresholds]
    
    # Find applicable tier
    prev_threshold = 0
    for i, (threshold, rate) in enumerate(thresholds):
        if income_for_mls <= threshold:
            if rate == 0:
                tier_name = "Base tier (no MLS)"
            elif rate == 0.01:
                tier_name = "Tier 1"
            elif rate == 0.0125:
                tier_name = "Tier 2"
            else:
                tier_name = "Tier 3"
            
            mls = income_for_mls * rate
            return MLSResult(
                income_for_mls=income_for_mls,
                mls_amount=round(mls, 2),
                mls_rate=rate,
                tier=tier_name,
                has_hospital_cover=False
            )
        prev_threshold = threshold
    
    return MLSResult(income_for_mls, 0, 0, "Unknown", False)


class Div293Result(NamedTuple):
    """Result of Division 293 calculation."""
    div293_income: float
    concessional_contributions: float
    div293_applies: bool
    div293_tax: float
    taxable_contributions: float
    notes: str


def calculate_div293(
    taxable_income: float,
    concessional_contributions: float,
    reportable_fringe_benefits: float = 0,
    net_investment_loss: float = 0
) -> Div293Result:
    """
    Calculate Division 293 tax for FY2024-25.
    
    Division 293 applies additional 15% tax on concessional super contributions
    for individuals with income + super > $250,000.
    
    Args:
        taxable_income: Taxable income
        concessional_contributions: Employer + salary sacrifice + personal deductible super
        reportable_fringe_benefits: Reportable fringe benefits total
        net_investment_loss: Net financial investment loss + net rental property loss
        
    Returns:
        Div293Result with tax details
    """
    # Division 293 income = taxable income + super contributions + fringe benefits
    # (Note: investment losses are added back)
    div293_income = taxable_income + reportable_fringe_benefits + net_investment_loss
    total_with_super = div293_income + concessional_contributions
    
    if total_with_super <= DIV293_THRESHOLD:
        return Div293Result(
            div293_income=div293_income,
            concessional_contributions=concessional_contributions,
            div293_applies=False,
            div293_tax=0,
            taxable_contributions=0,
            notes=f"Income + super (${total_with_super:,.2f}) below ${DIV293_THRESHOLD:,} threshold"
        )
    
    # Amount over threshold
    excess = total_with_super - DIV293_THRESHOLD
    
    # Taxable contributions = lesser of (excess over threshold, total contributions)
    taxable_contributions = min(excess, concessional_contributions)
    
    # Div 293 tax = 15% of taxable contributions
    div293_tax = taxable_contributions * DIV293_RATE
    
    return Div293Result(
        div293_income=div293_income,
        concessional_contributions=concessional_contributions,
        div293_applies=True,
        div293_tax=round(div293_tax, 2),
        taxable_contributions=taxable_contributions,
        notes=f"${taxable_contributions:,.2f} of super taxed at additional 15%"
    )


class HELPResult(NamedTuple):
    """Result of HELP loan repayment calculation."""
    repayment_income: float
    repayment_rate: float
    repayment_amount: float
    notes: str


def calculate_help_repayment(repayment_income: float) -> HELPResult:
    """
    Calculate HELP/HECS loan compulsory repayment for FY2024-25.
    
    Note: FY2024-25 uses percentage of TOTAL repayment income (not marginal rates).
    From FY2025-26, marginal rates will be used.
    
    Args:
        repayment_income: Repayment income (taxable income + fringe benefits + 
                         net investment loss + reportable super contributions + 
                         exempt foreign employment income)
        
    Returns:
        HELPResult with repayment details
    """
    if repayment_income < 0:
        raise ValueError("Repayment income cannot be negative")
    
    # Find applicable threshold and rate
    prev_threshold = 0
    for threshold, rate in HELP_THRESHOLDS_2024_25:
        if repayment_income <= threshold:
            repayment = repayment_income * rate
            return HELPResult(
                repayment_income=repayment_income,
                repayment_rate=rate,
                repayment_amount=round(repayment, 2),
                notes=f"{rate*100:.1f}% of total repayment income" if rate > 0 else "Below repayment threshold"
            )
        prev_threshold = threshold
    
    # Highest tier: 10%
    repayment = repayment_income * 0.10
    return HELPResult(
        repayment_income=repayment_income,
        repayment_rate=0.10,
        repayment_amount=round(repayment, 2),
        notes="10% of total repayment income"
    )


class CCSResult(NamedTuple):
    """Result of CCS threshold check."""
    combined_income: float
    above_cutoff: bool
    estimated_subsidy_rate: str
    notes: str


def check_ccs_threshold(combined_income: float, children_in_care: int = 1) -> CCSResult:
    """
    Check CCS (Child Care Subsidy) threshold status.
    
    Note: Actual CCS rates depend on many factors. This is a simplified check
    against the income cutoff thresholds.
    
    Args:
        combined_income: Combined family adjusted taxable income
        children_in_care: Number of children in approved care
        
    Returns:
        CCSResult with threshold status
    """
    cutoff = CCS_THRESHOLDS['multi_child_cutoff'] if children_in_care > 1 else CCS_THRESHOLDS['standard_cutoff']
    
    if combined_income <= CCS_THRESHOLDS['max_subsidy_threshold']:
        return CCSResult(
            combined_income=combined_income,
            above_cutoff=False,
            estimated_subsidy_rate="Maximum (85%+)",
            notes=f"Below ${CCS_THRESHOLDS['max_subsidy_threshold']:,} - eligible for maximum CCS rate"
        )
    
    if combined_income > cutoff:
        return CCSResult(
            combined_income=combined_income,
            above_cutoff=True,
            estimated_subsidy_rate="0% or minimum",
            notes=f"Above ${cutoff:,} cutoff - may receive 0% CCS (check Services Australia for exact calculation)"
        )
    
    return CCSResult(
        combined_income=combined_income,
        above_cutoff=False,
        estimated_subsidy_rate="Reduced (check actual rate)",
        notes=f"Between ${CCS_THRESHOLDS['max_subsidy_threshold']:,} and ${cutoff:,} - CCS rate reduces with income"
    )


# =============================================================================
# SUMMARY CALCULATION
# =============================================================================

class TaxSummary(NamedTuple):
    """Complete tax summary for an individual."""
    taxable_income: float
    income_tax: float
    medicare_levy: float
    medicare_levy_surcharge: float
    help_repayment: float
    div293_tax: float
    total_tax: float
    net_income: float
    effective_rate: float


def calculate_summary(
    taxable_income: float,
    reportable_fringe_benefits: float = 0,
    net_investment_loss: float = 0,
    concessional_super: float = 0,
    has_hospital_cover: bool = True,
    has_help_debt: bool = False,
    sapto_eligible: bool = False,
    family: bool = False,
    dependent_children: int = 0
) -> TaxSummary:
    """
    Calculate complete tax summary for FY2024-25.
    
    Args:
        taxable_income: Taxable income
        reportable_fringe_benefits: Reportable fringe benefits
        net_investment_loss: Net investment losses (positive number)
        concessional_super: Concessional super contributions
        has_hospital_cover: Has appropriate private hospital cover (affects MLS)
        has_help_debt: Has HELP/HECS debt requiring repayment
        sapto_eligible: Eligible for Seniors and Pensioners Tax Offset
        family: Has spouse/de facto (affects MLS thresholds)
        dependent_children: Number of MLS dependent children
        
    Returns:
        TaxSummary with all tax components
    """
    # Income tax
    tax_result = calculate_income_tax(taxable_income)
    income_tax = tax_result.tax_payable
    
    # Medicare levy
    medicare_result = calculate_medicare_levy(taxable_income, sapto_eligible)
    medicare_levy = medicare_result.medicare_levy
    
    # Medicare levy surcharge
    mls_income = taxable_income + reportable_fringe_benefits + net_investment_loss
    mls_result = calculate_mls(mls_income, family, dependent_children, has_hospital_cover)
    mls = mls_result.mls_amount
    
    # HELP repayment
    help_repayment = 0
    if has_help_debt:
        repayment_income = taxable_income + reportable_fringe_benefits + net_investment_loss
        help_result = calculate_help_repayment(repayment_income)
        help_repayment = help_result.repayment_amount
    
    # Division 293
    div293_result = calculate_div293(
        taxable_income, concessional_super, 
        reportable_fringe_benefits, net_investment_loss
    )
    div293_tax = div293_result.div293_tax
    
    # Totals
    total_tax = income_tax + medicare_levy + mls + help_repayment + div293_tax
    net_income = taxable_income - total_tax
    effective_rate = total_tax / taxable_income if taxable_income > 0 else 0
    
    return TaxSummary(
        taxable_income=taxable_income,
        income_tax=income_tax,
        medicare_levy=medicare_levy,
        medicare_levy_surcharge=mls,
        help_repayment=help_repayment,
        div293_tax=div293_tax,
        total_tax=round(total_tax, 2),
        net_income=round(net_income, 2),
        effective_rate=round(effective_rate, 4)
    )


# =============================================================================
# CLI INTERFACE
# =============================================================================

def format_currency(amount: float) -> str:
    """Format amount as Australian currency."""
    if amount >= 0:
        return f"${amount:,.2f}"
    return f"-${abs(amount):,.2f}"


def format_percentage(rate: float) -> str:
    """Format rate as percentage."""
    return f"{rate * 100:.2f}%"


def cmd_tax(args: argparse.Namespace) -> None:
    """Handle 'tax' command."""
    result = calculate_income_tax(args.income)
    
    print(f"\n{'='*60}")
    print("INCOME TAX CALCULATION - FY2024-25")
    print(f"{'='*60}")
    print(f"Taxable Income:    {format_currency(result.taxable_income)}")
    print(f"Income Tax:        {format_currency(result.tax_payable)}")
    print(f"Marginal Rate:     {format_percentage(result.marginal_rate)}")
    print(f"Effective Rate:    {format_percentage(result.effective_rate)}")
    print(f"Bracket:           {result.bracket_description}")
    print(f"{'='*60}\n")


def cmd_medicare(args: argparse.Namespace) -> None:
    """Handle 'medicare' command."""
    result = calculate_medicare_levy(args.income, args.sapto)
    
    print(f"\n{'='*60}")
    print("MEDICARE LEVY CALCULATION - FY2024-25")
    print(f"{'='*60}")
    print(f"Taxable Income:    {format_currency(result.taxable_income)}")
    print(f"Medicare Levy:     {format_currency(result.medicare_levy)}")
    print(f"Effective Rate:    {format_percentage(result.levy_rate)}")
    print(f"Status:            {result.notes}")
    print(f"{'='*60}\n")


def cmd_mls(args: argparse.Namespace) -> None:
    """Handle 'mls' command."""
    result = calculate_mls(
        args.income, 
        args.family, 
        args.children if hasattr(args, 'children') else 0,
        args.has_cover
    )
    
    print(f"\n{'='*60}")
    print("MEDICARE LEVY SURCHARGE - FY2024-25")
    print(f"{'='*60}")
    print(f"Income for MLS:    {format_currency(result.income_for_mls)}")
    print(f"Hospital Cover:    {'Yes' if result.has_hospital_cover else 'No'}")
    print(f"Family Status:     {'Family' if args.family else 'Single'}")
    print(f"MLS Tier:          {result.tier}")
    print(f"MLS Rate:          {format_percentage(result.mls_rate)}")
    print(f"MLS Amount:        {format_currency(result.mls_amount)}")
    print(f"{'='*60}\n")


def cmd_div293(args: argparse.Namespace) -> None:
    """Handle 'div293' command."""
    result = calculate_div293(
        args.income,
        args.super_contributions,
        args.fringe_benefits if hasattr(args, 'fringe_benefits') else 0,
        args.investment_loss if hasattr(args, 'investment_loss') else 0
    )
    
    print(f"\n{'='*60}")
    print("DIVISION 293 TAX - FY2024-25")
    print(f"{'='*60}")
    print(f"Taxable Income:         {format_currency(args.income)}")
    print(f"Concessional Super:     {format_currency(result.concessional_contributions)}")
    print(f"Div 293 Income:         {format_currency(result.div293_income)}")
    print(f"Total (Income + Super): {format_currency(result.div293_income + result.concessional_contributions)}")
    print(f"Threshold:              {format_currency(DIV293_THRESHOLD)}")
    print(f"Div 293 Applies:        {'Yes' if result.div293_applies else 'No'}")
    if result.div293_applies:
        print(f"Taxable Contributions:  {format_currency(result.taxable_contributions)}")
        print(f"Div 293 Tax (15%):      {format_currency(result.div293_tax)}")
    print(f"Notes:                  {result.notes}")
    print(f"{'='*60}\n")


def cmd_help_loan(args: argparse.Namespace) -> None:
    """Handle 'help-loan' command."""
    result = calculate_help_repayment(args.income)
    
    print(f"\n{'='*60}")
    print("HELP/HECS LOAN REPAYMENT - FY2024-25")
    print(f"{'='*60}")
    print(f"Repayment Income:  {format_currency(result.repayment_income)}")
    print(f"Repayment Rate:    {format_percentage(result.repayment_rate)}")
    print(f"Repayment Amount:  {format_currency(result.repayment_amount)}")
    print(f"Notes:             {result.notes}")
    print(f"{'='*60}\n")


def cmd_ccs(args: argparse.Namespace) -> None:
    """Handle 'ccs' command."""
    result = check_ccs_threshold(args.income, args.children if hasattr(args, 'children') else 1)
    
    print(f"\n{'='*60}")
    print("CCS THRESHOLD CHECK - FY2024-25")
    print(f"{'='*60}")
    print(f"Combined Income:       {format_currency(result.combined_income)}")
    print(f"CCS Cutoff:            {format_currency(CCS_THRESHOLDS['standard_cutoff'])}")
    print(f"Above Cutoff:          {'⚠️  YES' if result.above_cutoff else '✅ NO'}")
    print(f"Estimated CCS Rate:    {result.estimated_subsidy_rate}")
    print(f"Notes:                 {result.notes}")
    print(f"{'='*60}\n")


def cmd_summary(args: argparse.Namespace) -> None:
    """Handle 'summary' command."""
    result = calculate_summary(
        taxable_income=args.income,
        reportable_fringe_benefits=args.fringe_benefits if hasattr(args, 'fringe_benefits') and args.fringe_benefits else 0,
        net_investment_loss=args.investment_loss if hasattr(args, 'investment_loss') and args.investment_loss else 0,
        concessional_super=args.super_contributions if hasattr(args, 'super_contributions') and args.super_contributions else 0,
        has_hospital_cover=not args.no_hospital_cover if hasattr(args, 'no_hospital_cover') else True,
        has_help_debt=args.help_debt if hasattr(args, 'help_debt') else False,
        sapto_eligible=args.sapto if hasattr(args, 'sapto') else False,
        family=args.family if hasattr(args, 'family') else False,
        dependent_children=args.children if hasattr(args, 'children') else 0
    )
    
    print(f"\n{'='*60}")
    print("TAX SUMMARY - FY2024-25")
    print(f"{'='*60}")
    print(f"Taxable Income:              {format_currency(result.taxable_income):>15}")
    print(f"{'─'*60}")
    print(f"Income Tax:                  {format_currency(result.income_tax):>15}")
    print(f"Medicare Levy:               {format_currency(result.medicare_levy):>15}")
    if result.medicare_levy_surcharge > 0:
        print(f"Medicare Levy Surcharge:     {format_currency(result.medicare_levy_surcharge):>15}")
    if result.help_repayment > 0:
        print(f"HELP Repayment:              {format_currency(result.help_repayment):>15}")
    if result.div293_tax > 0:
        print(f"Division 293 Tax:            {format_currency(result.div293_tax):>15}")
    print(f"{'─'*60}")
    print(f"TOTAL TAX:                   {format_currency(result.total_tax):>15}")
    print(f"NET INCOME:                  {format_currency(result.net_income):>15}")
    print(f"Effective Tax Rate:          {format_percentage(result.effective_rate):>15}")
    print(f"{'='*60}\n")


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Australian Tax Calculator CLI - FY2024-25",
        epilog="All rates are from the Australian Taxation Office (ATO) for FY2024-25."
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # tax command
    tax_parser = subparsers.add_parser('tax', help='Calculate income tax')
    tax_parser.add_argument('income', type=float, help='Taxable income in AUD')
    tax_parser.set_defaults(func=cmd_tax)
    
    # medicare command
    medicare_parser = subparsers.add_parser('medicare', help='Calculate Medicare levy')
    medicare_parser.add_argument('income', type=float, help='Taxable income in AUD')
    medicare_parser.add_argument('--sapto', action='store_true', 
                                 help='Eligible for Seniors and Pensioners Tax Offset')
    medicare_parser.set_defaults(func=cmd_medicare)
    
    # mls command
    mls_parser = subparsers.add_parser('mls', help='Calculate Medicare levy surcharge')
    mls_parser.add_argument('income', type=float, 
                           help='Income for MLS purposes (taxable + FBT + investment loss + super)')
    mls_parser.add_argument('--family', action='store_true', help='Family/couple status')
    mls_parser.add_argument('--children', type=int, default=0, 
                           help='Number of MLS dependent children')
    mls_parser.add_argument('--has-cover', action='store_true', 
                           help='Has appropriate private hospital cover')
    mls_parser.set_defaults(func=cmd_mls)
    
    # div293 command
    div293_parser = subparsers.add_parser('div293', help='Calculate Division 293 super tax')
    div293_parser.add_argument('income', type=float, help='Taxable income in AUD')
    div293_parser.add_argument('super_contributions', type=float, 
                              help='Concessional super contributions')
    div293_parser.add_argument('--fringe-benefits', type=float, default=0,
                              help='Reportable fringe benefits')
    div293_parser.add_argument('--investment-loss', type=float, default=0,
                              help='Net investment loss')
    div293_parser.set_defaults(func=cmd_div293)
    
    # help-loan command
    help_parser = subparsers.add_parser('help-loan', help='Calculate HELP/HECS repayment')
    help_parser.add_argument('income', type=float, 
                            help='Repayment income (taxable + FBT + investment loss + super)')
    help_parser.set_defaults(func=cmd_help_loan)
    
    # ccs command
    ccs_parser = subparsers.add_parser('ccs', help='Check CCS threshold status')
    ccs_parser.add_argument('income', type=float, help='Combined family adjusted taxable income')
    ccs_parser.add_argument('--children', type=int, default=1, 
                           help='Number of children in approved child care')
    ccs_parser.set_defaults(func=cmd_ccs)
    
    # summary command
    summary_parser = subparsers.add_parser('summary', help='Full tax summary')
    summary_parser.add_argument('income', type=float, help='Taxable income in AUD')
    summary_parser.add_argument('--fringe-benefits', type=float, default=0,
                               help='Reportable fringe benefits')
    summary_parser.add_argument('--investment-loss', type=float, default=0,
                               help='Net investment loss')
    summary_parser.add_argument('--super-contributions', type=float, default=0,
                               help='Concessional super contributions')
    summary_parser.add_argument('--no-hospital-cover', action='store_true',
                               help='No private hospital cover (adds MLS)')
    summary_parser.add_argument('--help-debt', action='store_true',
                               help='Has HELP/HECS debt')
    summary_parser.add_argument('--sapto', action='store_true',
                               help='Eligible for SAPTO')
    summary_parser.add_argument('--family', action='store_true',
                               help='Family status for MLS')
    summary_parser.add_argument('--children', type=int, default=0,
                               help='MLS dependent children')
    summary_parser.set_defaults(func=cmd_summary)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        args.func(args)
        return 0
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
