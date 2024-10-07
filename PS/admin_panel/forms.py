from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class InternUserCreationForm(UserCreationForm):
    arrival = forms.DateField(required=True, widget=forms.SelectDateWidget)
    departure = forms.DateField(required=True, widget=forms.SelectDateWidget)
    regime = forms.IntegerField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class EventApprovalForm(forms.Form):
    event_id = forms.IntegerField(widget=forms.HiddenInput)
    approve_event = forms.BooleanField(required=False)
    reject_event = forms.BooleanField(required=False)
    staff_comment = forms.CharField(required=False, widget=forms.Textarea)

class ServiceTimerForm(forms.Form):
    service_id = forms.IntegerField(widget=forms.HiddenInput)
    service_comment = forms.CharField(required=False, widget=forms.Textarea)