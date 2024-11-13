# Imports
from .forms import CancelEventForm, RequestEventForm
from .models import Event, PublicHolidays
from intern.models import Intern
from PS.calc import *
from planning.handler import *

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from datetime import timedelta

@login_required
def planning(request):
    if request.method == 'POST':
        requestEventForm = RequestEventForm(request.POST)
        if requestEventForm.is_valid():
            start_date      = requestEventForm.cleaned_data['start_date']
            end_date        = requestEventForm.cleaned_data['end_date']
            reason          = requestEventForm.cleaned_data['reason']
            is_half_day     = requestEventForm.cleaned_data['is_half_day']
            if request.user.is_staff:
                intern      = Intern.objects.get(id=requestEventForm.cleaned_data['intern_id'])
                event       = update_or_create_event(0, intern, reason, is_half_day, start_date, end_date, 1, f"Added by {request.user.username}")
                if event.reason == 'Congé':
                    intern.daysoff_left -= event.duration
                    intern.save()
            else:
                intern  = Intern.objects.get(user=request.user.id)
                event   = update_or_create_event(0, intern, reason, is_half_day, start_date, end_date, 0, 'NA')
                if event.reason == 'Congé':
                    intern.daysoff_onhold += event.duration
                    intern.save()

        cancelEventForm = CancelEventForm(request.POST)
        if cancelEventForm.is_valid():
            event_buf   = Event.objects.get(id=cancelEventForm.cleaned_data['event_id'])
            event       = update_or_create_event(event_buf.id, 0, event_buf.reason, 0, event_buf.start_date, event_buf.end_date, 3, event_buf.comment)
            if event.reason == 'Congé':
                intern  = event.intern
                intern.daysoff_left += event.duration
                intern.save()
            return redirect('planning')

    context = {
        'daysoff_left'  : 0 if request.user.is_staff else request.user.intern.daysoff_left,
        'daysoff_onhold': 0 if request.user.is_staff else request.user.intern.daysoff_onhold,
        'intern_list'   : Intern.objects.all() if request.user.is_staff else request.user.intern,
        'event_list'    : Event.objects.all() if request.user.is_staff else Event.objects.filter(intern=request.user.intern),
        'reasons'       : ['Congé', 'Congé de maladie', 'Autre'],
    }
    return render(request, 'planning.html', context)

@login_required
def events_json(request):
    event_list = []
    for holiday in PublicHolidays.objects.all():
        event_list.append({
            'title'             : holiday.name,
            'start'             : holiday.date,
            'end'               : holiday.date,
            'backgroundColor'   : 'orange',
        })
    for event in Event.objects.filter(intern=request.user.intern):
        if event.approbation == 0:
            background_color    = 'blue'
        elif event.approbation == 1:
            background_color    = 'green'
        elif event.approbation == 2 or event.approbation == 3:
            background_color    = 'red'
        event_list.append({
            'title'             : event.reason,
            'start'             : event.start_date,
            'end'               : event.end_date + timedelta(days=1),
            'backgroundColor'   : background_color,
        })
    return JsonResponse(event_list, safe=False)
