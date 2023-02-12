from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from Tournament.models import Tournament
from Teams.models import Team
# Create your views here.
def starttournament_page(request):
    if request.method == "POST":
        try:
            name = request.POST['name'].upper()
            venue = request.POST['venue'].upper()
            budget = request.POST['budget']
            number_of_teams = request.POST['number_of_teams']
            overs = request.POST['overs']
            new_tournament = Tournament.objects.create(name=name, venue=venue, auction_budget=budget, number_of_teams=number_of_teams, overs=overs)
            new_tournament.save()
            redirection = "/tournament/"+str(name.lower())+str("/")
            return redirect(redirection)
        except Exception as e:
            print(e)
    else:
        pass    
    return render(request, 'starttournament.html')

def base(request, name):
    try:    
        tournament = Tournament.objects.get(name__iexact=name)
        teams = tournament.teams.all()
        if request.method == "POST":
            if len(teams) < tournament.number_of_teams:
                team_name = request.POST['team_name'].upper()
                owner = request.POST['owner'].title()
                team = Team.objects.create(name=team_name, owner_name=owner)
                team.save()
                tournament.teams.add(team)
                tournament.save()
            else:
                print("LIMIT EXCEEDED TO ADD TEAMS IN A TOURNAMENT")
        else:
            pass
        return render(request, "TournamentPage.html", {'tournament':tournament, 'teams':teams})

    except Exception as e:
        print(e)
        return redirect('/')

def pointstable(request, name):
    try:
        tournament = Tournament.objects.get(name__iexact=name)
        teams = tournament.teams.all()
        return render(request, "pointsTable.html", {'tournament':tournament, 'teams':teams})
    except:
        return redirect('/')

def auction(request, name):
    try:
        tournament = Tournament.objects.get(name__iexact=name)
        teams = tournament.teams.all()
        return redirect('http://localhost:8000/players/batsman/')
    except:
        return redirect('/')