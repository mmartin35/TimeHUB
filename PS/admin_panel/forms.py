from django import forms

class EventApprovalForm(forms.Form):
    event_id = forms.IntegerField(widget=forms.HiddenInput)
    approve_event = forms.BooleanField(required=False)
    reject_event = forms.BooleanField(required=False)
    staff_comment = forms.CharField(required=False, widget=forms.Textarea)
