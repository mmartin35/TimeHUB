from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Event
from .forms import EventForm
from calendar import HTMLCalendar
from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required

class EventCalendar(HTMLCalendar):
    def __init__(self, events, uname, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.events = events
        self.uname = uname
        self.theyear = None
        self.themonth = None

    def formatday(self, day, weekday):
        if day == 0:
            return '<td class="empty"></td>'

        day_date = timezone.make_aware(datetime(self.theyear, self.themonth, day), timezone.get_current_timezone()).date()
        events_today = self.events.filter(date=day_date, uname=self.uname)

        day_html = f'<td class="{self.cssclasses[weekday]}">'
        if events_today.exists():
            day_html += f'<div class="event" style="background-color: red; color: white;">{day}</div>'
        else:
            day_html += f'{day}'
        day_html += '</td>'
        return day_html

    def formatmonth(self, theyear, themonth, withyear=True):
        self.theyear = theyear
        self.themonth = themonth
        return super().formatmonth(theyear, themonth, withyear)

def get_month_date(year, month):
    if month < 1:
        year -= 1
        month = 12
    elif month > 12:
        year += 1
        month = 1
    return timezone.make_aware(datetime(year, month, 1), timezone.get_current_timezone())

def add_month(year, month):
    if month == 12:
        return year + 1, 1
    return year, month + 1

def subtract_month(year, month):
    if month == 1:
        return year - 1, 12
    return year, month - 1

@login_required
def planning(request):
    month_str = request.GET.get('month')
    if month_str:
        try:
            month = timezone.make_aware(datetime.strptime(month_str, '%Y-%m'), timezone.get_current_timezone())
        except ValueError:
            month = timezone.localtime()
    else:
        month = timezone.localtime()

    events = Event.objects.all()
    uname = request.user.username

    event_calendar = EventCalendar(events, uname)
    cal_html = event_calendar.formatmonth(month.year, month.month)

    prev_year, prev_month = subtract_month(month.year, month.month)
    next_year, next_month = add_month(month.year, month.month)

    prev_month_date = get_month_date(prev_year, prev_month)
    next_month_date = get_month_date(next_year, next_month)

    prev_month_str = prev_month_date.strftime('%Y-%m')
    next_month_str = next_month_date.strftime('%Y-%m')

    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            date = form.cleaned_data['date']
            duration = form.cleaned_data['duration']

            for i in range(duration):
                if Event.objects.filter(uname=uname, date=date + timedelta(days=i)).exists():
                    return render(request, 'error.html', {'content': 'An event already exists for this date'})

            for i in range(duration):
                event_date = date + timedelta(days=i)
                if not Event.objects.filter(uname=uname, date=event_date).exists():
                    Event.objects.create(
                        title=title,
                        date=event_date,
                        uname=uname
                    )

            return redirect('planning')
    else:
        form = EventForm()

    context = {
        'calendar': cal_html,
        'current_month': month.strftime('%B %Y'),
        'prev_month': prev_month_str,
        'next_month': next_month_str,
        'form': form,
    }
    return render(request, 'planning.html', context)
