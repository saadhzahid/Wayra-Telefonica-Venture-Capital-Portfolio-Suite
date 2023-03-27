from django.db import models
from django_countries.fields import CountryField

from portfolio.models import Individual


class ResidentialAddress(models.Model):
    """Model to store addresses for individuals"""
    address_line1 = models.CharField("Address line 1", max_length=50, blank=False)
    address_line2 = models.CharField("Address line 2", max_length=50, blank=True)
    postal_code = models.CharField("Postal code", max_length=10)
    city = models.CharField("City", max_length=50, blank=False)
    state = models.CharField("State/Province", max_length=50, blank=True)
    country = CountryField(blank_label="Select country")
    individual = models.ForeignKey(Individual, on_delete=models.CASCADE)
