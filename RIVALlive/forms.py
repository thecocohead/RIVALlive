import datetime

from django import forms

from RIVALlive.models import ScoreDetail


class SchedulerForm(forms.Form):
    rounds = forms.IntegerField(min_value=1)
    cycleTime = forms.FloatField(min_value=0)
    startTime = forms.DateTimeField(initial=datetime.datetime.now())

class ScoreForm(forms.ModelForm):
    class Meta:
        model = ScoreDetail
        fields = ['nearL0normalMissile',
                  'nearL0bonusMissile',
                  'nearL1normalMissile',
                  'nearL1bonusMissile',
                  'nearL2normalMissile',
                  'nearL2bonusMissile',
                  'nearL3normalMissile',
                  'nearL3bonusMissile',
                  'farL0normalMissile',
                  'farL0bonusMissile',
                  'farL1normalMissile',
                  'farL1bonusMissile',
                  'farL2normalMissile',
                  'farL2bonusMissile',
                  'farL3normalMissile',
                  'farL3bonusMissile',
                  'robot1Fortify',
                  'robot2Fortify',
                  'penalties',
                  'robot1dq',
                  'robot2dq']