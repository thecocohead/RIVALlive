from django.http import HttpResponse
from .models import Event
from .models import Match

def index(request):
    events = Event.objects.order_by('event_start_date')

    output = "<style>table, th, td {  border:1px solid black; } </style><table><tr><th>Event Code</th><th>Event Name</th><th>Event Start Date</th><th>Event End Date</th></tr>"

    for event in events:
        startDate = event.event_start_date.strftime("%B %d, %Y")
        endDate = event.event_end_date.strftime("%B %d, %Y")
        # table row header
        output += "<tr>"
        # table row
        output += f"<td><a href=/event/{event.event_code}>{event.event_code}</a></td><td> <b>{event.event_name}</b> </td><td>{startDate}</td><td> {endDate}"
        # table row footer
        output += "</tr>"
    # table footer
    output += "</table>"
    return HttpResponse(output)

def event(request, event_code):
    event = Event.objects.get(event_code=event_code)
    startDate = event.event_start_date.strftime("%B %d, %Y")
    endDate = event.event_end_date.strftime("%B %d, %Y")
    # Header
    output = ""
    output += "<style>table, th, td {  border:1px solid black; } </style>"
    # Event Information
    output += f"<h1>{event.event_name}</h1>"
    output += f"From {startDate} to {endDate}<br>"
    # Teams
    output += "Teams:<br><ul>"
    for team in event.teams.all():
        output += f"<li>{team.team_name}</li>"
    # Schedule
    output += ("Schedule:<br>"
               "<table>"
               "<tr>"
               "<th>Match</th><th>Time</th><th>Red Teams</th><th>Blue Teams</th><th>Red Score</th><th>Blue Score</th>")
    for match in Match.objects.filter(event=event):
        output += f"<tr><td>{match.phase} {match.nbr}</td><td>{match.scheduled_time}</td><td>{match.redTeam1} {match.redTeam2}</td><td>{match.blueTeam1} {match.redTeam2}</td><td>{match.redScore}</td><td>{match.blueScore}</td></tr>"

    # Back Button
    output += "</ul><br><a href=/>Back</a>"
    return HttpResponse(output)