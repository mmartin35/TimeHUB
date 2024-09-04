from django import forms

class EventForm(forms.Form):
    title = forms.CharField(max_length=200, required=True)
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    duration = forms.IntegerField(min_value=1, required=True, help_text="Duration in days")
