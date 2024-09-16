from django import forms

class EventForm(forms.Form):
    reason = forms.CharField(max_length=200, required=True)
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    half_day_start = forms.IntegerField(required=True)
    half_day_end = forms.IntegerField(required=True)
