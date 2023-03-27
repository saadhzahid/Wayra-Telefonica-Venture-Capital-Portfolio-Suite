import os
import shutil

from django.core.management import BaseCommand

from vcpms.settings import BASE_DIR, MEDIA_ROOT


class Command(BaseCommand):
    """Removes all data from the database and media directory."""

    def handle(self, *args, **options):
        # Warn the user of the potential data loss.
        unseed = True if input("This will delete all stored data. Proceed? (y/n)\n").lower() == "y" else False

        if unseed:
            try:
                # Remove all data within the database.
                os.remove(os.path.join(BASE_DIR, "db.sqlite3"))

                # Remove all files within the media directory.
                shutil.rmtree(MEDIA_ROOT)
                os.mkdir(MEDIA_ROOT)
                print("Unseeding complete. Migrating database...")

            except FileNotFoundError as e:
                print(f"Unseeding failed with error: {e}")

            try:
                # Migrate the database.
                os.system("python3 manage.py migrate")
                print("Database migrated.")

            except Exception as e:
                print(f"Database migration failed with error: {e}\nPlease migrate the database manually.")

        else:
            print("Unseeding cancelled.")
