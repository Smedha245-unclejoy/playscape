
#from django.db.models.fields import DateField
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.core.validators import MinValueValidator, MaxValueValidator



# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    gender_choices = (('M','Male'),
                        ('F','Female'),
                        ('O','Others'))
    user_gender = models.CharField(choices = gender_choices,max_length=1,blank=True,default='Male')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    #dob = models.DateField()
    last_location = models.PointField(max_length=40, blank=True,null=True)
    prefered_radius = models.IntegerField(default=5, help_text="in kilometers")
    objects = models.GeoManager()

    def save(self, *args, **kwargs):
        if self.latitude and self.longitude:
             self.last_location = Point(self.longitude, self.latitude)

        super(Foo, self).save(*args, **kwargs)
