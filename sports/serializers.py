from rest_framework import serializers
from sports.models import Sport

class SportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sport
        fields = ('id','sport_name','min_participants','max_participants','team')
