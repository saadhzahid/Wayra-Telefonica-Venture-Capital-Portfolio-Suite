from django import forms
from django.contrib.auth.models import Group
from django.test import TestCase

from portfolio.forms import UserCreationForm, EditUserForm
from portfolio.models import User


class CreateUserFormTestCase(TestCase):
    # Set up an examplery input to use for the tests
    def setUp(self):
        self.form_input = {
            "email": "test@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "password": "Password123",
            "phone": "+447412345678",
            "is_active": True,
            "group": Group.objects.first()
        }

    # Test if the form accepts valid input
    def test_valid_create_user_form(self):
        form = UserCreationForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    # Test the form having the required fields inside it
    def test_form_has_necessary_fields(self):
        form = UserCreationForm()
        self.assertIn("email", form.fields)
        self.assertIn("first_name", form.fields)
        self.assertIn("last_name", form.fields)
        self.assertIn("password", form.fields)
        self.assertTrue(isinstance(form.fields["password"].widget, forms.PasswordInput))
        self.assertIn("phone", form.fields)
        self.assertIn("is_active", form.fields)
        self.assertIn("group", form.fields)
        self.assertTrue(isinstance(form.fields['group'], forms.ModelChoiceField))

    def test_email_cannot_be_blank(self):
        self.form_input['email'] = ''
        form = UserCreationForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_first_name_cannot_be_blank(self):
        self.form_input['first_name'] = ''
        form = UserCreationForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_last_name_cannot_be_blank(self):
        self.form_input['last_name'] = ''
        form = UserCreationForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_cannot_be_blank(self):
        self.form_input['password'] = ''
        form = UserCreationForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_phone_cannot_be_blank(self):
        self.form_input['phone'] = ''
        form = UserCreationForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    # Test if the form saves correctly
    def test_form_must_save_correctly(self):
        form = UserCreationForm(data=self.form_input)
        before_count = User.objects.count()
        form.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count + 1)
        new_user = User.objects.get(email='test@example.com')
        self.assertEqual(new_user.first_name, 'John')
        self.assertEqual(new_user.last_name, "Doe")
        self.assertEqual(new_user.phone, "+447412345678")
        self.assertEqual(new_user.is_active, True)


class EditUserFormTestCase(TestCase):
    def setUp(self):
        self.form_input = {
            "email": "test@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "phone": "+447412345678",
            "is_active": True,
            "group": Group.objects.first()
        }

    def test_valid_create_user_form(self):
        form = EditUserForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    # Test the form having the required fields inside it
    def test_form_has_necessary_fields(self):
        form = EditUserForm()
        self.assertIn("email", form.fields)
        self.assertIn("first_name", form.fields)
        self.assertIn("last_name", form.fields)
        self.assertIn("phone", form.fields)
        self.assertIn("is_active", form.fields)
        self.assertIn("group", form.fields)
        self.assertTrue(isinstance(form.fields['group'], forms.ModelChoiceField))

    def test_email_cannot_be_blank(self):
        self.form_input['email'] = ''
        form = EditUserForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_first_name_cannot_be_blank(self):
        self.form_input['first_name'] = ''
        form = EditUserForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_last_name_cannot_be_blank(self):
        self.form_input['last_name'] = ''
        form = EditUserForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_phone_cannot_be_blank(self):
        self.form_input['phone'] = ''
        form = EditUserForm(data=self.form_input)
        self.assertFalse(form.is_valid())
