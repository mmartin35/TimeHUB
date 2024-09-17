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
            total_days_requested = (end_date - start_date).days + 1
            reason = form.cleaned_data['reason']
            half_day_start = form.cleaned_data['half_day_start']
            half_day_end = form.cleaned_data['half_day_end']

            # Ensure start date is before or equal to end date, if user has enough days, if start date isnt in the past
            if start_date > end_date:
                return HttpResponse('Start date cannot be after end date.', status=401)
            if total_days_requested > intern.days_off_left:
                return HttpResponse('Requested time off exceeds the remaining days off', status=401)
            if start_date < start_date.today():
                return HttpResponse('Start date cannot be in the past', status=401)
            existing_events = Event.objects.filter(intern=intern, start_date__lte=end_date, end_date__gte=start_date)
            if existing_events.exists():
                return HttpResponse('An event already exists within the selected date range', status=401)

            # Add each day as a separate event
            i=0
            for single_date in (start_date + timedelta(days=n) for n in range(total_days_requested)):
                if half_day_start == 1 and i == 0 or (half_day_end == 0 and i == total_days_requested - 1):
                    intern.days_off_left -= 0.5
                else:
                    intern.days_off_left -= 1
                Event.objects.create(
                    intern=intern,
                    reason=reason,
                    start_date=single_date,
                    end_date=single_date,
                )
                i += 1
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
    # Fetch all events for the logged-in user
    events = Event.objects.filter(intern=request.user.intern)
    event_list = []
    for event in events:
        if event.reason == 'Initial request' or event.is_archived:
            continue
        event_list.append({
            'title': event.reason,
            'start': event.start_date.strftime('%Y-%m-%d'),
            'end': event.end_date.strftime('%Y-%m-%d'),
            'allDay': True,
        })
    return JsonResponse(event_list, safe=False)
