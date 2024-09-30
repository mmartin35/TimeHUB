from django import forms

class PointerForm(forms.Form):
    t1 = forms.TimeField()
    t2 = forms.TimeField()
    t3 = forms.TimeField()
    t4 = forms.TimeField()

class ServiceForm(forms.Form):
    t1_service = forms.TimeField()
    t2_service = forms.TimeField()
