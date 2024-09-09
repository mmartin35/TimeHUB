from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Event
from .forms import EventForm
from calendar import HTMLCalendar
from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required

## PDF Declarations
from reportlab.pdfgen import canvas

class EventCalendar(HTMLCalendar):
    def __init__(self, events, uname, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.events = events
        self.uname = uname
        self.theyear = None
        self.themonth = None

    # Create formated day cell
    def formatday(self, day, weekday):
        if day == 0:
            return '<td class="empty"></td>'
        day_date = timezone.make_aware(datetime(self.theyear, self.themonth, day), timezone.get_current_timezone()).date()
        events_today = self.events.filter(date=day_date, uname=self.uname)
        if events_today.exists():
            day_html = f'<td class="{self.cssclasses[weekday]}" style="background-color: red; color: white;">'
        else:
            day_html = f'<td class="{self.cssclasses[weekday]}" style="background-color: #2ce51c; color: white;">'
    
        day_html += f'<a href="?month={self.theyear}-{self.themonth:02d}&day={day_date}" style="color: white; text-decoration: none;">{day}</a>'
        day_html += '</td>'
        return day_html



    # Adjust to fit with months
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

# Create all objects and fills the form to sender
@login_required
def planning(request):
    daysoff = 10
    month_str = request.GET.get('month')
    day_str = request.GET.get('day')

    # Fix non comparable types
    if month_str:
        try:
            month = timezone.make_aware(datetime.strptime(month_str, '%Y-%m'), timezone.get_current_timezone())
        except ValueError:
            month = timezone.localtime()
    else:
        month = timezone.localtime()

    # Create objects
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
    selected_day = None

    if day_str:
        try:
            selected_day = datetime.strptime(day_str, '%Y-%m-%d').date()
        except ValueError:
            selected_day = None

    # Fills the form
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            date = form.cleaned_data['date']
            duration = form.cleaned_data['duration']

            # Check availability
            if duration > daysoff - Event.objects.filter(uname=uname).count():
                return render(request, 'error.html', {'content': 'Not enough days off left'})
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
        form = EventForm(initial={'date': selected_day})
    context = {
        'calendar': cal_html,
        'current_month': month.strftime('%B %Y'),
        'prev_month': prev_month_str,
        'next_month': next_month_str,
        'form': form,
        'date': selected_day,
        'days_left': daysoff - Event.objects.filter(uname=uname).count()
    }
    return render(request, 'planning.html', context)

def generate_pdf(request):
    # Create a response object and specify the content type as PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    # Create the PDF object using ReportLab
    p = canvas.Canvas(response)

    # Add content to the PDF
    p.drawString(100, 750, "Hello, this is a PDF generated using ReportLab.")

    # Save the PDF
    p.showPage()
    p.save()

    return response
