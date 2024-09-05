from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from planning.models import Event
from pointer.models import Timer

@login_required
def stats(request):
    daysoff = 10
    daysoff_left = daysoff - Event.objects.filter(uname=request.user.username).count()
    content = {
        'username': request.user.username,
        'logtime_today': 8,
        'breaktime_today': 1,
        'lunchtime_today': 1,

        'days_off': daysoff,
        'days_left': daysoff_left,

        'hours_lastweek': 30,
        'hours_lastmonth': 20,
        'breaktime_avg': 1,
    }
    return render(request, 'stats.html', content)
