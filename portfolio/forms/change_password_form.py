"""Forms for the VC portfolio management site"""
from django import forms
from django.contrib.auth.hashers import check_password
from django.core.validators import RegexValidator


# Form for creating an individual / client
class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(),
        validators=[
            RegexValidator(
                regex=r'^(?=.*[A-Z](?=.*[a-z])(?=.*[0-9])).*$',
                message="Password must contain an uppercase character, a lowercase character and a number."
            )
        ]
    )
    confirm_password = forms.CharField(label="Confirm password", widget=forms.PasswordInput())

    class Meta:
        widgets = {
            'old_password': forms.PasswordInput(),
            'new_password': forms.PasswordInput(),
            'confirm_password': forms.PasswordInput(),
        }

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        super().clean()
        old_password = self.cleaned_data.get("old_password")
        new_password = self.cleaned_data.get("new_password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if new_password != confirm_password:
            self.add_error("confirm_password", "Confirmation does not match password.")

        if not check_password(old_password, self.user.password): \
                self.add_error("old_password", "Incorrect Password.")

    def save(self):
        self.user.set_password(self.cleaned_data.get("new_password"))
        self.user.save()
