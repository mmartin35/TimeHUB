from django.shortcuts import render
from django.http import HttpResponse

def disp_stats(request):
    return render(request, 'stats.html', {'name': 'Matthieu'})
