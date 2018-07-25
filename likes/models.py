from django.db import models
from django.contrib.auth.models import User
from posts.models import Post


# Create your models here.

class Preference(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post =  models.ForeignKey(Post,on_delete=models.CASCADE)
    value= models.IntegerField()

    class Meta:
       unique_together = ('user', 'post', 'value')

class Comment(models.Model):
    post = models.ForeignKey(Post, editable=False,
         related_name='comments',on_delete=models.CASCADE)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    author_name = models.CharField(max_length=200,default='Medha')
