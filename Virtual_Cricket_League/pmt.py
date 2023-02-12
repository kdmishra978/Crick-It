import random
from Player import *
import math

MaxScore = 5.9833

class PlayerMatchTime(Player):

    def __init__(self, playerData, teamName):
        super().__init__(playerData)
        self.flag = 0 # this decides next ball result, 0 means off, -1 = w, 1 = wd/nb
        
        self.confidence = 0  # all these variables should be set, when player is coming to play
        self.confidenceVarsBowl = {}
        self.confidenceVars = {}
        #        
        self.teamName = teamName
        
        self.stamina = 0
        self.setInitialStamina()
        #
        self.pressure = 0
        self.setInitialPressure()
        #
        self.comfort = 0  # homeground, order, against type
        self.comfortVars = {"ground": 0, "order": 0, "opponent": 0}
        #
        self.battingScore = 0
        self.bowlingScore = 0
        # initially the following values will be 0, but will be updated as match proceeds 
        # and then at the end of match, these will be saved to a database
        # for batsman:
        self.ballsFaced = 0
        self.runs = 0
        # for bowler:
        self.wickets = 0
        self.runsGiven = 0
        self.ballsBowled = 0
        self.lastOver = None 
        #

    def calculateBatsmanScore(self):
        self.calcTotalComfort()
        self.batsmanScore = self.batSkill + self.experience
        self.batsmanScore += self.confidence + self.stamina + self.comfort
        self.batsmanScore -= (self.pressure)
    
    def calculateBowlerScore(self):
        self.calcTotalComfort()
        self.bowlerScore = self.bowlSkill + self.experience
        self.bowlerScore += self.confidence + self.stamina + self.comfort
        self.bowlerScore -= (self.pressure)
    
# stamina related functions
    def setInitialStamina(self):
        if self.age <= 90:
            self.stamina = math.cos(self.age*0.0175)*100
        else:
            self.stamina = 0
    
    def bowler_stamina(self, currentOver):
        if  self.ballsBowled % 6 == 1:  # i.e. first ball of the over
            if self.lastOver:  
                gap = currentOver - (self.lastOver+1)
                self.stamina += math.sin(gap*0.0175)*50
                if self.stamina > 100:
                    self.stamina = 100
            else:
                pass
        if self.ballsBowled % 6 != 0:
            self.stamina -= 2*math.log(2)
        else:
            self.stamina -= 2*math.log(2)
            self.lastOver = currentOver
        if self.stamina <= 0:
            self.stamina = 0

    def batsman_stamina(self, run):
        if run in ["wd", "nb", "w"]:
            pass
        elif run <= 3:
            self.stamina -= math.tan(run*0.0175)*15
        else:
            self.stamina -= math.log(run)
        if self.stamina <= 0:
                self.stamina = 0
    
# comfort related functions:
    # comfort scores may create a lot of differnce between players, so can manage these as per results
    def calcTotalComfort(self):
        self.comfort = self.comfortVars["ground"] + self.comfortVars["order"] + self.comfortVars["opponent"]
        self.comfort = self.comfort/3

    def setInitialBatComfort(self, order, groundAdvantage = False):  # needs to be called when player comes to play!!!
        if groundAdvantage:
            self.comfortVars["ground"] = 20
        else:
            self.comfortVars["ground"] = 0
        self.comfortVars["order"] = self.battingOrder[order]

    def setInitialBowlComfort(self, crrOver, groundAdvantage = False):  # needs to be called when player comes to play!!!
        if groundAdvantage:
            self.comfortVars["ground"] = 20
        else:
            self.comfortVars["ground"] = 0
        self.overWiseComfort(crrOver)

    def overWiseComfort(self, crrOver):
        if self.checkBowlingOrder(crrOver):                         # this needs to be called when bowler is coming to bowl
            self.comfortVars["order"] = self.bowlSkill
        else:
            self.comfortVars["order"] = 50

    def updateBowlComfort(self, batsman):  # needs to be called everytime batsman changes
        if self.checkBatsman(batsman):
            if self.bowlSkill > batsman.batSkill:
                try:
                    rd = (self.bowlSkill - batsman.batSkill)/batsman.batSkill
                    rd *= 100
                    if rd>50:
                        rd = 50
                except:
                    rd = 50
                self.comfortVars["opponent"] = rd
            else:
                self.comfortVars["opponent"] = 0
        else:
            self.comfortVars["opponent"] = 0

    def updateBatComfort(self, bowler):  # needs to be called after every over
        if self.checkBowler(bowler):
            if self.batSkill > bowler.bowlSkill:
                try:
                    rd = (self.batSkill - bowler.bowlSkill)/bowler.bowlSkill
                    rd *= 100
                    if rd>50:
                        rd = 50
                except:
                    rd = 50
                self.comfortVars["opponent"] = rd
            else:
                self.comfortVars["opponent"] = 0
        else:
            self.comfortVars["opponent"] = 0
        
    def checkBowlingOrder(self, crrOver):
        if 1 <= crrOver <= 6:
            crrOver = "powerplay"
        elif 7 <= crrOver <= 15:
            crrOver = "midover"
        elif 16 <= crrOver <= 20:
            crrOver = "deathover"
        if crrOver in self.bowlingOrder:
            return True
        else:
            return False

    def checkBatsman(self, batsman: Player):
        if batsman.battingHand in self.bowlComfort:
            return True
        else:
            return False

    def checkBowler(self, bowler: Player):
        result = False
        for comfort in self.batComfort:
            if comfort in bowler.bowlingType:
                result = True
        return result
