"""Unit tests of the Profile Picture form."""
import logging
from io import BytesIO

from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from portfolio.forms import ProfilePictureForm
from portfolio.models import User

logging.getLogger("PIL").setLevel(logging.WARNING)


class CompanyCreateFormTestCase(TestCase):
    fixtures = [
        "portfolio/tests/fixtures/default_user.json",
    ]

    # Set up an examplery input to use for the tests
    def setUp(self):
        self.user = User.objects.get(email="john.doe@example.org")
        image_file = BytesIO()
        image_file.write(open("portfolio/static/images/wayra_logo.png", 'rb').read())
        image_file.seek(0)
        self.file_data = SimpleUploadedFile("portfolio/static/images/wayra_logo.png", image_file.read(),
                                            content_type="image/png")
        self.form_input = {
            "profile_picture": self.file_data,
        }

    # Default Tests
    def test_valid_profile_picture_form(self):
        form = ProfilePictureForm(data=self.form_input, instance=self.user, files=self.form_input)
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid())

    def test_profile_picture_form_has_necessary_fields(self):
        form = ProfilePictureForm()
        self.assertIn('profile_picture', form.fields)
        profile_picture_field = form.fields['profile_picture']
        self.assertTrue(isinstance(profile_picture_field, forms.ImageField))

    def test_profile_picture_form_uses_model_validation(self):
        form = ProfilePictureForm()
        self.assertFalse(form.is_valid())
        # self.assertEqual(form.errors['profile_picture'][0], 'Please select an image.')

    def test_profile_picture_form_must_save_correctly(self):
        form = ProfilePictureForm(data=self.form_input, instance=self.user, files=self.form_input)
        old_profile_picture = self.user.profile_picture
        if form.is_valid():
            form.save()
        self.user = User.objects.get(email="john.doe@example.org")
        new_profile_picture = self.user.profile_picture
        self.assertNotEqual(old_profile_picture, new_profile_picture)
        # self.assertEqual(self.user.profile_picture.url, "/media/wayra_logo.png")
        self.user.profile_picture.delete()
