"""Forms for the VC portfolio management site"""
from django import forms
from django.core.validators import RegexValidator

from portfolio.models import User


# Form for updating a user model
class ContactDetailsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

    phone = forms.CharField(
        label="Phone Number",
        validators=[
            RegexValidator(
                regex=r'^(?:0|\+?44)(?:\d\s?){9,10}$',
                message="Your phone number should be of the format: 0712345678 or +44712345678"
            )
        ])

    def __init__(self, user, *args, **kwargs):
        super(ContactDetailsForm, self).__init__(*args, **kwargs)
        self.user = user

    def save(self):
        self.user.first_name = self.cleaned_data["first_name"]
        self.user.last_name = self.cleaned_data["last_name"]
        self.user.email = self.cleaned_data["email"]
        self.user.phone = self.cleaned_data["phone"]
        self.user.save()
