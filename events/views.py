from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db import IntegrityError
from django.urls import reverse
import datetime
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_date, parse_time
from django.utils import timezone
from .models import User, Event, WatchList

# Create your views here.
def index(request):
    """This is the home page of the app"""
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    user = request.user
    all_events = Event.objects.filter(user=user).order_by('event_datetime')
    upcoming_events = [event for event in all_events if event.event_datetime >= timezone.now()]
    for event in upcoming_events:
        if WatchList.objects.filter(user=user, event=event).exists():
            event.status = True
    return render(request, "events/index.html", {
        'events': upcoming_events
    })

def event(request, name):
    """This view displays the selected event"""
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    user=request.user
    the_event = Event.objects.get(user=user, event_name=name)
    return render(request, "events/event.html", {
        'event': the_event
    })

def past(request):
    """This view displays all past events"""
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    user = request.user
    all_events = Event.objects.filter(user=user).order_by('-event_datetime')

    past_events = [event for event in all_events if event.event_datetime < timezone.now()]
    return render(request, "events/past.html", {
        'events': past_events
    })

def create(request):
    """This view displays a form that allows to add new event"""
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    user = request.user
    if request.method == 'POST':
        event_name = request.POST.get('eventName')
        event_date = request.POST.get('eventDate')
        event_time = request.POST.get('eventTime')
        event_location = request.POST.get('eventLocation')
        event_description = request.POST.get('eventDescription')

        new_event = Event(
            user=user,
            event_name=event_name,
            event_description=event_description,
            event_datetime=datetime.datetime.combine(parse_date(event_date), parse_time(event_time)),
            event_location=event_location,
        )
        new_event.save()
        return redirect('index')
    return render(request, "events/create.html")

def search(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    user = request.user
    query = request.GET.get('q')

    if query:
        results = Event.objects.filter(event_name__icontains=query, user=user).order_by('event_date')
    else:
        results = []

    for event in results:
        if event.event_datetime >= timezone.now():
            event.status = True
        else:
            event.status = False

    return render(request, 'events/search.html', {
        'query': query,
        'results': results
    })


def delete(request, name):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    user=request.user
    event = get_object_or_404(Event, event_name=name, user=user)
    event.delete()
    return redirect('index')

def watchlist(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    user = request.user
    events = WatchList.objects.filter(user=user)
    return render(request, "events/watchlist.html", {
        'events': events
    })

def addToWatchlist(request, name):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    user = request.user
    event = Event.objects.get(event_name=name)
    if not WatchList.objects.filter(user=user, event=event).exists():
        watchlist_entry = WatchList(user=user, event=event)
        watchlist_entry.save()
    return redirect('index')

def removeFromWatchlist(request, name):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    user=request.user
    the_event = Event.objects.get(user=user, event_name=name)
    event = get_object_or_404(WatchList, event=the_event)
    event.delete()
    return redirect('index')

def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "events/signup.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "events/signup.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "events/signup.html")

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
            return render(request, "events/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "events/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))