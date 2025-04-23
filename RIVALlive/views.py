from django.http import HttpResponse
from django.shortcuts import render
from .models import Event
from .models import Match
from .forms import ScheduleGenerationForm

def index(request):
    events = Event.objects.order_by('startDate')
    output = []
    for event in events:
        newEvent = {
            "code": event.code,
            "name": event.name,
            "startDate": event.startDate.strftime("%B %d, %Y"),
            "endDate": event.endDate.strftime("%B %d, %Y")
        }
        output.append(newEvent)
    data = {
        "events": output,
    }
    return render(request, 'index.html', data)

def event(request, code):
    event = Event.objects.get(code=code)
    startDate = event.startDate.strftime("%B %d, %Y")
    endDate = event.endDate.strftime("%B %d, %Y")

    data = {
        "event" : event,
        "startDate" : startDate,
        "endDate" : endDate,
        "teams" : event.teams.all(),
        "matches" : Match.objects.filter(event=event),
    }

    return render(request, "event.html", data)