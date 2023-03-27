import random
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.uploadedfile import SimpleUploadedFile
from portfolio.models import Document, Company, Individual, Programme
from portfolio.seeders import Seeder


class DocumentSeeder(Seeder):
    """A seeder for documents."""

    # The number of documents to seed per company, individual or programme (not evenly distributed between entities).
    DOCUMENT_COUNT = 6
    # The number of companies in the db.
    COMPANY_COUNT = 0
    # The number of individuals in the db.
    INDIVIDUAL_COUNT = 0
    # The number of programmes in the db.
    PROGRAMME_COUNT = 0

    def seed(self):
        # Get the number of companies, individuals and programmes in the db.
        self.COMPANY_COUNT = Company.objects.count()
        self.INDIVIDUAL_COUNT = Individual.objects.count()
        self.PROGRAMME_COUNT = Programme.objects.count()

        # Seed documents if there are companies, individuals and programmes in the db.
        if self.COMPANY_COUNT and self.INDIVIDUAL_COUNT and self.PROGRAMME_COUNT:
            total_count = self.DOCUMENT_COUNT * self.COMPANY_COUNT + self.DOCUMENT_COUNT * self.INDIVIDUAL_COUNT + self.DOCUMENT_COUNT * self.PROGRAMME_COUNT
            self._create_documents(total_count)
            print(f"{Document.objects.count()} documents in the db.\n")
        else:
            print(f"Couldn't seed documents. Seed companies, individuals and programmes first.")

    def _create_documents(self, count):
        for i in range(1, count + 1):
            try:
                Document.objects.get(file_id=i)
                print(f"Document with the id {i} is already seeded.")

            except ObjectDoesNotExist:
                is_file = random.choice([True, False])
                foreign_model = random.choice(["company", "individual", "programme"])

                name = self.faker.file_name(category=None)

                # Ensure the file name is unique.
                while Document.objects.filter(file_name=name).exists():
                    name = self.faker.file_name(category=None)

                extension = name.split(".")[-1]

                if is_file:
                    if foreign_model == "company":
                        company_id = random.randint(1, self.COMPANY_COUNT)
                        document = Document.objects.create(
                            file_name=f"{name}",
                            file_type=extension,
                            company=Company.objects.get(id=company_id),
                            individual=None,
                            programme=None,
                            file=SimpleUploadedFile(f"{name}", b"file contents")
                        )
                    elif foreign_model == "individual":
                        individual_id = random.randint(1, self.INDIVIDUAL_COUNT)
                        document = Document.objects.create(
                            file_name=f"{name}",
                            file_type=extension,
                            company=None,
                            individual=Individual.objects.get(id=individual_id),
                            programme=None,
                            file=SimpleUploadedFile(f"{name}", b"file contents")
                        )
                    elif foreign_model == "programme":
                        programme_id = random.randint(1, self.PROGRAMME_COUNT)
                        document = Document.objects.create(
                            file_name=f"{name}",
                            file_type=extension,
                            company=None,
                            individual=None,
                            programme=Programme.objects.get(id=programme_id),
                            file=SimpleUploadedFile(f"{name}", b"file contents")
                        )
                    else:
                        raise ValueError("Associated model must be a company, individual or programme.")
                else:
                    if foreign_model == "company":
                        company_id = random.randint(1, self.COMPANY_COUNT)
                        document = Document.objects.create(
                            file_name=f"{name}",
                            file_type="URL",
                            company=Company.objects.get(id=company_id),
                            individual=None,
                            programme=None,
                            url="https://www.wayra.uk"
                        )
                    elif foreign_model == "individual":
                        individual_id = random.randint(1, self.INDIVIDUAL_COUNT)
                        document = Document.objects.create(
                            file_name=f"{name}",
                            file_type="URL",
                            company=None,
                            individual=Individual.objects.get(id=individual_id),
                            programme=None,
                            url="https://www.wayra.uk"
                        )
                    elif foreign_model == "programme":
                        programme_id = random.randint(1, self.PROGRAMME_COUNT)
                        document = Document.objects.create(
                            file_name=f"{name}",
                            file_type="URL",
                            company=None,
                            individual=None,
                            programme=Programme.objects.get(id=programme_id),
                            url="https://www.wayra.uk"
                        )
                    else:
                        raise ValueError("Associated model must be a company, individual or programme.")

                document.save()
                print(f"The document with the id {i} has been seeded.")
