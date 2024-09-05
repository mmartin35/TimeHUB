from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta
from .models import Timer

def logout_view(request):
    logout(request)
    return redirect('/login')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('')
        else:
            return HttpResponse('Invalid login', status=401)
    return render(request, 'login.html')

@login_required
def pointer(request):
    today = timezone.now().date()
    timer, created = Timer.objects.get_or_create(uname=request.user.username, date=today)

    if request.method == 'POST':
        if 'toggle_work' in request.POST:
            if timer.work_start_time:
                timer.stop_work()
            else:
                timer.start_work()
            timer.save()

        if 'toggle_lunch' in request.POST:
            if timer.lunch_start_time:
                timer.stop_lunch()
            else:
                timer.start_lunch()
            timer.save()

    current_time = timezone.now()
    work_time = timer.work_time_elapsed
    if timer.work_start_time:
        work_time += current_time - timer.work_start_time

    lunch_time = timer.lunch_time_elapsed
    if timer.lunch_start_time:
        lunch_time += current_time - timer.lunch_start_time


    context = {
        'work_time': work_time,
        'lunch_time': lunch_time,
        'work_timer_active': bool(timer.work_start_time),
        'lunch_timer_active': bool(timer.lunch_start_time),
        'date': today,
    }
    return render(request, 'pointer.html', context)
