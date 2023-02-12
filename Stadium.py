import random
from pmt import *
class Stadium:
    def __init__(self, data):
        self.name = data['name']
        self.weather = data['weather'] # hot, cold, humid, windy, dew
        self.pitch = data['pitch']   # hard, soft, dusty, flat, Sprinkle of grass->green, moist, uneven, cracked
        self.field = data['field'] # more grass, less grass, large/small out field, soft ground and moist ground
        self.averageRuns = data['average'] #averge runs on that pitch
    
    def batsman_stadium_benefits(self):  # called while calculating score
        benefit = 0.0
        # weather is out of 5:
        if self.weather == "hot":
            benefit += 3  
        elif self.weather == "cold":
            benefit += 4
        elif self.weather == "dew":
            benefit += 5
        # pitch is out of 5:
        if self.pitch == "flat":
            benefit += 3
        return benefit

    def bowler_stadium_benefits(self, bowler):  # called while calculating score
        benefit = 0
        # for spinners:
        if "spin" in bowler.bowlingType:
            # weather:
            if self.weather == "hot":
                benefit += 5
            # pitch:
            if self.pitch in ["soft", "dusty", "cracked"]:
                benefit += 5
            elif self.pitch in ["moist", "uneven"]:
                benefit += 4
        # for fast:
        elif "fast" in bowler.bowlingType:
            # weather:
            if self.weather in ["windy", "humid"]:
                benefit += 5
            # pitch:
            if self.pitch in ["hard", "green"]:
                benefit += 5
            elif self.pitch in ["moist", "uneven"]:
                benefit += 4
        # for seam:
        elif "seam" in bowler.bowlingType:
            # weather:
            if self.weather in ["windy", "humid"]:
                benefit += 4
            # pitch:
            if self.pitch in ["soft", "green"]:
                benefit += 3
            elif self.pitch in ["moist", "uneven"]:
                benefit += 4
        return benefit

    def checkField(self, result):  # called after result is decided
        if self.field == "moregrass" and result == 4:
            result = random.choice([4,3,2])
        elif self.field == "lessgrass" and result in [2, 3]:
            if result == 3:
                result = random.choice([4,3])
            else:
                result = random.choice([2, 2, 2, 3])
        elif self.field == "largeoutfield":
            if result == 4:
                result = random.choice([4,3,4,4]) 
            elif result == 6:
                result = random.choice([4,3,6,"w",6])
        elif self.field == "smalloutfield":
            if result == 4:
                result = random.choice([4, 4, 6])
            if result == 3:
                result = random.choice([3, 4, 4])
        elif self.field == "soft":
            if result == 4:
                result = random.choice([4,3,2,4])
        elif self.field == "moist":
            if result == 4:
                result = random.choice([4,3,2,4])
        return result