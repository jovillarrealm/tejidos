from django.core.management.base import BaseCommand

from amigurumi.factories import PatronFactory


class Command(BaseCommand):
    help = "Seed the database with products"

    def handle(self, *args, **kwargs):
        PatronFactory.create_batch(10)

        self.stdout.write(self.style.SUCCESS("Successfully seeded products"))
