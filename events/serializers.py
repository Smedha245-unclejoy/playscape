from rest_framework import serializers
from .models import Event,Participators
from django.contrib.auth.models import User


class PartcipatorsSerializer(serializers.ModelSerializer):

    class Meta:
        model=Participators
        fields=('id','event','participant','participant_name','confirm')



class EventSerializer(serializers.ModelSerializer):
    participants = PartcipatorsSerializer(source='participators_set',many=True,read_only=True)

    class Meta:
        model=Event
        fields=('id','sport_category','playground_destination','author','date','time_from','time_to','created_at','participants','name','description','duration','is_active')

        def create(self,validated_data):
            participant_data = self.context.get('view').request.data.getlist('participants')
            event = Event.objects.update_or_create(name=validated_data.get('name','name'),description=validated_data.get('description','no description provided'),sport_category=validated_data.get('sport_category',0),playground_destination=validated_data.get('playground_destination',0),
                               author=self.context.get('view').request.user.id,date=validated_data.get('date',''),time_from=validated_data.get('time_from',''),time_to=validated_data.get('time_to',''),duration=validated_data.get('duration',''),is_active=validated_data.get('is_active',True))
            for participant_name in partcipants:
                participant_object = User.objects.get(username=participant_name)
                Participators.objects.update_or_create(event=event,participant=participant_object.id,participant_name=participant_name)
