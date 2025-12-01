from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('artist/<str:username>/', views.dashboard, name='artist_dashboard'),
    path('manager/', views.dashboard, name='manager_dashboard'),
    path('manager/reset/<int:artist_id>/', views.reset_artist, name='reset_artist_stats'),
    path('add_track/', views.add_track, name='add_track'),
    path('add_concert/', views.add_concert, name='add_concert'),
]
