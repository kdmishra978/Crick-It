from django.shortcuts import render, HttpResponse, redirect
from Teams.models import Team, Stadium
from Players.models import Player
import json
from Virtual_Cricket_League.match import Match as mt
from Virtual_Cricket_League.Team import Team as tm
import random

# Create your views here.
def set_team(request, team_name):
    try:
        team = Team.objects.get(name__iexact=team_name)
        players = sorted(team.players.all(), key=lambda x:x.batskill-x.age, reverse=True)
        if request.method == "POST":
            player1, player2, player3, player4, player5, player6, player7, player8, player9, player10, player11 = request.POST['player1'], request.POST['player2'], request.POST['player3'], request.POST['player4'], request.POST['player5'], request.POST['player6'], request.POST['player7'], request.POST['player8'], request.POST['player9'], request.POST['player10'], request.POST['player11']
            captain = request.POST['captain']
            if captain == "null":
                print("captain is not assigned.")
                return render(request, "setTeam.html", {'team':team, 'players':players})
            wicketkeeper = request.POST['wicketkeeper']
            if wicketkeeper == "null":
                print("wktkeeper is not assigned.")
                return render(request, "setTeam.html", {'team':team, 'players':players})
            
            players_list = [player1, player2, player3, player4, player5, player6, player7, player8, player9, player10, player11]
            players_list = [" ".join(player.split('-')) for player in players_list]
            
            total_overs = 0
            battingLineup = ""
            bowling = ""    
            
            # for default bowling lineup
            # original_players = []
            # for player in players_list:
            #     p = Player.objects.get(name__iexact=player)
            #     original_players.append(p)
            
            # temp_team = tm(original_players)
            # for bowler in temp_team.bowlingLineup:
            #     bowling+=(bowler.name+"\n") 
            
            bowler_dict = {}     
            for player in players_list:
                battingLineup+=(player+"\n")
                overs = int(request.POST[player])
                total_overs += overs
                bowler_dict[player] = overs
                # for i in range(overs):
                #     bowling+=(player+"\n")
            
            total = 20
            ct=0
            bowler_dict = dict(reversed(list(bowler_dict.items())))
            while ct!=total:
                for bowler in bowler_dict:
                    if bowler_dict[bowler]!=0:
                        bowling+=(bowler+"\n")
                        ct+=1
                        bowler_dict[bowler]-=1
            
            if total_overs != 20:
                print("overs are not assigned correctly.")
                return render(request, "setTeam.html", {'team':team, 'players':players})
            else:
                captain = Player.objects.get(name__iexact=captain)
                wicketkeeper = Player.objects.get(name__iexact=wicketkeeper)
                team.captain = captain
                team.wicketkeeper = wicketkeeper
                team.battingLineup = battingLineup
                team.bowlingLineup = bowling
                team.lineup_flag = True
                team.save()
                return redirect('home')
        else:
            return render(request, "setTeam.html", {'team':team, 'players':players})
    except Exception as e:
        print(e)
        return redirect('home')
    
def get_team_data(request, team_name):
    data = {}
    try:
        print(team_name)
        team = Team.objects.get(name__iexact=team_name)
        data = json.loads(team.get_team_details()) #returns the complete data so that we can easily create an oject for our local class Team 
        players = []
        for player in team.players.all():
            if player.name in team.battingLineup:
                players.append(player)
        
        print(len(players))        
    except Exception as e:
        print(e)
    return HttpResponse("hi")