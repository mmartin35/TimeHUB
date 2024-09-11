from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import ReportForm
from .models import Report

def reporting(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            Report.objects.create(
                name=form.cleaned_data['name'] or 'Anonymous',
                subject=form.cleaned_data['subject'],
                detailed=form.cleaned_data['detailed'],
                contact=form.cleaned_data['contact'],
            )
            return redirect('reporting')
    else:
        form = ReportForm()

    context = {'form': form}
    return render(request, 'reporting.html', context)
