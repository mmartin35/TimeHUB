from django.shortcuts import render
from django.http import HttpResponse

def stats(request):
    return render(request, 'stats.html')
