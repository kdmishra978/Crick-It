from Team import Team
from Stadium import Stadium
from pmt import *
import random
import copy

class Match:
    def __init__(self, batTeam: Team, bowlTeam: Team, currGround: Stadium, overs=20, target=150, innings=1):  # this function is the main function
        self.superOverScore = {}
        self.perBallResults = {}
        self.perBallResults1 = {}
        self.perBallResults2 = {}
        self.perOverRuns = {}
        self.totalRuns = 0
        self.wickets = 0
        self.balls = 0
        self.requiredRunRate = 0
        self.actualReqRunRate = 0
        self.currentRunRate = 0
        self.frequency = {}  # testing
        self.bfrequency = {} # testing
        self.extras = {"wd": 0, "nb": 0, "total": 0}
        self.boundaries = {6:0, 4:0, 3:0, 2:0, 1:0, 0:0}
        
        self.battingTeam = batTeam
        self.bowlingTeam = bowlTeam
        self.battingLineup = batTeam.battingLineup
        self.bowlingLineup = bowlTeam.bowlingLineup
        
        self.striker = self.battingLineup.pop(0)
        self.battingTeam.batsmanBin.append(self.striker)
        self.nonStriker = self.battingLineup.pop(0)
        self.battingTeam.batsmanBin.append(self.nonStriker)
        self.bowler = self.bowlingLineup.pop(0)
        self.bowlingTeam.bowlerBin.append(self.bowler)

        self.ground = currGround
        self.target = target
        
        self.alreadyBowled = []
        self.alreadyBowled.append(self.bowler.name)
        self.alreadyBat = []

        self.win = {"bowler":0, "batsman":0}
        self.batComeback = False
        self.bowlComeback = False
    
        self.overs = overs
        self.innings = innings
        
        self.scorecard1st = dict()
        self.scorecard2nd = dict()
        self.winner = None
    
    def nextInnings(self):
        self.target = self.totalRuns
        self.perOverRuns = {}
        self.perBallResults = {}
        self.totalRuns = 0
        self.wickets = 0
        self.balls = 0
        self.requiredRunRate = 0
        self.currentRunRate = 0
        self.frequency = {}  # testing
        self.bfrequency = {} # testing
        self.extras = {"wd": 0, "nb": 0, "total": 0}
        self.boundaries = {6:0, 4:0, 3:0, 2:0, 1:0, 0:0}
        
        self.battingTeam, self.bowlingTeam = self.bowlingTeam, self.battingTeam
        self.battingLineup = self.battingTeam.battingLineup
        self.bowlingLineup = self.bowlingTeam.bowlingLineup
        
        self.striker = self.battingLineup.pop(0)
        self.battingTeam.batsmanBin.append(self.striker)
        self.nonStriker = self.battingLineup.pop(0)
        self.battingTeam.batsmanBin.append(self.nonStriker)
        self.bowler = self.bowlingLineup.pop(0)
        self.bowlingTeam.bowlerBin.append(self.bowler)
        
        self.alreadyBowled = []
        self.alreadyBowled.append(self.bowler.name)
        self.alreadyBat = []

        self.win = {"bowler":0, "batsman":0}
        self.batComeback = False
        self.bowlComeback = False
        self.innings = 2

    def updateProjectedScore(self):
        if self.innings != 1 or self.currentRunRate == 0:
            return
        if self.balls in [60, 90] or self.requiredRunRate <= 0:
            self.target = self.currentRunRate * 20

    def updateRunRate(self):
        try:
            self.requiredRunRate = ((self.target-self.totalRuns)/(120-self.balls))*6
        except:
            self.requiredRunRate = (self.target-self.totalRuns)
        if self.innings == 1:
            try:
                self.actualReqRunRate = ((self.ground.averageRuns-self.totalRuns)/(120-self.balls))*6
            except:
                self.actualReqRunRate = (self.ground.averageRuns-self.totalRuns)
        else:
            self.actualReqRunRate = self.requiredRunRate
        try:
            self.currentRunRate = (self.totalRuns/self.balls)*6
        except:
            self.currentRunRate = 0
    
    def startMatch(self):  # this function is the main function
        self.updateRunRate()
        self.setupPlayers()  # setting up some values which need to be set when player comes
        for over in range(self.overs):
            if self.target < self.totalRuns and self.innings != 1:
                    break
            if self.wickets == 10:
                    break
            ball = 1
            prevOverRuns = self.totalRuns  # testing
            prevOverWickets = self.wickets  # testing
            while ball != 7:
                self.updateProjectedScore() # this will only run after 10 and 15 overs.   **************NEW********************
                if self.target < self.totalRuns and self.innings != 1:
                    break
                if self.wickets == 10:
                    break
                # print(over, ".", ball, sep="", end="\t")
                temp = self.nextBallPre()
                if temp:
                    result = temp 
                else:
                    result = self.thisBall()  # remember to handle case of noball and wide. ball-=1, run+=1 and next ball no wicket for noball,
                if result == "wd" or result == "nb":
                    ball -= 1
                self.updateRunRate()
                self.updateScoreCard(result)  # this function updates runs, balls, player runs, etc.
                ball += 1
                self.disp()
                
            
            self.perOverRuns[over] = (self.totalRuns - prevOverRuns, self.wickets - prevOverWickets, self.bowler.name)  # testing
            
            if over == 19:
                break
            self.nextOver()
        
        self.displayPlayerStats()
        if self.innings == 1:
            self.perBallResults1 = self.perBallResults
            self.setScorecard()
            self.nextInnings()
            self.startMatch()
        
        if self.innings == 2:
            self.perBallResults2 = self.perBallResults
            self.setScorecard()
            if self.target < self.totalRuns:
                self.winner = self.battingTeam.name
            elif self.target > self.totalRuns:
                self.winner = self.bowlingTeam.name
            else:
                self.superOver()
            self.innings = 0
    
    @staticmethod
    def sorter(e):
        return e.runs
    
    @staticmethod
    def sort_bowler(e):
        return e.bowlSkill + e.experience
    
    def selectTop3Batsman(self):
        temp = sorted(self.battingTeam.batsmanBin, key=Match.sorter, reverse=True)
        x = len(temp) 
        i = 0
        while x<3:
            temp.append(self.battingTeam.battingLineup[i])
            x += 1
            i += 1
        return temp[:3]
    
    def selectTopBowler(self):
        bowler = sorted(self.bowlingTeam.bowlerBin, key=Match.sort_bowler, reverse=True)
        return bowler[0]
    
    def superOver(self):
        tempbatline = self.selectTop3Batsman()
        striker = tempbatline[0]
        nonStriker = tempbatline[1]
        bowler = self.selectTopBowler()
        total = 0
        wickets = 0
        
        perball1 = {}
        perball2 = {}

        for i in range(6):
            result = random.choice([0, 1, 2, 3, 4, 6, "w"])
            if result == "w":
                wickets += 1
                striker = tempbatline[2]
            else:
                if result in [1, 3]:
                    striker, nonStriker = nonStriker, striker
                total += result
            
            print("Result:", result)
            print("Striker:",striker, " Non-Striker:", nonStriker, " Bowler:", bowler)
            print("Score:", total, "/", wickets)
            perball1[i+1] = {
            "score":str(total)+"/"+str(wickets),
            "striker":{"name": striker.name, "runs": striker.runs, "balls": striker.ballsFaced},
            "nonstriker":{"name": nonStriker.name, "runs": nonStriker.runs, "balls": nonStriker.ballsFaced},
            "bowler":{"name": bowler.name, "runs": bowler.runsGiven, "balls": bowler.ballsBowled, "wickets": bowler.wickets},
            "result": result}
            if wickets == 2:
                break
        # innings 2
        print("\n\nInnings 2:\n")
        target = total
        self.battingTeam, self.bowlingTeam = self.bowlingTeam, self.battingTeam
        tempbatline = self.selectTop3Batsman()
        striker = tempbatline[0]
        nonStriker = tempbatline[1]
        bowler = self.selectTopBowler()
        total = 0
        wickets = 0
        for i in range(6):
            result = random.choice([0, 1, 2, 3, 4, 6, "w"])
            if result == "w":
                wickets += 1
                striker = tempbatline[2]
            else:
                if result in [1, 3]:
                    striker, nonStriker = nonStriker, striker
                total += result
            
            print("Result:", result)
            print("Striker:",striker, " Non-Striker:", nonStriker, " Bowler:", bowler)
            print("Score:", total, "/", wickets)
            perball2[i+1] = {
            "score":str(total)+"/"+str(wickets),
            "striker":{"name": striker.name, "runs": striker.runs, "balls": striker.ballsFaced},
            "nonstriker":{"name": nonStriker.name, "runs": nonStriker.runs, "balls": nonStriker.ballsFaced},
            "bowler":{"name": bowler.name, "runs": bowler.runsGiven, "balls": bowler.ballsBowled, "wickets": bowler.wickets},
            "result": result}
            if wickets == 2:
                break
            
            if total > target:
                break
            
        if target > total:
            self.winner = self.bowlingTeam.name
        elif target < total:
            self.winner = self.battingTeam.name
        else:
            self.winner = "Draw"
        self.superOverScore['perBallResults1'] = perball1
        self.superOverScore['perBallResults2'] = perball2

    def nextBallPre(self):
        if self.striker.flag == -1 and self.balls <= 108: # player is overconfident, not considerd in last 2 overs
            self.striker.flag = 0
            return "w"
        if self.striker.flag == -2: # player is underconfident
            self.striker.flag = 0
            return "w"
        if self.bowler.flag == 1:
            self.bowler.flag = 0
            return random.choice([2, 4, 6, "wd", "nb"])
        return False

    def nextOver(self):
        self.striker, self.nonStriker = self.nonStriker, self.striker  # changing strike
        self.bowler = self.bowlingLineup.pop(0)  # next bowler
        if self.bowler.name not in self.alreadyBowled:
            self.alreadyBowled.append(self.bowler.name)
            self.bowlingTeam.bowlerBin.append(self.bowler)
            self.setupNewBowler()
        else:
            crrOver = int(self.balls / 6)
            self.bowler.overWiseComfort(crrOver)
            self.bowler.updateBowlComfort(self.striker)
        self.striker.updateBatComfort(self.bowler)
        self.nonStriker.updateBatComfort(self.bowler)

    def setupNewBowler(self):
        # for stamina:
        self.bowler.setInitialStamina()
        # for comfort:
        if self.bowlingTeam.homeGround.name == self.ground.name:
            homeGround = True
        else:
            homeGround = False
        crrOver = int(self.balls / 6) + 1
        self.bowler.setInitialBowlComfort(crrOver, homeGround)
        self.bowler.updateBowlComfort(self.striker)
        # for pressure:
        self.bowler.setInitialPressure()
        # for confidence:
        self.bowler.setBowlerConfidence()

    def update_win(self, batsmanScore, bowlerScore):
        if batsmanScore > bowlerScore:
            if self.win['bowler'] + self.win['batsman'] < 10:
                self.win['batsman'] += 1
            else:
                if self.requiredRunRate < self.currentRunRate:
                    self.comeback("bowler")
                self.win['bowler'] = 0
                self.win['batsman'] = 0
        elif bowlerScore > batsmanScore:
            if self.win['bowler'] + self.win['batsman'] < 10:
                self.win['bowler'] += 1
            else:
                if self.requiredRunRate > self.currentRunRate:
                    self.comeback("batsman")
                self.win['bowler'] = 0
                self.win['batsman'] = 0
        else:
            self.win['bowler'] += 0
            self.win['batsman'] += 0
    
    def batPowerPlay(self, relativeDiff, agg):
        result = 0
        
        if agg == "super":
            if 0 < relativeDiff <= 1:
                result = random.choice([0, 1, 2])
            elif 1 < relativeDiff <= 2:
                result = random.choice([0, 1, 1, 1, 2, 4])
            elif 2 < relativeDiff <= 5:
                result = random.choice([0, 1, 2, 2, 4, 4])
            elif 5 < relativeDiff <= 9:
                result = random.choice([0, 1, 2, 2, 4, 4])
            elif 9 < relativeDiff <= 10:
                result = random.choice([0, 1, 2, 2, 4, 4, 6])    
            elif 10 < relativeDiff <= 15:
                result = random.choice([1, 2, 4, 6])
            elif 15 < relativeDiff <= 20:
                result = random.choice([2, 4, 4, 6])
            elif 20 < relativeDiff <= 25:
                result = random.choice([2, 4, 4, 4, 1, 4, 6, 6, 4])
            else:
                result = random.choice([2, 4, 4, 4, 2, 1, 6, 6, 6, 6, 4])

        elif agg == "high":
            if 0 < relativeDiff <= 1:
                result = random.choice([0, 0, 1, 2])
            elif 1 < relativeDiff <= 2:
                result = random.choice([0, 0, 1, 1, 1, 2])
            elif 2 < relativeDiff <= 5:
                result = random.choice([0, 1, 1, 2, 2, 4])
            elif 5 < relativeDiff <= 9:
                result = random.choice([0, 1, 1, 2, 4])
            elif 9 < relativeDiff <= 10:
                result = random.choice([0, 1, 2, 2, 4, 6])    
            elif 10 < relativeDiff <= 15:
                result = random.choice([0, 1, 2, 4, 6])
            elif 15 < relativeDiff <= 20:
                result = random.choice([2, 4, 4, 6])
            elif 20 < relativeDiff <= 25:
                result = random.choice([2, 4, 4, 4, 1, 6, 4, 6])
            else:
                result = random.choice([2, 4, 4, 4, 2, 1, 6, 6, 6])
        
        elif agg == "normal":
            if 0 < relativeDiff <= 1:
                result = random.choice([0, 0, 1, 1, 2])
            elif 1 < relativeDiff <= 2:
                result = random.choice([0, 0, 1, 1, 1, 2])
            elif 2 < relativeDiff <= 5:
                result = random.choice([0, 0, 1, 1, 2, 2, 3, 4])
            elif 5 < relativeDiff <= 9:
                result = random.choice([0, 1, 2, 2, 4])
            elif 9 < relativeDiff <= 10:
                result = random.choice([0, 1, 2, 2, 2, 4, 6])    
            elif 10 < relativeDiff <= 15:
                result = random.choice([0, 1, 2, 2, 4, 6])
            elif 15 < relativeDiff <= 20:
                result = random.choice([1, 2, 4, 4, 6])
            elif 20 < relativeDiff <= 25:
                result = random.choice([2, 4, 4, 2, 1, 4, 6, 4])
            else:
                result = random.choice([2, 4, 4, 2, 1, 6, 6, 4])
        
        elif agg == "low":
            if 0 < relativeDiff <= 1:
                result = random.choice([0, 0, 0, 1, 1, 2])
            elif 1 < relativeDiff <= 2:
                result = random.choice([0, 0, 1, 1, 1, 2])
            elif 2 < relativeDiff <= 5:
                result = random.choice([0, 0, 1, 1, 2, 2, 3])
            elif 5 < relativeDiff <= 9:
                result = random.choice([0, 1, 2, 2, 2, 1, 1, 4])
            elif 9 < relativeDiff <= 10:
                result = random.choice([0, 1, 2, 2, 2, 2, 4])    
            elif 10 < relativeDiff <= 15:
                result = random.choice([0, 1, 2, 2, 2, 3, 4])
            elif 15 < relativeDiff <= 20:
                result = random.choice([0, 1, 2, 2, 2, 4, 2])
            elif 20 < relativeDiff <= 25:
                result = random.choice([0, 1, 4, 2, 4, 2, 2])
            else:
                result = random.choice([0, 1, 4, 2, 6, 2, 2])

        return result

    def batMiddle(self, relativeDiff, agg):
        result = 0
        if agg == "super":
            if 0 < relativeDiff <= 1:
                result = random.choice([0, 1, 1, 2])
            elif 1 < relativeDiff <= 2:
                result = random.choice([0, 1, 1, 1, 2, 3])
            elif 2 < relativeDiff <= 5:
                result = random.choice([0, 1, 2, 2, 4])
            elif 5 < relativeDiff <= 9:
                result = random.choice([0, 1, 2, 2, 4])
            elif 9 < relativeDiff <= 10:
                result = random.choice([0, 1, 2, 2, 4, 6])    
            elif 10 < relativeDiff <= 15:
                result = random.choice([0, 2, 2, 4, 4, 6])
            elif 15 < relativeDiff <= 20:
                result = random.choice([1, 2, 2, 4, 4, 6, 6])
            elif 20 < relativeDiff <= 25:
                result = random.choice([2, 4, 4, 6])
            elif 25 < relativeDiff <= 30:
                result = random.choice([2, 4, 4, 4, 2, 1, 6, 4, 6, 4])
            else:
                result = random.choice([2, 4, 4, 4, 2, 1, 6, 6, 6, 6, 4])

        elif agg == "high":
            if 0 < relativeDiff <= 1:
                result = random.choice([0, 1, 1, 2])
            elif 1 < relativeDiff <= 2:
                result = random.choice([0, 1, 1, 1, 2, 3])
            elif 2 < relativeDiff <= 5:
                result = random.choice([0, 1, 2, 2, 2, 2, 4])
            elif 5 < relativeDiff <= 9:
                result = random.choice([0, 1, 1, 2, 2, 4])
            elif 9 < relativeDiff <= 10:
                result = random.choice([0, 1, 2, 4, 2, 4])    
            elif 10 < relativeDiff <= 15:
                result = random.choice([0, 1, 2, 2, 4, 6])
            elif 15 < relativeDiff <= 20:
                result = random.choice([1, 2, 2, 4, 4, 6])
            elif 20 < relativeDiff <= 25:
                result = random.choice([2, 4, 4, 6])
            elif 25 < relativeDiff <= 30:
                result = random.choice([2, 4, 4, 4, 2, 1, 6, 4, 6])
            else:
                result = random.choice([2, 4, 4, 4, 2, 1, 6, 6, 6])
        
        elif agg == "normal":
            if 0 < relativeDiff <= 1:
                result = random.choice([0, 0, 0, 1, 1, 1, 2])
            elif 1 < relativeDiff <= 2:
                result = random.choice([0, 1, 1, 1, 2, 2, 3])
            elif 2 < relativeDiff <= 5:
                result = random.choice([0, 1, 2, 2, 1, 2])
            elif 5 < relativeDiff <= 9:
                result = random.choice([0, 1, 1, 2, 2, 2, 4])
            elif 9 < relativeDiff <= 10:
                result = random.choice([0, 1, 2, 2, 3, 4])    
            elif 10 < relativeDiff <= 15:
                result = random.choice([0, 1, 2, 2, 4, 4])
            elif 15 < relativeDiff <= 20:
                result = random.choice([1, 2, 2, 2, 4, 4, 6])
            elif 20 < relativeDiff <= 25:
                result = random.choice([1, 2, 2, 4, 4, 6])
            elif 25 < relativeDiff <= 30:
                result = random.choice([2, 4, 4, 2, 1, 4, 6, 4])
            else:
                result = random.choice([2, 4, 4, 2, 1, 6, 6, 4])
        
        elif agg == "low":
            if 0 < relativeDiff <= 1:
                result = random.choice([0, 0, 1, 1, 1, 1, 2])
            elif 1 < relativeDiff <= 2:
                result = random.choice([0, 1, 1, 1, 2, 2, 2, 3])
            elif 2 < relativeDiff <= 5:
                result = random.choice([0, 1, 2, 2])
            elif 5 < relativeDiff <= 9:
                result = random.choice([0, 1, 1, 2, 2, 2])
            elif 9 < relativeDiff <= 10:
                result = random.choice([0, 1, 2, 2, 3, 4])    
            elif 10 < relativeDiff <= 15:
                result = random.choice([0, 1, 2, 2, 2, 4])
            elif 15 < relativeDiff <= 20:
                result = random.choice([1, 2, 2, 2, 3, 4])
            elif 20 < relativeDiff <= 25:
                result = random.choice([1, 2, 2, 4, 2, 6, 2])
            elif 25 < relativeDiff <= 30:
                result = random.choice([1, 2, 2, 4, 2, 6, 2])
            else:
                result = random.choice([2, 2, 1, 2, 6, 4])

        return result

    def batDeath(self, relativeDiff, agg):
        result = 0
        if agg == "super":
            if 0 < relativeDiff <= 1:
                result = random.choice([0, 1, 2])
            elif 1 < relativeDiff <= 2:
                result = random.choice([0, 1, 2, 4])
            elif 2 < relativeDiff <= 5:
                result = random.choice([0, 1, 2, 2, 2, 4, 6])
            elif 5 < relativeDiff <= 9:
                result = random.choice([0, 1, 2, 4, 6])
            elif 9 < relativeDiff <= 10:
                result = random.choice([0, 1, 2, 4, 4, 6])    
            elif 10 < relativeDiff <= 15:
                result = random.choice([0, 2, 4, 4, 6, 4, 4, 6])
            else:
                result = random.choice([2, 4, 4, 4, 2, 6, 6, 6, 6, 4])

        elif agg == "high":
            if 0 < relativeDiff <= 1:
                result = random.choice([0, 0, 1, 2])
            elif 1 < relativeDiff <= 2:
                result = random.choice([0, 1, 2, 2, 3])
            elif 2 < relativeDiff <= 5:
                result = random.choice([0, 1, 1, 2, 2, 2, 4, 6])
            elif 5 < relativeDiff <= 9:
                result = random.choice([0, 1, 2, 4])
            elif 9 < relativeDiff <= 10:
                result = random.choice([0, 1, 2, 4, 4, 6])    
            elif 10 < relativeDiff <= 15:
                result = random.choice([0, 4, 1, 2, 6, 2, 4, 4, 6])
            elif 15 < relativeDiff <= 20:
                result = random.choice([2, 4, 4, 6])
            elif 20 < relativeDiff <= 25:
                result = random.choice([4, 4, 6, 2, 6])
            else:
                result = random.choice([2, 4, 4, 4, 2, 6, 6, 6])
        
        elif agg == "normal":
            if 0 < relativeDiff <= 1:
                result = random.choice([0, 0, 1, 2])
            elif 1 < relativeDiff <= 2:
                result = random.choice([0, 1, 1, 2, 3])
            elif 2 < relativeDiff <= 5:
                result = random.choice([0, 0, 1, 1, 2, 2, 2, 4])
            elif 5 < relativeDiff <= 9:
                result = random.choice([0, 1, 2, 2, 4])
            elif 9 < relativeDiff <= 10:
                result = random.choice([1, 0, 2, 2, 2, 2, 4, 6])    
            elif 10 < relativeDiff <= 15:
                result = random.choice([0, 1, 2, 2, 2, 4, 4, 6, 4])
            elif 15 < relativeDiff <= 20:
                result = random.choice([1, 2, 2, 4, 4, 6])
            elif 20 < relativeDiff <= 25:
                result = random.choice([1, 2, 4, 4, 6])
            else:
                result = random.choice([2, 4, 4, 2, 1, 6, 6, 4])
        
        elif agg == "low":
            if 0 < relativeDiff <= 1:
                result = random.choice([0, 0, 1, 2, 2])
            elif 1 < relativeDiff <= 2:
                result = random.choice([0, 0, 1, 1, 2, 2, 2, 3])
            elif 2 < relativeDiff <= 5:
                result = random.choice([0, 0, 1, 1, 2, 2, 2, 2, 4])
            elif 5 < relativeDiff <= 9:
                result = random.choice([0, 1, 2, 2, 2, 4])
            elif 9 < relativeDiff <= 10:
                result = random.choice([0, 1, 2, 2, 4, 4])    
            elif 10 < relativeDiff <= 15:
                result = random.choice([1, 2, 2, 2, 2, 4, 4, 6])
            elif 15 < relativeDiff <= 20:
                result = random.choice([1, 2, 2, 2, 4, 4, 6])
            elif 20 < relativeDiff <= 25:
                result = random.choice([1, 2, 4, 4, 6])
            else:
                result = random.choice([2, 4, 1, 6, 6, 4])

        return result
    
    def bowlPowerPlay(self, relativeDiff, agg):
        result = 0
        if agg == "super":
            if 0 < relativeDiff <= 2:
                result = random.choice([0, 0, 1, 2])
            elif 2 < relativeDiff <= 5:
                result = random.choice([0, 0, 0, 1, 1, 2])
            elif 5 < relativeDiff <= 9:
                result = random.choice([0, 1, 0, 1, "w"])
            elif 9 < relativeDiff <= 10:
                result = random.choice([0, 1, 0, "w"])
            elif 10 < relativeDiff <= 15:
                result = random.choice([0, 1, "w"])
            elif 15 < relativeDiff <= 30:
                result = random.choice([0, 1, "w"])
            elif 30 < relativeDiff <= 50:
                result = random.choice([0, "w"])
            else:
                result = "w"

        elif agg == "high":
            if 0 < relativeDiff <= 2:
                result = random.choice([0, 1, 1, 2])
            elif 2 < relativeDiff <= 5:
                result = random.choice([0, 0, 1, 1, 1, 2])
            elif 5 < relativeDiff <= 9:
                result = random.choice([0, 1, 0, 1, 1, "w"])
            elif 9 < relativeDiff <= 10:
                result = random.choice([0, 0, 0, 1, "w"])
            elif 10 < relativeDiff <= 15:
                result = random.choice([0, 0, 1, "w"])
            elif 15 < relativeDiff <= 30:
                result = random.choice([0, 1, "w"])
            elif 30 < relativeDiff <= 50:
                result = random.choice([0, "w"])
            else:
                result = "w"
        
        elif agg == "normal":
            if 0 < relativeDiff <= 2:
                result = random.choice([0, 1, 1, 2])
            elif 2 < relativeDiff <= 5:
                result = random.choice([0, 0, 1, 1, 1, 2])
            elif 5 < relativeDiff <= 9:
                result = random.choice([0, 0, 0, 1, 1, 1, 1, "w"])
            elif 9 < relativeDiff <= 10:
                result = random.choice([0, 1, 0, 1, 1, 1, "w"])
            elif 10 < relativeDiff <= 15:
                result = random.choice([0, 1, 1, "w"])
            elif 15 < relativeDiff <= 30:
                result = random.choice([0, 1, "w"])
            elif 30 < relativeDiff <= 50:
                result = random.choice([0, "w"])
            else:
                result = "w"
        
        elif agg == "low":
            if 0 < relativeDiff <= 2:
                result = random.choice([0, 1, 2, 2, 3])
            elif 2 < relativeDiff <= 5:
                result = random.choice([0, 0, 1, 2, 1, 2])
            elif 5 < relativeDiff <= 9:
                result = random.choice([0, 0, 0, 1, 1, 1, 1, 2, 1])
            elif 9 < relativeDiff <= 10:
                result = random.choice([0, 1, 0, 1, 1, 1])
            elif 10 < relativeDiff <= 15:
                result = random.choice([0, 1])
            elif 15 < relativeDiff <= 50:
                result = random.choice([0, 1])
            else:
                result = random.choice([0, 1])

        return result

    def bowlMiddle(self, relativeDiff, agg):
        result = 0

        if agg == "super":
            if 0 < relativeDiff <= 2:
                result = random.choice([0, 1, 1, 2])
            elif 2 < relativeDiff <= 4:
                result = random.choice([0, 0, 1, 1, 2, 1])
            elif 4 < relativeDiff <= 6:
                result = random.choice([0, 0, 0, 1, 1, "w"])
            elif 6 < relativeDiff <= 10:
                result = random.choice([0, 0, 0, 1, "w"])
            elif 10 < relativeDiff <= 15:
                result = random.choice([0, 1, "w"])
            elif 15 < relativeDiff <= 25:
                result = random.choice([0, "w"])
            else:
                result = "w"

        elif agg == "high":
            if 0 < relativeDiff <= 2:
                result = random.choice([0, 1, 1, 2])
            elif 2 < relativeDiff <= 4:
                result = random.choice([0, 0, 1, 1, 2, 1])
            elif 4 < relativeDiff <= 10:
                result = random.choice([0, 0, 0, 1, 1, "w"])
            elif 10 < relativeDiff <= 15:
                result = random.choice([0, 1, "w"])
            elif 15 < relativeDiff <= 25:
                result = random.choice([0, "w"])
            else:
                result = "w"
        
        elif agg == "normal":
            if 0 < relativeDiff <= 2:
                result = random.choice([0, 1, 2, 2])
            elif 2 < relativeDiff <= 4:
                result = random.choice([0, 0, 1, 2, 2, 1])
            elif 4 < relativeDiff <= 10:
                result = random.choice([0, 0, 0, 1, 1, 1, "w"])
            elif 10 < relativeDiff <= 15:
                result = random.choice([0, 1, "w"])
            elif 15 < relativeDiff <= 25:
                result = random.choice([0, "w"])
            else:
                result = "w"
        
        elif agg == "low":
            if 0 < relativeDiff <= 2:
                result = random.choice([0, 1, 1, 2, 3])
            elif 2 < relativeDiff <= 4:
                result = random.choice([0, 0, 1, 1, 2, 1, 2])
            elif 4 < relativeDiff <= 10:
                result = random.choice([0, 0, 0, 1, 1, 1, 1])
            elif 10 < relativeDiff <= 15:
                result = random.choice([0, 1, 1])
            elif 15 < relativeDiff <= 25:
                result = random.choice([0, 1])
            else:
                result = random.choice([0, 1])

        return result

    def bowlDeath(self, relativeDiff, agg):
        result = 0

        if agg == "super":
            if 0 < relativeDiff <= 2:
                result = random.choice([0, 1])
            elif 2 < relativeDiff <= 5:
                result = random.choice([0, 0, 1, "w"])
            elif 5 < relativeDiff <= 10:
                result = random.choice([0, 1, "w"])
            elif 10 < relativeDiff <= 15:
                result = random.choice([0, "w"])
            else:
                result = "w"

        elif agg == "high":
            if 0 < relativeDiff <= 2:
                result = random.choice([0, 1, 1, 2])
            elif 2 < relativeDiff <= 5:
                result = random.choice([0, 0, 1, 1, 1, "w"])
            elif 5 < relativeDiff <= 10:
                result = random.choice([0, 0, 1, "w"])
            elif 10 < relativeDiff <= 15:
                result = random.choice([0, 1, "w"])
            elif 15 < relativeDiff <= 25:
                result = random.choice([0, "w"])
            else:
                result = "w"
        
        elif agg == "normal":
            if 0 < relativeDiff <= 2:
                result = random.choice([0, 1, 1, 2])
            elif 2 < relativeDiff <= 5:
                result = random.choice([0, 0, 1, 1, 1])
            elif 5 < relativeDiff <= 10:
                result = random.choice([0, 0, 1, "w"])
            elif 10 < relativeDiff <= 15:
                result = random.choice([0, 1, "w"])
            elif 15 < relativeDiff <= 25:
                result = random.choice([0, "w"])
            else:
                result = "w"
        
        elif agg == "low":
            if 0 < relativeDiff <= 2:
                result = random.choice([0, 1, 1, 2, 3])
            elif 2 < relativeDiff <= 5:
                result = random.choice([0, 0, 1, 1, 1, 2])
            elif 5 < relativeDiff <= 10:
                result = random.choice([0, 0, 1, 1, "w"])
            elif 10 < relativeDiff <= 15:
                result = random.choice([0, 0, 1, "w"])
            elif 15 < relativeDiff <= 25:
                result = random.choice([0, "w"])
            else:
                result = "w"

        return result

    def calculateResult(self, relativeDiff, win):
        result = 0
        if self.striker.batSkill < 60:  # for tailenders
            exp =  self.striker.experience
            skill = self.bowler.bowlSkill
            if skill > 80:
                if 0 <= exp < 60:
                    result = random.choice([0, 0, 0, 1, "w", "w", 2, 2, 1, 0])
                elif 60 <= exp < 75:
                    result = random.choice([0, 0, 1, 1, "w", 0, 2, 2, 2, 1, 4])
                elif 75 <= exp < 85:
                    result = random.choice([0, 0, 1, 1, "w", 2, 2, 2, 1, 4])
                else:
                    result = random.choice([0, 0, 1, 1, "w", 2, 2, 2, 1, 4, 1, 0])
            else:
                if 0 <= exp < 60:
                    result = random.choice([0, 1, "w", "w", 2, 2, 1, 0])
                elif 60 <= exp < 70:
                    result = random.choice([0, 0, 0, 1, 1, "w", 2, 2, 2, 1, 4])
                elif 70 <= exp < 85:
                    result = random.choice([0, 0, 0, "w", 1, 1, 2, 2, 2, 1, 4])
                else:
                    result = random.choice([0, 0, 0, "w", 1, 1, 1, 2, 2, 2, 1, 4, 6])
        
        elif win == "bat":
            if self.balls<=36:
                agg = "normal"
            else:
                agg = "low"
            
            if self.actualReqRunRate - self.currentRunRate > 1:
                agg = self.striker.batAggression
            try:
                strikeRate = ((self.striker.runs*100)/self.striker.ballsFaced)
            except:
                strikeRate = 0
            if strikeRate <= 125:
                agg = self.striker.batAggression
            
            if self.striker.confidenceVars["bl10b"] == 0:
                agg = self.striker.batAggression
            
            if self.balls <= 36:  # hard hitting
                result = self.batPowerPlay(relativeDiff, agg)
           
            elif self.balls <= 96:  # normal hits
                result = self.batMiddle(relativeDiff, agg)
            
            elif self.balls <= 120:  # hard hitting
                if self.balls>=102:
                    agg = self.striker.batAggression
                result = self.batDeath(relativeDiff, agg)
            
        elif win == "bowl":
            agg = "low"
            if self.currentRunRate - self.actualReqRunRate >= 1:
                agg = self.bowler.bowlAggression
            try:
                if (self.bowler.runsGiven * 6)/self.bowler.ballsBowled >= 8:
                    agg = self.bowler.bowlAggression
            except:
                pass
            if self.balls <= 36:
                result = self.bowlPowerPlay(relativeDiff, agg)
            elif self.balls <= 96:
                result = self.bowlMiddle(relativeDiff, agg)
            elif self.balls <= 120:
                if self.balls>=102:
                    agg = self.bowler.bowlAggression
                result = self.bowlDeath(relativeDiff, agg)

        return result

    def thisBall(self):
        result = None
        batsmanScore = self.getBatsmanScore()
        bowlerScore = self.getBowlerScore()
        batsmanScore /= MaxScore
        bowlerScore /= MaxScore
        # print("Batsman Score:", batsmanScore, "Bowler Score:", bowlerScore)  # testing
        #comeback
        self.update_win(batsmanScore, bowlerScore)

        if self.batComeback:
            self.batComeback = False
            return random.choice([2, 3, 4, 4, 4, 6, 6])
        elif self.bowlComeback:
            self.bowlComeback = False
            if self.bowler.bowlSkill > 70:
                return random.choice([0, 0, 0, 1, 1, 2, "w"])
            else:
                return random.choice([0, 0, 0, 1, 1, 2])
        else:
            pass

        if batsmanScore == bowlerScore:
            relativeDiff = 0
            result = random.choice([0, 1])
            self.relativeBowlFrequency(relativeDiff)

        elif batsmanScore > bowlerScore:
            try:
                relativeDiff = ((batsmanScore - bowlerScore) / bowlerScore) * 100 
            except:
                relativeDiff = 100
            self.relativeFrequency(relativeDiff)

            # deciding result
            result = self.calculateResult(relativeDiff,"bat")
        else:
            try:
                relativeDiff = ((bowlerScore - batsmanScore) / batsmanScore) * 100 
            except:
                relativeDiff = 100
            self.relativeBowlFrequency(relativeDiff)
            # deciding result
            result = self.calculateResult(relativeDiff,"bowl")

        result = self.ground.checkField(result)  # checking field type for the result, and changing the result.
        # print("Relative:", relativeDiff)  # testing
        return result

    def getBowlerScore(self): # depends on dynamic variables
        self.bowler.calculateBowlerScore()
        score = self.bowler.bowlerScore
        score += self.bowlingTeam.captain.experience + self.bowlingTeam.wktKeeper.wktSkill
        score += self.ground.bowler_stadium_benefits(self.bowler)
        return score

    def getBatsmanScore(self): # depends on dynamic variables
        self.striker.calculateBatsmanScore()
        score = self.striker.batsmanScore
        score += self.battingTeam.captain.experience + self.nonStriker.experience
        score += self.ground.batsman_stadium_benefits()
        return score

    def setupPlayers(self):
        if self.striker is not None and self.nonStriker is not None and self.bowler is not None:
            # for striker and non striker:
            # for stamina:
            self.striker.setInitialStamina()
            self.nonStriker.setInitialStamina()
            # for comfort:
            if self.battingTeam.homeGround.name == self.ground.name:
                homeGround = True
            else:
                homeGround = False
            self.striker.setInitialBatComfort(self.wickets, homeGround)
            self.nonStriker.setInitialBatComfort(self.wickets, homeGround)
            self.striker.updateBatComfort(self.bowler)
            self.nonStriker.updateBatComfort(self.bowler)
            # for pressure:
            self.striker.setInitialPressure()
            self.nonStriker.setInitialPressure()        
            # for confidence:
            self.striker.setBatsmanConfidence(self.balls)
            self.nonStriker.setBatsmanConfidence(self.balls)
            
            # for bowler:
            # for stamina:
            self.bowler.setInitialStamina()
            # for comfort:
            if self.bowlingTeam.homeGround.name == self.ground.name:
                homeGround = True
            else:
                homeGround = False
            crrOver = int(self.balls / 6) + 1
            self.bowler.setInitialBowlComfort(crrOver, homeGround)
            self.bowler.updateBowlComfort(self.striker)
            # for pressure:
            self.bowler.setInitialPressure()
            # for confidence:
            self.bowler.setBowlerConfidence()

    def setupNewBatsman(self):
        if self.striker is not None:
            # for stamina:
            self.striker.setInitialStamina()
            # for comfort:
            if self.battingTeam.homeGround.name == self.ground.name:
                homeGround = True
            else:
                homeGround = False
            self.striker.setInitialBatComfort(self.wickets, homeGround)
            self.striker.updateBatComfort(self.bowler)
            # for pressure:
            self.striker.setInitialPressure()
            # for confidence:
            self.striker.setBatsmanConfidence(self.balls)

    def comeback(self, needOfComeback=None):
        if needOfComeback == "batsman":
            if self.win['batsman'] <= 4:
                if self.striker.battingType in ['top', 'middle', 'finisher']:
                    if self.striker.pressure >= 25:
                        self.batComeback = True
                        if self.currentRunRate < self.requiredRunRate:
                            self.striker.setInitialPressure()
                            self.nonStriker.setInitialPressure()
                        else:
                            pass
                        
                    if self.striker.confidence < 75:
                        self.striker.confidence = 90

                    if self.nonStriker.confidence < 75:
                        self.nonStriker.confidence = 90

        else:
            if self.win['bowler'] <= 3:
                if 1 <= self.wickets <= 5:
                    if self.bowler.pressure >= 25:
                        self.bowlComeback = True
                        if self.currentRunRate > self.requiredRunRate:
                            self.bowler.setInitialPressure()
                        else:
                            pass
                        if self.bowler.pressure < 0:
                            self.bowler.setInitialPressure()

                    if self.bowler.confidence < 75:
                        self.bowler.confidence = 90
        
    def updatePlayers(self, result):
        if self.striker is not None and self.nonStriker is not None and self.bowler is not None: 
            extra = None
            if result in [0, 1, 2, 3, 4, 6]:
                self.totalRuns += result
                self.balls += 1
                self.striker.runs += result
                self.striker.ballsFaced += 1
                self.bowler.runsGiven += result
                self.bowler.ballsBowled += 1
                self.boundaries[result] += 1  # testing
                # print("This ball result:", result)  # testing
            elif result == "wd":
                self.extras["wd"] += 1 # testing
                self.bowler.runsGiven += 1
                self.totalRuns += 1
                # print("This ball result:", result)  # testing 
            elif result == "nb":
                self.extras["nb"] += 1  # testing
                extra = random.choice([0, 0,  2, 2, 2, 4, 4, 6])
                self.striker.runs += extra
                self.bowler.runsGiven += 1 + extra
                result = extra
                self.totalRuns += 1 + extra
                # print("This ball result: nb +", result)  # testing
            elif result == "w":
                self.balls += 1
                self.bowler.wickets += 1
                self.bowler.ballsBowled += 1
                self.striker.ballsFaced += 1
                # print("This ball result:", result)  # testing
                # for bowler:
                # for stamina:
                currentOver = int(self.balls/6)
                self.bowler.bowler_stamina(currentOver)
                # for comfort: comfort handeled after new striker comes
                # for pressure:
                self.bowler.update_bowler_pressure(result, self.requiredRunRate, self.currentRunRate, self.wickets, self.balls)
                # for confidence:
                self.bowler.updateBowlerConfidence(result)
                return

            # for striker and non striker:
            # for stamina:
            if result in [1, 2, 3]:
                self.striker.batsman_stamina(result)
                self.nonStriker.batsman_stamina(result)
            else:
                self.striker.batsman_stamina(result)
            # for comfort:
            # no need to update comfort here, comfort changes after an over
            # for confidence:
            self.striker.updateBatsmanConfidence(result)
            # for pressure:
            self.striker.update_batsman_pressure(result, self.requiredRunRate, self.actualReqRunRate, self.currentRunRate, self.wickets, self.balls)

            # for bowler:
            # for stamina:
            currentOver = int(self.balls/6)
            self.bowler.bowler_stamina(currentOver)
            # for comfort:
            self.bowler.updateBowlComfort(self.striker)        
            # for confidence:
            self.bowler.updateBowlerConfidence(result)
            # for pressure:
            self.bowler.update_bowler_pressure(result, self.requiredRunRate, self.currentRunRate, self.wickets, self.balls)

            # returning extra runs on a no ball
            return extra

    def updateScoreCard(self, result):
        extra = self.updatePlayers(result)  # this is called before strike changes
        if result == "w":  # use random for different out results
            self.wickets += 1
            try:
                self.alreadyBat.append(self.striker.name)
                self.striker = self.battingLineup.pop(0)
                self.battingTeam.batsmanBin.append(self.striker)
            except:
                pass
            self.setupNewBatsman()
            self.bowler.updateBowlComfort(self.striker)
        elif result in [1, 3]:
            self.striker, self.nonStriker = self.nonStriker, self.striker  # interchanging batsmen, when strike changes
        
        # if extra != None:
            #     result = str(result) + "+" + str(extra)
            
        if result in ["wd", "nb"]:
            if result == "wd":
                self.extras["wd"] += 1
            else:
                self.extras["nb"] += 1
            self.extras["total"] += 1  
        else:
            self.perBallResults[self.balls] = {
                "score":str(self.totalRuns)+"/"+str(self.wickets), 
                "striker":{"name": self.striker.name, "runs": self.striker.runs, "balls": self.striker.ballsFaced},
                "nonstriker":{"name": self.nonStriker.name, "runs": self.nonStriker.runs, "balls": self.nonStriker.ballsFaced},
                "bowler":{"name": self.bowler.name, "runs": self.bowler.runsGiven, "balls": self.bowler.ballsBowled, "wickets": self.bowler.wickets},
                "result": result}

    # testing
    def relativeFrequency(self, rd):
        if 0<=rd<=1:
            self.frequency["0-1"] = self.frequency.get("0-1",0) + 1
        elif 1<=rd<=2:
            self.frequency["1-2"] = self.frequency.get("1-2",0) + 1
        elif 3<=rd<=4:
            self.frequency["3-4"] = self.frequency.get("3-4",0) + 1
        elif 4<=rd<=5:
            self.frequency["4-5"] = self.frequency.get("4-5",0) + 1
        elif rd<=10:
            self.frequency["5-10"] = self.frequency.get("5-10",0) + 1
        elif rd<=15:
            self.frequency["10-15"] = self.frequency.get("10-15",0) + 1
        elif rd<=20:
            self.frequency["15-20"] = self.frequency.get("15-20",0) + 1
        elif rd<=25:
            self.frequency["20-25"] = self.frequency.get("20-25",0) + 1
        elif rd<=30:
            self.frequency["25-30"] = self.frequency.get("25-30",0) + 1
        elif rd<=40:
            self.frequency["30-40"] = self.frequency.get("30-40",0) + 1
        elif rd<=50:
            self.frequency["40-50"] = self.frequency.get("40-50",0) + 1
        else:
            self.frequency["50-"] = self.frequency.get("50-",0) + 1

    def relativeBowlFrequency(self, rd):
        if 0<=rd<=1:
            self.bfrequency["0-1"] = self.bfrequency.get("0-1",0) + 1
        elif 1<=rd<=2:
            self.bfrequency["1-2"] = self.bfrequency.get("1-2",0) + 1
        elif 3<=rd<=4:
            self.bfrequency["3-4"] = self.bfrequency.get("3-4",0) + 1
        elif 4<=rd<=5:
            self.bfrequency["4-5"] = self.bfrequency.get("4-5",0) + 1
        elif rd<=10:
            self.bfrequency["5-10"] = self.bfrequency.get("5-10",0) + 1
        elif rd<=15:
            self.bfrequency["10-15"] = self.bfrequency.get("10-15",0) + 1
        elif rd<=20:
            self.bfrequency["15-20"] = self.bfrequency.get("15-20",0) + 1
        elif rd<=25:
            self.bfrequency["20-25"] = self.bfrequency.get("20-25",0) + 1
        elif rd<=30:
            self.bfrequency["25-30"] = self.bfrequency.get("25-30",0) + 1
        elif rd<=40:
            self.bfrequency["30-40"] = self.bfrequency.get("30-40",0) + 1
        elif rd<=50:
            self.bfrequency["40-50"] = self.bfrequency.get("40-50",0) + 1
        else:
            self.bfrequency["50-"] = self.bfrequency.get("50-",0) + 1

    def disp(self):
        return
        print("Total-Runs:", self.totalRuns, "    Remaining:", self.target-self.totalRuns, '   balls-remaining:', 120-self.balls)
        print()
        print("currentRunRate:", self.currentRunRate, "requiredRunRate:", self.requiredRunRate)
        print(" Striker: ", self.striker.name, " stamina: ", "{:.2f}".format(self.striker.stamina), " pressure:", "{:.2f}".format(self.striker.pressure), " confidence:", "{:.2f}".format(self.striker.confidence), "comfort:", "{:.2f}".format(self.striker.comfort))
        print(" Non Striker: ", self.nonStriker.name, " stamina: ", "{:.2f}".format(self.nonStriker.stamina), " pressure:", "{:.2f}".format(self.nonStriker.pressure), " confidence:", "{:.2f}".format(self.nonStriker.confidence), "comfort:", "{:.2f}".format(self.nonStriker.comfort))
        print(" Bowler: ", self.bowler.name, " stamina: ", "{:.2f}".format(self.bowler.stamina), " pressure:", "{:.2f}".format(self.bowler.pressure), " confidence:", "{:.2f}".format(self.bowler.confidence), "comfort:", "{:.2f}".format(self.bowler.comfort))
        print("========================================================================================================")
        print()
    
    def displayPlayerStats(self):
        return
        print("Score: ", self.totalRuns, "/", self.wickets, "  Overs: ", self.balls//6, ".", self.balls%6, sep="")
        if self.innings == 2:
            print("Target:", self.target)
        print("Batting Team:")
        for i in self.battingTeam.batsmanBin:
            if self.striker.name == i.name or self.nonStriker.name == i.name:
                print(i.name+"*", ": Runs:", i.runs, " Balls:", i.ballsFaced)
            else:
                print(i.name, ": Runs:", i.runs, " Balls:", i.ballsFaced)
        print("\nBowling Team:")
        for i in self.bowlingTeam.bowlerBin:
            print(i.name, ": Runs:", i.runsGiven, " Wickets:", i.wickets, " Balls:", i.ballsBowled)    
        # testing
        print("Per Over Results:")
        ovrs = []
        ct = 1
        for i in self.perOverRuns:
            nm = self.perOverRuns[i][2].split()
            nm = nm[0][0] + " " +nm[len(nm)-1]
            ovrs.append(str(ct)+" "+ nm)
            ct += 1 
        rns = [self.perOverRuns[i][0] for i in self.perOverRuns]
        wkts = [self.perOverRuns[i][1] for i in self.perOverRuns]
        graphs = [("*" * i)+("w" * j) for i,j in list(zip(rns, wkts))]
        titles = ['Overs', 'Runs', 'Wickets', 'Graphs']
        data = [titles] + list(zip(ovrs, rns, wkts, graphs))
        t = 0
        for i, d in enumerate(data):
            line = '| '.join(str(x).ljust(18) for x in d)
            if i == 0:
                t = len(line)
                print('-' * len(line))
            print(line)
            if i == 0:
                t = len(line)
                print('-' * len(line))
        print('-' * t)
      
        print("Innings", self.innings, "end!")

        print("\nBowlers:", self.bfrequency)
        print("Batsmen:", self.frequency)
        print(self.boundaries)

    def setScorecard(self):
        if self.innings == 1:
            self.scorecard1st['score'] = self.totalRuns
            self.scorecard1st['wickets'] = self.wickets
            self.scorecard1st['overs'] = str(self.balls//6) + "." +str(self.balls%6)
            self.scorecard1st['extras'] = self.extras

            batting = dict()
            bowling = dict()
            number = 1
            for i in self.battingTeam.batsmanBin:
                if self.striker.name == i.name or self.nonStriker.name == i.name:
                    if self.wickets == 10:  # when wickets are 10, only one is not out!
                        if self.nonStriker.name == i.name:
                            p = dict()
                            p['number'] = number
                            p['runs'] = str(i.runs) + "*"
                            p['ballsfaced'] = i.ballsFaced
                            batting[i.name] = p
                        continue
                    p = dict()
                    p['number'] = number
                    p['runs'] = str(i.runs) + "*"
                    p['ballsfaced'] = i.ballsFaced
                    batting[i.name] = p
                else:
                    p = dict()
                    p['number'] = number
                    p['runs'] = str(i.runs)
                    p['ballsfaced'] = i.ballsFaced
                    batting[i.name] = p
                number += 1
             
            for i in self.bowlingTeam.bowlerBin:
                p = dict()
                p['runsgiven'] = i.runsGiven
                p['wickets'] = i.wickets
                p['ballsbowled'] = str(i.ballsBowled // 6) + "." + str(i.ballsBowled % 6)
                bowling[i.name] = p
            
            self.scorecard1st['batting'] = batting
            self.scorecard1st['bowling'] = bowling
            self.scorecard1st['battingTeam'] = self.battingTeam.name
            self.scorecard1st['bowlingTeam'] = self.bowlingTeam.name
        else:
            self.scorecard2nd['target'] = self.target
            self.scorecard2nd['score'] = self.totalRuns
            self.scorecard2nd['wickets'] = self.wickets
            self.scorecard2nd['overs'] = str(self.balls//6) + "." +str(self.balls%6)
            self.scorecard2nd['extras'] = self.extras

            batting = dict()
            bowling = dict()
            number = 1
            for i in self.battingTeam.batsmanBin:
                if self.striker.name == i.name or self.nonStriker.name == i.name:
                    if self.wickets == 10:
                        if self.nonStriker.name == i.name:
                            p = dict()
                            p['number'] = number
                            p['runs'] = str(i.runs) + "*"
                            p['ballsfaced'] = i.ballsFaced
                            batting[i.name] = p
                        continue
                    p = dict()
                    p['number'] = number
                    p['runs'] = str(i.runs) + "*"
                    p['ballsfaced'] = i.ballsFaced
                    batting[i.name] = p
                else:
                    p = dict()
                    p['number'] = number
                    p['runs'] = str(i.runs)
                    p['ballsfaced'] = i.ballsFaced
                    batting[i.name] = p
                number += 1
                
            for i in self.bowlingTeam.bowlerBin:
                p = dict()
                p['runsgiven'] = i.runsGiven
                p['wickets'] = i.wickets
                p['ballsbowled'] = str(i.ballsBowled // 6) + "." + str(i.ballsBowled % 6)
                bowling[i.name] = p
            
            self.scorecard2nd['batting'] = batting
            self.scorecard2nd['bowling'] = bowling
            self.scorecard2nd['battingTeam'] = self.battingTeam.name
            self.scorecard2nd['bowlingTeam'] = self.bowlingTeam.name
            
    def getScorecardDetails(self):
        scorecard = dict()
        scorecard[1] = self.scorecard1st
        scorecard[2] = self.scorecard2nd
        scorecard['winner'] = self.winner
        
        totalBalls = len(self.perBallResults1)    
        remainingBalls = 6 - totalBalls%6
        if remainingBalls != 6:
            for i in range(remainingBalls):
                self.perBallResults1[totalBalls+i+1] = self.perBallResults1[totalBalls+i].copy()
                self.perBallResults1[totalBalls+i+1]["result"] = "-"


        totalBalls = len(self.perBallResults2)    
        remainingBalls = 6 - totalBalls%6
        if remainingBalls != 6:
            for i in range(remainingBalls):
                self.perBallResults2[totalBalls+i+1] = self.perBallResults2[totalBalls+i].copy()
                self.perBallResults2[totalBalls+i+1]["result"] = "-"

        scorecard['perBallResults1'] = self.perBallResults1
        scorecard['perBallResults2'] = self.perBallResults2
        scorecard['superover'] = self.superOverScore
        return scorecard