# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from datetime import date
from .models import Timer

def logout_view(request):
    logout(request)
    return redirect('login')

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

@login_required
def pointer(request):
    timer, created = Timer.objects.get_or_create(user=request.user, date=date.today())

    # Forms
    if request.method == 'POST':
        current_time = timezone.now().time()
        if timer.work_start_morning is None:
            timer.work_start_morning = current_time
        elif timer.work_end_morning is None:
            timer.work_end_morning = current_time
        elif timer.work_start_afternoon is None:
            timer.work_start_afternoon = current_time
        elif timer.work_end_afternoon is None:
            timer.work_end_afternoon = current_time
        else:
            return HttpResponse('You have already completed the day', status=400)
        timer.save()

        # Check status
        if (timer.work_start_morning is not None and timer.work_end_morning is None) or (timer.work_start_afternoon is not None and timer.work_end_afternoon is None):
            status = 0
        else:
            status = 1
        context = {
            'user': request.user,
            'status': status,
            'work_start_morning': timer.work_start_morning,
            'work_end_morning': timer.work_end_morning,
            'work_start_afternoon': timer.work_start_afternoon,
            'work_end_afternoon': timer.work_end_afternoon,
        }
        return render(request, 'pointer.html', context)
    context = {
        'user': request.user,
    }
    return render(request, 'pointer.html', context)
