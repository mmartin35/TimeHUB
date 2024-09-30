from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Insert public holidays'

    def handle(self, *args, **options):
