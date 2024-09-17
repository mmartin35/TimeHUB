from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.http import HttpResponse

@staff_member_required
def admin_panel(request):
    context = {
        'users': User.objects.all(),
        'active_users': User.objects.filter(is_active=True),
    }
    return render(request, 'admin_panel.html', context)
