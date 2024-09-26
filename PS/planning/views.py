from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from .forms import EventForm
from .models import Event, Intern
from datetime import timedelta, datetime

@login_required
def planning(request):
    if request.user.is_staff:
        return redirect('admin_panel')
    intern = request.user.intern

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            reason = form.cleaned_data['reason']
            half_day = form.cleaned_data['half_day']
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
            existing_events = Event.objects.filter(intern=intern, start_date__lte=end_date, end_date__gte=start_date)
            if existing_events.filter(approbation=0).exists():
                return HttpResponse('An event already exists within the selected date range', status=401)

            # Assign values
            intern.days_off_onhold += duration
            intern.save()

            # Create event
            Event.objects.create(
                intern=intern,
                reason=reason,
                start_date=start_date,
                end_date=end_date,
                duration=duration,
                half_day=half_day,
            )
            return redirect('planning')
    else:
        form = EventForm()

    responses = Event.objects.filter(intern=intern, approbation__in=[1, 2])

    context = {
        'form': form,
        'name': request.user.first_name,
        'days_off_left': intern.days_off_left,
        'days_off_onhold': intern.days_off_onhold,
        'responses': responses,
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
        elif event.approbation == 2:
            background_color = 'red'
        event_list.append({
            'title': event.reason,
            'start': event.start_date,
            'end': event.end_date,
            'backgroundColor': background_color,
        })
    return JsonResponse(event_list, safe=False)
