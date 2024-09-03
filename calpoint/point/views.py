from django.shortcuts import render, HttpResponse

def pointing(request):
    return render(request, 'point.html')
