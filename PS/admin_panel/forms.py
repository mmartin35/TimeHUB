from django import forms

class EventApprovalForm(forms.Form):
    approve_event = forms.BooleanField(required=False)
    reject_event = forms.BooleanField(required=False)
    archive_event = forms.BooleanField(required=False)
    comment_staff = forms.CharField(required=False, widget=forms.Textarea)
    event_id = forms.IntegerField(widget=forms.HiddenInput)
