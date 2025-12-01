# Run this AFTER you've done: makemigrations & migrate
# Usage: activate virtualenv then: python setup_sample.py
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music_career.settings')
import django
django.setup()

from django.contrib.auth.models import User
from careers.models import ArtistProfile, ManagerProfile, Track, Concert, Contract
from datetime import date

# create manager
if not User.objects.filter(username='manager1').exists():
    m = User.objects.create_user('manager1', email='manager1@example.com', password='managerpass')
    ManagerProfile.objects.create(user=m, company_name='Top Management')
    print('Created manager1')

# create artist
if not User.objects.filter(username='artist1').exists():
    a = User.objects.create_user('artist1', email='artist1@example.com', password='artistpass')
    artist_profile = ArtistProfile.objects.create(user=a, genre='Pop')
    # sample track
    Track.objects.create(artist=artist_profile, title='Hit Song', release_date=date(2024,6,1), spotify_streams=50000, spotify_earnings=125.50)
    # sample concert
    Concert.objects.create(artist=artist_profile, date=date(2024,9,15), venue='Arena', tickets_sold=2000, revenue=40000.00)
    print('Created artist1 with sample track and concert')

# create contract linking them
try:
    manager = ManagerProfile.objects.first()
    artist = ArtistProfile.objects.first()
    if manager and artist and not Contract.objects.filter(manager=manager, artist=artist).exists():
        Contract.objects.create(manager=manager, artist=artist, start_date=date(2024,1,1))
        print('Created contract between manager and artist')
except Exception as e:
    print('Error creating contract:', e)
