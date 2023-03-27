from django.db import models

from portfolio.models.company_model import Company


class InvestorCompany(models.Model):
    VENTURE_CAPITAL = 'VC'
    PRIVATE_EQUITY_FIRM = 'PEF'
    ACCELERATOR = 'A'
    INVESTMENT_PARTNER = 'IP'
    CORPORATE_VENTURE_CAPITAL = 'CVC'
    MICRO_VC = 'MVC'
    ANGEL_GROUP = 'AG'
    INCUBATOR = 'I'
    INVESTMENT_BANK = 'IB'
    FAMILY_INVESTMENT_OFFICE = 'FIO'
    VENTURE_DEBT = 'VD'
    CO_WORKING_SPACE = 'CWS'
    FUND_OF_FUNDS = 'FOF'
    HEDGE_FUND = 'HF'
    GOVERNMENT_OFFICE = 'GO'
    UNIVERSITY_PROGRAM = 'UP'
    ENTREPRENEURSHIP_PROGRAM = 'EP'
    SECONDARY_PURCHASER = 'SP'
    STARTUP_COMPETITION = 'SC'
    SYNDICATE = 'S'
    PENSION_FUNDS = 'PF'

    INVESTOR_TYPES = [
        ('VENTURE_CAPITAL', 'Venture Capital'),
        ('PRIVATE_EQUITY_FIRM', 'Private Equity Firm'),
        ('ACCELERATOR', 'Accelerator'),
        ('INVESTMENT_PARTNER', 'Investment Partner'),
        ('CORPORATE_VENTURE_CAPITAL', 'Corporate Venture Capital'),
        ('MICRO_VC', 'Micro VC'),
        ('ANGEL_GROUP', 'Angel Group'),
        ('INCUBATOR', 'Incubator'),
        ('INVESTMENT_BANK', 'Investment Bank'),
        ('FAMILY_INVESTMENT_OFFICE', 'Family Investment Office'),
        ('VENTURE_DEBT', 'Venture Debt'),
        ('CO_WORKING_SPACE', 'Co-Working Space'),
        ('FUND_OF_FUNDS', 'Fund Of Funds'),
        ('HEDGE_FUND', 'Hedge Fund'),
        ('GOVERNMENT_OFFICE', 'Government Office'),
        ('UNIVERSITY_PROGRAM', 'University Program'),
        ('ENTREPRENEURSHIP_PROGRAM', 'Entrepreneurship Program'),
        ('SECONDARY_PURCHASER', 'Secondary Purchaser'),
        ('STARTUP_COMPETITION', 'Startup Competition'),
        ('SYNDICATE', 'Syndicate'),
        ('PENSION_FUNDS', ' Pension Funds'),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    angelListLink = models.URLField("Angellist link", max_length=200)
    crunchbaseLink = models.URLField("Crunchbase link", max_length=200)
    linkedInLink = models.URLField("Linkedin link", max_length=200)
    classification = models.CharField(
        max_length=50,
        choices=INVESTOR_TYPES,
        default=VENTURE_CAPITAL,
    )
