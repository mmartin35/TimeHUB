# Django
from .models import Event, PublicHolidays
# Python
from datetime import datetime, timedelta

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
def update_or_create_event(event_id, intern, reason, is_half_day, start, end, approbation, comment):
    if event_id == 0:
        event, created = Event.objects.get_or_create(intern=intern)
    else:
        try:
            event = Event.objects.get(pk=event_id)
        except:
            print(f"[ERROR]: Couldnt fetch event data. intern={intern.user.username}, start={start}, end={end}")
            return None

    if created:
        if is_half_day:
            duration = 0.5
            if PublicHolidays.objects.filter(date=start).exists():
                duration = 0
        else:
            duration        = 0
            index           = start
            while index <= end:
                if index.weekday() < 5:
                    duration += 1
                index += timedelta(days=1)
            duration -= PublicHolidays.objects.filter(date__range=[start, end])
        if duration > intern.daysoff_left and reason == 'Congé':
            return None
        elif duration <= 0:
            return None
        elif start > end:
            return None
        elif Event.objects.filter(intern=intern, start_date__lte=end, end_date__gte=start, approbation=1).exists():
            return None
        event.request_date = datetime.now().date()
    event.reason        = reason
    event.is_half_day   = is_half_day
    event.start_date    = start
    event.end_date      = end
    event.approbation   = approbation
    event.comment       = comment
    event.save()
    return event