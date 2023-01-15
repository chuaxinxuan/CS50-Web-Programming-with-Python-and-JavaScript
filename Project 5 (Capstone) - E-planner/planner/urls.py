from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_event", views.create_event, name="create_event"),
    path("invites", views.invites, name="invites"),
    path("accept/<int:eventid>", views.accept, name="accept"),
    path("decline/<int:eventid>", views.decline, name="decline"),
    path("event/<int:userid>", views.event, name="event"),
    path("get_event/<int:year>/<int:month>/<int:day>", views.get_event, name="get_event"),
    path("delete_event/<int:eventid>", views.delete_event, name="delete_event"),
    path("reject_event/<int:eventid>", views.reject_event, name="reject_event")
]