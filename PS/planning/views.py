from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import configparser
from datetime import timedelta
from .forms import EventForm
from .models import Event

@login_required
def planning(request):
    # Calculate days off left
    daysoff_left = 25 - Event.objects.filter(user=request.user).count()

    # Check form submission
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            total_days_requested = (end_date - start_date).days + 1
            reason = form.cleaned_data['reason']
            half_day = form.cleaned_data['half_day']

            # Validation: Ensure the start date is before or equal to the end date
            if start_date > end_date:
                form.add_error('start_date', 'Start date must be before or on the end date.')
                return render(request, 'planning.html', {'form': form, 'daysoff_left': daysoff_left})

            # Validation: Check if the user has enough days off left
            if total_days_requested > daysoff_left:
                form.add_error('end_date', f'The requested time off exceeds the remaining days off ({daysoff_left} days).')
                return render(request, 'planning.html', {'form': form, 'daysoff_left': daysoff_left})

            # Add each day as a separate event
            for single_date in (start_date + timedelta(days=n) for n in range(total_days_requested)):
                Event.objects.create(
                    user=request.user,
                    reason=reason,
                    start_date=single_date,
                    end_date=single_date,
                    half_day=half_day
                )
            return redirect('planning')

    else:
        form = EventForm()

    context = {
        'user': request.user.username,
        'daysoff_left': daysoff_left,
        'form': form
    }
    return render(request, 'planning.html', context)
