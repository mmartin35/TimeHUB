# Django
from intern.models import Intern
from pointer.models import DailyTimer, ServiceTimer
# Python
from datetime import datetime, time

'''
Global update: Database content
'''
def update_data():
    # service timers
    for service in ServiceTimer.objects.all():
        if service.t2 is None and service.date < datetime.now().date():
            service.t2 = "19:30:00"
        service.save()

    # intern status
    for intern in Intern.objects.all():
        if datetime.now().date() <= intern.departure and datetime.now().date() >= intern.arrival:
            intern.is_ongoing = True
        else:
            intern.is_ongoing = False
        intern.save()
    return True

'''
Structure: Database content
'''
def structure_data(intern_id: int):
    class Intern_item:
        def __init__(self):
            self.months = {month: [] for month in range(1, 13)}
            self.weeks  = {week: [] for week in range(1, 54)}
    intern_data = Intern_item()    
    for timer in DailyTimer.objects.filter(intern=intern_id):
        if datetime.now().year != timer.date.year:
            continue
        intern_data.months[timer.date.month].append(timer)
        intern_data.weeks[timer.date.isocalendar()[1]].append(timer)
    return intern_data

'''
Convert: Time to hours
'''
def convert_time_to_hours_from_midnight(time_field: time):
    time_obj = datetime.combine(datetime.today(), time_field)
    return (time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second) / 3600
