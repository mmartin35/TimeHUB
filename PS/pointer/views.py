# Files
from .forms import RequestDailyTimerForm
from .models import DailyTimer, ServiceTimer, RequestTimer
from planning.models import Event

# Imports
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from datetime import datetime


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
        return redirect('dashboard')
    # Create data
    intern = request.user.intern
    timer, created = DailyTimer.objects.get_or_create(intern=intern, date=datetime.today())

    # Handle POST requests
    if request.method == 'POST':
        current_time = timezone.now().time()
        action = request.POST.get('action')
        if action == 'pointer':
            if timer.t1 is None:
                timer.t1 = current_time
            elif timer.t2 is None: # 5 min delay
                timer.t2 = current_time
                timer.worktime += convert_time_to_hours_from_midnight(timer.t2) - convert_time_to_hours_from_midnight(timer.t1)
            elif timer.t3 is None:
                timer.t3 = current_time
            elif timer.t4 is None:
                timer.t4 = current_time
                timer.worktime += convert_time_to_hours_from_midnight(timer.t4) - convert_time_to_hours_from_midnight(timer.t3)
            else:
                return HttpResponse('You have already completed the day', status=400)
            timer.save()
        if action == 'service':
            unpaired_service = ServiceTimer.objects.filter(intern=intern, date=datetime.today(), t2=None).first()
            if not unpaired_service:
                ServiceTimer.objects.create(intern=intern, date=datetime.today(), t1=current_time)
            else:
                unpaired_service.t2 = current_time
                unpaired_service.save()

        requestDailyTimerForm = RequestDailyTimerForm(request.POST)
        if requestDailyTimerForm.is_valid():
            date_edit = requestDailyTimerForm.cleaned_data['date']
            timer_edit = DailyTimer.objects.get(intern=intern, date=date_edit)
            RequestTimer.objects.create(
                intern=intern,
                date=date_edit,
                comment=requestDailyTimerForm.cleaned_data['comment'],

                original_t1=timer_edit.t1,
                original_t2=timer_edit.t2,
                original_t3=timer_edit.t3,
                original_t4=timer_edit.t4,

                altered_t1=requestDailyTimerForm.cleaned_data['t1'],
                altered_t2=requestDailyTimerForm.cleaned_data['t2'],
                altered_t3=requestDailyTimerForm.cleaned_data['t3'],
                altered_t4=requestDailyTimerForm.cleaned_data['t4']
            )

    # STATUS CHECK
    if (timer.t1 is not None and timer.t2 is None) or (timer.t3 is not None and timer.t4 is None):
        intern.is_active = True
    else:
        intern.is_active = False
    intern.save()
    alert_list = []
    context = {
        # General variables
        'name': request.user.first_name,
        # Specific variables
        'status': intern.is_active,
        'timer': timer,
        'is_half_day': Event.objects.filter(start_date__lte=datetime.today(), end_date__gte=datetime.today(), intern=intern, approbation=1).exists(),
        'service_state': ServiceTimer.objects.filter(intern=intern, date=datetime.today(), t2=None).exists(),
        # Lists
        'service_list': ServiceTimer.objects.filter(intern=intern),
        'request_list': RequestTimer.objects.filter(intern=intern, approbation=0),
        'alert_list': alert_list,
    }
    return render(request, 'pointer.html', context)

def convert_time_to_hours_from_midnight(time_field):
    time_obj = datetime.combine(datetime.today(), time_field)
    return (time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second) / 3600
