from rest_framework import serializers

class FriendSerializer(serializers.Serializer):
    creator=serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    friend = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model=friendship
        fields = ('id','creator','friend','created')


    def create(self,validated_data):
        friendship = Friendship.objects.create(creator=self.context.get('view').request.user,friend = validated_data.get('friend'))
        return friendship
