"""Unit tests of the change Passworrd form."""
from django import forms
from django.test import TestCase

from portfolio.forms import ChangePasswordForm
from portfolio.models import User


class CompanyCreateFormTestCase(TestCase):
    fixtures = [
        "portfolio/tests/fixtures/default_user.json",
    ]

    # Set up an examplery input to use for the tests
    def setUp(self):
        self.user = User.objects.get(email="john.doe@example.org")
        self.form_input = {
            "old_password": "Password123",
            "new_password": "Password321",
            "confirm_password": "Password321",
        }

    # Default Tests
    def test_valid_change_password_form(self):
        form = ChangePasswordForm(data=self.form_input, user=self.user)
        self.assertTrue(form.is_valid())

    def test_change_password_form_has_necessary_fields(self):
        form = ChangePasswordForm(user=self.user)
        self.assertIn('old_password', form.fields)
        old_password_field = form.fields['old_password']
        self.assertTrue(isinstance(old_password_field, forms.CharField))
        self.assertIn('new_password', form.fields)
        new_password_field = form.fields['new_password']
        self.assertTrue(isinstance(new_password_field, forms.CharField))
        self.assertIn('confirm_password', form.fields)
        confirm_password_field = form.fields['confirm_password']
        self.assertTrue(isinstance(confirm_password_field, forms.CharField))

    def test_change_password_form_uses_model_validation(self):
        self.form_input['confirm_password'] = 'x' * 5
        form = ChangePasswordForm(data=self.form_input, user=self.user)
        self.assertFalse(form.is_valid())

    def test_change_password_form_checks_users_old_password(self):
        self.form_input['old_password'] = 'x' * 5
        form = ChangePasswordForm(data=self.form_input, user=self.user)
        self.assertFalse(form.is_valid())

    def test_change_password_form_must_save_correctly(self):
        form = ChangePasswordForm(data=self.form_input, user=self.user)
        old_password = self.user.password
        if form.is_valid():
            form.save()
        new_password = self.user.password
        self.assertNotEqual(old_password, new_password)
