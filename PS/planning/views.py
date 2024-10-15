# Files
from .forms import CancelEventForm, RequestEventForm
from .models import Event, PublicHolidays
from intern.models import Intern

# Imports
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse

@login_required
def planning(request):
    if request.method == 'POST':
        requestEventForm = RequestEventForm(request.POST)
        print(requestEventForm.errors)
        if requestEventForm.is_valid():
            intern = Intern.objects.get(pk=requestEventForm.cleaned_data['intern_id'])
            start_date = requestEventForm.cleaned_data['start_date']
            end_date = requestEventForm.cleaned_data['end_date']
            reason = requestEventForm.cleaned_data['reason']
            is_half_day = requestEventForm.cleaned_data['is_half_day']
            duration = 0
            if start_date == end_date and is_half_day:
                duration = 0.5
            else:
                duration = (end_date - start_date).days
            # Check values
            if start_date > end_date:
                return HttpResponse('Start date cannot be after end date', status=401)
            if duration > intern.daysoff_left:
                return HttpResponse('Requested time off exceeds the remaining days off', status=401)
            if start_date < start_date.today():
                return HttpResponse('Start date cannot be in the past', status=401)
            if Event.objects.filter(intern=intern, start_date__lte=end_date, end_date__gte=start_date, approbation=1).exists():
                return HttpResponse('An event already exists within the selected date range', status=401)
            if PublicHolidays.objects.filter(date__range=[start_date, end_date]).exists():
                duration -= PublicHolidays.objects.filter(date__range=[start_date, end_date]).count()
            if duration < 0:
                return HttpResponse('The selected date range is during public holidays', status=401)

           # Create event
            intern.daysoff_onhold += duration
            if request.user.is_staff:
                approbation = 1
            else:
                approbation = 0
            intern.daysoff_left -= duration
            intern.daysoff_onhold -= duration
            intern.save()
            Event.objects.create(
                intern=intern,
                reason=reason,
                start_date=start_date,
                end_date=end_date,
                duration=duration,
                is_half_day=is_half_day,
                approbation=approbation,
            )
        
        cancelEventForm = CancelEventForm(request.POST)
        if cancelEventForm.is_valid():
            event = Event.objects.get(pk=cancelEventForm.cleaned_data['event_id'])
            intern = event.intern
            intern.daysoff_left += event.duration
            event.approbation = 3
            intern.save()
            event.save()
        return redirect('planning')

    else:
        eventForm = RequestEventForm()

    if request.user.is_staff:
        intern_list = Intern.objects.all()
        event_list = Event.objects.all()
        daysoff_left = 0
        daysoff_onhold = 0
    else:
        intern_list = request.user.intern
        event_list = Event.objects.filter(intern=intern_list)
        daysoff_left = intern_list.daysoff_left
        daysoff_onhold = intern_list.daysoff_onhold

    context = {
        # General variables
        'name': request.user.first_name,
        # Specific variables
        'form': eventForm,
        'daysoff_left': daysoff_left,
        'daysoff_onhold': daysoff_onhold,
        # Lists
        'intern_list': intern_list,
        'event_list': event_list[::-1],
        'reasons': ['Congé', 'Congé de maladie', 'Autre'],
    }
    return render(request, 'planning.html', context)

@login_required
def events_json(request):
    events = Event.objects.filter(intern=request.user.intern)
    event_list = []
    for event in events:
        if event.approbation == 0:
            background_color = 'blue'
        elif event.approbation == 1:
            background_color = 'green'
        elif event.approbation == 2 or event.approbation == 3:
            background_color = 'red'
        event_list.append({
            'title': event.reason,
            'start': event.start_date,
            'end': event.end_date,
            'backgroundColor': background_color,
        })
    return JsonResponse(event_list, safe=False)
