from django.core.exceptions import ObjectDoesNotExist

from portfolio.models import User
from portfolio.seeders import Seeder


class UserSeeder(Seeder):
    def seed(self):
        self._create_standard_user()
        self._create_admin_user()
        print(f"{User.objects.count()} users in the db.\n")

    def _create_standard_user(self):
        try:
            User.objects.get(email="john.doe@example.org")
            print("john doe has already seeded.")

        except (ObjectDoesNotExist):
            user_john = User.objects.create_user(
                email="john.doe@example.org",
                password="Password123",
                first_name="John",
                last_name="Doe",
                phone="+447312345678"
            )
            user_john.save()
            print("john doe has been seeded.")

    def _create_admin_user(self):
        try:
            User.objects.get(email="petra.pickles@example.org")
            print("petra pickles has already seeded.")

        except (ObjectDoesNotExist):
            user_petra = User.objects.create_superuser(
                email="petra.pickles@example.org",
                password="Password123",
                first_name="Petra",
                last_name="Pickles",
                phone="+447312345678"
            )
            user_petra.save()
            print("petra has been seeded.")
