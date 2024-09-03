from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Event
from .forms import EventForm
from calendar import HTMLCalendar
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class EventCalendar(HTMLCalendar):
    def __init__(self, events, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.events = events
        self.theyear = None
        self.themonth = None

    def formatday(self, day, weekday):
        if day == 0:  # Skip days outside of the current month
            return '<td class="empty"></td>'

        day_date = timezone.make_aware(datetime(self.theyear, self.themonth, day), timezone.get_current_timezone())
        events_today = self.events.filter(
            start_time__year=self.theyear,
            start_time__month=self.themonth
        )
        
        is_event_day = False
        for event in events_today:
            event_end_date = event.start_time + timedelta(days=event.duration)
            if event.start_time <= day_date < event_end_date:
                is_event_day = True
                break
        
        day_html = f'<td class="{self.cssclasses[weekday]}">'
        if is_event_day:
            day_html += f'<span class="day-event">{day}</span>'
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

def calendar(request):
    month_str = request.GET.get('month')
    if month_str:
        try:
            month = timezone.make_aware(datetime.strptime(month_str, '%Y-%m'), timezone.get_current_timezone())
        except ValueError:
            month = timezone.localtime()  # Fallback to the current time if parsing fails
    else:
        month = timezone.localtime()  # Use timezone-aware datetime for the current time

    events = Event.objects.all()
    event_calendar = EventCalendar(events)
    cal_html = event_calendar.formatmonth(month.year, month.month)

    prev_month = get_month_date(month.year, month.month) - relativedelta(months=1)
    next_month = get_month_date(month.year, month.month) + relativedelta(months=1)
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
