from django.core.exceptions import ValidationError
from django.db import models

from portfolio.models import Company, Individual


class Investor(models.Model):
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

    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, related_name="company",
                                default=None)
    individual = models.ForeignKey(Individual, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="individual", default=None)
    classification = models.CharField(
        max_length=50,
        choices=INVESTOR_TYPES,
        default=VENTURE_CAPITAL,
    )

    def clean(self):
        if (self.company is None and self.individual is None) or \
                (self.company and self.individual):
            raise ValidationError('company and individual cannot both be null')
