from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass
 

class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posted_by")
    post = models.TextField()
    created = models.DateTimeField(default = timezone.now)
    likes = models.IntegerField(default=0)
    liked_by = models.ManyToManyField(User)


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    user_followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")

