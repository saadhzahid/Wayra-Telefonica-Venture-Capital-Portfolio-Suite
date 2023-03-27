"""Unit tests of the settings views"""
import logging
from io import BytesIO

from django.contrib.auth.hashers import check_password
from django.contrib.messages import get_messages
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse

from portfolio.forms import ChangePasswordForm, ContactDetailsForm, ProfilePictureForm
from portfolio.models import User
from portfolio.tests.helpers import LogInTester, reverse_with_next

logging.getLogger("PIL").setLevel(logging.WARNING)
from django.conf import settings as django_settings


class SettingsViewTestCase(TestCase, LogInTester):
    """Unit tests of the dashboard view"""
    fixtures = [
        "portfolio/tests/fixtures/default_user.json",
    ]

    def setUp(self) -> None:
        self.url = reverse('account_settings')
        self.change_password_url = reverse('change_password')
        self.contact_details_url = reverse('contact_details')
        self.upload_profile_picture_url = reverse('upload_profile_picture')
        self.remove_profile_picture_url = reverse('remove_profile_picture')
        self.user = User.objects.get(email="john.doe@example.org")
        self.change_password_form_input = {
            "old_password": "Password123",
            "new_password": "Password321",
            "confirm_password": "Password321",
        }
        self.contact_details_form_input = {
            "first_name": "Johnny",
            "last_name": "Doe",
            "email": "john.doe@example.org",
            "phone": "0712345678",
        }
        image_file = BytesIO()
        image_file.write(open("portfolio/static/images/wayra_logo.png", 'rb').read())
        image_file.seek(0)
        self.file_data = SimpleUploadedFile("portfolio/static/images/wayra_logo.png", image_file.read(),
                                            content_type="image/png")
        self.upload_profile_picture_form_input = {
            "profile_picture": self.file_data,
        }
        self.set_session_variables()

    def test_account_settings_urls(self):
        self.assertEqual(self.url, '/account_settings/')
        self.assertEqual(self.change_password_url, '/account_settings/change_password')
        self.assertEqual(self.contact_details_url, '/account_settings/contact_details')
        self.assertEqual(self.upload_profile_picture_url, '/account_settings/upload_profile_picture')
        self.assertEqual(self.remove_profile_picture_url, '/account_settings/remove_profile_picture')

    def test_get_account_settings(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'settings/account_settings.html')

    def test_get_account_settings_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_account_settings_uses_the_correct_templates(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'settings/change_password_section.html')
        self.assertTemplateUsed(response, 'settings/contact_details_section.html')
        self.assertTemplateUsed(response, 'settings/deactivate_account.html')
        self.assertTemplateUsed(response, 'settings/upload_profile_section.html')

    def test_get_account_settings_parses_the_correct_form(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        form = response.context['change_password_form']
        self.assertTrue(isinstance(form, ChangePasswordForm))
        self.assertFalse(form.is_bound)

    # Change password Tests
    def test_password_changed_successful(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.change_password_url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse)

        form = ChangePasswordForm(data=self.change_password_form_input, user=self.user)
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)
        self.assertTrue(check_password(self.change_password_form_input["old_password"], self.user.password))

        response = self.client.post(self.change_password_url, self.change_password_form_input, follow=True)
        user = User.objects.get(email=self.user.email)
        self.assertTrue(user)
        response_url = reverse('account_settings')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTrue(check_password(self.change_password_form_input["new_password"], user.password))

    def test_password_changed_unsuccessful(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.change_password_url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse)

        form = ChangePasswordForm(data=self.change_password_form_input, user=self.user)
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)
        self.assertTrue(check_password(self.change_password_form_input["old_password"], self.user.password))

        self.change_password_form_input["confirm_password"] = "WrongPassword"

        response = self.client.post(self.change_password_url, self.change_password_form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(check_password(self.change_password_form_input["old_password"], self.user.password))
        self.assertFalse(check_password(self.change_password_form_input["new_password"], self.user.password))
        form = response.context['change_password_form']
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['confirm_password'][0], 'Confirmation does not match password.')

    # Contact details Tests
    def test_contact_details_changed_successful(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.contact_details_url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse)

        form = ContactDetailsForm(data=self.contact_details_form_input, user=self.user, instance=self.user)
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)
        self.user = User.objects.get(email="john.doe@example.org")
        self.assertEqual(self.user.first_name, "John")

        response = self.client.post(self.contact_details_url, self.contact_details_form_input, follow=True)
        user = User.objects.get(email=self.user.email)
        self.assertTrue(user)
        response_url = reverse('account_settings')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertEqual(user.first_name, self.contact_details_form_input["first_name"])

    def test_contact_details_changed_unsuccessful(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.contact_details_url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse)

        self.contact_details_form_input["phone"] = "wrong phone number"
        form = ContactDetailsForm(data=self.contact_details_form_input, user=self.user, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertGreater(len(form.errors), 0)
        self.user = User.objects.get(email="john.doe@example.org")
        self.assertEqual(self.user.first_name, "John")

        response = self.client.post(self.contact_details_url, self.contact_details_form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.user = User.objects.get(email="john.doe@example.org")
        self.assertEqual(self.user.first_name, "John")
        self.assertNotEqual(self.user.first_name, self.contact_details_form_input["first_name"])
        form = response.context['contact_details_form']
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['phone'][0],
                         'Your phone number should be of the format: 0712345678 or +44712345678')

    # Upload Profile Picture view tests
    def test_profile_picture_uploaded_successful(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.upload_profile_picture_url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse)

        form = ProfilePictureForm(data=self.upload_profile_picture_form_input, instance=self.user,
                                  files=self.upload_profile_picture_form_input)
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)

        response = self.client.post(self.upload_profile_picture_url, self.upload_profile_picture_form_input,
                                    follow=True)
        user = User.objects.get(email=self.user.email)
        self.assertTrue(user)
        response_url = reverse('account_settings')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        # self.assertEqual(user.profile_picture.url, "/media/wayra_logo.png")
        user.profile_picture.delete()

    def test_profile_picture_uploaded_unsuccessful(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.upload_profile_picture_url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse)

        self.upload_profile_picture_form_input["profile_picture"] = ""
        form = ProfilePictureForm(data=self.upload_profile_picture_form_input, instance=self.user,
                                  files=self.upload_profile_picture_form_input)
        self.assertFalse(form.is_valid())
        self.assertGreater(len(form.errors), 0)

        response = self.client.post(self.upload_profile_picture_url, self.upload_profile_picture_form_input,
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.user = User.objects.get(email="john.doe@example.org")
        self.assertFormError(response, 'profile_picture_form', 'profile_picture', 'Please select an image.')
        form = response.context['profile_picture_form']
        self.assertFalse(form.is_valid())

    # Remove Profile Picture view tests
    def test_profile_picture_removed_successful(self):
        self.client.login(email=self.user.email, password='Password123')

        # assign user a profile picture
        response = self.client.post(self.upload_profile_picture_url, self.upload_profile_picture_form_input,
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.user = User.objects.get(email=self.user.email)
        # self.assertEqual(self.user.profile_picture.url, "/media/wayra_logo.png")

        response = self.client.get(self.remove_profile_picture_url)
        self.user = User.objects.get(email=self.user.email)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Successfully removed your profile picture!")

    def test_profile_picture_removed_unsuccessful(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.remove_profile_picture_url)
        self.user = User.objects.get(email=self.user.email)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You do not have a profile picture!")

    # Helper functions
    def set_session_cookies(self, session):
        # Set the cookie to represent the session
        session_cookie = django_settings.SESSION_COOKIE_NAME
        self.client.cookies[session_cookie] = session.session_key
        cookie_data = {
            'max-age': None,
            'path': '/',
            'domain': django_settings.SESSION_COOKIE_DOMAIN,
            'secure': django_settings.SESSION_COOKIE_SECURE or None,
            'expires': None}
        self.client.cookies[session_cookie].update(cookie_data)

    def set_session_variables(self):
        session = self.client.session
        session['company_filter'] = 1
        session['company_layout'] = 1
        session.save()
        self.set_session_cookies(session)


class DeactiveAccountViewTestCase(TestCase, LogInTester):
    fixtures = ['portfolio/tests/fixtures/default_user.json', 'portfolio/tests/fixtures/other_users.json']

    def setUp(self) -> None:
        self.url = reverse('logout')
        self.user = User.objects.get(email="john.doe@example.org")
        self.admin_user = User.objects.get(email="petra.pickles@example.org")
        self.url = reverse('deactivate_account')

    def test_deactivate_account_url(self):
        self.assertEqual(self.url, '/deactivate_account')

    def test_get_deactivate_account_url(self):
        self.client.login(email=self.user.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        before_count = User.objects.count()
        response = self.client.get(self.url, follow=True)
        after_count = User.objects.count()
        self.assertEqual(before_count - 1, after_count)
        response_url = reverse('login')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'login/login.html')
        self.assertFalse(self._is_logged_in())

    def test_get_deactivate_account_url_for_admin_user(self):
        self.client.login(email=self.admin_user.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        before_count = User.objects.count()
        response = self.client.get(self.url, follow=True)
        after_count = User.objects.count()
        self.assertEqual(before_count - 1, after_count)
        response_url = reverse('login')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'login/login.html')
        self.assertFalse(self._is_logged_in())

    def test_get_deactivate_account_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
