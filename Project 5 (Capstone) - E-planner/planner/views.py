from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.db import IntegrityError
from .models import *
from django.contrib.auth.decorators import login_required
from django import forms
from django.forms import SelectMultiple
from datetime import date, datetime
from django.views.decorators.csrf import csrf_exempt
import calendar


time_choices = (("00:00", "00:00"), ("01:00", "01:00"), ("02:00", "02:00"), ("03:00", "03:00"),
                ("04:00", "04:00"), ("05:00", "05:00"), ("06:00", "06:00"), ("07:00", "07:00"),
                ("08:00", "08:00"), ("09:00", "09:00"), ("10:00", "10:00"), ("11:00", "11:00"),
                ("12:00", "12:00"), ("13:00", "13:00"), ("14:00", "14:00"), ("15:00", "15:00"),
                ("16:00", "16:00"), ("17:00", "17:00"), ("18:00", "18:00"), ("19:00", "19:00"),
                ("20:00", "20:00"), ("21:00", "21:00"), ("22:00", "22:00"), ("23:00", "23:00"))

class NewEventForm(forms.Form):
    username_choices = [(user.id, user) for user in User.objects.all()]

    title = forms.CharField(label="Title", widget=forms.Textarea(), required=True)
    description = forms.CharField(label="Description", widget=forms.Textarea(attrs={'rows': 5, 'cols': 150}), required=False)
    date = forms.DateField(label="Date", widget=forms.SelectDateWidget, initial=f'{date.today()}', required=True)
    start_time = forms.TimeField(label="Start time", widget=forms.Select(choices=time_choices), required=True)
    end_time = forms.TimeField(label="End time", widget=forms.Select(choices=time_choices), required=True)
    attendees = forms.MultipleChoiceField(choices=username_choices, widget=SelectMultiple, required=False)

    def __init__(self, *args, **kwargs):
        super(NewEventForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['style'] = 'width: 70vw; height: 30px;'
        self.fields['description'].widget.attrs['style'] = 'width: 70vw; height: 150px;'

# Create your views here.
def home(request):
    logout(request)
    return render(request, "planner/home_page.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("event", args=[request.user.id]))
        else:
            return render(request, "planner/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "planner/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "planner/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "planner/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("event", args=[request.user.id]))
    else:
        return render(request, "planner/register.html")


@login_required(login_url='login')
def create_event(request):
    # Check if method is POST
    if request.method == "POST":
        # Take in the data the user submitted and save it as form
        form = NewEventForm(request.POST)

        # Check if form data is valid (server-side)
        if not form.is_valid():
            if 'date' in form.errors.get_json_data():
                return render(request, "planner/create_event.html", {
                    "form": NewEventForm(),
                    "error": "True",
                    "message": form.errors.get_json_data()['date'][0]['message']
                })        
        elif form.is_valid():
            # Isolate the task from the 'cleaned' version of form data
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']            
            date = form.cleaned_data['date']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            attendees = form.cleaned_data['attendees']

            if date < date.today(): 
                return render(request, "planner/create_event.html", {
                    "form": NewEventForm(),
                    "error": "True",
                    "message": f'Cannot create an event earlier than {date.today()}!'
                })
            elif start_time >= end_time:
                return render(request, "planner/create_event.html", {
                    "form": NewEventForm(),
                    "error": "True",
                    "message": 'End time must be later than start time!'
                })
            else:
                # Save to event database
                add_event = Event(created_by=User.objects.get(id = request.user.id), title=title, description = description,
                                                            date = date, start_time = start_time, end_time = end_time)

                # Save to UserEvent database
                if str(request.user.id) not in attendees:
                    attendees.append(str(request.user.id))

                # Check for schedule clash:
                for j in attendees:
                    user_schedule = UserEvent.objects.filter(status = 'Accepted', user=User.objects.get(id = j), event__date = date)
                    for i in user_schedule:
                        temp_event = i.event
                        if ((start_time >= temp_event.start_time) and (start_time <= temp_event.end_time)) or ((end_time >= temp_event.start_time) and (end_time <= temp_event.end_time)):
                            return render(request, "planner/create_event.html", {
                                "form": NewEventForm(),
                                "error": "True",
                                "message": f'Unable to schedule event. Schedule clash for {User.objects.get(id = j)}!'
                            })
                
                add_event.save()
                for j in attendees:
                    if j == str(request.user.id):
                        add_userevent = UserEvent(user=User.objects.get(id = request.user.id), event=add_event, status='Accepted')
                        add_userevent.save()
                    else:
                        add_userevent = UserEvent(user=User.objects.get(id = j), event=add_event)
                        add_userevent.save()

                return render(request, "planner/create_event.html", {
                    "form": NewEventForm(),
                    "error": "False",
                    "message": 'Event successfully created!'
                })
    return render(request, "planner/create_event.html", {
        "form": NewEventForm(),
        "error": None,
        "message": None
    })


@login_required(login_url='login')
def invites(request):
    pending_invites = UserEvent.objects.filter(status = 'No response', user=User.objects.get(id = request.user.id))
    return render(request, "planner/invites.html", {
        "events": pending_invites
    })


@csrf_exempt
@login_required(login_url='login')
def accept(request, eventid):
    if request.method == 'POST':
        # check for event clash
        new_event = Event.objects.get(id = eventid)
        clash = False
        accepted_events =  UserEvent.objects.filter(status='Accepted', user=User.objects.get(id = request.user.id), event__date = new_event.date)
        for i in accepted_events:
            if ((new_event.start_time >= i.event.start_time) and (new_event.start_time <= i.event.end_time)) or ((new_event.end_time >= i.event.start_time) and (new_event.end_time <= i.event.end_time)):
                clash = True
        print(clash)
        # If no event clash:
        if not clash:
            # update status
            update_userevent = UserEvent.objects.get(user=User.objects.get(id = request.user.id), event=new_event)
            update_userevent.status = 'Accepted'
            update_userevent.save()
            return JsonResponse({'status': 'success'}, status=200)
        else: 
            return JsonResponse({'status': 'fail'}, status=200)


@csrf_exempt
@login_required(login_url='login')
def decline(request, eventid):
    if request.method == 'POST':
        # update status
        update_userevent = UserEvent.objects.get(user=User.objects.get(id = request.user.id), event=Event.objects.get(id = eventid))
        update_userevent.status = 'Declined'
        update_userevent.save()
        return JsonResponse({}, status=200)


@login_required(login_url='login')
def event(request, userid):
    var_dict =  {
        'current_day': datetime.now().day,
        'current_month': datetime.now().strftime('%B'),
        'current_year': datetime.now().year 
    }
    # Accepted events for today:
    today_events = UserEvent.objects.filter(status = 'Accepted', user=User.objects.get(id = request.user.id)).order_by('event__date', 'event__start_time')
    today_events = [event.event for event in today_events if (event.event.date == date.today())]
    var_dict['today_events'] = today_events
    var_dict['today_events_len'] = len(today_events)

    grid_list = [f'grid_{i}' for i in range(1,43)]
    date_list = calendar.monthcalendar(datetime.now().year, datetime.now().month)
    date_list = [item for sublist in date_list for item in sublist]

    for i in range(42):
        if date_list[i] != 0:
            var_dict[grid_list[i]] = date_list[i]

    # Accepted events for that month and year
    accepted_events = UserEvent.objects.filter(status = 'Accepted', user=User.objects.get(id = request.user.id)).order_by('event__date', 'event__start_time')
    accepted_events = [event.event for event in accepted_events if (event.event.date.month == datetime.now().month) and (event.event.date.year == datetime.now().year)] 

    for event in accepted_events:
        if f'event_{date_list.index(event.date.day) + 1}' not in var_dict:
            var_dict[f'event_{date_list.index(event.date.day) + 1}'] = [event]
        else:
            var_dict[f'event_{date_list.index(event.date.day) + 1}'] = var_dict[f'event_{date_list.index(event.date.day) + 1}'] + [event]

    # current year:
    return render(request, "planner/event.html", var_dict)


@csrf_exempt
@login_required(login_url='login')
def get_event(request, year, month, day):
    event_list = UserEvent.objects.filter(status = 'Accepted', user=User.objects.get(id = request.user.id)).order_by('event__date', 'event__start_time')
    event_title = [event.event.title for event in event_list if (event.event.date == datetime(year,month,day).date())] 
    event_organiser = [event.event.created_by.username for event in event_list if (event.event.date == datetime(year,month,day).date())] 
    event_starttime = [event.event.start_time.strftime('%H:%M') for event in event_list if (event.event.date == datetime(year,month,day).date())] 
    event_endtime = [event.event.end_time.strftime('%H:%M') for event in event_list if (event.event.date == datetime(year,month,day).date())] 
    event_description = [event.event.description for event in event_list if (event.event.date == datetime(year,month,day).date())] 
    event_id = [event.event.id for event in event_list if (event.event.date == datetime(year,month,day).date())] 
    return JsonResponse({'request_user': request.user.username, 'event_id': event_id, 'event_title': event_title, 'event_organiser': event_organiser,
                        'event_starttime': event_starttime, 'event_endtime': event_endtime, 'event_description': event_description}, status=200)


@csrf_exempt
@login_required(login_url='login')
def delete_event(request, eventid):
    # delete event
    Event.objects.filter(id = eventid).delete()
    return HttpResponseRedirect(reverse("event", args=[request.user.id]))


@csrf_exempt
@login_required(login_url='login')
def reject_event(request, eventid):
    # update userevent database
    update_userevent = UserEvent.objects.get(user = User.objects.get(id = request.user.id), event = Event.objects.get(id = eventid))
    update_userevent.status = 'Declined'
    update_userevent.save()
    return HttpResponseRedirect(reverse("event", args=[request.user.id]))