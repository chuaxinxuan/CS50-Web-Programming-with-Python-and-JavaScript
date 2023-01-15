from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("listing/<int:listing_id>", views.listing_page, name="listing_page"),
    path("watching/<int:listing_id>", views.watching, name="watching"),
    path("unwatch/<int:listing_id>", views.unwatch, name="unwatch"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name = "categories"),
    path("categories/<str:category_name>", views.category, name="category"),
    path("closebid/<int:listing_id>", views.closebid, name="closebid"),
    path("comment/<int:listing_id>", views.comment, name="comment")
]
