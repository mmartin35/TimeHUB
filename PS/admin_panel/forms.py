from django import forms

# Interns
class CreateInternForm(forms.Form):
    intern          = forms.IntegerField(required=False)
    first_name      = forms.CharField(required=True, widget=forms.Textarea)
    last_name       = forms.CharField(required=True, widget=forms.Textarea)
    email           = forms.EmailField(required=True)

    cns             = forms.IntegerField(required=False)
    internship_type = forms.CharField(required=True)
    department      = forms.CharField(required=True)
    tutor           = forms.CharField(required=True)
    mission         = forms.CharField(required=True)

    arrival         = forms.DateField(required=True, widget=forms.SelectDateWidget)
    departure       = forms.DateField(required=True, widget=forms.SelectDateWidget)
    regime          = forms.IntegerField(required=True)

class UpdateInternForm(forms.Form):
    intern_id   = forms.IntegerField(widget=forms.HiddenInput)
    date        = forms.DateField(required=True, widget=forms.SelectDateWidget)
    worktime    = forms.FloatField(required=True)

# Timers
class ApproveServiceTimerForm(forms.Form):
    service_id      = forms.IntegerField(widget=forms.HiddenInput)
    service_comment = forms.CharField(required=False, widget=forms.Textarea)

# Events
class ApproveEventForm(forms.Form):
    event_id        = forms.IntegerField(widget=forms.HiddenInput)
    event_approve   = forms.BooleanField(required=False)
    event_reject    = forms.BooleanField(required=False)
    event_comment   = forms.CharField(required=True)

# Corrections
class ApproveRequestForm(forms.Form):
    request_id      = forms.IntegerField(widget=forms.HiddenInput)
    request_approve = forms.BooleanField(required=False)
    request_reject  = forms.BooleanField(required=False)
    request_comment = forms.CharField(required=False, widget=forms.Textarea)

# Public holidays
class AddPublicHolidayForm(forms.Form):
    added_holiday_name = forms.CharField(required=True)
    added_holiday_date = forms.DateField(required=True, widget=forms.SelectDateWidget)

class RemovePublicHolidayForm(forms.Form):
    removed_holiday_date = forms.DateField(required=True, widget=forms.SelectDateWidget)

# Miscellanous
class CarouselForm(forms.Form):
    user_id = forms.IntegerField(widget=forms.HiddenInput)

class PreviewForm(forms.Form):
    selected_month = forms.IntegerField(required=True)