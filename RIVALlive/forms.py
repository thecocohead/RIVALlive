import datetime

from django import forms

class SchedulerForm(forms.Form):
    rounds = forms.IntegerField(min_value=1)
    cycleTime = forms.FloatField(min_value=0)
    startTime = forms.DateTimeField(initial=datetime.datetime.now())
