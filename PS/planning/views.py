from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import timedelta
from .forms import EventForm
from .models import Event

@login_required
def planning(request):
    # Calculate remaining days off
    daysoff_left = 25 - Event.objects.filter(user=request.user).count() + 1

    # Check form submission
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            total_days_requested = (end_date - start_date).days + 1
            reason = form.cleaned_data['reason']
            half_day = form.cleaned_data['half_day']

            # Ensure start date is before or equal to end date
            if start_date > end_date:
                context = {
                    'content': 'Start date cannot be after end date',
                }
                return render(request, 'error.html', context)

            # Check if user has enough days off
            if total_days_requested > daysoff_left:
                return render(request, 'error.html', context = {'content': 'Requested time off exceeds the remaining days off'})

            # Ensure start date is not in the past
            if start_date < start_date.today():
                return render(request, 'error.html', context = {'content': 'Start date cannot be in the past'})

            # Check for existing events within the same date range
            existing_events = Event.objects.filter(
                user=request.user,
                start_date__lte=end_date,
                end_date__gte=start_date
            )

            if existing_events.exists():
                return render(request, 'error.html', context = {'content': 'An event already exists within the selected date range'})

            # Add each day as a separate event
            for single_date in (start_date + timedelta(days=n) for n in range(total_days_requested)):
                if half_day:
                    daysoff_left += 0.5
                    Event.objects.create(
                        user=request.user,
                        reason=reason,
                        start_date=single_date,
                        end_date=single_date,
                        half_day=half_day,
                        remaining_days=daysoff_left,
                    )
                    half_day = False
                else:
                    Event.objects.create(
                        user=request.user,
                        reason=reason,
                        start_date=single_date,
                        end_date=single_date,
                        half_day=half_day,
                        remaining_days=daysoff_left,
                    )
            return redirect('planning')

    else:
        form = EventForm()

    context = {
        'user': request.user,
        'daysoff_left': daysoff_left,
        'form': form
    }
    return render(request, 'planning.html', context)

@login_required
def events_json(request):
    # Fetch all events for the logged-in user
    events = Event.objects.filter(user=request.user)
    event_list = []
    for event in events:
        if event.reason == 'Initial request':
            continue
        event_list.append({
            'title': event.reason,
            'start': event.start_date.strftime('%Y-%m-%d'),
            'end': event.end_date.strftime('%Y-%m-%d'),
            'allDay': True,
            'backgroundColor': 'green' if event.approved else 'orange',
        })
    return JsonResponse(event_list, safe=False)
