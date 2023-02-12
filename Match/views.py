from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from Teams.models import Team
from Players.models import Player
from Virtual_Cricket_League.match import Match as mt
from Virtual_Cricket_League.Team import Team as tm
import random
import json

scorecard = dict()

# Create your views here.
def home(request):
    teams = Team.objects.all()
    return render(request, "matchhome.html", {'teams':teams})

def startmatch(request):
    try:
        if request.method == "POST":
            team1_name = request.POST['team1']
            team2_name = request.POST['team2']
            
            team1 = Team.objects.get(name__iexact=team1_name)
            team2 = Team.objects.get(name__iexact=team2_name)
            
            team1_players = team1.players.all()
            team2_players = team2.players.all()
    
            team1_data = json.loads(team1.get_team_details())
            team2_data = json.loads(team2.get_team_details())
            
            t1 = tm(team1_data)
            t2 = tm(team2_data)            
                        
            team1_lineup = t1.battingLineup
            team2_lineup = t2.battingLineup
            
            if team1.battingLineup.lower() == "not set" or team1.battingLineup == "":
                if len(team1.players.all()) != 11:
                    print("error, please set team1 correctly")
                    return redirect('matchhome')
                else:
                    default_lineup = ""
                    count = 0
                    for i in t1.battingLineup:
                        count += 1
                        default_lineup += i.name
                        if count != 11:    
                            default_lineup += "\n"
                    team1.battingLineup = default_lineup
                    team1.save()
            else:
                print("set1")
                lineup = team1.battingLineup.split("\n")
                print(lineup)
                count = 0
                for l in lineup:
                    if l == '':
                        continue
                    if l[-1] == "\r":
                        lineup[count] = l[0:-1]
                    else:
                        pass
                    count += 1
                count = 0
                for player in lineup:
                    for p in team1.players.all():
                        if p.name.lower() == player.lower():
                            count += 1
                print(count)
                if count == 11:
                    team1_lineup = lineup
            
            if team2.battingLineup.lower() == "not set" or team2.battingLineup == "":
                if len(team2.players.all()) != 11:
                    print("error, please set team2 correctly")
                    return redirect('matchhome')
                else:
                    default_lineup = ""
                    count = 0
                    for i in t1.battingLineup:
                        count += 1
                        default_lineup += i.name
                        if count != 11:    
                            default_lineup += "\n"
                    team2.battingLineup = default_lineup
                    team2.save()
            else:
                print("set2")
                lineup = team2.battingLineup.split("\n")
                count = 0
                for l in lineup:
                    if l == '':
                        continue
                    if l[-1] == "\r":
                        lineup[count] = l[0:-1]
                    else:
                        pass
                    count += 1
                count = 0
                for player in lineup:
                    for p in team2.players.all():
                        if p.name.lower() == player.lower():
                            count += 1
                print(count)
                if count == 11:
                    team2_lineup = lineup
                
            #bowling
            t1flg = True
            t2flg = True
            team1_bowling_lineup = t1.bowlingLineup
            if len(t1.bowlingLineup) < 20:
                t1flg = False
            team2_bowling_lineup = t2.bowlingLineup
            if len(t2.bowlingLineup) < 20:
                t2flg = False
            
            if t1flg:
                if team1.bowlingLineup.lower() == "not set" or team1.bowlingLineup == "":
                    default_lineup = ""
                    count = 0
                    for i in t1.bowlingLineup:
                        count += 1
                        default_lineup += i.name
                        if count != 20:    
                            default_lineup += "\n"
                    team1.bowlingLineup = default_lineup
                    team1.save()
                else:
                    lineup = team1.bowlingLineup.split("\n")
                    count = 0
                    for i in range(20):
                        for j in range(20):
                            if team1_bowling_lineup[i].name.lower() == lineup[j].lower():
                                count += 1
                    if count == 20:
                        team1_bowling_lineup = lineup
            
            else:
                team1_bowling_lineup = team1.bowlingLineup.split("\n")
            
            if t2flg:    
                if team2.bowlingLineup.lower() == "not set":
                    default_lineup = ""
                    count = 0
                    for i in t2.bowlingLineup:
                        count += 1
                        default_lineup += i.name 
                        if count != 20:
                            default_lineup += "\n"
                    team2.bowlingLineup = default_lineup
                    team2.save()
                else:
                    lineup = team2.bowlingLineup.split("\n")
                    count = 0
                    for i in range(20):
                        for j in range(20):
                            if team2_bowling_lineup[i] == lineup[j]:
                                count += 1
                    if count == 20:
                        team2_bowling_lineup = lineup
            else:
                team2_bowling_lineup = team2.bowlingLineup.split("\n")   
                
            return render(request, "startmatch.html", {'team1':team1, 'team2':team2, 'team1_players':team1_players, 'team2_players':team2_players, 'team1_lineup':team1_lineup, 'team2_lineup':team2_lineup, 'team1_bowling_lineup':team1_bowling_lineup, 'team2_bowling_lineup':team2_bowling_lineup})
        
        else:
            print("get method")
    except Exception as e:
        print(e, 'error')
        return redirect('matchhome')

