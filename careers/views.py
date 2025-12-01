from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.db import transaction
from django.contrib import messages
from django.urls import reverse

from .models import ArtistProfile, ManagerProfile, Contract, Track, Concert, artist_total_earnings
from .forms import UserRegisterForm, TrackForm, ConcertForm

def manager_required(view_func):
    def _wrapped(request, *args, **kwargs):
        if hasattr(request.user, 'managerprofile'):
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden('Accesso riservato ai manager')
    return _wrapped

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, '⚠️ Credenziali errate o utente inesistente')
            return redirect('login')
    return render(request, 'registration/login.html')

@transaction.atomic
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(username=data['username'], email=data['email'], password=data['password'])
            if data.get('is_manager'):
                ManagerProfile.objects.create(user=user)
            else:
                ArtistProfile.objects.create(user=user)
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request, username=None):
    if username and hasattr(request.user, 'managerprofile'):
        user = get_object_or_404(User, username=username)
        try:
            artist = user.artistprofile
        except ArtistProfile.DoesNotExist:
            return HttpResponseForbidden('Utente non è un artista')
        contract = artist.contracts.order_by('-start_date').first()
        return render(request, 'artist_dashboard.html', {
            'artist': artist,
            'contract': contract,
            'tracks': artist.tracks.all(),
            'concerts': artist.concerts.all(),
            'total_earnings': artist_total_earnings(artist),
        })

    if hasattr(request.user, 'artistprofile'):
        artist = request.user.artistprofile
        contract = artist.contracts.order_by('-start_date').first()
        return render(request, 'artist_dashboard.html', {
            'artist': artist,
            'contract': contract,
            'tracks': artist.tracks.all(),
            'concerts': artist.concerts.all(),
            'total_earnings': artist_total_earnings(artist),
        })
    if hasattr(request.user, 'managerprofile'):
        manager = request.user.managerprofile
        artists = ArtistProfile.objects.all()
        artist_data = []
        for a in artists:
            last_contract = a.contracts.order_by('-start_date').first()
            total = artist_total_earnings(a)
            artist_data.append({'artist': a, 'contract': last_contract, 'total': total})
        return render(request, 'manager_dashboard.html', {'manager': manager, 'artist_data': artist_data})
    return render(request, 'base.html')

@login_required
def add_track(request):
    if not hasattr(request.user, 'artistprofile'):
        return HttpResponseForbidden('Solo artisti possono aggiungere brani')
    if request.method == 'POST':
        form = TrackForm(request.POST)
        if form.is_valid():
            track = form.save(commit=False)
            track.artist = request.user.artistprofile
            track.save()
            messages.success(request, 'Brano aggiunto')
            return redirect('dashboard')
    else:
        form = TrackForm()
    return render(request, 'add_track.html', {'form': form})

@login_required
def add_concert(request):
    if not hasattr(request.user, 'artistprofile'):
        return HttpResponseForbidden('Solo artisti possono aggiungere concerti')
    if request.method == 'POST':
        form = ConcertForm(request.POST)
        if form.is_valid():
            concert = form.save(commit=False)
            concert.artist = request.user.artistprofile
            concert.save()
            messages.success(request, 'Concerto aggiunto')
            return redirect('dashboard')
    else:
        form = ConcertForm()
    return render(request, 'add_concert.html', {'form': form})

@login_required
@manager_required
def reset_artist(request, artist_id):
    artist = get_object_or_404(ArtistProfile, id=artist_id)
    if request.method == 'POST':
        artist.tracks.all().delete()
        artist.concerts.all().delete()
        messages.success(request, f'Statistiche e dati di {artist.user.username} cancellati')
        return redirect('dashboard')
    return render(request, 'confirm_reset.html', {'artist': artist})

@login_required
def custom_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return HttpResponseForbidden()
