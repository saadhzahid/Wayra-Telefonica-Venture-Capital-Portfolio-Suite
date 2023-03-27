"""Forms for the individual creation."""
from django import forms
from django_countries.widgets import CountrySelectWidget
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from portfolio.models import Individual, ResidentialAddress
from portfolio.models.past_experience_model import PastExperience


# Form for creating an individual / client
class IndividualCreateForm(forms.ModelForm):
    class Meta:
        model = Individual
        fields = ["name", "AngelListLink", "CrunchbaseLink", "LinkedInLink",
                  "Company", "Position", "Email", "PrimaryNumber", "SecondaryNumber", "profile_pic"]
        exclude = ('is_archived',)

    def __init__(self, *args, **kwargs):
        super(IndividualCreateForm, self).__init__(*args, **kwargs)
        self.fields['PrimaryNumber'].widget = PhoneNumberPrefixWidget()
        self.fields['SecondaryNumber'].widget = PhoneNumberPrefixWidget()


# Form for creating addresses
class AddressCreateForm(forms.ModelForm):
    class Meta:
        model = ResidentialAddress
        fields = ['address_line1', 'address_line2', 'postal_code', 'city', 'state', 'country']
        exclude = ('individual',)
        widgets = {
            "country": CountrySelectWidget()
        }


# Form for creating past experience of individual
class PastExperienceForm(forms.ModelForm):
    class Meta:
        model = PastExperience
        fields = ['companyName', 'workTitle', 'start_year', 'end_year', 'Description']
        exclude = ('individual', 'duration',)
