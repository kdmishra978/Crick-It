from django.shortcuts import render, HttpResponse
from django.contrib import messages
import random
from Teams.models import Team

def handle_toss(request, team1, team2):
    team1 = Team.objects.get(name__iexact=team1)
    team2 = Team.objects.get(name__iexact=team2)
    if request.method == "GET":
        try:
            return render(request, 'Toss.html', {'team1':team1.name, 'team2':team2.name})
        except Exception as e:
            print(e)
            return HttpResponse("Error")
    else:
        try:
            team1_coin = None
            team2_coin = request.POST['team2_coin']
            if team2_coin.lower() == "heads": team1_coin='Tails'
            else: team1_coin='Heads'
            if team1_coin == team2_coin:
                messages.error(request, "Both of the teams can't have same coin.")
                return render(request, 'Toss.html', {'team1':team1.name, 'team2':team2.name})
            else:
                choices = ['Heads', 'Tails']
                result = random.choice(choices)
                won = team1 if team1_coin == result else team2
                return render(request, 'TossResult.html', {'result':result, 'won':won, 'team1':team1.name, 'team2':team2.name})
        except Exception as e:
            print(e)
            return HttpResponse("Error")