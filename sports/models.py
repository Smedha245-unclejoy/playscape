from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Sport(models.Model):
     sport_name = models.CharField(max_length=100)
     min_participants = models.IntegerField(default=0)
     max_participants = models.IntegerField(default=1)
     team_choices = (('Single Team','SingleTeam'),
                         ('Multiple Team','MultipleTeam'),
                         )
     team = models.CharField(choices=team_choices,max_length=15)

     class Meta:
        ordering = ('sport_name',)


     def save(self, *args, **kwargs):
         super(Sport, self).save(*args, **kwargs)

class SportFollower(models.Model):
    sport = models.ForeignKey(Sport,on_delete=models.CASCADE)
    sport_name = models.CharField(choices = [ (str(o), str(o)) for o in Sport.objects.filter(pk=self.sport)],max_length=20)
    follower = models.ForeignKey(User,on_delete=models.CASCADE)
