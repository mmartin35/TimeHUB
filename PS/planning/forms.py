from django import forms

class RequestEventForm(forms.Form):
    intern_id = forms.IntegerField(required=True)
    reason = forms.CharField(max_length=200, required=True)
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    is_half_day = forms.BooleanField(required=False)
 
class CancelEventForm(forms.Form):
    event_id = forms.IntegerField(widget=forms.HiddenInput())