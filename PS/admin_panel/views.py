from turtle import st
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from intern.models import Intern
from pointer.models import Timer, ServiceTimer
from planning.models import Event
from .forms import CarouselForm, EventApprovalForm, InternUserCreationForm, ServiceTimerForm
from django.http import JsonResponse
from datetime import datetime

month_names = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

@staff_member_required
def admin_panel(request):
    update_data(request)
    requested_user = None
    if request.method == 'POST':
        carouselForm = CarouselForm(request.POST)
        if carouselForm.is_valid():
            requested_user = carouselForm.cleaned_data['user_id']
        eventForm = EventApprovalForm(request.POST)
        if eventForm.is_valid():
            event_id = eventForm.cleaned_data['event_id']
            event = get_object_or_404(Event, id=event_id)
            intern = event.intern
            if eventForm.cleaned_data['staff_comment']:
                event.staff_comment = eventForm.cleaned_data['staff_comment']
            if eventForm.cleaned_data['approve_event']:
                event.approbation = 1
                event.is_archived = True
                intern.days_off_left -= event.duration
                intern.days_off_onhold -= event.duration
            elif eventForm.cleaned_data['reject_event']:
                event.approbation = 2
                event.is_archived = True
                intern.days_off_onhold -= event.duration
            event.save()
            intern.save()
    
    # Get data for each intern
    intern_weeks_data = structure_data(request, requested_user).weeks
    if intern_weeks_data is not None:
        for week, days in intern_weeks_data.items():
            intern_weeks_data[week] = days[::-1]

        
    alerts = []
#    for intern, intern_data in interns_data:
#        if intern.is_ongoing:
#            week = intern_data.weeks[datetime.now().isocalendar()[1] - 1]
#            weekly_hours = sum(timer.working_hours for timer in week)
#            if weekly_hours < 40 * intern.regime / 100:
#                alerts.append(f"{intern.user.first_name} {intern.user.last_name} has worked {round(weekly_hours)}h last week, which is less than the mandatory {round(40 * intern.regime / 100)}h.")
#            if weekly_hours > 40 * intern.regime / 100:
#                alerts.append(f"{intern.user.first_name} {intern.user.last_name} has worked {round(weekly_hours)}h last week, which is more than the mandatory {round(40 * intern.regime / 100)}h.")

    for service in ServiceTimer.objects.filter(comment='NA'):
        alerts.append(f"{service.intern.user.first_name} {service.intern.user.last_name} added a service entry.")
    
    context = {
        'name': request.user.first_name,
        'interns_list': Intern.objects.filter(is_ongoing=True),
        'requested_user': requested_user,
        'intern_weeks_data': intern_weeks_data,
        'events_list': Event.objects.select_related('intern').all(),
        'requested_month': datetime.now().month,
        'alerts': alerts,
    }
    return render(request, 'admin_panel.html', context)

@staff_member_required
def setup(request):
    update_data(request)
    if request.method == 'POST':
        user_form = InternUserCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.is_staff = False
            user.save()
            arrival = user_form.cleaned_data['arrival']
            departure = user_form.cleaned_data['departure']
            regime = user_form.cleaned_data['regime']
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
        service_form = ServiceTimerForm(request.POST)
        if service_form.is_valid():
            service = ServiceTimer.objects.get(id=service_form.cleaned_data['service_id'])
            service.t2_service = datetime.now().time()
            service.comment = service_form.cleaned_data['service_comment']
            service.save()
            print('Service updated successfully!')
            return redirect('setup')

    context = {
        'name': request.user.first_name,
        'form': InternUserCreationForm(),
        'interns': Intern.objects.all(),
        'services': ServiceTimer.objects.filter(comment='NA'),
        'requested_month' : datetime.now().month,
        'events': Event.objects.select_related('intern').filter(approbation__in=[1, 2]),
    }
    return render(request, 'setup.html', context)

@staff_member_required
def global_report(request, month):
    interns_data = []
    for intern in Intern.objects.filter(is_ongoing=True):
        intern_data = structure_data(request, intern.id)
        monthly_hours = sum(timer.working_hours for timer in intern_data.months[month])
        interns_data.append({
            'intern': intern,
            'monthly_hours': monthly_hours
        })
    
    event_list = []
    for event in Event.objects.filter(approbation=1):
        event_list.append({
            'intern': event.intern.user.first_name + ' ' + event.intern.user.last_name,
            'reason': event.reason,
            'start_date': event.start_date,
            'end_date': event.end_date,
            'duration': event.duration,
        })

    month = month_names[month - 1]

    context = {
        'interns_data': interns_data,
        'event_list': event_list,
        'month': month,
        'date': datetime.now().date(),
    }
    return render(request, 'global_report.html', context)

@staff_member_required
def report(request, username, month):
    intern = get_object_or_404(Intern, user__username=username)
    intern_data = structure_data(request, intern.id)
    monthly_hours = 0
    weeks_data = []

    # Calculate weekly hours and accepted vacations
    for timer in intern_data.months[month]:
        week_number = timer.date.isocalendar()[1]
        if not any(week['week_number'] == week_number for week in weeks_data):
            weekly_hours = sum(t.working_hours for t in intern_data.weeks[week_number])
            weeks_data.append({
                'week_number': week_number,
                'weekly_hours': weekly_hours,
            })
    event_list = []
    for event in Event.objects.filter(intern=intern, approbation=1):
        event_list.append({
            'reason': event.reason,
            'start_date': event.start_date,
            'end_date': event.end_date,
            'duration': event.duration,
        })
        monthly_hours += 8 * event.duration

    # Calculate monthly hours
    for timer in intern_data.months[month]:
        monthly_hours += timer.working_hours
    if monthly_hours > 173:
        monthly_hours = 173

    month = month_names[month - 1]

    context = {
        'intern': intern,
        'intern_data': intern_data,
        'month': month,
        'date': datetime.now().date(),
        'monthly_hours': monthly_hours,
        'weeks_data': weeks_data,
        'days_left': (datetime.now().date() - intern.departure).days * -1,
        'event_list': event_list,
    }
    return render(request, 'report.html', context)

@staff_member_required
def structure_data(request, intern_id):
    class Intern_item:
        def __init__(self):
            self.months = {month: [] for month in range(1, datetime.now().month + 1)}
            self.weeks = {week: [] for week in range(1, datetime.now().isocalendar()[1] + 1)}
    
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
        if service_timer.t2_service is None and service_timer.date != datetime.now().date():
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