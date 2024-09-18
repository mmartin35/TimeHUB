from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from datetime import timedelta
from .forms import EventForm
from .models import Event, Intern

@login_required
def planning(request):
    if request.user.is_staff:
        return redirect('admin_panel')

    # Calculate remaining days off
    intern = request.user.intern

    # Check form submission
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            reason = form.cleaned_data['reason']
            half_day_start = form.cleaned_data['half_day_start']
            half_day_end = form.cleaned_data['half_day_end']
            duration = (end_date - start_date).days + 1

            # Ensure start date is before or equal to end date, if user has enough days, if start date isnt in the past
            if start_date > end_date:
                return HttpResponse('Start date cannot be after end date.', status=401)
            if duration > intern.days_off_left:
                return HttpResponse('Requested time off exceeds the remaining days off', status=401)
            if start_date < start_date.today():
                return HttpResponse('Start date cannot be in the past', status=401)
            existing_events = Event.objects.filter(intern=intern, start_date__lte=end_date, end_date__gte=start_date)
            if existing_events.exists():
                return HttpResponse('An event already exists within the selected date range', status=401)

            # Add days to event
            for i in range(duration):
                if half_day_start == 1 and i == 0:
                    intern.days_off_left -= 0.5
                elif half_day_end == 0 and i == duration - 1:
                    intern.days_off_left -= 0.5
                else:
                    intern.days_off_left -= 1
            Event.objects.create(
                intern=intern,
                reason=reason,
                start_date=start_date,
                end_date=end_date,
                duration=duration,
            )
            intern.save()
            return redirect('planning')
    else:
        form = EventForm()
    context = {
        'user': request.user,
        'daysoff_left': intern.days_off_left,
        'form': form
    }
    return render(request, 'planning.html', context)

@login_required
def events_json(request):
    # Fetch all events for all users or logged in user
    if request.user.is_staff:
        events = Event.objects.all()
    else:
        events = Event.objects.filter(intern=request.user.intern)
    event_list = []
    for event in events:
        if event.approved == 0:
            event_list.append({
                'title': event.reason,
                'start': event.start_date.strftime('%Y-%m-%d'),
                'end': event.end_date.strftime('%Y-%m-%d'),
                'allDay': True,
                'backgroundColor': 'blue',
            })
        elif event.approved == 1:
            event_list.append({
                'title': event.reason,
                'start': event.start_date.strftime('%Y-%m-%d'),
                'end': event.end_date.strftime('%Y-%m-%d'),
                'allDay': True,
                'backgroundColor': 'green',
            })
        elif event.approved == 2:
            event_list.append({
                'title': event.comment_staff,
                'start': event.start_date.strftime('%Y-%m-%d'),
                'end': event.end_date.strftime('%Y-%m-%d'),
                'allDay': True,
                'backgroundColor': 'red',
            })
    return JsonResponse(event_list, safe=False)
