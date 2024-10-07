from django.core.management.base import BaseCommand
from datetime import datetime

class Command(BaseCommand):
    help = 'Insert public holidays'

    def handle(self, *args, **options):
        from datetime import date
        from planning.models import PublicHolidays

        holidays = [
            {'name': 'Nouvel an', 'date': date(datetime.now().year, 1, 1)},
            {'name': 'Lundi de Paques', 'date': date(datetime.now().year, 4, 1)},
            {'name': 'Premier Mai', 'date': date(datetime.now().year, 5, 1)},
            {'name': 'Ascension', 'date': date(datetime.now().year, 5, 9)},
            {'name': 'Journee de l Europe', 'date': date(datetime.now().year, 5, 9)},
            {'name': 'Lundi de Pentecote', 'date': date(datetime.now().year, 5, 20)},
            {'name': 'Fete Nationale', 'date': date(datetime.now().year, 6, 23)},
            {'name': 'Assomption', 'date': date(datetime.now().year, 8, 15)},
            {'name': 'Toussaint', 'date': date(datetime.now().year, 11, 1)},
            {'name': 'Noel', 'date': date(datetime.now().year, 12, 25)},
            {'name': 'Deuxieme jour de Noel', 'date': date(datetime.now().year, 12, 26)}
        ]

        for holiday in holidays:
            PublicHolidays.objects.create(name=holiday['name'], date=holiday['date'])
            print(f'{holiday["name"]} on {holiday["date"]} inserted')