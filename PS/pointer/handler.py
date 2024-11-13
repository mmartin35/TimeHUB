# Django
from .models import DailyTimer, ServiceTimer, RequestTimer
from intern.models import Intern

# Python
from typing import Optional
from datetime import datetime, date, time

# External
from PS.data import convert_time_to_hours_from_midnight
from PS.calc import  calculate_worktime

'''
Handles update and creation: timer
Note:
    duration    = 0     -> todays timer
    duration    = 1     -> future timer
    duration    > 1     -> multiple timers
Return:
    timer   = Success
    False   = Error
'''
def update_or_create_timer(intern: Intern, date: date, is_half_day: bool) -> Optional[DailyTimer]:
    timer, created = DailyTimer.objects.get_or_create(intern=intern, date=date)

    if timer.t1 is None:
        timer.t1        = datetime.now().time()
    elif timer.t2 is None:
        timer.t2        = datetime.now().time()
        timer.worktime  += convert_time_to_hours_from_midnight(timer.t2) - convert_time_to_hours_from_midnight(timer.t1)
    elif timer.t3 is None and not is_half_day:
        timer.t3        = datetime.now().time()
    elif timer.t4 is None and not is_half_day:
        timer.t4        = datetime.now().time()
        timer.worktime  += convert_time_to_hours_from_midnight(timer.t4) - convert_time_to_hours_from_midnight(timer.t3)
    else:
        return None
    timer.save()
    return timer

'''
Handles update and creation: service timer
Return:
    service = Success
    None    = Error
'''
def update_or_create_service(service_id: ServiceTimer, intern: Intern, date: date, comment: str) -> Optional[ServiceTimer]:
    if service_id == 0:
        service = ServiceTimer.objects.get_or_create(intern=intern, date=date, t2=None).first()
    else:
        try:
            service = ServiceTimer.objects.get(id=service_id)
        except:
            print(f"[ERROR]: Couldnt fetch service data. intern={intern.user.username}, date={date}")
            return None

    if not service:
        ServiceTimer.objects.create(intern=intern, date=datetime.now().date(), t1=datetime.now().time())
    else:
        service.t2 = datetime.now().time()
    service.comment = comment
    service.save()
    return service

'''
Handles update and creation: request timer
Note:
    approbation = 0     -> requested
    approbation = 1     -> approved
    approbation = 2     -> rejected
Return:
    request = Success
    None    = Error
'''
def update_or_create_request(request_id: int, intern: Intern, date: date, t1: time, t2: time, t3: time, t4: time, approbation: int, comment: str) -> Optional[RequestTimer]:
    if request_id == 0:
        request, created = RequestTimer.objects.get_or_create(intern=intern, date=date)
    else:
        try:
            request = RequestTimer.objects.get(pk=request_id)
            created = False
        except:
            print(f"[ERROR]: Couldnt fetch request data. intern={intern.user.username}, date={date}")
            return None

    if date > datetime.now().date():
        print(f"[ERROR]: Couldnt create request object. date={date}")
        return None
    try:
        timer = DailyTimer.objects.get(intern=intern, date=date)
    except:
        print(f"[ERROR]: Couldnt fetch timer data. intern={intern.user.username} date=({date})")
        return None
    if created:
        request.original_t1 = timer.t1
        request.original_t2 = timer.t2
        request.original_t3 = timer.t3
        request.original_t4 = timer.t4
        request.altered_t1  = t1
        request.altered_t2  = t2
        request.altered_t3  = t3
        request.altered_t4  = t4
    else:
        if approbation == 1:
            timer.worktime              = calculate_worktime(request.altered_t1, request.altered_t2, request.altered_t3, request.altered_t4)
            timer.t1                    = request.altered_t1
            timer.t2                    = request.altered_t2
            timer.t3                    = request.altered_t3
            timer.t4                    = request.altered_t4
            timer.save()
    request.comment     = comment
    request.approbation = approbation
    request.save()
    return request
