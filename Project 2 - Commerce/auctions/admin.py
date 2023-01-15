from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "password")

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "title", "description", "bid", "current_bid", "image_url", "category", "active")

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("username", "listing")

class BidAdmin(admin.ModelAdmin):
    list_display = ("username", "listing", "bid_price")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("username", "listing", "comment", "created")

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(AuctionListing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(WatchList, WatchlistAdmin)