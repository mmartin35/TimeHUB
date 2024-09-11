from django import forms

class ReportForm(forms.Form):
    name = forms.CharField(max_length=50, required=False)
    subject = forms.CharField(max_length=100, required=True)
    detailed = forms.CharField(widget=forms.Textarea, max_length=400, required=True)
    contact = forms.CharField(max_length=100, required=False)