def handle_match(request, team1, team2):
    try:
        team1 = Team.objects.get(name__iexact=team1)
        team2 = Team.objects.get(name__iexact=team2)
        if request.method == "POST":
            won = request.POST['won']
            try:
                selected = request.POST['selected']
                message = won + " has won the toss and selected to " + selected + " first."
                
                team1_data = json.loads(team1.get_team_details())
                team2_data = json.loads(team2.get_team_details())                
                
                
                team1 = tm(team1_data, flag=True)
                team2 = tm(team2_data, flag=True)
                
                # homeground = random.choice([team1.homeGround, team2.homeGround])
                homeground = team1.homeGround
                bat_team = None
                bowl_team = None
                if won == team1.name:
                    if selected == "bat":
                        bat_team = team1
                        bowl_team = team2
                    else:
                        bat_team = team2
                        bowl_team = team1
                else:
                    if selected == "bat":
                        bat_team = team2
                        bowl_team = team1
                    else:
                        bat_team = team1
                        bowl_team = team2
                
                players = []
                for player in bat_team.players:
                    if player.name in bat_team.battingLineup:
                        players.append(player)
                bat_team.players = players
                
                players = []
                for player in bowl_team.players:
                    if player.name in bowl_team.battingLineup:
                        players.append(player)
                bowl_team.players = players
                
                match = mt(bat_team, bowl_team, homeground, 20, homeground.averageRuns)
                match.startMatch()
                
                global scorecard
                between = str(team1.name) + str(' vs ') + str(team2.name)
                scorecard[between] = match.getScorecardDetails()
                
                scoreboard = scorecard[between]
                
                temp1 = scoreboard[1]['battingTeam']
                temp2 = scoreboard[2]['battingTeam']
                
                team1__print_name = str()
                team2__print_name = str()
                # Edited ADI:
                temp1 = temp1.split()
                temp2 = temp2.split()

                if len(temp1) == 1:
                    if len(temp1[0]) > 4:
                        team1__print_name = temp1[0][:3] # three letters
                    else:
                        team1__print_name = temp1[0]
                else:
                    for i in temp1:
                        if i.isdigit():
                            team1__print_name += i 
                        else:
                            team1__print_name += i[0]
                team1__print_name = team1__print_name[:4]

                if len(temp2) == 1:
                    if len(temp2[0]) > 4:
                        team2__print_name = temp2[0][:3] # three letters
                    else:
                        team2__print_name = temp2[0]
                else:
                    for i in temp2:
                        if i.isdigit():
                            team2__print_name += i 
                        else:
                            team2__print_name += i[0]
                team2__print_name = team2__print_name[:4]
                       
                return render(request, 'ResultPage.html', {'team1':team1, 'team2':team2, 'battingTeam1':scoreboard[1]['battingTeam'], 'bowlingTeam1':scoreboard[1]['bowlingTeam'], 'battingTeam2':scoreboard[2]['battingTeam'], 'bowlingTeam2':scoreboard[2]['bowlingTeam'],'winner':scoreboard['winner'], 'team1_print_name':team1__print_name, 'team2_print_name':team2__print_name})
            except Exception as e:
                print(e, 'error')
                return HttpResponse("Error")
        else:
            return HttpResponse("None")
    except Exception as e:
        print(e)
        return HttpResponse("Error")
    
def get_json_response(request, team1, team2):
    global scorecard
    return JsonResponse(scorecard)

def get_player_json(request, team1, team2, name):
    try:
        player = Player.objects.get(name__iexact=name)
        return JsonResponse({'img_href':player.image.url})
    except Exception as e:
        print(e)
        return JsonResponse({'good':False})

def set_lineup(request, team1, team2):
    if request.method == "POST":
        t1_lineup = eval(request.POST['t1_data'])
        t2_lineup = eval(request.POST['t2_data'])
        t1_bowl_lineup = eval(request.POST['t1_bowl_data'])
        t2_bowl_lineup = eval(request.POST['t2_bowl_data'])
        
        team1 = Team.objects.get(name__iexact=team1)
        team2 = Team.objects.get(name__iexact=team2)
        
        t1 = ""
        t2 = ""
        for i in range(11):
            temp = t1_lineup[i].split(" ")
            if "(C)" in temp:
                temp.remove("(C)")
                t1_lineup[i] = " ".join(temp)
            if "(WK)" in temp:
                temp.remove("(WK)")
                t1_lineup[i] = " ".join(temp)
            temp = t2_lineup[i].split(" ")
            if "(C)" in temp:
                temp.remove("(C)")
                t2_lineup[i] = " ".join(temp)
            if "(WK)" in temp:
                temp.remove("(WK)")
                t2_lineup[i] = " ".join(temp)
            t1 += t1_lineup[i]
            t2 += t2_lineup[i]
            if i != 10:
                t1 += "\n"
                t2 += "\n"
        
        team1.battingLineup = t1
        team2.battingLineup = t2
        
        t1 = ""
        t2 = ""
        for i in range(20):
            temp = t1_bowl_lineup[i].split(" ")
            temp = temp[0:]
            t1 += " ".join(temp)
            temp = t2_bowl_lineup[i].split(" ")
            temp = temp[0:]
            t2 += " ".join(temp)
            if i != 19:
                t1 += "\n"
                t2 += "\n"
        
        team1.bowlingLineup = t1
        team1.lineup_flag = True
        
        team2.bowlingLineup = t2
        team2.lineup_flag = True 
        
        team1.save()
        team2.save()
    return JsonResponse({'h':'hello'})