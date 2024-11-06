# Files
from .forms import RequestDailyTimerForm
from .models import DailyTimer, ServiceTimer, RequestTimer
from planning.models import Event
from admin_panel.views import structure_data
from pointer.handler import *

# Imports
import requests
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from datetime import datetime

def login_view(request):
    if request.user.is_authenticated:
        redirect('pointer')
    return render(request, 'login.html')

def login_allauth(request):
    url = f"https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id={settings.CLIENT_ID}&response_type=code&redirect_uri={settings.REDIRECT_URI}&response_mode=query&scope=openid+profile+User.Read&state=random_string_for_csrf"
    return redirect(url)

def callback(request):
    code = request.GET.get('code')
    if not code:
        return HttpResponse('Authorization failed', status=400)
    url  = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
    data = {
        'client_id'     : settings.CLIENT_ID,
        'client_secret' : settings.CLIENT_SECRET,
        'code'          : code,
        'redirect_uri'  : settings.ABSOLUTE_URI,
        'grant_type'    : 'authorization_code',
    }
    response = requests.get(url, data=data)
    if response.status_code == 200:
        user_info_url       = 'https://graph.microsoft.com/v1.0/me'
        token_info          = response.json()
        access_token        = token_info.get('access_token')
        headers             = {'Authorization': f'Bearer {access_token}'}
        user_info_response  = requests.get(user_info_url, headers=headers)
        user_info           = user_info_response.json()
        mail                = user_info.get('mail')
        cleaned_mail        = mail.lower()
        user                = User.objects.get(username=cleaned_mail)
        if user is not None:
            login(request, user)
            return redirect('pointer')
        else:
            return HttpResponse('Your credentials has not been found', status=400)
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def pointer(request):
    if request.user.is_staff:
        return redirect('dashboard')
    # Create data
    intern = request.user.intern

    # Handle POST requests
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'pointer':
            update_or_create_timer(0, intern, datetime.now().date(), Event.objects.filter(start_date__lte=datetime.now().date(), end_date__gte=datetime.now().date(), intern=intern, approbation=1).exists(), 0)
        if action == 'service':
            update_or_create_service(0, intern, datetime.now().date(), 'NA')

        requestDailyTimerForm = RequestDailyTimerForm(request.POST)
        if requestDailyTimerForm.is_valid():
            date    = requestDailyTimerForm.cleaned_data['date']
            t1      = requestDailyTimerForm.cleaned_data['t1']
            t2      = requestDailyTimerForm.cleaned_data['t2']
            t3      = requestDailyTimerForm.cleaned_data['t3']
            t4      = requestDailyTimerForm.cleaned_data['t4']
            update_or_create_request(0, intern, date, t1, t2, t3, t4, 0, 'NA')
    try:
        timer = DailyTimer.objects.get(intern=intern, date=datetime.now().date())
    except :
        timer = DailyTimer(intern=intern, date=datetime.now().date(), t1=None, t2=None, t3=None, t4=None)
    if (timer.t1 is not None and timer.t2 is None) or (timer.t3 is not None and timer.t4 is None):
        intern.is_active = True
    else:
        intern.is_active = False
    intern.save()

    context = {
        'status'                        : intern.is_active,
        'timer'                         : timer,
        'week'                          : datetime.now().isocalendar()[1],
        'is_half_day'                   : Event.objects.filter(start_date__lte=datetime.today(), end_date__gte=datetime.today(), intern=intern, approbation=1).exists(),
        'service_state'                 : ServiceTimer.objects.filter(intern=intern, date=datetime.today(), t2=None).exists(),
        'intern_last_week_data'         : structure_data(intern.id).weeks[datetime.now().isocalendar()[1]],
        
        'service_list'                  : ServiceTimer.objects.filter(intern=intern),
        'request_list'                  : RequestTimer.objects.filter(intern=intern, approbation=0),
        'alert_list'                    : [],
    }
    return render(request, 'pointer.html', context)