from django import forms

class EventForm(forms.Form):
    intern = forms.IntegerField(required=True)
    reason = forms.CharField(max_length=200, required=True)
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    half_day = forms.BooleanField(required=False)
 
class CancelEventForm(forms.Form):
    cancel_event = forms.IntegerField(widget=forms.HiddenInput())