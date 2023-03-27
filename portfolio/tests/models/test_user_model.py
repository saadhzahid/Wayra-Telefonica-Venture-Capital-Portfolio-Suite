"""Unit tests of the User model."""

from django.core.exceptions import ValidationError
from django.test import TestCase

from portfolio.models import User


class UserModelTestCase(TestCase):
    fixtures = ['portfolio/tests/fixtures/default_user.json',
                'portfolio/tests/fixtures/other_users.json']

    def setUp(self):
        self.user = User.objects.get(email="john.doe@example.org")

    def _assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except ValidationError:
            self.fail("Test user should be valid")

    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()

    def test_valid_user(self):
        self._assert_user_is_valid()

    def test_first_name_must_not_be_blank(self):
        self.user.first_name = ""
        self._assert_user_is_invalid()

    def test_first_name_valid_255_or_less_chr(self):
        self.user.first_name = "A" * 255
        self._assert_user_is_valid()

    def test_first_name_invalid_more_than_255_chr(self):
        self.user.first_name = "A" * (255 + 1)
        self._assert_user_is_invalid()

    def test_first_name_valid_when_not_unique(self):
        second_user = User.objects.get(email="petra.pickles@example.org")
        self.user.first_name = second_user.first_name
        self._assert_user_is_valid()

    def test_last_name_must_not_be_blank(self):
        self.user.last_name = ""
        self._assert_user_is_invalid()

    def test_last_name_valid_255_or_less_chr(self):
        self.user.last_name = "A" * 255
        self._assert_user_is_valid()

    def test_last_name_invalid_more_than_255_chr(self):
        self.user.last_name = "A" * (255 + 1)
        self._assert_user_is_invalid()

    def test_last_name_valid_when_not_unique(self):
        second_user = User.objects.get(email="petra.pickles@example.org")
        self.user.last_name = second_user.last_name
        self._assert_user_is_valid()

    def test_email_must_be_unique(self):
        second_user = User.objects.get(email="petra.pickles@example.org")
        self.user.email = second_user.email
        self._assert_user_is_invalid()

    def test_email_must_be_less_than_or_equal_255_chr(self):
        self.user.email = "A" * 243 + "@example.org"
        self._assert_user_is_valid()

    def test_email_invalid_more_than_255_chr(self):
        self.user.email = "A" * 244 + "@example.org"
        self._assert_user_is_invalid()

    def test_email_must_not_be_blank(self):
        self.user.email = ""
        self._assert_user_is_invalid()

    def test_email_must_have_domain(self):
        self.user.email = "ABC"
        self._assert_user_is_invalid()

    def test_email_must_have_username(self):
        self.user.email = "@example.org"
        self._assert_user_is_invalid()

    def test_email_must_not_contain_multiple_at_symbol(self):
        self.user.email = "aa@@example.org"
        self._assert_user_is_invalid()

    def test_user_phone_must_not_be_blank(self):
        self.user.phone = ""
        self._assert_user_is_invalid()
