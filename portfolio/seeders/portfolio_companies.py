import random

from django.core.exceptions import ObjectDoesNotExist

from portfolio.models import Portfolio_Company, Company
from portfolio.seeders import Seeder


class PortfolioCompaniesSeeder(Seeder):
    COMPANIES_COUNT = 25

    def seed(self):
        self._create_portfolio_companies(self.COMPANIES_COUNT)
        print(f"{Portfolio_Company.objects.count()} portfolio companies in the db.\n")

    def _create_portfolio_companies(self, count):
        for i in range(1, count + 1):
            try:
                Portfolio_Company.objects.get(wayra_number=f"WN-{i}")
                print(f"Portfolio_Company with id({i}) has already seeded.")

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

                p_company = Company.objects.create(
                    name=name,
                    company_registration_number=crn,
                    trading_names=trading_name,
                    previous_names=previous_name,
                    registered_address=address,
                    jurisdiction=city,
                    incorporation_date=self.faker.date_this_century(),
                )
                p_company.save()

                portfolio = Portfolio_Company.objects.create(
                    parent_company=p_company,
                    wayra_number=f"WN-{i}"
                )
                portfolio.save()

                print(f"Portfolio_Company with id({i}) has been seeded.")
