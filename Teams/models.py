from django.db import models
from django.core.validators import RegexValidator
from multiselectfield import MultiSelectField
from Players.models import Player
import json

class Stadium(models.Model):
    name = models.CharField(max_length=150, null=False)
    
    weather_choices = (
        ('hot', 'Hot'),
        ('cold', 'Cold'),
        ('humid', 'Humid'),
        ('windy', 'Windy'),
        ('dew', 'Dew'),
    )

    weather = models.CharField(max_length=10, choices=weather_choices, default='hot')
    
    pitch_choices = ( 
        ('hard', 'Hard'),
        ('soft', 'Soft'),
        ('dusty', 'Dusty'),
        ('flat', 'Flat'),
        ('green', 'Sprinkle of grass'),
        ('moist', 'Moist'),
        ('uneven', 'Uneven'),
        ('cracked', 'Cracked')
    )
    
    pitch = models.CharField(max_length=30, choices=pitch_choices, default='hard')
    
    field_choices = (
        ('moregrass', 'More Grass'),
        ('lessgrass', 'Less Grass'),
        ('largeoutfield', 'Large Out Field'),
        ('smalloutfield', 'Small Out Field'),
        ('soft', 'Soft Ground'),
        ('moist', 'Moist Ground'),
    ) 
    
    field = models.CharField(max_length=30, choices=field_choices, default='moregrass')
    
    average = models.IntegerField(default=160)
    
    def __str__(self):
        return self.name
    
    def get_stadium_details(self):
        data={'name':self.name, 'weather':self.weather, 'pitch':self.pitch, 'field':self.field, 'average':self.average}
        return data
    
class Team(models.Model):
    name = models.CharField(max_length=100, null=False)
    players = models.ManyToManyField(Player, related_name="players", null=True)
    captain = models.ForeignKey(Player, on_delete=models.CASCADE, null=True, related_name='captain')
    wicketkeeper = models.ForeignKey(Player, on_delete=models.CASCADE, null=True, related_name='wicketkeeper')
    homeground = models.ForeignKey(Stadium, on_delete=models.CASCADE, related_name='homeground', null=True)
    battingLineup = models.TextField(max_length=400, default='NOT SET')
    bowlingLineup = models.TextField(max_length=400, default='NOT SET')
    lineup_flag = models.BooleanField(default=False)
    bugdet = models.FloatField(default=100.0)
    
    owner_name = models.CharField(max_length=100, default="geetansh")
    
    def __str__(self):
        return self.name
    
    def get_team_details(self):
        captain = Player.objects.get(name__iexact=self.captain.name)
        wicketkeeper = Player.objects.get(name__iexact=self.wicketkeeper.name)
        homeground = Stadium.objects.get(name__iexact=self.homeground)
        
        players_list = []
        for player in self.players.all():
            players_list.append(player.get_player_details())
        
        try:
            data={
                'name':self.name,
                'players':players_list,
                'captain':captain.get_player_details(),
                'wktkeeper':wicketkeeper.get_player_details(),
                'homeground':homeground.get_stadium_details(),
                'battinglineup':self.battingLineup,
                'bowlinglineup':self.bowlingLineup,
                'lineup_flag':self.lineup_flag,
            }
        except:
            data ={
                'name':"Default",
                'players':None,
                'captain':None,
                'wktkeeper':None,
                'homeground':None,   
            }
        return json.dumps(data)
    
    def get_team_budget(self):
        return self.budget