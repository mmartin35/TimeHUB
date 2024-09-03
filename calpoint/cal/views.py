from django.shortcuts import render, redirect
from .models import Event
from .forms import EventForm
import calendar as cal
from calendar import HTMLCalendar
from datetime import datetime

class EventCalendar(HTMLCalendar):
    def __init__(self, events, *args, **kwargs):
        super(EventCalendar, self).__init__(*args, **kwargs)
        self.events = events

    def formatday(self, day, weekday, themonth, theyear):
        events_today = self.events.filter(start_time__year=theyear, start_time__month=themonth, start_time__day=day)
        day_html = f'<td class="{self.cssclasses[weekday]}">'
        if day != 0:
            if events_today:
                day_html += f'<span class="day-event">{day}</span>'
            else:
                day_html += f'{day}'
        day_html += '</td>'
        return day_html

    def formatmonth(self, theyear, themonth, withyear=True):
        events = Event.objects.filter(start_time__year=theyear, start_time__month=themonth)
        self.events = events
        return super().formatmonth(theyear, themonth, withyear=withyear)

def get_month_date(year, month):
    if month < 1:
        year -= 1
        month = 12
    elif month > 12:
        year += 1
        month = 1
    return datetime(year, month, 1)

def calendar(request):
    month_str = request.GET.get('month')
    if month_str:
        month = datetime.strptime(month_str, '%Y-%m')
    else:
        month = datetime.today()

    event_calendar = EventCalendar(events=Event.objects.all())
    cal_html = event_calendar.formatmonth(month.year, month.month)

    prev_month = get_month_date(month.year, month.month - 1)
    next_month = get_month_date(month.year, month.month + 1)
    prev_month_str = prev_month.strftime('%Y-%m')
    next_month_str = next_month.strftime('%Y-%m')

    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('calendar')
    else:
        form = EventForm()

    context = {
        'calendar': cal_html,
        'current_month': month.strftime('%B %Y'),
        'prev_month': prev_month_str,
        'next_month': next_month_str,
        'form': form,
    }
    return render(request, 'calendar.html', context)
