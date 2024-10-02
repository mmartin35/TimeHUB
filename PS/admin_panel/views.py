from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from intern.models import Intern
from pointer.models import Timer, ServiceTimer
from planning.models import Event
from .forms import EventApprovalForm, InternUserCreationForm
from django.http import JsonResponse
from datetime import datetime, timedelta

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
    
    # Get data for each intern
    interns_data = []
    for intern in Intern.objects.all():
        intern_data = structure_data(request, intern.id)
        interns_data.append((intern, intern_data))
    # Get services for the last week
    services_list = []
    for service in ServiceTimer.objects.all():
        if service.date >= datetime.now().date() - timedelta(days=7):
            services_list.append(service)
    context = {
        'name': request.user.first_name,
        'interns_list': Intern.objects.filter(is_ongoing=True),
        'interns_weeks_data': interns_data,
        'services_list': services_list,
        'events_list': Event.objects.select_related('intern').all(),
    }
    return render(request, 'admin_panel.html', context)

@staff_member_required
def setup(request):
    update_data(request)
    if request.method == 'POST':
        form = InternUserCreationForm(request.POST)
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
            )
            print('Intern created successfully!')
            return redirect('setup')
    context = {
        'name': request.user.first_name,
        'form': InternUserCreationForm(),
        'interns': Intern.objects.all(),
        'events': Event.objects.select_related('intern').all(),
    }
    return render(request, 'setup.html', context)

@staff_member_required
def structure_data(request, intern_id):
    class Intern_item:
        def __init__(self):
            self.months = {month: [] for month in range(1, 12)}
            self.weeks = {week: [] for week in range(1, 53)}
    intern_data = Intern_item()
    for timer in Timer.objects.filter(intern=intern_id):
        if datetime.now().year != timer.date.year:
            continue
        intern_data.months[timer.date.month].append(timer)
        intern_data.weeks[timer.date.isocalendar()[1]].append(timer)
    return intern_data

@staff_member_required
def print_data(request, intern_id, intern_item):
    # Print monthly total
    for month, timers in intern_item.months.items():
        month_total = sum(timer.working_hours for timer in timers)
        print(f"Total in month {month} for user: {month_total}")

    # Print weekly total
    for week, timers in intern_item.weeks.items():
        weekly_total = sum(timer.working_hours for timer in timers)
        print(f"Total in week {week} for user: {weekly_total}")

@staff_member_required
def update_data(request):
    # Manage service timers
    for service_timer in ServiceTimer.objects.all():
        if service_timer.t2_service is None and service_timer.date != datetime.now().date() and datetime.now().date() == "19:30":
            service_timer.t2_service = "19:30"
        service_timer.save()

    # Manage intern status
    for intern in Intern.objects.all():
        if datetime.now().date() < intern.departure and datetime.now().date() > intern.arrival:
            intern.is_ongoing = True
        else:
            intern.is_ongoing = False
        intern.save()

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