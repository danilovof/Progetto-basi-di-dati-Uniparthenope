from django import forms
from django.contrib.auth.models import User
from .models import Track, Concert

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    is_manager = forms.BooleanField(required=False, initial=False, label='Registrati come manager')

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'is_manager']

class TrackForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = ['title', 'release_date', 'spotify_streams', 'spotify_earnings']

class ConcertForm(forms.ModelForm):
    class Meta:
        model = Concert
        fields = ['date', 'venue', 'tickets_sold', 'revenue']
