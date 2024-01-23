from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=64)
    email = models.EmailField()
    password = models.CharField(max_length=255)


class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    event_name = models.CharField(max_length=64)
    event_description = models.TextField()
    event_datetime = models.DateTimeField()
    event_location = models.CharField(max_length=32)
    short_description = models.CharField(max_length=50, blank=True, null=True)
    event_date = models.DateField(blank=True, null=True)
    event_time = models.TimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.short_description:
            self.short_description = self.event_description[:50]
        if not self.event_date:
            self.event_date = self.event_datetime.date()
        if not self.event_time:
            self.event_time = self.event_datetime.time()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.event_name
    
    def get_absolute_url(self):
        return reverse('event_details', args=[str(self.event_name)])
    
class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlists')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='watchlist')

    def __str__(self):
        return f"{self.user.username}'s Watchlist"

    