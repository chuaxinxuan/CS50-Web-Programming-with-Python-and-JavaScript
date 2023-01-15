from django.contrib import admin
from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")

class PostsAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "post", "created", "likes")

class FollowAdmin(admin.ModelAdmin):
    list_display = ("user", "user_followed")


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Posts, PostsAdmin)
admin.site.register(Follow, FollowAdmin)
