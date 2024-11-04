from pointer.models import DailyTimer
from datetime import datetime, timedelta

def validate_event(intern, is_half_day, date, duration):
    intern.daysoff_left -= duration
    intern.save()
    if is_half_day:
        timer, created = DailyTimer.objects.get_or_create(intern=intern, date=date)
        timer.worktime += 4
        timer.save()
    else:
        index = date
        for i in range (int(duration)):
            print(i)
            if index.weekday() >= 5:
                index += timedelta(days=1)
                i -= 1
                continue
            timer, created = DailyTimer.objects.get_or_create(intern=intern, date=index)
            timer.worktime = 8
            timer.save()
            index += timedelta(days=1)
            
def fetch_daysoff(day_gap, x, y, rnd, ratio):
    return (round(day_gap * (x / y), rnd) * ratio / 100)