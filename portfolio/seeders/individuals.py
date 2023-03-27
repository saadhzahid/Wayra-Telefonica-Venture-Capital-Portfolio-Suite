from portfolio.models import Individual, ResidentialAddress
from portfolio.seeders import Seeder


class IndividualSeeder(Seeder):
    INDIVIDUAL_COUNT = 25

    def seed(self):
        self._populate_individuals(self.INDIVIDUAL_COUNT)
        print(f"{Individual.objects.count()} individuals in the db.\n")

    def _populate_individuals(self, count):
        """Seeder for fake individuals"""
        print('seeding individuals...')
        for i in range(1, count + 1):
            name = self.faker.name()
            company = self.faker.company()
            position = self.faker.job()
            email = self.faker.email()
            primary_phone_number = self.faker.phone_number()
            secondary_phone_number = self.faker.phone_number()

            individual = Individual.objects.create(
                name=name,
                AngelListLink="https://www.AngelList.com",
                CrunchbaseLink="https://www.Crunchbase.com",
                LinkedInLink="https://www.LinkedIn.com",
                Company=company,
                Position=position,
                Email=email,
                PrimaryNumber=primary_phone_number,
                SecondaryNumber=secondary_phone_number
            )
            individual.save()

            address1 = self.faker.building_number()
            address2 = self.faker.street_address()
            city = self.faker.city()
            postcode = self.faker.postcode()
            state = self.faker.country_code()
            country = self.faker.country()
            addr = ResidentialAddress.objects.create(
                address_line1=address1,
                address_line2=address2,
                postal_code=postcode,
                city=city,
                state=state,
                country=country,
                individual=individual
            )
            addr.save()
