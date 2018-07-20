from rest_framework import serializers
from .models import Post,PostImage
from django.contrib.auth.models import User

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ('image','post')

class PostSerializer(serializers.HyperlinkedModelSerializer):
    user_id = serializers.ReadOnlyField(source='user.id')
    images = PostImageSerializer(source='postimage_set', many=True, read_only=True)
    body = serializers.CharField(required=True)
    class Meta:
        model = Post
        fields = ('id','user_id','body','created_at','is_active','images')

    def create(self, validated_data):
        #print("Inside serializers")
        images_data = self.context.get('view').request.FILES.getlist('file')
        task = Post.objects.create(body = validated_data.get('body', 'no-title'),is_active = validated_data.get('is_active', True),
                        user_id=self.context.get('view').request.user)
        for image_data in images_data:
            PostImage.objects.create(post=task, image=image_data)
        return task
