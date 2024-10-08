from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from datetime import date, datetime
from .models import Timer, ServiceTimer
from planning.models import Event

def login_view(request):
    if request.user.is_authenticated:
        return redirect('pointer')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('pointer')
        else:
            return HttpResponse('Invalid login', status=401)
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('logout')

@login_required
def pointer(request):
    if request.user.is_staff:
        return redirect('admin_panel')
    
    intern = request.user.intern
    timer, created = Timer.objects.get_or_create(intern=intern, date=date.today())
    
    if request.method == 'POST':
        current_time = timezone.now().time()

        # Handling the pointer form (T1-T4)
        if 'action' in request.POST:
            if timer.t1 is None:
                timer.t1 = current_time
            elif timer.t2 is None:
                timer.t2 = current_time
                timer.working_hours += convert_time_to_hours_from_midnight(timer.t2) - convert_time_to_hours_from_midnight(timer.t1)
            elif timer.t3 is None:
                timer.t3 = current_time
            elif timer.t4 is None:
                timer.t4 = current_time
                timer.working_hours += convert_time_to_hours_from_midnight(timer.t4) - convert_time_to_hours_from_midnight(timer.t3)
            else:
                return HttpResponse('You have already completed the day', status=400)
            timer.save()

        # Handling the service form (leave and back)
        elif 'service' in request.POST:
            # Check for an unpaired 't1_service' (leave)
            unpaired_service = ServiceTimer.objects.filter(intern=intern, date=date.today(), t2_service=None).first()

            if 'service' in request.POST:
                if not unpaired_service:
                    ServiceTimer.objects.create(intern=intern, date=date.today(), t1_service=current_time)
                else:
                    unpaired_service.t2_service = current_time
                    unpaired_service.save()

    # STATUS CHECK
    if (timer.t1 is not None and timer.t2 is None) or (timer.t3 is not None and timer.t4 is None):
        intern.is_active = True
    else:
        intern.is_active = False
    intern.save()

    # Check for half or full day events
    half_day = False
    full_day = False
    events = Event.objects.filter(start_date__lte=date.today(), end_date__gte=date.today(), intern=intern, approbation=1)
    if events.exists():
        half_day = events.filter(half_day='1').exists()
    else:
        full_day = True

    service_state = ServiceTimer.objects.filter(intern=intern, date=date.today(), t2_service=None).exists()

    # ALERTS
    show_days_off_alert = (intern.mandatory_hours - intern.total_hours) <= 3 * intern.days_off_left

    context = {
        'name': request.user.first_name,
        'status': intern.is_active,
        't1': timer.t1,
        't2': timer.t2,
        't3': timer.t3,
        't4': timer.t4,
        'half_day': half_day,
        'full_day': full_day,
        'service_state': service_state,
        'show_days_off_alert': show_days_off_alert,
    }
    return render(request, 'pointer.html', context)

def convert_time_to_hours_from_midnight(time_field):
    time_obj = datetime.combine(datetime.today(), time_field)
    return (time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second) / 3600
