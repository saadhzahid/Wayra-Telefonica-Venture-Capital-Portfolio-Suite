import random

from django.core.exceptions import ObjectDoesNotExist

from portfolio.models import Company
from portfolio.seeders import Seeder


class CompanySeeder(Seeder):
    COMPANIES_COUNT = 25

    def seed(self):
        self._create_companies(self.COMPANIES_COUNT)
        print(f"{Company.objects.count()} companies in the db.\n")

    def _create_companies(self, count):
        for i in range(1, count + 1):
            try:
                Company.objects.get(id=i)
                print(f"Company with id({i}) has already seeded.")

            except ObjectDoesNotExist:
                name = self.faker.company()
                if name in Company.objects.values_list('name', flat=True):
                    name = f'{name} {i}'

                trading_name = self.faker.company()
                if trading_name in Company.objects.values_list('trading_names', flat=True):
                    trading_name = f'{trading_name} {i}'

                previous_name = self.faker.company()
                if previous_name in Company.objects.values_list('previous_names', flat=True):
                    previous_name = f'{previous_name} {i}'

                crn = random.randint(0, 10 ** 8)
                address = self.faker.address()
                city = self.faker.city()
                company = Company.objects.create(name=name,
                                                 company_registration_number=crn,
                                                 trading_names=trading_name,
                                                 previous_names=previous_name,
                                                 registered_address=address,
                                                 jurisdiction=city,
                                                 incorporation_date=self.faker.date_this_century()
                                                 )
                company.save()
                print(f"Company with id({i}) has been seeded.")
