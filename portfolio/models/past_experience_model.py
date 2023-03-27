from django.db import models

from portfolio.models import Individual


class PastExperience(models.Model):
    """Model to store past experiences"""
    companyName = models.CharField(max_length=100)
    workTitle = models.CharField(max_length=100)
    start_year = models.PositiveSmallIntegerField()
    end_year = models.PositiveSmallIntegerField()
    duration = models.CharField(max_length=50, default="present")
    Description = models.CharField(max_length=500, blank=True)
    individual = models.ForeignKey(Individual, on_delete=models.CASCADE)
