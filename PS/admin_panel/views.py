from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from intern.models import Intern
from planning.models import Event
from .forms import EventApprovalForm

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
                event.save()
            
            elif form.cleaned_data['reject_event']:
                event.approved = 2
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
