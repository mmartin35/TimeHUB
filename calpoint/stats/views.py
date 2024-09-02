from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def disp_stats(request):
    i = 2
    i = i + 2
    if i == 4:
        return HttpResponse('Hello, world')
    return render(request, 'stats.html', {'name': 'Matthieu'})
