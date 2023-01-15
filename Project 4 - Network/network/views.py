from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from .models import *
import json


class NewPostForm(forms.Form):
    post = forms.CharField(label = "", widget=forms.Textarea(attrs={'rows': 3, 'cols': 245}))


def index(request):   
    post_list = Posts.objects.all().order_by('-created')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "form": NewPostForm(),
        "page_obj": page_obj 
    })
 

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required(login_url='login')
def post(request):
    # Check if method is POST
    if request.method == "POST":
        # Take in the data the user submitted and save it as form
        form = NewPostForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():
            # Isolate the task from the 'cleaned' version of form data
            post = form.cleaned_data['post']

            # Save to database
            add_post = Posts(user=User.objects.get(id = request.user.id), post=post)
            add_post.save()

            return HttpResponseRedirect(reverse("index"))
    return HttpResponseRedirect(reverse("index"))


def profile(request, userid):
    user = User.objects.get(id = userid)
    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(user=User.objects.get(id = request.user.id), user_followed=user).exists()

    post_list = Posts.objects.filter(user=user).order_by('-created')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/profile.html", {
        "user_profile": user,
        "num_followers": Follow.objects.filter(user_followed=user).count(),
        "num_followings": Follow.objects.filter(user=user).count(),
        "page_obj": page_obj,
        "is_following": is_following
    })

@login_required(login_url='login')
def follow(request, userid):
    # Save to database
    add_follow = Follow(user=request.user, user_followed=User.objects.get(id=userid))
    add_follow.save()
    return HttpResponseRedirect(reverse("profile", args=[userid]))

@login_required(login_url='login')
def unfollow(request, userid):
    # Remove from database
    Follow.objects.filter(user=request.user, user_followed=User.objects.get(id=userid)).delete()
    return HttpResponseRedirect(reverse("profile", args=[userid]))


@login_required(login_url='login')
def following(request):
    follow_list = Follow.objects.filter(user=request.user).values_list('user_followed', flat = True)

    post_list = Posts.objects.filter(user__in = follow_list).order_by('-created')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "page_obj": page_obj
    })

@csrf_exempt
@login_required(login_url='login')
def edit_post(request, postid):
    if request.method == 'POST':
        # update post in django model
        update_post = Posts.objects.get(id = postid)
        jsonData = json.loads(request.body)
        update_post.post = jsonData.get('new_post')
        update_post.save()
        return JsonResponse({}, status=200)
    return JsonResponse({"Error 404": "Unable to edit post"}, status=404)


@csrf_exempt
@login_required(login_url='login')
def like_post(request, postid):
    if request.method == 'POST':
        # update like count in django model
        update_like = Posts.objects.get(id = postid)
        update_like.likes = update_like.likes + 1

        # update liked_by
        update_like.liked_by.add(User.objects.get(id = request.user.id))
        update_like.save()

        return JsonResponse({'count': update_like.likes}, status=200)


@csrf_exempt
@login_required(login_url='login')
def unlike_post(request, postid):
    if request.method == 'POST':
        # update like count in django model
        update_like = Posts.objects.get(id = postid)
        update_like.likes = update_like.likes - 1

        # update Likes model
        update_like.liked_by.remove(User.objects.get(id = request.user.id))
        update_like.save()

        return JsonResponse({'count': update_like.likes}, status=200)