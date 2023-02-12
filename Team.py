from pmt import PlayerMatchTime
from Stadium import *
from math import ceil, floor
import random

class Team:
    def __init__(self, data, flag=False):
        self.name = data['name']
        self.players = self.generate_players_list(data['players'])
        self.captain = PlayerMatchTime(data['captain'], self.name)
        self.wktKeeper = PlayerMatchTime(data['wktkeeper'], self.name)
        self.homeGround = Stadium(data['homeground'])
        
        self.lineup_flag = data['lineup_flag']
        
        self.overs = 20
        
        try:
            if flag == True:
                self.battingLineup = self.set_batting_lineup_according_to_order(data['battinglineup'].split('\n'))
            else:
                raise Exception
        except:
            self.battingLineup = self.set_default_batting_lineup()
        try:
            if self.lineup_flag == True:
                self.bowlingLineup = self.set_bowling_lineup_according_to_order(data['bowlinglineup'].split('\n'))
            else:
                raise Exception
        except Exception as e:
            self.bowlingLineup = self.set_default_bowling_lineup()
        self.batsmanBin = []
        self.bowlerBin = []
        
    def generate_players_list(self, players):
        players_list = []
        for player in players:
            p = PlayerMatchTime(player, self.name)
            players_list.append(p)
        return players_list

    @staticmethod
    def sorter(player):
        return player.batSkill
    
    def set_batting_lineup_according_to_order(self, data):
        lineup = []
        for player in data:
            for p in self.players:
                if p.name.lower() == player.lower():
                    lineup.append(p)
        return lineup
    
    def set_bowling_lineup_according_to_order(self, data):
        lineup = []
        
        for i in range(20):
            for p in self.players:
                if p.name.lower() == data[i].lower():
                    lineup.append(p)
        return lineup
    
    def set_default_batting_lineup(self):
        batting_lineup = []
        top = []
        middle = []
        finisher = []
        tailEnder = []
        
        for player in self.players:
            if player.battingType.lower() == "top":
                top.append(player)
            elif player.battingType.lower() == "middle":
                middle.append(player)
            elif player.battingType.lower() == "finisher":
                finisher.append(player)
            else:
                tailEnder.append(player)
        
        top = sorted(top, key=Team.sorter, reverse=True)
        middle = sorted(middle, key=Team.sorter, reverse=True)
        finisher = sorted(finisher, key=Team.sorter, reverse=True)
        tailEnder = sorted(tailEnder, key=Team.sorter, reverse=True)
        
        for i in range(1, 12, 1):
            if i >= 1 and i <= 3:
                if len(top) != 0:
                    batting_lineup.append(top[0])
                    top.pop(0)
                elif len(middle) != 0:
                    batting_lineup.append(middle[0])
                    middle.pop(0)
                elif len(finisher) != 0:
                    batting_lineup.append(finisher[0])
                    finisher.pop(0)
                else:
                    batting_lineup.append(tailEnder[0])
                    tailEnder.pop(0)
            elif i >= 4 and i <= 5:
                if i == 4:
                    if len(top) != 0:
                        for i in range(0, len(top)):
                            middle.append(top[0])
                            top.pop(0)
                    else:
                        pass
                middle = sorted(middle, key=Team.sorter, reverse=True)
                if len(middle) != 0:
                    batting_lineup.append(middle[0])
                    middle.pop(0)
                elif len(finisher) != 0:
                    batting_lineup.append(finisher[0])
                    finisher.pop(0)
                else:
                    batting_lineup.append(tailEnder[0])
                    tailEnder.pop(0)
            elif i >= 6 and i <= 7:
                if i == 6:
                    if len(middle) != 0:
                        for player in middle:
                            finisher.append(middle[0])
                            middle.pop(0)
                finisher = sorted(finisher, key=Team.sorter, reverse=True)
                if len(finisher) != 0:
                    batting_lineup.append(finisher[0])
                    finisher.pop(0)
                else:
                    batting_lineup.append(tailEnder[0])
                    tailEnder.pop(0)
            else:
                if i == 8:
                    if len(finisher) != 0:
                        for player in finisher:
                            tailEnder.append(finisher[0])
                            finisher.pop(0)
                tailEnder = sorted(tailEnder, key=Team.sorter, reverse=True)
                if len(tailEnder) != 0:
                    batting_lineup.append(tailEnder[0])
                    tailEnder.pop(0)
        
        if len(batting_lineup) != 11:
            for p in self.players:
                if p not in batting_lineup:
                    batting_lineup.append(p)
                    
        return batting_lineup

    @staticmethod
    def bowlsorter(player):
        return player.bowlSkill    
    
    def set_default_bowling_lineup(self):
        bowling_lineup = []
        bowlers = []
        allrounders = []
        
        for player in self.players:
            if player.playerType.lower() == "bowler":
                bowlers.append(player)
            elif player.playerType.lower() == "allrounder":
                allrounders.append(player)
            else:
                pass
        
        powerplay = []
        midover = []
        death = []
        
        for bowler in bowlers:
            if "powerplay" in bowler.bowlingOrder:
                powerplay.append(bowler)
            elif "midover" in bowler.bowlingOrder:
                midover.append(bowler)
            elif "death" in bowler.bowlingOrder:
                death.append(bowler)
            else:
                pass
        
        for bowler in allrounders:
            if "powerplay" in bowler.bowlingOrder:
                powerplay.append(bowler)
            elif "midover" in bowler.bowlingOrder:
                midover.append(bowler)
            elif "death" in bowler.bowlingOrder:
                death.append(bowler)
            else:
                pass
        
        powerplay = sorted(powerplay, key=Team.bowlsorter, reverse=True)
        midover = sorted(midover, key=Team.bowlsorter, reverse=True)
        death = sorted(death, key=Team.bowlsorter, reverse=True)
        
        remaining_overs = self.overs-(len(bowlers)*(self.overs/5))
        overs = {'bowlers':0, 'allrounders':0}
        overs['bowlers'] = len(bowlers)*(self.overs/5)
        overs['allrounders'] = remaining_overs
        
        bowler_per_over = dict()
        for bowler in bowlers:
            bowler_per_over[bowler] = (self.overs/5)
        
        allrounders = sorted(allrounders, key=Team.bowlsorter, reverse=True)
        
        if remaining_overs > 0:
            temp = remaining_overs/len(allrounders)
            i = 0
            while remaining_overs >= 0:
                if ceil(temp) >= remaining_overs:
                    temp = remaining_overs
                    remaining_overs = 0
                bowler_per_over[allrounders[i]] = ceil(temp)
                remaining_overs -= ceil(temp)
                if remaining_overs == 1:
                    bowler_per_over[allrounders[0]] += 1
                    remaining_overs = 0
                    break
                i += 1
        else:
            pass
        
        bowling_lineup = Team.getBowling(self.overs, bowler_per_over, powerplay, midover, death)
        
        if bowling_lineup == None:
            bowling_lineup = self.poor_lineup()
        
        return bowling_lineup
    
    @staticmethod
    def getBowling(overs, bowler_per_over, powerplay, midover, death):
        bowling_lineup = []
        powerplay_overs = Team.getPowerplayOvers(overs)
        death_overs = Team.getDeathOvers(overs)
        mid_overs = overs-powerplay_overs-death_overs
        
        bpo = bowler_per_over.copy()
        count = 0
        
        data = Team.setPowerplayBowler(bowler_per_over, bowling_lineup, powerplay, midover, death, powerplay_overs, count)
        bowling_lineup = data['bowling_lineup']
        bowler_per_over = data['bowler_per_over']
        count += data['count']
        
        data = Team.setMidBowler(bowler_per_over, bowling_lineup, powerplay, midover, death, mid_overs, count)
        bowling_lineup = data['bowling_lineup']
        bowler_per_over = data['bowler_per_over']
        count += data['count']
        
        data = Team.setDeathBowler(bowler_per_over, bowling_lineup, powerplay, midover, death, death_overs, count)
        bowling_lineup = data['bowling_lineup']
        bowler_per_over = data['bowler_per_over']
        count += data['count']
        
        if count == 3 or len(bowling_lineup)!=20:
            bowling_lineup = Team.getDefault(bpo, powerplay, midover, death)
        
        if bowling_lineup:
            if len(bowling_lineup) != 20:
                print('error invalid choice for bowlers.')
                bowling_lineup = None
        
        return bowling_lineup
    
    @staticmethod
    def check(bowling_lineup, bowler, bowler_per_over):
        if len(bowling_lineup) != 0:
            if bowling_lineup[len(bowling_lineup)-1] is not bowler and bowler_per_over[bowler] > 2:
                return True
            else:
                return False
        else:
            return True
    
    @staticmethod
    def check_mid_death(bowling_lineup, bowler, bowler_per_over):
        if len(bowling_lineup) != 0:
            if bowling_lineup[len(bowling_lineup)-1] is not bowler and bowler_per_over[bowler] > 0:
                return True
            else:
                return False
        else:
            return True
    
    @staticmethod  
    def check_for_overs_left(order, bowler_per_over, powerplay, midover, death):
        if order == "powerplay":
            for p in powerplay:
                if bowler_per_over[p] > 0:
                    pass
                else:
                    return False 
        elif order == "midover":
            for p in midover:
                if bowler_per_over[p] > 0:
                    pass
                else:
                    return False 
        else:
            for p in death:
                if bowler_per_over[p] > 0:
                    pass
                else:
                    return False 
        return True
    
    @staticmethod
    def getPowerplayOvers(overs):
        powerplay_overs = 0
        if overs == 20:
            powerplay_overs = 6
        elif overs == 50:
            powerplay_overs = 10
        else:
            powerplay_overs = round(overs/4.5)
        return powerplay_overs

    @staticmethod
    def getDeathOvers(overs):
        death_overs = overs//5
        return death_overs
    
    @staticmethod
    def getList(powerplay, midover, death):
        l = []
        for p in powerplay:
            if p not in l:
                l.append(p)

        for p in midover:
            if p not in l:
                l.append(p)

        for p in death:
            if p not in l:
                l.append(p)
        return l
    
    @staticmethod
    def setPowerplayBowler(bowler_per_over, bowling_lineup, powerplay, midover, death, powerplay_overs, count):
        powerplay_it = 0
        midover_it = 0
        death_it = 0
        over = 0
        
        found = False
        
        while over != powerplay_overs:
            try:
                if len(powerplay) != 0:
                    if Team.check_for_overs_left("powerplay", bowler_per_over, powerplay, midover, death):
                        if Team.check(bowling_lineup, powerplay[powerplay_it], bowler_per_over):
                            bowling_lineup.append(powerplay[powerplay_it])
                            bowler_per_over[powerplay[powerplay_it]] -= 1
                            powerplay_it += 1
                            over += 1
                            if powerplay_it >= (len(powerplay)-1):
                                powerplay_it = 0
                        else:
                            if powerplay_it >= (len(powerplay)-1):
                                found = True
                                powerplay_it = 0
                            else:
                                powerplay_it += 1
                    else:
                        found = True
                else:
                    found = True
                
                if found == True:
                    found = False
                    if len(midover) != 0:
                        if Team.check_for_overs_left("midover", bowler_per_over, powerplay, midover, death):
                            if Team.check_mid_death(bowling_lineup, midover[midover_it], bowler_per_over):
                                bowling_lineup.append(midover[midover_it])
                                bowler_per_over[midover[midover_it]] -= 1
                                midover_it += 1
                                over += 1
                                if midover_it >= (len(midover)-1):
                                    midover_it = 0
                            else:
                                if midover_it >= (len(midover)-1):
                                    found = True
                                    midover_it = 0
                                else:
                                    midover_it += 1
                        else:
                            found = True
                    else:
                        found = True
                
                if found == True:
                    found = False
                    if len(death) != 0:
                        if Team.check_for_overs_left("death", bowler_per_over, powerplay, midover, death):
                            if Team.check_mid_death(bowling_lineup, death[death_it], bowler_per_over):
                                bowling_lineup.append(death[death_it])
                                bowler_per_over[death[death_it]] -= 1
                                death_it += 1
                                over += 1
                                if death_it >= (len(death)-1):
                                    death_it = 0
                            else:
                                if death_it >= (len(death)-1):
                                    found = True
                                    death_it = 0
                                else:
                                    death_it += 1
                        else:
                            found = True
                    else:
                        found = True
                        

                if found == True:
                    count += 1
                    break
                
            except Exception as e:
                break
        
        return {'bowling_lineup':bowling_lineup, 'count':count, 'bowler_per_over':bowler_per_over} 
    
    @staticmethod
    def setMidBowler(bowler_per_over, bowling_lineup, powerplay, midover, death, mid_overs, count):
        powerplay_it = 0
        midover_it = 0
        death_it = 0
        over = 0
        
        found = False
        
        while over != mid_overs:
            try:
                if len(midover) != 0:
                    if Team.check_for_overs_left("midover", bowler_per_over, powerplay, midover, death):
                        if Team.check_mid_death(bowling_lineup, midover[midover_it], bowler_per_over):
                            bowling_lineup.append(midover[midover_it])
                            bowler_per_over[midover[midover_it]] -= 1
                            midover_it += 1
                            over += 1
                            if midover_it >= (len(midover)-1):
                                midover_it = 0
                        else:
                            if midover_it >= (len(midover)-1):
                                found = True
                                midover_it = 0
                            else:
                                midover_it += 1
                    else:
                        found = True
                else:
                    found = True
                
                if found == True:
                    found = False
                    if len(powerplay) != 0:
                        if Team.check_for_overs_left("powerplay", bowler_per_over, powerplay, midover, death):
                            if Team.check_mid_death(bowling_lineup, powerplay[powerplay_it], bowler_per_over):
                                bowling_lineup.append(powerplay[powerplay_it])
                                bowler_per_over[powerplay[powerplay_it]] -= 1
                                powerplay_it += 1
                                over += 1
                                if powerplay_it >= (len(powerplay)-1):
                                    powerplay_it = 0
                            else:
                                if powerplay_it >= (len(powerplay)-1):
                                    found = True
                                    powerplay_it = 0
                                else:
                                    powerplay_it += 1
                        else:
                            found = True
                    else:
                        found = True
                
                if found == True:
                    found = False
                    if len(death) != 0:
                        if Team.check_for_overs_left("death", bowler_per_over, powerplay, midover, death):
                            if Team.check_mid_death(bowling_lineup, death[death_it], bowler_per_over):
                                bowling_lineup.append(death[death_it])
                                bowler_per_over[death[death_it]] -= 1
                                death_it += 1
                                over += 1
                                if death_it >= (len(death)-1):
                                    death_it = 0
                            else:
                                if death_it >= (len(death)-1):
                                    found = True
                                    death_it = 0
                                else:
                                    death_it += 1
                        else:
                            found = True
                    else:
                        found = True
                        

                if found == True:
                    count += 1
                    break
                
            except Exception as e:
                break
        return {'bowling_lineup':bowling_lineup, 'count':count, 'bowler_per_over':bowler_per_over} 
    
    @staticmethod
    def setDeathBowler(bowler_per_over, bowling_lineup, powerplay, midover, death, death_overs, count):
        powerplay_it = 0
        midover_it = 0
        death_it = 0
        over = 0
        
        found = False
        
        while over != death_overs:
            try:
                if len(death) != 0:
                    if Team.check_for_overs_left("death", bowler_per_over, powerplay, midover, death):
                        if Team.check_mid_death(bowling_lineup, death[death_it], bowler_per_over):
                            bowling_lineup.append(death[death_it])
                            bowler_per_over[death[death_it]] -= 1
                            death_it += 1
                            over += 1
                            if death_it >= (len(death)-1):
                                death_it = 0
                        else:
                            if death_it >= (len(death)-1):
                                found = True
                                death_it = 0
                            else:
                                death_it += 1
                    else:
                        found = True
                else:
                    found = True
                
                if found == True:
                    found = False
                    if len(powerplay) != 0:
                        if Team.check_for_overs_left("powerplay", bowler_per_over, powerplay, midover, death):
                            if Team.check_mid_death(bowling_lineup, powerplay[powerplay_it], bowler_per_over):
                                bowling_lineup.append(powerplay[powerplay_it])
                                bowler_per_over[powerplay[powerplay_it]] -= 1
                                powerplay_it += 1
                                over += 1
                                if powerplay_it >= (len(powerplay)-1):
                                    powerplay_it = 0
                            else:
                                if powerplay_it >= (len(powerplay)-1):
                                    found = True
                                    powerplay_it = 0
                                else:
                                    powerplay_it += 1
                        else:
                            found = True
                    else:
                        found = True
                
                if found == True:
                    found = False
                    if len(midover) != 0:
                        if Team.check_for_overs_left("midover", bowler_per_over, powerplay, midover, death):
                            if Team.check_mid_death(bowling_lineup, midover[midover_it], bowler_per_over):
                                bowling_lineup.append(midover[midover_it])
                                bowler_per_over[midover[midover_it]] -= 1
                                midover_it += 1
                                over += 1
                                if midover_it >= (len(midover)-1):
                                    midover_it = 0
                            else:
                                if midover_it >= (len(midover)-1):
                                    found = True
                                    midover_it = 0
                                else:
                                    midover_it += 1
                        else:
                            found = True
                    else:
                        found = True
                        

                if found == True:
                    count += 1
                    break
                
            except Exception as e:
                break
            
        return {'bowling_lineup':bowling_lineup, 'count':count, 'bowler_per_over':bowler_per_over} 
    
    @staticmethod
    def check_default(bowler, temp, bpo):
        try:
            if len(temp) != 0:
                if temp[len(temp)-1] is not bowler and bpo[bowler] > 0:
                    return True
                else:
                    return False
            else:
                return True
        except :
            return False
    @staticmethod
    def getDefault(bpo, powerplay, midover, death):
        bowlers = Team.getList(powerplay, midover, death)
        temp = []
        x = 0
        i = 0
        mid = True
        d = True
        
        count = 0
        flag = False
        
        while i != 20:
            if 0 <= i < 6:
                if Team.check_default(bowlers[x], temp, bpo):
                    temp.append(bowlers[x])
                    bpo[bowlers[x]] -= 1
                    i += 1
                    count = 0
                if x < 3:
                    x += 1
                else:
                    x = 0
            elif 6 <= i < 16:
                if mid:
                    x = 2
                    mid = False    
                if Team.check_default(bowlers[x], temp, bpo):
                    temp.append(bowlers[x])
                    bpo[bowlers[x]] -= 1
                    i += 1
                    count = 0
                if x < (len(bowlers)-1):
                    x += 1
                else:
                    x = 0
            else:
                if d:
                    x = 4
                    d = False
                if Team.check_default(bowlers[x], temp, bpo):
                    temp.append(bowlers[x])
                    bpo[bowlers[x]] -= 1
                    i += 1
                    count = 0
                if x < (len(bowlers)-1):
                    x += 1
                else:
                    x = 0
            
            if count > len(bowlers)*100:
                temp = None
                break
            count += 1
        return temp
    
    
    def poor_lineup(self):
        bowlingLineup = []
        for player in self.players:
            if player.playerType == "bowler" or player.playerType == "allrounder":
                bowlingLineup.append(player)
            if len(bowlingLineup) == 20:
                break
        for i in range(4):
            if len(bowlingLineup) >= 20 or len(bowlingLineup) == 0:
                break
            bowlingLineup += bowlingLineup
        if len(bowlingLineup) < 20:
            bowlingLineup = []
        if len(bowlingLineup) > 20:
            while True:
                bowlingLineup.pop()
                if len(bowlingLineup) == 20:
                    break
        return bowlingLineup
    
    def __str__(self):
        return self.name