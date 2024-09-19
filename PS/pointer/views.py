from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from datetime import date, datetime
from .models import Timer, Intern

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
    return redirect('login')

@login_required
def pointer(request):
    if request.user.is_staff:
        return redirect('admin_panel')
    intern = request.user.intern
    timer, created = Timer.objects.get_or_create(intern=request.user.intern, date=date.today())

    if request.method == 'POST':
        current_time = timezone.now().time()

        # Check values
        if timer.work_start_morning is None:
            timer.work_start_morning = current_time
        elif timer.work_end_morning is None:
            timer.work_end_morning = current_time
            timer.working_hours += convert_time_to_hours_from_midnight(timer.work_end_morning) - convert_time_to_hours_from_midnight(timer.work_start_morning)
        elif timer.work_start_afternoon is None:
            timer.work_start_afternoon = current_time
        elif timer.work_end_afternoon is None:
            timer.work_end_afternoon = current_time
            timer.working_hours += convert_time_to_hours_from_midnight(timer.work_end_afternoon) - convert_time_to_hours_from_midnight(timer.work_start_afternoon)
        else:
            return HttpResponse('You have already completed the day', status=400)
        timer.save()

    # Set status
    if (timer.work_start_morning is not None and timer.work_end_morning is None) or (timer.work_start_afternoon is not None and timer.work_end_afternoon is None):
        intern.is_active = True
    else:
        intern.is_active = False
    intern.save()

    context = {
        'name': request.user.first_name,
        'status': intern.is_active,
        'work_start_morning': timer.work_start_morning,
        'work_end_morning': timer.work_end_morning,
        'work_start_afternoon': timer.work_start_afternoon,
        'work_end_afternoon': timer.work_end_afternoon,
    }
    return render(request, 'pointer.html', context)

def convert_time_to_hours_from_midnight(time_field):
    time_obj = datetime.combine(datetime.today(), time_field)
    return (time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second) / 3600
