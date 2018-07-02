from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Friendship(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    creator = models.ForeignKey(User, related_name="friendship_creator_set",on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name="friend_set",on_delete=models.CASCADE)
