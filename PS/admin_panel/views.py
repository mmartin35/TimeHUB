from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from intern.models import Intern
from planning.models import Event
from .forms import EventApprovalForm
from django.http import JsonResponse, HttpResponse

@staff_member_required
def admin_panel(request):
    if request.method == 'POST':
        form = EventApprovalForm(request.POST)
        if form.is_valid():
            event_id = form.cleaned_data['event_id']
            event = get_object_or_404(Event, id=event_id)

            if form.cleaned_data['comment_staff']:
                event.comment_staff = form.cleaned_data['comment_staff']
                event.save()

            if form.cleaned_data['approve_event']:
                event.approved = 1
                event.is_archived = True
                event.save()

            elif form.cleaned_data['reject_event']:
                event.approved = 2
                event.is_archived = True
                event.save()

            elif form.cleaned_data['archive_event']:
                event.is_archived = True
                event.save()

    interns_with_timers = Intern.objects.prefetch_related('timer_set', 'event_set').all()
    context = {
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
    # Fetch all events
    events = Event.objects.select_related('intern').all()
    event_list = []
    for event in events:
        intern = event.intern
        if event.approved == 0:
            background_color = 'blue'
        elif event.approved == 1:
            background_color = 'green'
        elif event.approved == 2:
            background_color = 'red'

        event_list.append({
            'title': intern.user.first_name + ' ' + intern.user.last_name,
            'start': event.start_date.strftime('%Y-%m-%d'),
            'end': event.end_date.strftime('%Y-%m-%d'),
            'allDay': True,
            'backgroundColor': background_color,
        })

    return JsonResponse(event_list, safe=False)
