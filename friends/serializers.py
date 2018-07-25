from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Friendship

class FriendSerializer(serializers.Serializer):
    creator=serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    friend = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model=Friendship
        fields = ('id','creator','friend','created','is_accepted')


    def create(self,validated_data):
        friendship = Friendship.objects.create(creator=self.context.get('view').request.user.id,friend = validated_data.get('friend'))
        return friendship

    def update(self,instance,validated_data):
        return super(PlaygroundSerializer, self).update(instance, validated_data)
