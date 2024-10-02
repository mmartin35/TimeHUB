from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Insert public holidays'

    def handle(self, *args, **options):
        from datetime import date
        from planning.models import PublicHolidays

        holidays = [
            {'name': 'Nouvel an', 'date': date(2021, 1, 1)},
            {'name': 'Lundi de Paques', 'date': date(2021, 4, 1)},
            {'name': 'Premier Mai', 'date': date(2021, 5, 1)},
            {'name': 'Ascension', 'date': date(2021, 5, 9)},
            {'name': 'Journee de l Europe', 'date': date(2024, 5, 9)},
            {'name': 'Lundi de Pentecote', 'date': date(2024, 5, 20)},
            {'name': 'Fete Nationale', 'date': date(2024, 6, 23)},
            {'name': 'Assomption', 'date': date(2024, 8, 15)},
            {'name': 'Toussaint', 'date': date(2024, 11, 1)},
            {'name': 'Noel', 'date': date(2024, 12, 25)},
            {'name': 'Deuxieme jour de Noel', 'date': date(2024, 12, 26)}
        ]

        for holiday in holidays:
            PublicHolidays.objects.create(name=holiday.name, date=holiday.date