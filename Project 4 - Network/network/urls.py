
from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post", views.post, name = "post"),
    path("profile/<int:userid>", views.profile, name = "profile"),
    path("follow/<int:userid>", views.follow, name = "follow"), 
    path("unfollow/<int:userid>", views.unfollow, name = "unfollow"),
    path("following", views.following, name="following"),
    path("edit_post/<int:postid>", views.edit_post, name="edit_post"),
    path("like/<int:postid>", views.like_post, name="like_post"),
    path("unlike/<int:postid>", views.unlike_post, name="unlike_post")
]
 