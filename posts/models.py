from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.CharField(blank=False,max_length=100000)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
       ordering = ('created_at',)

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)

class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.FileField(blank=True,upload_to='post_images/')
