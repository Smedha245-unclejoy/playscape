from rest_framework import serializers
from django.contrib.auth.models import User
from posts.models import Post
from .models import Comment,Preference

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())


    class Meta:
        model = Comment
        fields = ('id','author','post','text','created')

    def create(self, validated_data):

        comment = Comment.objects.create(author = self.context.get('view').request.user,post = validated_data.get('post'),
                                       text = validated_data.get('text'))
        return comment

class PreferenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Preference
        fields = ('id','user','post','value')
