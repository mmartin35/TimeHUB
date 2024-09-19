from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from intern.models import Intern
from pointer.models import Timer
from planning.models import Event
from .forms import EventApprovalForm
from django.http import JsonResponse, HttpResponse
from datetime import timedelta

@staff_member_required
def admin_panel(request):
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
                intern.days_off_left -= intern.days_off_onhold
                intern.days_off_onhold = 0
                event.is_archived = True
            elif form.cleaned_data['reject_event']:
                event.approbation = 2
                event.is_archived = True
            event.save()
            intern.save()

    for intern in Intern.objects.all():
        intern.total_hours = 0
        for timer in Timer.objects.filter(intern=intern):
            intern.total_hours += timer.working_hours
        intern.save()

    interns_with_timers = Intern.objects.prefetch_related('timer_set', 'event_set').all()
    context = {
        '': 'monthly_working_hours',
        '': 'monthly_days_off',
        'interns_with_timers': interns_with_timers,
        'active_users': Intern.objects.filter(is_active=True),
        'inactive_users': Intern.objects.filter(is_active=False),
    }
    return render(request, 'admin_panel.html', context)

@staff_member_required
def archive(request):
    interns_list = Intern.objects.prefetch_related('event_set').all()
    context = {
        'interns_list': interns_list,
    }
    return render(request, 'archive.html', context)

@staff_member_required
def admin_events_json(request):
    events = Event.objects.select_related('intern').all()
    event_list = []
    for event in events:
        intern = event.intern
        if event.approbation == 0:
            background_color = 'blue'
        elif event.approbation == 1:
            background_color = 'green'
        elif event.approbation == 2:
            background_color = 'red'
        event_list.append({
            'title': intern.user.first_name + ' ' + intern.user.last_name,
            'start': event.start_date.strftime('%Y-%m-%d'),
            'end': event.end_date + timedelta(days=1).strftime('%Y-%m-%d'),
            'backgroundColor': background_color,
        })
    return JsonResponse(event_list, safe=False)
