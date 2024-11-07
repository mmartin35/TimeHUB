from pointer.models import DailyTimer
from PS.calc import calculate_worktime
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Recalculate hours'

    def handle(self, *args, **options):
        for timer in DailyTimer.objects.all():
            timer.worktime = calculate_worktime(timer.t1, timer.t2, timer.t3, timer.t4)
            print(f"Timer {timer} processed. worktime=({timer.worktime})")
            timer.save()
