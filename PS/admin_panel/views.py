from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from intern.models import Intern
from pointer.models import Timer

@staff_member_required
def admin_panel(request):
    interns_with_timers = Intern.objects.prefetch_related('timer_set').all()

    context = {
        'interns_with_timers': interns_with_timers,
        'active_users': Intern.objects.filter(is_active=True),
        'inactive_users': Intern.objects.filter(is_active=False),
    }
    return render(request, 'admin_panel.html', context)

