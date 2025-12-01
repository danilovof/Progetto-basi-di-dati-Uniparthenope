from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from django.db.models import Sum

class ArtistProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    genre = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Artist: {self.user.username}"

class ManagerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Manager: {self.user.username}"

class Contract(models.Model):
    artist = models.ForeignKey(ArtistProfile, on_delete=models.CASCADE, related_name='contracts')
    manager = models.ForeignKey(ManagerProfile, on_delete=models.CASCADE, related_name='contracts')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Contract {self.artist.user.username} - {self.manager.user.username}"

class Track(models.Model):
    artist = models.ForeignKey(ArtistProfile, on_delete=models.CASCADE, related_name='tracks')
    title = models.CharField(max_length=200)
    release_date = models.DateField(null=True, blank=True)
    spotify_streams = models.PositiveIntegerField(default=0)
    spotify_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return f"{self.title} ({self.artist.user.username})"

class Concert(models.Model):
    artist = models.ForeignKey(ArtistProfile, on_delete=models.CASCADE, related_name='concerts')
    date = models.DateField()
    venue = models.CharField(max_length=200)
    tickets_sold = models.PositiveIntegerField(default=0)
    revenue = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return f"Concert {self.artist.user.username} @ {self.venue} on {self.date}"

def artist_total_earnings(artist_profile):
    track_sum = artist_profile.tracks.aggregate(sum=Sum('spotify_earnings'))['sum'] or Decimal('0.00')
    concert_sum = artist_profile.concerts.aggregate(sum=Sum('revenue'))['sum'] or Decimal('0.00')
    return track_sum + concert_sum
