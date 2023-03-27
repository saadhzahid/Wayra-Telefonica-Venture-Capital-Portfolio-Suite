"""Forms for the VC portfolio management site"""
from django import forms

from portfolio.models import User


# Form for updating a user model
class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["profile_picture"]
        error_messages = {
            'profile_picture': {
                'required': "Please select an image.",
            },
        }

    def __init__(self, *args, **kwargs):
        super(ProfilePictureForm, self).__init__(*args, **kwargs)
        self.fields['profile_picture'].required = True

    def save(self):
        user = self.instance
        user.profile_picture = self.cleaned_data["profile_picture"]
        user.save()
