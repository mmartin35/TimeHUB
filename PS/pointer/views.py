# Files
from .forms import RequestDailyTimerForm
from .models import DailyTimer, ServiceTimer, RequestTimer
from planning.models import Event
from admin_panel.views import structure_data, convert_time_to_hours_from_midnight

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
    url                                 = 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=' + settings.CLIENT_ID + '&response_type=code&redirect_uri=' + settings.REDIRECT_URI + '&response_mode=query&scope=openid+profile+User.Read&state=random_string_for_csrf'
    return redirect(url)

def callback(request):
    code                                =  request.GET.get('code')
    if not code:
        return HttpResponse('Authorization failed', status=400)
    url                                 = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
    data = {
        'client_id'                     : settings.CLIENT_ID,
        'client_secret'                 : settings.CLIENT_SECRET,
        'code'                          : code,
        'redirect_uri'                  : settings.ABSOLUTE_URI,
        'grant_type'                    : 'authorization_code',
    }
    response                            = requests.get(url, data=data)
    if response.status_code == 200:
        user_info_url                   = 'https://graph.microsoft.com/v1.0/me'
        token_info                      = response.json()
        access_token                    = token_info.get('access_token')
        headers                         = {'Authorization': f'Bearer {access_token}'}
        user_info_response              = requests.get(user_info_url, headers=headers)
        user_info                       = user_info_response.json()
        mail                            = user_info.get('mail')
        cleaned_mail                    = mail.lower()
        user                            = User.objects.get(username=cleaned_mail)
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
    intern                              = request.user.intern
    timer, created                      = DailyTimer.objects.get_or_create(intern=intern, date=datetime.today())

    # Handle POST requests
    if request.method == 'POST':
        current_time                    = timezone.now().time()
        action                          = request.POST.get('action')
        if action == 'pointer':
            if timer.t1 is None:
                timer.t1                = current_time
            elif timer.t2 is None:
                timer.t2                = current_time
                timer.worktime          += convert_time_to_hours_from_midnight(timer.t2) - convert_time_to_hours_from_midnight(timer.t1)
            elif timer.t3 is None:
                timer.t3                = current_time
            elif timer.t4 is None:
                timer.t4                = current_time
                timer.worktime          += convert_time_to_hours_from_midnight(timer.t4) - convert_time_to_hours_from_midnight(timer.t3)
            else:
                return HttpResponse('You have already completed the day', status=400)
            timer.save()
        if action == 'service':
            unpaired_service            = ServiceTimer.objects.filter(intern=intern, date=datetime.today(), t2=None).first()
            if not unpaired_service:
                ServiceTimer.objects.create(intern=intern, date=datetime.today(), t1=current_time)
            else:
                unpaired_service.t2     = current_time
                unpaired_service.save()

        requestDailyTimerForm           = RequestDailyTimerForm(request.POST)
        if requestDailyTimerForm.is_valid():
            date_edit                   = requestDailyTimerForm.cleaned_data['date']
            current_time                = datetime.now()
            if date_edit >= current_time.date():
                return HttpResponse('You can only request for a correction at most the day after.', status=400)
            try:
                DailyTimer.objects.get(intern=intern, date=date_edit)
            except:
                DailyTimer.objects.create(
                    intern              = intern,
                    date                = date_edit,

                    t1                  = None,
                    t2                  = None,
                    t3                  = None,
                    t4                  = None
                )
            timer_edit                  = DailyTimer.objects.get(intern=intern, date=date_edit)
            RequestTimer.objects.create(
                intern                  = intern,
                date                    = date_edit,
                comment                 = requestDailyTimerForm.cleaned_data['comment'],

                original_t1             = timer_edit.t1,
                original_t2             = timer_edit.t2,
                original_t3             = timer_edit.t3,
                original_t4             = timer_edit.t4,

                altered_t1              = requestDailyTimerForm.cleaned_data['t1'],
                altered_t2              = requestDailyTimerForm.cleaned_data['t2'],
                altered_t3              = requestDailyTimerForm.cleaned_data['t3'],
                altered_t4              = requestDailyTimerForm.cleaned_data['t4'],
            )

    # STATUS CHECK
    if (timer.t1 is not None and timer.t2 is None) or (timer.t3 is not None and timer.t4 is None):
        intern.is_active                = True
    else:
        intern.is_active                = False
    intern.save()
    alert_list                          = []
    intern_weeks_data = structure_data(request, intern.id).weeks
    week_number = datetime.now().isocalendar()[1]
    context = {
        # General variables
        'name'                          : request.user.username,
        # Specific variables
        'status'                        : intern.is_active,
        'timer'                         : timer,
        'is_half_day'                   : Event.objects.filter(start_date__lte=datetime.today(), end_date__gte=datetime.today(), intern=intern, approbation=1).exists(),
        'service_state'                 : ServiceTimer.objects.filter(intern=intern, date=datetime.today(), t2=None).exists(),
        # Lists
        'intern_last_week_data'         : intern_weeks_data[week_number],
        'week'                          : week_number,
        'service_list'                  : ServiceTimer.objects.filter(intern=intern),
        'request_list'                  : RequestTimer.objects.filter(intern=intern, approbation=0),
        'alert_list'                    : alert_list,
    }
    return render(request, 'pointer.html', context)