from django import forms
from django.contrib.auth.models import Group, Permission
from django.test import TestCase

from portfolio.forms import CreateGroupForm, EditGroupForm


class CreatePermissionGroupFormTestCase(TestCase):

    # Set up an examplery input to use for the tests
    def setUp(self):
        self.form_input = {
            "name": "TestGroup",
            "permissions": ["add_company"]
        }

    # Test if the form accepts valid input
    def test_valid_create_group_form(self):
        form = CreateGroupForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    # Test the form having the required fields inside it
    def test_form_has_necessary_fields(self):
        form = CreateGroupForm()
        self.assertIn("name", form.fields)
        self.assertIn("permissions", form.fields)
        self.assertTrue(isinstance(form.fields['permissions'], forms.MultipleChoiceField))

    # Test the form using model validation
    def test_form_uses_model_validation(self):
        self.form_input['name'] = ''
        form = CreateGroupForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    # Test if the form saves correctly
    def test_form_must_save_correctly(self):
        form = CreateGroupForm(data=self.form_input)
        before_count = Group.objects.count()
        form.save()
        after_count = Group.objects.count()
        self.assertEqual(after_count, before_count + 1)
        new_group = Group.objects.get(name='TestGroup')
        self.assertEqual(list(new_group.permissions.all()), [Permission.objects.get(codename="add_company")])


class EditPermissionGroupFormTestCase(TestCase):
    # Set up an examplery input to use for the tests
    def setUp(self):
        Group.objects.create(name="TestGroup2")
        self.form_input = {
            "name": "TestGroup",
            "permissions": ["add_company"]
        }

    # Test if the form accepts valid input
    def test_valid_create_group_form(self):
        form = EditGroupForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    # Test the form having the required fields inside it
    def test_form_has_necessary_fields(self):
        form = EditGroupForm()
        self.assertIn("name", form.fields)
        self.assertIn("permissions", form.fields)
        self.assertTrue(isinstance(form.fields['permissions'], forms.MultipleChoiceField))

    # Test the form using model validation
    def test_form_uses_model_validation(self):
        self.form_input['name'] = ''
        form = EditGroupForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_name_cannot_be_the_same(self):
        self.form_input['name'] = 'TestGroup2'
        form = EditGroupForm(data=self.form_input)
        self.assertFalse(form.is_valid())
