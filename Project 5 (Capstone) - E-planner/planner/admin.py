from django.contrib import admin
from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")

class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "created_by", "title", "description", "date", "start_time", "end_time")

class UserEventAdmin(admin.ModelAdmin):
    list_display = ("user", "event", "status")

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(UserEvent, UserEventAdmin)
