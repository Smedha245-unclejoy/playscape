from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)

    body = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    activity_choices =(('active','ActivePost'),
                       ('inactive','InactivePost')
                       )
    activity = models.CharField(choices = activity_choices,max_length=8,default='active')
    likes= models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)

class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.FileField(blank=True,upload_to='images/')