# pressure related functions:
    def setInitialPressure(self):
        pressure = 0
        if self.experience < 90:
            pressure = (1-math.sin(self.experience*0.0175))*50
        else:
            pressure = 0
        self.pressure = pressure

    def update_batsman_pressure(self, result, requiredRunRate, actualReqRunRate, currentRunRate, wickets, balls):
        if result == "w":
            return
        if balls <= 6:  # first over handelled
            if result == 0:
                result = -4
            elif result == 1:
                result = 0
            elif result == "wd":
                result = 1
            self.pressure -= result * 0.25
            if self.pressure < 0:
                self.pressure = 0
            elif self.pressure > 100:
                self.pressure = 100
            return

        elif balls > 114:   # in last over pressure is set according to experience
            self.setInitialPressure()
            return

        difference = requiredRunRate - currentRunRate
        if result == "wd":
            result = 0
        if difference > 0:
            try:
                x = math.tan((self.experience - 20) * 0.01745329)  # divide difference by x
                if x <= 0:
                    x = 1
            except:
                x = 1
            increment = (difference/x) - result
            depthBenefit = 0
            if increment > 0:
                # checking batting depth:
                if 0 <= wickets <= 6:
                    depthBenefit = math.tan((6 - wickets) * 0.01745) * 15
            self.pressure += increment - depthBenefit

        elif difference < 0:
            self.pressure += difference  # see the dip or rise of graph... ( earlier: self.pressure -= result * 0.25)
        if self.pressure < 0:
            self.pressure = 0
        elif self.pressure > 100:
            self.pressure = 100

        # this is confidence related, but runrate is required, so it is placed here
        difference = actualReqRunRate - currentRunRate
        temp = 0
        if self.runs>100 and ((self.runs*100)/self.ballsFaced) >= 200 and difference<0:
            temp = random.choice([0,0,1])
        elif self.runs>100 and difference<0:
            temp = random.choice([0,0,1,0])
        elif self.runs>100 and difference>0:
            temp = random.choice([0,0,1,0,0,0])
        elif self.runs>50 and ((self.runs*100)/self.ballsFaced) >= 200 and difference<-2:
            temp = random.choice([0,1,0])
        elif self.runs>50 and difference<-2 and wickets<4:
            temp = random.choice([0,0,0,1,0,0])
        
        if temp == 1: #means player is overconfident
            self.flag = -1
            # print(self.name,"(",self.runs,"in",self.ballsFaced,")", "is overconfident! \n")
            # input()
                
        if self.ballsFaced>36 and ((self.runs*100)/self.ballsFaced)<=120 and difference > 0 and wickets <= 5:
            # print("Underconfident!!")
            # print(self.name,"(",self.runs,"in",self.ballsFaced,")", "is underconfident! \n")
            # input()
            temp = random.choice([0,1])
            if temp == 0 and self.confidenceVars["boost"] == False:  # testing, experimental!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                self.confidenceVars["boost"] = True
                self.confidence = random.choice([40, 90])
            elif temp == 1: #means player is underconfident
                self.flag = -2
        
        elif self.ballsFaced>24 and ((self.runs*100)/self.ballsFaced)<=100 and difference > 0 and wickets <= 5:
            # print("Underconfident!!")
            # print(self.name,"(",self.runs,"in",self.ballsFaced,")", "is underconfident! \n")
            # input()
            temp = random.choice([0,0,0,1])
            if temp == 0 and self.confidenceVars["boost"] == False:  # testing, experimental!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                self.confidenceVars["boost"] = True
                self.confidence = random.choice([40, 90])
            elif temp == 1: #means player is underconfident
                self.flag = -2

    def update_bowler_pressure(self,  result, requiredRunRate, currentRunRate, wickets, balls):
        if balls <= 6:  # first over handelled
            if result == "w":
                result = -6
            elif result == 0:
                result = -4
            elif result == 1:
                result = 0
            elif result in ["wd","nb"]:
                result = 1
            self.pressure += result * 0.25
            if self.pressure < 0:
                self.pressure = 0
            elif self.pressure > 100:
                self.pressure = 100
            return

        elif balls > 114:   # in last over pressure is set according to experience
            self.setInitialPressure()
            return

        if result == "w":
            result = -8
        difference = requiredRunRate - currentRunRate
        if result in ["wd", "nb"]:
            result = 1
        if difference < 0:
            try:
                x = math.tan((self.experience - 20) * 0.01745329)  # divide difference by x
                if x <= 0:
                    x = 1
            except:
                x = 1
            if result == 0:  # for dot ball pressure should decrease
                result = -6
            elif result == 1:  # for single pressure should decrease
                result = -4
            increment = (result * 0.5) - (difference/x)
            depthBenefit = 0
            if increment > 0:
                # checking batting depth:
                if 3 <= wickets <= 10:
                    depthBenefit = math.tan(wickets * 0.01745) * 15
            self.pressure += increment - depthBenefit

        elif difference > 0:
            self.pressure -= difference
        if self.pressure < 0:
            self.pressure = 0
        elif self.pressure > 100:
            self.pressure = 100

