from django.db import models
from django.contrib.auth.models import User
from sports.models import Sport
from django.conf import settings
from playground.models import Playground

# Create your models here.

class Event(models.Model):
    sport_category = models.ForeignKey(Sport,on_delete=models.CASCADE)
    playground_destination = models.ForeignKey(Playground,on_delete=models.CASCADE)
    description = models.TextField(default='No description')
    duration = models.TimeField(blank=False)
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=200,blank=False)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateField(blank=False)
    time_from = models.TimeField(blank=False)
    time_to = models.TimeField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True,blank=False)

    class Meta:
       ordering = ('created_at',)


    def save(self, *args, **kwargs):
        super(Event, self).save(*args, **kwargs)



class Participators(models.Model):
    event = models.OneToOneField(Event,on_delete=models.CASCADE)
    participant = models.ForeignKey(User,on_delete=models.CASCADE)
    #participant_name is username so that it will be unique
    participant_name = models.CharField(max_length=100,blank=True)
    confirm = models.BooleanField(default= False)

    class Meta:
       ordering = ('participant_name',)


    def save(self, *args, **kwargs):
        super(Participators, self).save(*args, **kwargs)
