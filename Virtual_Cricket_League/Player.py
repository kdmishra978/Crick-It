class Player:
    def __init__(self, data: dict):
        try:
            self.name = data['name']
            self.playerType = data['playertype']  # "allrounder" or "batsman" or "bowler" or "keeper batsman"
            self.battingHand = data['battinghand']  # "right" or "left"
            self.bowlingType = data['bowlingtype']  # "right arm seamer" or "left arm seamer" or "right arm leg spinner" or "left arm off spinner" or "right arm fast" or "left arm fast"
          
            self.experience = data['experience']
            self.age = data['age']
            self.batSkill = data['batskill']
            self.bowlSkill = data['bowlskill']
            self.wktSkill = data['wktskill']

            # something for batting order = [50,50,50,50,85,90,85,50,50,50]
            # {"top":[1-3],"middle":[4-5],"finisher":[6-7],"tailEnder":[8-11]}
            # self.battingType = "top"
            self.battingOrder = eval(data['battingorder'])
            self.battingType = "middle"
            self.setBattingType()
            # something for bowling order = ["powerplay" or "midover" or "deathover"]
            # [1-6,7-15,16-20]
            self.bowlingOrder = data['bowlingorder']
            
            # self.batComfort = ["spin", "seam", "right"]
            # self.bowlComfort = ["right", "left"] -> favourable batting hand to bowl
            self.batComfort = data['batcomfort']
            self.bowlComfort = data['bowlcomfort']

            #NEW *****************************************************************************************************************
            self.bowlAggression = data['bowlaggression']
            self.batAggression = data['bataggression']

        except Exception as e:
            print("Invalid Data in Dictonary", e)

    def getPlayerInfo(self):
        data = {'name':self.name, 'playertype':self.playerType, 'battinghand': self.battingHand, 'bowlingtype': self.bowlingType, 'experience':self.experience, 'age':self.age, 'batskill':self.batSkill, 'bowlskill':self.bowlSkill, 'wktskill':self.wktSkill, 'batcomfort':self.batComfort, 'bowlcomfort':self.bowlComfort, 'battingorder':self.battingOrder, 'bowlingorder':self.bowlingOrder, 'battingtype':self.battingType, 'battingscore':self.battingScore, 'bowlingscore':self.bowlingScore}
        return data
    
    def get_experience(self):
        return self.experience
    
    def get_batSkills(self):
        return self.experience
    
    def get_bowlSkills(self):
        return self.experience
    
    def setBattingType(self):
        order = self.battingOrder.index(max(self.battingOrder))
        order += 1
        if order >= 1 and order <= 3:
            self.battingType = "top"
        elif order >= 4 and order <= 5:
            self.battingType = "middle"
        elif order >= 6 and order <= 7:
            self.battingType = "finisher"
        else:
            self.battingType = "tailEnder"
    
    def __str__(self):
        temp = self.playerType
        if temp == "bowler":
            temp += " (" + self.bowlingType + ")"
        return self.name + "-" + temp

