from django.core.validators import MinValueValidator, validate_image_file_extension
from django.db import models

from portfolio.models import Individual, Company
import os

DEFAULT_PATH = "programmes/"


# Returns the storage path of a file.
def get_path(instance, file_name):
    return os.path.join(DEFAULT_PATH, instance.name, file_name)


class Programme(models.Model):
    """Model for programmes"""
    name = models.CharField(max_length=255)
    cohort = models.PositiveIntegerField(validators=[MinValueValidator(1, message="cohort has to be at least 1")])
    partners = models.ManyToManyField(Company, related_name="partners")
    participants = models.ManyToManyField(Company, related_name="participants")
    coaches_mentors = models.ManyToManyField(Individual)
    cover = models.ImageField(blank=True, validators=[validate_image_file_extension], upload_to=get_path)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ('name', 'cohort')
