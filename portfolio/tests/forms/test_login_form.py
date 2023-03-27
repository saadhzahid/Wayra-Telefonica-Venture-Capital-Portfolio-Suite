"""Unit tests of the log in form."""

from django import forms
from django.test import TestCase

from portfolio.forms import LogInForm
from portfolio.models import User


class LogInFormTestCase(TestCase):
    """Unit tests of the log in form."""
    fixtures = ["portfolio/tests/fixtures/default_user.json"]

    def setUp(self):
        self.user = User.objects.get(email="john.doe@example.org")
        self.form_input = {'email': 'john.doe@example.org', 'password': 'Password123'}

    def test_form_contains_required_fields(self):
        form = LogInForm()
        self.assertIn('email', form.fields)
        self.assertIn('password', form.fields)
        password_field = form.fields['password']
        self.assertTrue(isinstance(password_field.widget, forms.PasswordInput))

    def test_form_accepts_valid_input(self):
        form = LogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank_email(self):
        self.form_input['email'] = ''
        form = LogInForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_password(self):
        self.form_input['password'] = ''
        form = LogInForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_accepts_incorrect_email(self):
        self.form_input['email'] = 'jane.d@example.org'
        form = LogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_accepts_incorrect_password(self):
        self.form_input['password'] = 'pwd'
        form = LogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_returns_correct_user(self):
        form = LogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())
        form_user = form.get_user()
        self.assertEqual(form_user, self.user)

    def test_form_returns_none_for_invalid_input(self):
        self.form_input['password'] = 'pwd'
        form = LogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())
        form_user = form.get_user()
        self.assertEqual(form_user, None)
