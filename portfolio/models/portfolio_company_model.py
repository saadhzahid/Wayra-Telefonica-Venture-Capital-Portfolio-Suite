from django.db import models

from portfolio.models import Company


class Portfolio_Company(models.Model):
    parent_company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name="parent_company")
    wayra_number = models.CharField(max_length=255, unique=True)
