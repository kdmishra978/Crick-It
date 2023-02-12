from email.errors import NonPrintableDefect
from django.shortcuts import render, redirect
from Players.models import Player
from Teams.models import Team
from django.db.models import Q

# Create your views here.
def players_page(request):
    return render(request, 'players.html')

def display_players(request, view):
    try:
        players = None
        if view == "batsman":
            players = Player.objects.filter(playertype__iexact=view, available=True)
            players = sorted(players, key=lambda x:x.batskill, reverse=True)
        elif view == "bowler":
            players = Player.objects.filter(playertype__iexact=view, available=True)
            players = sorted(players, key=lambda x:x.bowlskill, reverse=True)
        elif view == "allrounder":
            players = Player.objects.filter(playertype__iexact=view, available=True)
            players = sorted(players, key=lambda x:x.bowlskill+x.batskill, reverse=True)
        elif view == "wicketkeeperbatsman":
            players = Player.objects.filter(playertype__iexact=view, available=True)
            players = sorted(players, key=lambda x:x.wktskill+x.batskill, reverse=True)
        elif view == "underdogs":
            players = Player.objects.filter(Q(experience__lte=72), available=True)
        elif view == "elite":
            players = Player.objects.filter(Q(experience__lte=79) & Q(experience__gte=73), available=True)
        elif view == "masters":
            players = Player.objects.filter(Q(experience__lte=86) & Q(experience__gte=80), available=True)
        elif view == "legends":
            players = Player.objects.filter(Q(experience__lte=100) & Q(experience__gte=87), available=True)
        else:
            return redirect('players')
        
        print(len(players))
        
        return render(request, "PlayersList.html", {'view':view, 'players':players})
    except Exception as e:
        print(e, "error")
        return redirect('players')

def sort_players(request, view, sort_type):
    try:
        players = Player.objects.filter(playertype__iexact=view, available=True)
        
        players = None
        
        if view == "batsman":
            players = Player.objects.filter(playertype__iexact=view, available=True)
            players = sorted(players, key=lambda x:x.batskill, reverse=True)
        elif view == "bowler":
            players = Player.objects.filter(playertype__iexact=view, available=True)
            players = sorted(players, key=lambda x:x.bowlskill, reverse=True)
        elif view == "allrounder":
            players = Player.objects.filter(playertype__iexact=view, available=True)
            players = sorted(players, key=lambda x:x.bowlskill+x.batskill, reverse=True)
        elif view == "wicketkeeperbatsman":
            players = Player.objects.filter(playertype__iexact=view, available=True)
            players = sorted(players, key=lambda x:x.wktskill+x.batskill, reverse=True)
        elif view == "underdogs":
            players = Player.objects.filter(Q(experience__lte=70), available=True)
        elif view == "elite":
            players = Player.objects.filter(Q(experience__lte=79) & Q(experience__gte=71), available=True)
        elif view == "masters":
            players = Player.objects.filter(Q(experience__lte=87) & Q(experience__gte=80), available=True)
        elif view == "legends":
            players = Player.objects.filter(Q(experience__lte=100) & Q(experience__gte=88), available=True)
        else:
            return redirect('players')
        
        if sort_type == "skills":
            if view == "batsman":
                players = sorted(players, key=lambda x:x.batskill, reverse=True)
            elif view == "bowler":
                players = sorted(players, key=lambda x:x.bowlskill, reverse=True)
            elif view == "allrounder":
                players = sorted(players, key=lambda x:x.bowlskill+x.batskill, reverse=True)
            elif view == "underdogs":
                players = sorted(players, key=lambda x:x.bowlskill+x.batskill, reverse=True)
            elif view == "elite":
                players = sorted(players, key=lambda x:x.bowlskill+x.batskill, reverse=True)
            elif view == "masters":
                players = sorted(players, key=lambda x:x.bowlskill+x.batskill, reverse=True)
            elif view == "legends":
                players = sorted(players, key=lambda x:x.bowlskill+x.batskill, reverse=True)
            else:
                players = sorted(players, key=lambda x:x.wktskill+x.batskill, reverse=True)
        elif sort_type == "age":
            players = sorted(players, key=lambda x:x.age)
        else:
            players = sorted(players, key=lambda x:x.experience, reverse=True)
        
        return render(request, "PlayersList.html", {'view':view, 'players':players})
    except Exception as e:
        print(e, "error")
        return redirect('players')

def view_player(request, view, name):
    if request.method == "GET":
        try:
            p = Player.objects.get(name__iexact=name)
            batorder = eval(p.battingorder)
            order = None
            batmax = batorder.index(max(batorder))+1
            if 1 <= batmax <= 3:
                order = "TOP ORDER"
            elif 4 <= batmax <= 5:
                order = "MIDDLE ORDER"
            elif 6 <= batmax <= 7:
                order = "FINISHER"
            else:
                order = "TAIL-ENDER"
            
            base_price = None
            if p.experience >= 88:
                base_price = "2 CRORES"
            elif p.experience >= 81:
                base_price = "1 CRORES"
            elif p.experience >= 71:
                base_price = "50 LAKHS"
            else:
                base_price = "20 LAKHS"
            # if p.playertype == "batsman":
            #     if p.batskill >= 85:
            #         base_price = "2 CRORES"
            #     elif p.batskill >= 80:
            #         base_price = "1 CRORES"
            #     elif p.batskill >= 70:
            #         base_price = "50 LAKHS"
            #     else:
            #         base_price = "20 LAKHS"
            # elif p.playertype == "bowler":
            #     if p.bowlskill >= 85:
            #         base_price = "2 CRORES"
            #     elif p.bowlskill >= 80:
            #         base_price = "1 CRORES"
            #     elif p.bowlskill >= 70:
            #         base_price = "50 LAKHS"
            #     else:
            #         base_price = "20 LAKHS"
            # elif p.playertype == "wicketkeeperbatsman":
            #     if p.wktskill >= 85:
            #         base_price = "2 CRORES"
            #     elif p.wktskill >= 80:
            #         base_price = "1 CRORES"
            #     elif p.wktskill >= 70:
            #         base_price = "50 LAKHS"
            #     else:
            #         base_price = "20 LAKHS"
            # else:
            #     if p.batskill >= 85 or p.bowlskill >= 85:
            #         base_price = "2 CRORES"
            #     elif p.batskill >= 80 or p.bowlskill >= 80:
            #         base_price = "1 CRORES"
            #     elif p.batskill >= 70 or p.bowlskill >= 70:
            #         base_price = "50 LAKHS"
            #     else:
            #         base_price = "20 LAKHS"
            
            return render(request, "viewPlayer2.html", {'player':p, 'order':order, 'base_price':base_price, 'view':view})
        except Exception as e:
            print(e, "error")
            return redirect('players')
    else:
        original = request.POST['price'].split(" ")
        print(original)
        if original[1] == "LAKHS":
            price = float(original[0])*0.01
        else:
            price = float(original[0])
        team_name = request.POST['teamname']
        team = Team.objects.get(name__iexact=team_name)
        player = Player.objects.get(name__iexact=name)
        
        if player.available:
            if team.bugdet >= price:
                team.players.add(player)
                team.bugdet -= round(price, ndigits=2)
                player.available = False
                player.save()
                team.save()
                
                teams = Team.objects.all()
                
                return render(request, "BUDGET_CONGRATS.html", {'type':player.playertype, 'team':team_name, 'teams':teams})
            else:
                #not enough budget
                pass 
        else:
            #player not available
            pass
        
        return redirect('players')