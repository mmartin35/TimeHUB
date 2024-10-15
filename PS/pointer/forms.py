from django import forms

class RequestDailyTimerForm(forms.Form):
    date = forms.DateField()
    comment = forms.CharField(widget=forms.Textarea)

    t1 = forms.TimeField()
    t2 = forms.TimeField()
    t3 = forms.TimeField()
    t4 = forms.TimeField()