"""Form for creating a founder."""
from django import forms

from portfolio.models.founder_model import Founder


class FounderForm(forms.ModelForm):
    """Form for creating a founder."""

    class Meta:
        model = Founder
        fields = ["companyFounded", "individualFounder"]
