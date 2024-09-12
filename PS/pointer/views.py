from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta
from .models import Timer

def logout_view(request):
    logout(request)
    return redirect('/login')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/pointer')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('')
        else:
            return HttpResponse('Invalid login', status=401)
    return render(request, 'login.html')

@login_required
def pointer(request):
    context = {
        'user': request.user,
    }
    return render(request, 'pointer.html', context)
