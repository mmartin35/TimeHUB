# Django
from .models import Event, PublicHolidays
from intern.models import Intern
# Python
from typing import Optional
from datetime import datetime, timedelta, date

'''
Handles update and creation: event
Note:
    approbation = 0     -> requested
    approbation = 1     -> approved
    approbation = 2     -> rejected
    approbation = 3     -> cancelled
Return:
    event   = Success
    None    = Error
'''
def update_or_create_event(event_id: int, intern: Intern, reason: str, is_half_day: bool, start: date, end: date, approbation: int, comment: str) -> Optional[Event]:
    if event_id == 0:
        event, created = Event.objects.get_or_create(intern=intern, start_date=start, end_date=end, comment=comment)
    else:
        try:
            event   = Event.objects.get(pk=event_id)
            created = False
        except:
            print(f"[ERROR]: Couldnt fetch event data. intern={intern.user.username}, start={start}, end={end}")
            return None

    if created:
        duration = 0
        if is_half_day:
            if start.weekday() < 5:
                duration = 0.5
        else:
            index = start
            while index <= end:
                if index.weekday() < 5:
                    duration += 1
                index += timedelta(days=1)
        holidays_count = PublicHolidays.objects.filter(date__range=[start, end]).count()
        duration -= holidays_count
        if duration > intern.daysoff_left and reason == 'Congé':
            print(f"[ERROR]: Couldnt create event object. duration({duration}) > days left({intern})")
            return None
        elif duration < 0.5:
            print(f"[ERROR]: Couldnt create event object. duration({duration}) <= 0")
            return None
        elif start > end:
            print(f"[ERROR]: Couldnt create event object. start({start}) > end({end})")
            return None
        elif Event.objects.filter(intern=intern, start_date__lte=end, end_date__gte=start, approbation=1).exists():
            print(f"[ERROR]: Couldnt create event object. date({start}-{end}) already exists")
            return None
        event.request_date  = datetime.now().date()
        event.duration      = duration
    event.reason        = reason
    event.start_date    = start
    event.end_date      = end
    event.approbation   = approbation
    event.comment       = comment
    event.save()
    return event
