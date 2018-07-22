
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from sports.models import Sport
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import Point
import base64

# Create your models here.

class Playground(models.Model):
    name = models.CharField(default='playground',max_length=200,blank=False)
    description=models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    sport = models.ForeignKey(Sport,on_delete=models.CASCADE)
    creator = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.TextField(blank=False)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    location = models.PointField(max_length=40, blank=True,null=True)
    preferred_radius = models.IntegerField(default=5, help_text="in kilometers")
    picture = models.ImageField(blank=True,upload_to='playground_picture/')


    def save(self, *args, **kwargs):
        if self.latitude and self.longitude:
             self.location = Point(self.longitude, self.latitude)

        super(Playground, self).save(*args, **kwargs)
