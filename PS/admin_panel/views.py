# Files
from turtle import st
from .forms import ApproveRequestForm, CreateInternForm, UpdateInternForm, ApproveServiceTimerForm, ApproveEventForm, AddPublicHolidayForm, RemovePublicHolidayForm, CarouselForm, PreviewForm
from intern.models import Intern
from pointer.models import DailyTimer, RequestTimer, ServiceTimer, ChangingLog
from planning.models import Event, PublicHolidays
from pointer.views import convert_time_to_hours_from_midnight

# Imports
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse, HttpResponse
from datetime import datetime

month_names = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

@staff_member_required
def dashboard(request):
    # Update data
    update_data(request)
    requested_user = 0

    # Handle POST requests
    if request.method == 'POST':
        carouselForm = CarouselForm(request.POST)
        if carouselForm.is_valid():
            requested_user = carouselForm.cleaned_data['user_id']

        eventForm = ApproveEventForm(request.POST)
        if eventForm.is_valid():
            event = Event.objects.get(id=eventForm.cleaned_data['event_id'])
            intern = event.intern
            if eventForm.cleaned_data['event_approve']:
                event.approbation = 1
                intern.daysoff_left -= event.duration
                intern.daysoff_onhold -= event.duration
            elif eventForm.cleaned_data['event_reject']:
                event.approbation = 2
                intern.daysoff_onhold -= event.duration
            event.comment = eventForm.cleaned_data['event_comment']
            event.save()
            intern.save()

        requestForm = ApproveRequestForm(request.POST)
        if requestForm.is_valid():
            requested = RequestTimer.objects.get(id=requestForm.cleaned_data['request_id'])
            if requestForm.cleaned_data['request_approve']:
                requested.approbation = 1
                worktime = convert_time_to_hours_from_midnight(requested.altered_t2) - convert_time_to_hours_from_midnight(requested.altered_t1) + convert_time_to_hours_from_midnight(requested.altered_t4) - convert_time_to_hours_from_midnight(requested.altered_t3)
                DailyTimer.objects.filter(intern=requested.intern, date=requested.date).update(
                    t1=requested.altered_t1,
                    t2=requested.altered_t2,
                    t3=requested.altered_t3,
                    t4=requested.altered_t4,
                    worktime=worktime
                )
            elif requestForm.cleaned_data['request_reject']:
                requested.approbation = 2
            requested.save()

        serviceForm = ApproveServiceTimerForm(request.POST)
        if serviceForm.is_valid():
            service = ServiceTimer.objects.get(id=serviceForm.cleaned_data['service_id'])
            if service.t2 is None:
                service.t2 = '19:30:00'
            service.comment = serviceForm.cleaned_data['service_comment']
            service.save()
            return redirect('dashboard')

    context = {
        # General variable
        'name': request.user.first_name,
        # Specific variables
        'requested_user': requested_user,
        'requested_month': datetime.now().month,
        'intern_weeks_data': structure_data(request, requested_user).weeks,
        # Lists
        'intern_list': Intern.objects.filter(is_ongoing=True),
        'event_list': Event.objects.filter(approbation=0),
        'request_list': RequestTimer.objects.filter(approbation=0),
        'timer_list': DailyTimer.objects.all(),
        'service_list': ServiceTimer.objects.all(),
    }
    return render(request, 'dashboard.html', context)

@staff_member_required
def preview_report(request):
    if request.method == 'POST':
        previewForm = PreviewForm(request.POST)
        if previewForm.is_valid():
            month = previewForm.cleaned_data['selected_month']
            return global_report(request, month)
    month = datetime.now().month
    interns_data = []
    for intern in Intern.objects.filter(is_ongoing=True):
        intern_data = structure_data(request, intern.id)
        monthly_hours = sum(timer.worktime for timer in intern_data.months[month])
        interns_data.append({
            'intern': intern,
            'monthly_hours': monthly_hours
        })
    context = {
        'name': request.user.first_name,
        'interns_data': interns_data,
        'event_list': Event.objects.filter(approbation=1, start_date__month=month),
        'month': month_names[month - 1],
        'date': datetime.now().date(),
    }
    return render(request, 'preview_report.html', context)

@staff_member_required
def create_intern(request):
    # Update data
    update_data(request)

    # Handle POST requests
    if request.method == 'POST':
        createInternForm = CreateInternForm(request.POST)
        if createInternForm.is_valid():
            user = createInternForm.save(commit=False)
            user.is_staff = False
            user.save()
            arrival = createInternForm.cleaned_data['arrival']
            departure = createInternForm.cleaned_data['departure']
            regime = createInternForm.cleaned_data['regime']
            day_gap = (departure - arrival).days
            Intern.objects.create(
                user=user,
                arrival=arrival,
                departure=departure,
                daysoff_total=round(day_gap * (26 / 365), 2),
                daysoff_left=round(day_gap * (26 / 365), 2),
                mandatory_hours=round(day_gap * (40 / 7), 2) * regime / 100,
            )
            return redirect('create_intern')

    context = {
        # General variable
        'name': request.user.first_name,
        # Specific variables
        'form': CreateInternForm(),
        # Lists
        'intern_list': Intern.objects.all(),
    }
    return render(request, 'create_intern.html', context)