# Confidence related functions:
    # for batsman
    def setBatsmanConfidence(self, inAtBall):  # this function should be called when batsman is coming to play !!!
        self.confidence = self.batSkill
        if inAtBall >= 90:
            x = 0
        else:
            try:
                x = -math.tan(inAtBall * 0.01745329) + 12
                x = int(x)
                if x < 0:
                    x = 0
            except:
                x = 0
        beta = ((self.batSkill - 20) / 180) * math.pi
        try:
            reduce = math.tan(beta) * 2
            if reduce < 0:
                reduce = 0
        except:
            reduce = 0
        theta = ((self.batSkill - 40) / 180) * math.pi
        try:
            penalty = int(math.tan(theta) * 3)
            if penalty < 0:
                penalty = 0
        except:
            penalty = 0
        self.confidenceVars = {"safe": x,  # number of balls up-to which confidence will boost, whatever be the outcome
                               "good": 88,  # good confidence value, above this is danger, below this is poor
                               "bq": [],  # boundary queue, stores result of last 10 balls
                               "bl6b": 0,  # number of boundaries in last 6 balls
                               "bl10b": 0,  # number of boundaries in last 10 balls
                               "penalty": penalty,
                               "reduce": reduce,
                               "overconfident": 0,  # if this is 1, player is out on next ball, due to overconfidence
                               "boost": False
                               }

    def basicConfidenceChange(self, run, slope=0):
        if run == 1:
            temp = -1
        elif run == 0:
            temp = -2
        else:
            temp = run
        slope += math.tan(temp * 7.5 * 0.01745329)
        self.confidence += slope

    def massiveConfidenceIncrement(self):
        slope = 4
        self.confidence += slope

    def massiveConfidenceDecrement(self):
        slope = -4
        self.confidence += slope

    def updateBoundaryQ(self, run):
        if len(self.confidenceVars["bq"]) == 10:
            self.confidenceVars["bq"].pop(0)
        if run >= 4:
            self.confidenceVars["bq"].append(1)
            self.confidenceVars["bl10b"] += 1  # once it reaches 4, it will be reset to 0 in updateBatsmanConfidence()
        else:
            self.confidenceVars["bq"].append(0)
        # calculating boundary in last 6 balls
        self.confidenceVars["bl6b"] = 0
        temp = self.confidenceVars["bq"][::-1]
        temp = temp[:6]
        for z in temp:
            if z == 1:
                self.confidenceVars["bl6b"] += 1

    def updateBatsmanConfidence(self, run):
        if run in ["wd","nb","w"]:
            return

        if self.batAggression == "low":
            if run <= 3:
                run += 1

        self.updateBoundaryQ(run)
        if self.ballsFaced < self.confidenceVars["safe"]:
            if self.confidenceVars["bl10b"] == 4:
                self.confidenceVars["bl10b"] = 0
            if self.confidence < self.confidenceVars["good"]:
                self.basicConfidenceChange(run, 1)
            else:
                pass
        
        else:
            if self.confidenceVars["bl10b"] == 4:
                self.massiveConfidenceIncrement()
                self.confidenceVars["bl10b"] = 0
            elif self.confidenceVars["bl6b"] < 1 and self.ballsFaced % 6 == 0:
                self.massiveConfidenceDecrement()
            else:
                self.basicConfidenceChange(run)
        # calculating penalty
        if self.confidence > 100:
            self.confidenceVars["penalty"] -= 1
            if self.confidenceVars["penalty"] < 0:
                self.confidenceVars["overconfident"] = 1
                self.flag = -1
            else:
                self.confidence -= self.confidenceVars["reduce"]

    # for bowler:
    def setBowlerConfidence(self):
        self.confidence = self.bowlSkill
        # penalty system is same as batsman, when bowler is overconfident, confidence is set to poor = 50 for that over
        # but number of penalties and reduction amount of a bowler are less than a batsman
        beta = ((self.bowlSkill - 25) / 180) * math.pi
        try:
            reduce = math.tan(beta) * 2
            if reduce < 0:
                reduce = 0
        except:
            reduce = 0
        theta = ((self.bowlSkill - 45) / 180) * math.pi
        try:
            penalty = int(math.tan(theta) * 4)
            if penalty < 0:
                penalty = 0
        except:
            penalty = 0
        # formula for bowlers' confidence => confidence += math.sqrt((run - c) / m)
        self.confidenceVarsBowl = {"m": 1/4,  # slope
                                   "c": 2,  # constant
                                   "penalty": penalty,
                                   "reduce": reduce,
                                   "poor": 50,
                                   "overconfident": 0,
                                   "ct": 0}  # counter ct is required when, we have to set confidence to poor for that over, to count remaining balls

    def updateBowlerConfidence(self, run):
        if run in ["wd","nb"]:
            return

        if self.confidenceVarsBowl["ct"] > 0:
            self.confidenceVarsBowl["ct"] -= 1
        delta = 2
        c = self.confidenceVarsBowl["c"]
        m = self.confidenceVarsBowl["m"]
        if run == "w":
            run = -1
        if run >= 2:
            delta = run
            change = - math.sqrt((delta - c) / m)
        else:
            if run == 1:
                delta = 3
            elif run == 0:
                delta = 4
            elif run == -1:
                delta = 6
            change = math.sqrt((delta - c) / m)
        self.confidence += change
        # calculating penalty
        if self.confidence > 100:
            self.confidenceVarsBowl["penalty"] -= 1
            if self.confidenceVarsBowl["penalty"] < 0:
                self.confidenceVarsBowl["overconfident"] = 1
                self.flag = 1 # remember to reset to 0
                self.confidence = self.confidenceVarsBowl["poor"]
                self.confidenceVarsBowl["ct"] = 7 - (self.ballsBowled % 6)  # 7 because next ball will be wd or nb
            else:
                self.confidence -= self.confidenceVarsBowl["reduce"]
        if self.confidenceVarsBowl["ct"] == 0 and self.confidenceVarsBowl["overconfident"] == 1:
            self.confidence = self.bowlSkill  # resetting the poor confidence to default, when the over ends  
            self.confidenceVarsBowl["overconfident"] = 0
    
    def __str__(self):
        return self.name

# data = {'name': 'Rohit Sharma', 'age': 31, 'playertype': 'batsman', 'battinghand': 'right', 'bowlingtype': 'right arm off spin', 'experience': 87, 'batskill': 89, 'bowlskill': 52, 'wktskill': 23, 'battingorder': '[90, 85, 80, 70, 50, 50, 50, 50, 50, 50, 50]', 'bowlingorder': ['midover'], 'batcomfort': ['fast', 'right'], 'bowlcomfort': ['left']}
# obj = PlayerMatchTime(data)
# print(obj.name)