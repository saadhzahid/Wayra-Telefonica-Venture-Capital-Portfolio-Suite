import random

from django.core.exceptions import ObjectDoesNotExist

from portfolio.models import Company, Investment, Portfolio_Company, Individual
from portfolio.models.investment_model import FOUNDING_ROUNDS, ContractRight
from portfolio.models.investor_model import Investor
from portfolio.seeders import Seeder


class InvestorCompanySeeder(Seeder):
    INVESTOR_COMPANY_COUNT = 5

    def seed(self):
        self._create_investor_companies(self.INVESTOR_COMPANY_COUNT)
        print(f"{Investor.objects.filter(individual__isnull=True).count()} investor companies in the db.\n")

    def _create_investor_companies(self, count):
        for i in range(1, count + 1):
            try:
                Investor.objects.get(id=i)
                print(f"InvestorCompany with id({i}) has already seeded.")
            except ObjectDoesNotExist:
                Investor.objects.create(
                    company=Company.objects.get(id=i),
                    classification=Investor.INVESTOR_TYPES[i],
                )
                print(f"InvestorCompany with id({i}) has been seeded.")


class InvestorIndividualSeeder(Seeder):
    INVESTOR_INDIVIDUAL_COUNT = 5

    def seed(self):
        self._create_investor_companies(self.INVESTOR_INDIVIDUAL_COUNT)
        print(f"{Investor.objects.filter(company__isnull=True).count()} investor companies in the db.\n")

    def _create_investor_companies(self, count):
        for i in range(1, count + 1):
            try:
                Investor.objects.get(id=i + InvestorCompanySeeder.INVESTOR_COMPANY_COUNT)
                print(f"InvestorIndividual with id({i}) has already seeded.")
            except ObjectDoesNotExist:
                Investor.objects.create(
                    individual=Individual.objects.get(id=i),
                    classification=Investor.INVESTOR_TYPES[i],
                )
                print(f"InvestorIndividual with id({i}) has been seeded.")


class InvestmentSeeder(Seeder):
    INVESTMENT_COUNT = 25

    contract_rights = [
        ('Wayra Investment', '25%'),
        ('split on investment', '30/70'),
        ('put-option', 'True'),
        ('current-split', '50/30/20'),
        ('affiliate transfer rights', 'True'),
        ('anti-dilution', 'False'),
        ('liquidation preference', 'None'),
        ('co-sale right', 'True'),
        ('exit', 'None'),
    ]

    def seed(self):
        self._create_investments_for_investor_companies(self.INVESTMENT_COUNT)
        self._create_investments_for_investor_individuals(self.INVESTMENT_COUNT)
        print(f"{Investment.objects.count()} investments in the db.\n")

    def _get_objects_from_models(self, model, index, slice_size):
        random_number_of_object = random.randint(1, slice_size)
        objects = list(
            model.objects.filter(id__in=range(index * slice_size, index * slice_size + random_number_of_object)))
        return objects

    def _create_investments_for_investor_companies(self, count):
        investor_count = 0
        investor_companies = list(Investor.objects.filter(individual__isnull=True))
        for i in range(1, count + 1):
            try:
                Investment.objects.get(id=i)
                print(f"InvestorCompany with id({i}) has already seeded.")
            except ObjectDoesNotExist:
                investment = Investment.objects.create(
                    investor=investor_companies[investor_count],
                    startup=Portfolio_Company.objects.get(wayra_number=f'WN-{i}'),
                    typeOfFoundingRounds=random.choice(FOUNDING_ROUNDS)[1],
                    investmentAmount=random.randint(10_000, 10_000_000),
                    dateInvested=self.faker.date_this_century(),
                )
                rights = set(random.choices(self.contract_rights, k=random.randint(1, len(self.contract_rights))))
                for right, detail in rights:
                    ContractRight.objects.create(
                        investment=investment,
                        right=right,
                        details=detail
                    )

                if random.randint(0, 101) > 30 and investor_count != len(investor_companies) - 1:
                    investor_count += 1

                print(f"Investment with id({i}) has been seeded.")

    def _create_investments_for_investor_individuals(self, count):
        investor_count = 0
        investor_individuals = list(Investor.objects.filter(company__isnull=True))
        for i in range(1, count + 1):
            try:
                Investment.objects.get(id=self.INVESTMENT_COUNT + i)
                print(f"Investment with id({self.INVESTMENT_COUNT + i}) has already seeded.")
            except ObjectDoesNotExist:
                investment = Investment.objects.create(
                    investor=investor_individuals[investor_count],
                    startup=Portfolio_Company.objects.get(wayra_number=f'WN-{i}'),
                    typeOfFoundingRounds=random.choice(FOUNDING_ROUNDS)[1],
                    investmentAmount=random.randint(10_000, 10_000_000),
                    dateInvested=self.faker.date_this_century(),
                )

                rights = set(random.choices(self.contract_rights, k=random.randint(1, len(self.contract_rights))))
                for right, detail in rights:
                    ContractRight.objects.create(
                        investment=investment,
                        right=right,
                        details=detail
                    )
                if random.randint(0, 101) > 30 and investor_count != len(investor_individuals) - 1:
                    investor_count += 1

                print(f"Investment with id({self.INVESTMENT_COUNT + i}) has been seeded.")
