"""Model to store investments"""
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils import timezone

from portfolio.models import Portfolio_Company
from portfolio.models.investor_model import Investor

FOUNDING_ROUNDS = [
    ('Seed round', 'Seed round'),
    ('Series A', 'Series A'),
    ('Series B', 'Series B'),
    ('Series C', 'Series C'),
    ('Coporate round', 'Coporate round'),
    ('Convertible note', 'Convertible note'),
    ('Venture round', 'Venture round'),
    ('Debt financing', 'Debt financing'),
    ('Post-IPO Equity', 'Post-IPO Equity')
]


class Investment(models.Model):
    """Investment model for a investment from an investor to a startups"""
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE, related_name="investor")
    startup = models.ForeignKey(Portfolio_Company, on_delete=models.CASCADE, related_name="startup")
    typeOfFoundingRounds = models.CharField(max_length=50, choices=FOUNDING_ROUNDS)
    investmentAmount = models.DecimalField(max_digits=15, decimal_places=2)
    dateInvested = models.DateField(validators=[MaxValueValidator(limit_value=timezone.now().date())])
    dateExit = models.DateField(blank=True, null=True)

    def clean(self):
        if self.dateExit is not None and self.dateInvested > self.dateExit:
            raise ValidationError('Date invest cannot be after date exit')


class ContractRight(models.Model):
    investment = models.ForeignKey(Investment, on_delete=models.CASCADE)
    right = models.CharField(max_length=255)
    details = models.CharField(max_length=255)
