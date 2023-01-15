from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    pass

class Event(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField()
    description = models.TextField(blank=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

class UserEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    status = models.CharField(default = "No response", max_length=100)
