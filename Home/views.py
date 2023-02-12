from django.shortcuts import render, redirect
from Players.models import Player
from Teams.models import Team

# Create your views here.
def home_page(request):
    if request.method == "POST":
        team_name = request.POST['team_name'].upper()
        owner_name = request.POST['owner'].upper()
        t = Team.objects.create(name=team_name, owner_name=owner_name)
        t.save()
        return redirect('home')
    else:
        return render(request, "home.html")

def refresh(request):
    teams = Team.objects.all()
    for team in teams:
        team.delete()
    players = Player.objects.filter(available=False)
    for p in players:
        p.available = True
        p.save()
    return redirect('home')