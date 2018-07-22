from rest_framework import serializers
from playground.models import Playground
from django.contrib.gis.geos import GEOSGeometry
from sportsapp.BaseField import Base64ImageField
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import fromstr



class PlaygroundSerializer(serializers.ModelSerializer):
       picture = Base64ImageField(source='playground.picture',required=False)
       location = serializers.SerializerMethodField(required=False,source='playgrpund.location')

       class Meta:
           model=Playground
           fields=('id','name','creator','created_at','address','latitude','longitude','location','preferred_radius','picture','description','sport')

       def get_location(self,instance):
           ret = instance
           pnt = fromstr(instance.location)
           pnt = {'longitude': pnt.coords[0], 'latitude': pnt.coords[1]}
           return pnt
