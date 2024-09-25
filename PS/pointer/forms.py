from django import forms

class PointerForm(forms.Form):
    t1 = forms.TimeField()
    t2 = forms.TimeField()
    t3 = forms.TimeField()
    t4 = forms.TimeField()
