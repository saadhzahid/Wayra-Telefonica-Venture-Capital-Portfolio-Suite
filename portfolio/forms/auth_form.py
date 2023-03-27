from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group

from portfolio.models import User


class LogInForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

    def get_user(self):
        """Returns authenticated user if possible."""
        user = None
        if self.is_valid():
            email = self.cleaned_data.get('email')
            password = self.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
        return user


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password", "phone", "is_active"]
        widgets = {
            'password': forms.PasswordInput()
        }

    group = forms.ModelChoiceField(
        label='Group',
        queryset=Group.objects.all(),
        empty_label=None,
        required=False
    )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        group = self.cleaned_data['group']
        user.set_password(self.cleaned_data['password'])
        user.save()
        user.groups.clear()
        user.groups.add(group)
        if commit:
            user.save()
        return user


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "phone", "is_active"]

    group = forms.ModelChoiceField(
        label='Group',
        queryset=Group.objects.all(),
        empty_label=None,
        required=False
    )

    def save(self):
        super().save(commit=False)
        user = self.instance
        user.email = self.cleaned_data['email']
        user.groups.clear()
        user.groups.add(self.cleaned_data['group'])
        user.save()
