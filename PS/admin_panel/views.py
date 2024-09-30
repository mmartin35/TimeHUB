from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from intern.models import Intern
from pointer.models import Timer, ServiceTimer
from planning.models import Event
from .forms import EventApprovalForm, InternUserCreationForm
from django.http import JsonResponse, HttpResponse
from datetime import timedelta, datetime


@staff_member_required
def admin_panel(request):
    update_data(request)
    if request.method == 'POST':
        form = EventApprovalForm(request.POST)
        if form.is_valid():
            event_id = form.cleaned_data['event_id']
            event = get_object_or_404(Event, id=event_id)
            intern = event.intern
            if form.cleaned_data['staff_comment']:
                event.staff_comment = form.cleaned_data['staff_comment']
            if form.cleaned_data['approve_event']:
                event.approbation = 1
                event.is_archived = True
                intern.days_off_left -= event.duration
                intern.days_off_onhold -= event.duration
            elif form.cleaned_data['reject_event']:
                event.approbation = 2
                event.is_archived = True
                intern.days_off_onhold -= event.duration
            event.save()
            intern.save()

    week_groups = []
    context = {
        'name': request.user.first_name,
        'interns_with_timers': Intern.objects.prefetch_related('timer_set').all(),
        'service_timers': ServiceTimer.objects.prefetch_related('intern').filter(t2_service__isnull=True),
        'week_groups_per_interns': week_groups,
        'active_users': Intern.objects.filter(is_active=True),
        'inactive_users': Intern.objects.filter(is_active=False),
    }
    return render(request, 'admin_panel.html', context)

@staff_member_required
def setup(request):
    if request.method == 'POST':
        form = InternUserCreationForm(request.POST)
        if form.errors:
            code = form.errors.as_data().popitem()
            return HttpResponse(code, status=401)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = False
            user.save()
            arrival = form.cleaned_data['arrival']
            departure = form.cleaned_data['departure']
            regime = form.cleaned_data['regime']
            day_gap = (departure - arrival).days
            Intern.objects.create(
                user=user,
                arrival=arrival,
                departure=departure,
                days_off_total=round(day_gap * (26 / 365), 2),
                days_off_left=round(day_gap * (26 / 365), 2),
                mandatory_hours=round(day_gap * (40 / 7), 2) * regime / 100,
                is_ongoing=True # TEMPORARY
            )
            print('Intern created successfully!')
            return redirect('setup')
    context = {
        'form': InternUserCreationForm(),
        'interns': Intern.objects.all(),
        'events': Event.objects.prefetch_related('intern').all(),
    }
    return render(request, 'setup.html', context)

@staff_member_required
def admin_events_json(request):
    events = Event.objects.select_related('intern').all()
    event_list = []
    for event in events:
        if event.approbation == 0:
            background_color = 'blue'
        elif event.approbation == 1:
            background_color = 'green'
        elif event.approbation == 2:
            background_color = 'red'
        event_list.append({
            'title': event.intern.user.first_name + ' ' + event.intern.user.last_name,
            'start': event.start_date,
            'end': event.end_date,
            'backgroundColor': background_color,
        })
    return JsonResponse(event_list, safe=False)
