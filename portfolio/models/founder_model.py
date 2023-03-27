"""Founder model of a company."""
from django.db import models

from portfolio.models.company_model import Company
from portfolio.models.individual_model import Individual, IndividualManager


class Founder(models.Model):
    """A founder of a company."""
    objects = IndividualManager()
    companyFounded = models.OneToOneField(Company, on_delete=models.CASCADE)
    individualFounder = models.OneToOneField(Individual, on_delete=models.CASCADE)