@staff_member_required
def add_publicholiday(request):
    # Handle POST requests
    if request.method == 'POST':
        addPublicHolidayForm = AddPublicHolidayForm(request.POST)
        if addPublicHolidayForm.is_valid():
            date = request.POST.get('added_holiday_date')
            name = request.POST.get('added_holiday_name')
            if not date or not name:
                return HttpResponse('Please fill in all the fields', status=400)
            if PublicHolidays.objects.filter(date=date).exists():
                return HttpResponse('This public holiday already exists', status=400)
            PublicHolidays.objects.create(date=date, name=name)

        removePublicHolidayForm = RemovePublicHolidayForm(request.POST)
        if removePublicHolidayForm.is_valid():
            date = request.POST.get('removed_holiday_date')
            if date is None:
                return HttpResponse('Error trying to remove the holiday.', status=400)
            PublicHolidays.objects.filter(date=date).delete()

    return render(request, 'add_publicholiday.html', {'name': request.user.first_name, 'public_holidays': PublicHolidays.objects.all()})

@staff_member_required
def edit_data(request):
    # Handle POST requests
    if request.method == 'POST':
        updateInternForm = UpdateInternForm(request.POST)
        if updateInternForm.is_valid():
            member = request.user.username
            intern = Intern.objects.get(id=updateInternForm.cleaned_data['intern_id'])
            worktime = updateInternForm.cleaned_data['worktime']
            date = updateInternForm.cleaned_data['date']
            print(date)
            print(worktime)
            if not DailyTimer.objects.filter(intern=intern, date=date).exists():
                return HttpResponse('Cannot change data: wrong date or intern', status=401)

            ChangingLog.objects.create(
                intern=intern,
                member=member,
                date=date,
                original_worktime=DailyTimer.objects.get(intern=intern, date=date).worktime,
                altered_worktime=worktime
            )
            DailyTimer.objects.filter(intern=intern, date=date).update(worktime=worktime)
           
    context = {
        # General variable
        'name': request.user.first_name,
        # Lists
        'intern_list': Intern.objects.all(),
        'timer_list': DailyTimer.objects.all()
    }
    return render(request, 'edit_data.html', context)

@staff_member_required
def global_report(request, month):
    interns_data = []
    for intern in Intern.objects.filter(is_ongoing=True):
        intern_data = structure_data(request, intern.id)
        monthly_hours = sum(timer.worktime for timer in intern_data.months[month])
        interns_data.append({
            'intern': intern,
            'monthly_hours': monthly_hours
        })
    context = {
        'name': request.user.first_name,
        'interns_data': interns_data,
        'event_list': Event.objects.filter(approbation=1, start_date__month=month),
        'month': month_names[month - 1],
        'date': datetime.now().date(),
    }
    return render(request, 'global_report.html', context)

@staff_member_required
def individual_report(request, username, month):
    intern = get_object_or_404(Intern, user__username=username)
    intern_data = structure_data(request, intern.id)
    monthly_hours = 0
    weeks_data = []
    for timer in intern_data.months[month]:
        week_number = timer.date.isocalendar()[1]
        if not any(week['week_number'] == week_number for week in weeks_data):
            weekly_hours = sum(t.worktime for t in intern_data.weeks[week_number])
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
    for timer in intern_data.months[month]:
        monthly_hours += timer.worktime
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
    return render(request, 'individual_report.html', context)

@staff_member_required
def update_data(request):
    # Manage service timers
    for service in ServiceTimer.objects.all():
        if service.t2 is None and service.date != datetime.now().date():
            service.t2 = "19:30:00"
        service.save()

    # Manage intern status
    for intern in Intern.objects.all():
        if datetime.now().date() < intern.departure and datetime.now().date() > intern.arrival:
            intern.is_ongoing = True
        else:
            intern.is_ongoing = False
        intern.save()

@staff_member_required
def structure_data(request, intern_id):
    class Intern_item:
        def __init__(self):
            self.months = {month: [] for month in range(1, datetime.now().month + 1)}
            self.weeks = {week: [] for week in range(1, datetime.now().isocalendar()[1] + 1)}
    intern_data = Intern_item()    
    for timer in DailyTimer.objects.filter(intern=intern_id):
        if datetime.now().year != timer.date.year:
            continue
        intern_data.months[timer.date.month].append(timer)
        intern_data.weeks[timer.date.isocalendar()[1]].append(timer)
    return intern_data

@staff_member_required
def admin_events_json(request):
    events = Event.objects.select_related('intern').all()
    event_list = []
    for event in events:
        if event.approbation == 0:
            background_color = 'blue'
        elif event.approbation == 1:
            background_color = 'green'
        elif event.approbation == 2 or event.approbation == 3:
            background_color = 'red'
        event_list.append({
            'title': event.intern.user.first_name + ' ' + event.intern.user.last_name,
            'start': event.start_date,
            'end': event.end_date,
            'backgroundColor': background_color,
        })
    return JsonResponse(event_list, safe=False)