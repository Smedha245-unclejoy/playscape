from rest_framework import serializers
from sports.models import Sport,SportFollower

class SportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sport
        fields = ('id','sport_name','min_participants','max_participants','team')

class SportFollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SportFollower
        fields = ('id','sport','follower')
