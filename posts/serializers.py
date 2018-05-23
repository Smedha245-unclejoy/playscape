from rest_framework import serializers
from posts.models import Post,PostImage
from django.contrib.auth.models import User

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ('image',)

class PostSerializer(serializers.HyperlinkedModelSerializer):
    user_id = serializers.ReadOnlyField(source='user.id')
    images = PostImageSerializer(source='postimage_set', many=True, read_only=True)
    activity_choices = (('active','ActivePost'),
                       ('inactive','InactivePost')
                        )
    activity = serializers.ChoiceField(source='post.activity',choices=activity_choices)
    likes = serializers.IntegerField(default=0)

    class Meta:
        model = Post
        fields = ('id','user_id' ,'body','created_at','activity','likes', 'images')

    def create(self, validated_data):
        #print("Inside serializers")
        images_data = self.context.get('view').request.FILES.getlist('file')
        task = Post.objects.create(body=validated_data.get('body', 'no-title'),activity = validated_data.get('activity', 'active'),
                        likes = validated_data.get('likes',0),user_id=self.context.get('view').request.user)
        for image_data in images_data:
            PostImage.objects.create(post=task, image=image_data)
        return task
