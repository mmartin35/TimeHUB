from django import forms

class PointerForm(forms.Form):
    date = forms.DateField()
    work_start_morning = forms.TimeField()
    work_end_morning = forms.TimeField()
    work_start_afternoon = forms.TimeField()
    work_end_afternoon = forms.TimeField()
