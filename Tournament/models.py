import json
from django.db import models
from Teams.models import Team

# Create your models here.
class Tournament(models.Model):
    name = models.CharField(max_length=100, null=False)
    venue = models.CharField(max_length=100, null=False)
    teams = models.ManyToManyField(Team, related_name="teams", null=True)
    number_of_teams = models.IntegerField(null=False)
    overs = models.IntegerField(null=False)
    auction_budget = models.IntegerField(default=100)
    
    def __str__(self):
        return self.name + str('-') + self.venue + str('-') + str(self.number_of_teams)
    
    def get_tournament_details(self):
        teams_list = []
        teams = self.teams.all()
        for team in teams:
            teams_list.append(team.name)
        
        data = {
            'name':self.name,
            'venue':self.venue,
            'teams':teams_list,
            'number_of_teams':self.number_of_teams,
            'overs':self.overs,
            'auction_budget':self.auction_budget
        }
        return json.dumps(data)