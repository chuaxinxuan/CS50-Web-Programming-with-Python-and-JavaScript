from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.db.models import Max

from .models import *



category_choice = [('No category or Others', 'No category or Others'),
                   ('Fashion', 'Fashion'), 
                   ('Toys', 'Toys'), 
                   ('Electronics', 'Electronics'), 
                   ('Home', 'Home')]
class CreateForm(forms.Form):
    title = forms.CharField(label = "", widget=forms.TextInput(attrs={'placeholder': 'Title', 'size': 247}))
    description = forms.CharField(label = "", widget=forms.Textarea(attrs={'placeholder': 'Description', 'rows': 12, 'cols': 250}))
    bid = forms.DecimalField(label = "", decimal_places = 2, widget=forms.NumberInput(attrs={'placeholder': 'Starting Bid', 'style': 'width: 1860px'}))
    image_url = forms.URLField(label = "", widget=forms.Textarea(attrs={'placeholder': 'Image URL (Optional)', 'rows': 1, 'cols': 250}), required = False)
    category = forms.CharField(label = "", widget=forms.Select(choices=category_choice, attrs={'style': 'width: 1860px'}), required=False)


class BidForm(forms.Form):
    bid = forms.DecimalField(label = "", decimal_places = 2, widget=forms.NumberInput(attrs={'placeholder': 'Bid', 'style': 'width: 1860px; height: 40px'}))

class DummyBidForm(forms.Form):
    bid = forms.DecimalField(label = "", decimal_places = 2, widget=forms.NumberInput(attrs={'placeholder': 'Bid', 'style': 'width: 1860px; height: 40px'}), disabled=True)


class CommentForm(forms.Form):
    comment = forms.CharField(label = "", widget=forms.Textarea(attrs={'placeholder': 'Add a comment...', 'rows': 12, 'cols': 250}))


def index(request):    
    return render(request, "auctions/index.html", {
        "listings": AuctionListing.objects.filter(active = True)
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url='login')
def create_listing(request):
    # Check if method is POST
    if request.method == "POST":
        # Take in the data the user submitted and save it as form
        form = CreateForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():
            # Get the 'cleaned' version of form data
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            bid = form.cleaned_data['bid']
            image_url = form.cleaned_data['image_url']
            category = form.cleaned_data['category']

            # If there is no image url, put a no picture icon
            if not image_url:
                image_url = "https://alpha.inkscape.org/vectors/www.inkscapeforum.com/download/filef3dd.png"

            # Insert into listing database
            listing = AuctionListing(username=request.user, title=title, description=description, bid=bid, current_bid = bid, image_url=image_url, category=category)
            listing.save()

            # Render the active listing page
            return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/create_listing.html", {
        "form": CreateForm()
    })


def listing_page(request, listing_id):
    # Check if an item is already on watchlist of user (for authenticated users only)
    is_watch = False
    if request.user.is_authenticated:
        is_watch = WatchList.objects.filter(username = request.user, listing = AuctionListing.objects.get(id = listing_id)).exists()
    
    starting_bid = AuctionListing.objects.get(id = listing_id).bid
    all_bids = Bid.objects.filter(listing = AuctionListing.objects.get(id = listing_id)).values_list('bid_price', flat = True)
    highest_bidder = Bid.objects.filter(listing = AuctionListing.objects.get(id = listing_id)).order_by('-bid_price').first()

    # get all comments
    all_comments = Comment.objects.filter(listing = AuctionListing.objects.get(id = listing_id)).order_by('-created')

    if highest_bidder != None:
        highest_bidder = highest_bidder.username

    # Check if method is POST
    if request.method == "POST":
        # Take in the data the user submitted and save it as form
        form = BidForm(request.POST)
        # Check if form data is valid (server-side)
        if form.is_valid():
            # Get the 'cleaned' version of form data
            price = form.cleaned_data["bid"]
            # Check if bid is as large as starting bid, and greater than any other bids that have been placed
            if (price >= starting_bid) and (all([price > x for x in all_bids])):
                # bid is successful
                new_bid = Bid(username = request.user, listing = AuctionListing.objects.get(id = listing_id), bid_price = price)
                new_bid.save()
                # update current_bid in AuctionListing
                update_listing = AuctionListing.objects.get(id = listing_id)
                update_listing.current_bid = price
                update_listing.save()
                return render(request, "auctions/listing_page.html", {
                    "listing": AuctionListing.objects.get(id=listing_id),
                    "is_watch": is_watch,
                    "form": BidForm(),
                    "dummy_form": DummyBidForm(),
                    "bid_success": "Pass",
                    "num_bids": len(all_bids) + 1,
                    "highest_bidder": request.user,
                    "comment_form": CommentForm(),
                    "all_comments": all_comments
                })
            else:
                # bid is unsuccessful
                return render(request, "auctions/listing_page.html", {
                    "listing": AuctionListing.objects.get(id=listing_id),
                    "is_watch": is_watch,
                    "form": BidForm(),
                    "dummy_form": DummyBidForm(),
                    "bid_success": "Fail",
                    "num_bids": len(all_bids),
                    "highest_bidder": highest_bidder,
                    "comment_form": CommentForm(),
                    "all_comments": all_comments
                })

    return render(request, "auctions/listing_page.html", {
        "listing": AuctionListing.objects.get(id=listing_id),
        "is_watch": is_watch,
        "form": BidForm(),
        "dummy_form": DummyBidForm(),
        "bid_success": None,
        "num_bids": len(all_bids),
        "highest_bidder": highest_bidder,
        "comment_form": CommentForm(),
        "all_comments": all_comments
    })


@login_required(login_url='login')
def watching(request, listing_id):
    # Add to watchlist database
    watchlist = WatchList(username = request.user, listing = AuctionListing.objects.get(id = listing_id))
    watchlist.save()
    
    return HttpResponseRedirect(reverse("listing_page", args=[listing_id]))


@login_required(login_url='login')
def unwatch(request, listing_id):
    # Remove from watchlist database
    WatchList.objects.filter(username = request.user, listing = AuctionListing.objects.get(id = listing_id)).delete()
    
    return HttpResponseRedirect(reverse("listing_page", args=[listing_id]))


@login_required(login_url='login')
def watchlist(request):
    listing_ids = WatchList.objects.filter(username = request.user).values_list('listing', flat = True)
    listings = AuctionListing.objects.filter(id__in = listing_ids)
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": ['Fashion', 'Toys', 'Electronics', 'Home', "No category or Others"]
    })
def category(request, category_name):
    listings = AuctionListing.objects.filter(category = category_name)
    return render(request, "auctions/category.html", {
        "listings": listings,
        "cat_name": category_name
    })


@login_required(login_url='login')
def closebid(request, listing_id):
    # set listing to inactive in AuctionListing Model
    update_listing = AuctionListing.objects.get(id = listing_id)
    update_listing.active = False
    update_listing.save()

    return HttpResponseRedirect(reverse("index"))


@login_required(login_url='login')
def comment(request, listing_id):
    # Check if method is POST
    if request.method == "POST":
        # Take in the data the user submitted and save it as form
        form = CommentForm(request.POST)
        # Check if form data is valid (server-side)
        if form.is_valid():
            # Get the 'cleaned' version of form data
            comment = form.cleaned_data["comment"]

            # save to database
            add_comment = Comment(username=request.user, listing=AuctionListing.objects.get(id = listing_id), comment=comment)
            add_comment.save()

    return HttpResponseRedirect(reverse("listing_page", args=[listing_id]))

