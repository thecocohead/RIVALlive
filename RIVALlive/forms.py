from django import forms

class ScheduleGenerationForm(forms.Form):
    rounds = forms.IntegerField(min_value=1)
    cycleTime = forms.IntegerField(min_value=0)
    startTime = forms.DateTimeField()