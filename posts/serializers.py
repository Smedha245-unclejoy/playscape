from rest_framework import serializers
from .models import Post,PostImage
from django.contrib.auth.models import User

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ('image','post')

class PostSerializer(serializers.ModelSerializer):
    #user_id = serializers.ReadOnlyField(source='user.id')
    images = PostImageSerializer(source='postimage_set', many=True, read_only=True)
    #body = serializers.CharField(required=True)
    class Meta:
        model = Post
        fields = ('id','author','body','created_at','is_active','images')

    def create(self, validated_data):
        #print("Inside serializers")
        images_data = self.context.get('view').request.FILES.getlist('file')
        task = Post.objects.create(body = validated_data.get('body', 'no-title'),is_active = validated_data.get('is_active', True),
                        author=self.context.get('view').request.user.id)
        for image_data in images_data:
            PostImage.objects.create(post=task, image=image_data)
        return task

    def update(self,instance,validated_data):
        images_data = self.context.get('view').request.FILES.getlist('file')
        task = super(PostSerializer, self).update(instance, validated_data)
        for image_data in images_data:
            PostImage.objects.update_or_create(post=task,defaults=image_data)

        return task
