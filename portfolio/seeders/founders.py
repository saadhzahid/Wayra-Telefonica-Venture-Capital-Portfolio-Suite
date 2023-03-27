from portfolio.models import Founder, Company, Individual
from portfolio.seeders import Seeder


class FounderSeeder(Seeder):
    FOUNDER_COUNT = 10

    def seed(self):
        self._populate_founders(self.FOUNDER_COUNT)
        print(f"{Founder.objects.count()} founders in the db.\n")

    def _populate_founders(self, count):
        """Seeder for fake founders"""

        print('seeding founders...')
        for i in range(1, count + 1):

            if Founder.objects.filter(id=i).exists():
                print(f"Founder with the id({i}) is already seeded.")
                continue

            if not Company.objects.filter(id=i).exists() and not Individual.objects.filter(id=i).exists():
                print(f"Company or individual with the id({i}) does not exist.")
                continue

            founder = Founder.objects.create(
                companyFounded=Company.objects.get(id=i),
                individualFounder=Individual.objects.get(id=i),
            )
            founder.save()
            print(F"Founders with id({founder.id}) has been seeded.")
