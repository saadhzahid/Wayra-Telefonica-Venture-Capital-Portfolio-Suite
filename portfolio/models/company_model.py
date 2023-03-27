from django.core.validators import RegexValidator, MinLengthValidator
from django.db import models


class Company(models.Model):
    """A company to store information about."""

    def __str__(self):
        return f'{self.name}'

    name = models.CharField(
        max_length=60,
        unique=True,
        blank=False,
        validators=[RegexValidator(
            regex=r"^[a-zA-Z0-9 ,]{3,}$",
            message="Company name must consist of three to sixty characters"
        )]
    )
    company_registration_number = models.CharField('Company Registration Number',
                                                   default="00000000",
                                                   blank=False,
                                                   max_length=8,
                                                   validators=[MinLengthValidator(8)])
    trading_names = models.CharField(
        max_length=60,
        unique=True,
        blank=True,
        validators=[RegexValidator(
            regex=r"^[a-zA-Z0-9 ,]{3,}$",
            message="Company name must consist of three to sixty characters"
        )]
    )
    previous_names = models.CharField(
        max_length=60,
        unique=True,
        blank=True,
        validators=[RegexValidator(
            regex=r"^[a-zA-Z0-9 ,]{3,}$",
            message="Company name must consist of three to sixty characters"
        )]
    )
    registered_address = models.CharField("Registered Address", max_length=50,
                                          blank=True)  # models.ForeignKey(ResidentialAddress, on_delete=models.CASCADE, null=True)
    jurisdiction = models.CharField("Jurisdiction", max_length=50, blank=True)
    founders = None  # models.ForeignKey(Individual)
    incorporation_date = models.DateField(auto_now=True)
    investors = None  # e.g. models.ForeignKey(Individual)
    is_archived = models.BooleanField(default=False)

    def archive(self):
        self.is_archived = True
        self.save()

    def unarchive(self):
        self.is_archived = False
        self.save()
