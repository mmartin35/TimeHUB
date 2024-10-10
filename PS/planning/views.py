from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from .forms import EventForm, CancelEventForm
from .models import Event, PublicHolidays, Intern

@login_required
def planning(request):
    if request.method == 'POST':
        eventForm = EventForm(request.POST)
        if eventForm.is_valid():
            intern = Intern.objects.get(pk=eventForm.cleaned_data['intern'])
            start_date = eventForm.cleaned_data['start_date']
            end_date = eventForm.cleaned_data['end_date']
            reason = eventForm.cleaned_data['reason']
            half_day = eventForm.cleaned_data['half_day']
            duration = 0
            if start_date == end_date and half_day != 0:
                duration = 0.5
            else:
                duration = (end_date - start_date).days

            # Check values
            if start_date > end_date:
                return HttpResponse('Start date cannot be after end date', status=401)
            if duration > intern.days_off_left:
                return HttpResponse('Requested time off exceeds the remaining days off', status=401)
            if start_date < start_date.today():
                return HttpResponse('Start date cannot be in the past', status=401)
            existing_events = Event.objects.filter(intern=intern, start_date__lte=end_date, end_date__gte=start_date, approbation__in=[1])
            if existing_events.exists():
                return HttpResponse('An event already exists within the selected date range', status=401)
            if PublicHolidays.objects.filter(date__range=[start_date, end_date]).exists():
                duration -= PublicHolidays.objects.filter(date__range=[start_date, end_date]).count()
            if duration < 0:
                return HttpResponse('The selected date range is during public holidays', status=401)
            # Assign values
            intern.days_off_onhold += duration
            intern.save()

            # Create event
            if request.user.is_staff:
                approbation = 1
                intern.days_off_left -= duration
                intern.days_off_onhold -= duration
            else:
                approbation = 0
            Event.objects.create(
                intern=intern,
                reason=reason,
                start_date=start_date,
                end_date=end_date,
                duration=duration,
                half_day=half_day,
                approbation=approbation,
            )
            return redirect('planning')
        cancelForm = CancelEventForm(request.POST)
        if cancelForm.is_valid():
            print("cancelForm is valid")
            event = Event.objects.get(pk=cancelForm.cleaned_data['cancel_event'])
            intern = event.intern
            intern.days_off_left += event.duration
            event.approbation = 3
            intern.save()
            event.save()
            return redirect('planning')
    else:
        eventForm = EventForm()

    reasons = ['Congé', 'Congé de maladie', 'Autre']
    if request.user.is_staff:
        interns = Intern.objects.all()
        responses = Event.objects.filter(approbation__in=[1, 2, 3])
        ongoings = Event.objects.filter(approbation=0)
        days_off_left = 0
        days_off_onhold = 0
    else:
        interns = request.user.intern
        responses = Event.objects.filter(intern=interns, approbation__in=[1, 2, 3])
        ongoings = Event.objects.filter(intern=interns, approbation=0)
        days_off_left = interns.days_off_left
        days_off_onhold = interns.days_off_onhold

    context = {
        'form': eventForm,
        'name': request.user.first_name,
        'interns': interns,
        'reasons': reasons,
        'days_off_left': days_off_left,
        'days_off_onhold': days_off_onhold,
        'responses': responses[::-1],
        'ongoings': ongoings[::-1],
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
