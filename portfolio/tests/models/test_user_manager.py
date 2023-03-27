"""Unit tests of the User manager class."""

from django.core.exceptions import ValidationError
from django.test import TestCase

from portfolio.models import User


class UserManagerTestCase(TestCase):
    """Unit tests of the User manager class."""

    def test_has_to_supply_first_name(self):
        with self.assertRaises(ValidationError):
            User.objects.create_user(
                email="john.doe@example.org",
                password="Password123",
                last_name="Doe",
                phone="+447312345678",
            )

    def test_has_to_supply_last_name(self):
        with self.assertRaises(ValidationError):
            User.objects.create_user(
                email="john.doe@example.org",
                password="Password123",
                first_name="John",
                phone="+447312345678",
            )

    def test_has_to_supply_phone(self):
        with self.assertRaises(ValidationError):
            User.objects.create_user(
                email="john.doe@example.org",
                password="Password123",
                first_name="John",
                last_name="Doe",
            )

    def test_has_to_supply_email(self):
        with self.assertRaises(ValidationError):
            User.objects.create_user(
                password="Password123",
                first_name="John",
                last_name="Doe",
                phone="+447312345678",
            )

    def test_can_create_valid_user(self):
        user_john = User.objects.create_user(
            email="john.doe@example.org",
            password="Password123",
            first_name="John",
            last_name="Doe",
            phone="+447312345678",
        )
        self.assertEqual(user_john.email, "john.doe@example.org")
        self.assertTrue(user_john.check_password("Password123"))
        self.assertEqual(user_john.first_name, "John")
        self.assertEqual(user_john.last_name, "Doe")
        self.assertEqual(user_john.phone, "+447312345678")

    def test_can_create_valid_admin(self):
        user_petra = User.objects.create_superuser(
            email="petra.pickle@example.org",
            password="Password123",
            first_name="Petra",
            last_name="Pickle",
            phone="+447312345678",
        )
        self.assertEqual(user_petra.email, "petra.pickle@example.org")
        self.assertTrue(user_petra.check_password("Password123"))
        self.assertEqual(user_petra.first_name, "Petra")
        self.assertEqual(user_petra.last_name, "Pickle")
        self.assertEqual(user_petra.phone, "+447312345678")

    def test_cannot_create_invalid_user(self):
        with self.assertRaises(ValidationError):
            User.objects.create_user(
                email="INVALID_EMAIL",
                password="Password123",
                first_name="John",
                last_name="Doe",
                phone="+447312345678",
            )

    def test_cannot_create_invalid_admin(self):
        with self.assertRaises(ValidationError):
            User.objects.create_superuser(
                email="INVALID_EMAIL",
                password="Password123",
                first_name="Petra",
                last_name="Pickle",
                phone="+447312345678",
            )
