from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name='room'),
    path('login/', views.login, name='login'),
    path('create-room/', views.createRoom, name='create-room'),  # Add URL for creating a new room.
]