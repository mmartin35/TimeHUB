# Django
from .models import DailyTimer, ServiceTimer, RequestTimer
# Python
from datetime import datetime, timedelta
# External
from PS.data import convert_time_to_hours_from_midnight

'''
Handles update and creation: timer
Note:
    duration    = 0     -> todays timer
    duration    = 1     -> future timer
    duration    > 1     -> multiple timers
Return:
    True    = Success
    False   = Error
'''
def update_or_create_timer(timer_id, intern, date, is_half_day, duration):
    if timer_id == 0:
        timer, created = DailyTimer.objects.get_or_create(intern=intern, date=date)
    else:
        try:
            timer = DailyTimer.objects.get(pk=timer_id)
        except:
            print(f"[ERROR]: Couldnt fetch timer data. intern={intern.user.username}, date={date}")
            return False

    if duration == 0:
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
            return False
        timer.save()
    elif duration == 1:
        if is_half_day:
            timer.worktime += 4
        else:
            timer.worktime = 8
        timer.save()
    else:
        index = date
        for i in range (int(duration)):
            if index.weekday() >= 5:
                index += timedelta(days=1)
                i -= 1
                continue
            update_or_create_timer(0, intern, index, False, 1)
    return True

'''
Handles update and creation: service timer
'''
def update_or_create_service(intern, date, comment):
    service = ServiceTimer.objects.get_or_create(intern=intern, date=date, t2=None).first()

    if not service:
        ServiceTimer.objects.create(intern=intern, date=datetime.now().date(), t1=datetime.now().time())
    else:
        service.t2 = datetime.now().time()
    service.comment = comment
    service.save()
    return True

'''
Handles update and creation: request timer
Note:
    approbation = 0     -> requested
    approbation = 1     -> approved
    approbation = 2     -> rejected
Return:
    True    = Success
    False   = Error
'''
def update_or_create_request(request_id, intern, date, t1, t2, t3, t4, approbation, comment):
    if request_id == 0:
        request, created = RequestTimer.objects.get_or_create(intern=intern, date=date)
    else:
        try:
            request = RequestTimer.objects.get(pk=request_id)
        except:
            print(f"[ERROR]: Couldnt fetch request data. intern={intern.user.username}, date={date}")
            return False

    if date >= datetime.now().date():
        return False
    try:
        timer = DailyTimer.objects.get(intern=intern, date=date)
    except:
        return False
    if created:
        request.comment     = comment
        request.approbation = approbation
        request.original_t1 = timer.t1
        request.original_t2 = timer.t2
        request.original_t3 = timer.t3
        request.original_t4 = timer.t4
        request.altered_t1  = t1
        request.altered_t2  = t2
        request.altered_t3  = t3
        request.altered_t4  = t4
    request.comment = comment
    request.approbation = approbation
    request.save()
    return True