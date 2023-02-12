from django.db import models
from django.core.validators import RegexValidator
from multiselectfield import MultiSelectField

class Player(models.Model):
    name = models.CharField(max_length=100, null=False)
    age = models.IntegerField(validators=[RegexValidator("[1-5]{1}[0-9]{1}", "Age of the player must be in the range of 10-59.", "Age of the player must be in the range of 10-59.")], null=False)
    
    image = models.ImageField(upload_to="Players/", default='Players/default.jpg')
    
    playerType = (
        ('batsman', 'Batsman'),
        ('bowler', 'Bowler'),
        ('allrounder', 'All-Rounder'),
        ('wicketkeeperbatsman', 'Wicket-Keeper Batsman')
    )
    
    playertype = models.CharField(max_length=25, choices=playerType, default='batsman')
    
    battingHand = (
        ('right', 'Right Hand Batsman'),
        ('left', 'Left Hand Batsman')
    )
    
    battinghand = models.CharField(max_length=20, choices=battingHand, default='right')
    
    bowlingType = (
        ('None', 'None'),
        ('right arm fast', 'Right Arm Fast'),
        ('left arm fast', 'Left Arm Fast'),
        ('right arm seam', 'Right Arm Seam'),
        ('left arm seam', 'Left Arm Seam'),
        ('right arm off spin', 'Right Arm Off Spin'),
        ('left arm off spin', 'Left Arm Off Spin'),
        ('right arm leg spin', 'Right Arm Leg Spin'),
        ('left arm leg spin', 'Left Arm Leg Spin'),
    )
    
    bowlingtype = models.CharField(max_length=50, choices=bowlingType, default='None')
    
    experience = models.IntegerField(validators=[RegexValidator("^([0-9]|[1-9][0-9]|100)$", "Value for Experience must be in the range of 0 to 100.", "Value for Experience must be in the range of 0 to 100.")], null=False)
    
    batskill = models.IntegerField(validators=[RegexValidator("^([0-9]|[1-9][0-9]|100)$", "Value for Bat-Skill must be in the range of 0 to 100.", "Value for Bat-Skill must be in the range of 0 to 100.")], null=False)
    
    bowlskill = models.IntegerField(validators=[RegexValidator("^([0-9]|[1-9][0-9]|100)$", "Value for Bowl-Skill must be in the range of 0 to 100.", "Value for Bowl-Skill must be in the range of 0 to 100.")], null=False)
    
    wktskill = models.IntegerField(validators=[RegexValidator("^([0-9]|[1-9][0-9]|100)$", "Value for WicketKeeping-Skill must be in the range of 0 to 100.", "Value for WicketKeeping-Skill must be in the range of 0 to 100.")], null=False)
    
    battingorder = models.CharField(max_length=100, default='[50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50]', null=False)
    
    bowlingOrder = (
        ('powerplay', 'Power-Play'), 
        ('midover', 'Mid-Overs'),
        ('deathover', 'Death-Bowler'),
    ) 
    
    bowlingorder = MultiSelectField(choices=bowlingOrder, max_choices=len(bowlingOrder),
                                 max_length=100)
    
    batComfort = (
        ('fast', 'Fast'),
        ('seam', 'Seam'),
        ('spin', 'Spin'),
        ('right', 'Right-Hand-Bowler'),
        ('left', 'Left-Hand-Bowler')
    )
    
    batcomfort = MultiSelectField(choices=batComfort, max_choices=len(batComfort),
                                 max_length=100)
    
    bowlComfort = (
        ('right', "Right-Hand-Batsman"),
        ('left', "Left-Hand-Batsman")
    )
    
    bowlcomfort = MultiSelectField(choices=bowlComfort, max_choices=len(bowlComfort),
                                 max_length=100)
    
    batAggression = (
        ('super', 'Super'),
        ('high', 'High'),
        ('normal', 'Normal'),
        ('low', 'Low')
    )
    
    bataggression = models.CharField(max_length=10, choices=batAggression, default='normal')
    
    bowlAggression = (
        ('super', 'Super'),
        ('high', 'High'),
        ('normal', 'Normal'),
        ('low', 'Low')
    )
    
    bowlaggression = models.CharField(max_length=10, choices=bowlAggression, default='normal')
    
    available = models.BooleanField(default=True)
    
    runs = models.IntegerField(default=0)
    wickets = models.IntegerField(default=0)
    innings = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name.title()
    
    def get_player_details(self):
        data = {'name':self.name, 'age':self.age, 'playertype':self.playertype, 'battinghand':self.battinghand, 'bowlingtype':self.bowlingtype, 'experience':self.experience, 'batskill':self.batskill, 'bowlskill':self.bowlskill, 'wktskill':self.wktskill, 'battingorder':self.battingorder, 'bowlingorder':self.bowlingorder, 'batcomfort':self.batcomfort, 'bowlcomfort':self.bowlcomfort, 'bataggression':self.bataggression, 'bowlaggression':self.bowlaggression}
        return data