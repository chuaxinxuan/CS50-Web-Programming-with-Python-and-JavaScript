from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass


class AuctionListing(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length = 100)
    description = models.TextField()
    bid = models.DecimalField(max_digits=10, decimal_places=2) # starting price
    current_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField()
    category = models.CharField(max_length = 100, default = "No category or Others")
    active = models.BooleanField(default = True)


class WatchList(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)


class Bid(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="listing")
    bid_price = models.DecimalField(max_digits=10, decimal_places=2)


class Comment(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE) 
    comment = models.TextField()
    created = models.DateTimeField(default = timezone.now)