from django.contrib import admin
from .models import ArtistProfile, ManagerProfile, Contract, Track, Concert
admin.site.register(ArtistProfile)
admin.site.register(ManagerProfile)
admin.site.register(Contract)
admin.site.register(Track)
admin.site.register(Concert)
